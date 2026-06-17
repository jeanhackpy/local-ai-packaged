#!/usr/bin/env python3
"""
start_services.py

This script starts the Supabase stack first, waits for it to initialize, and then starts
the local AI stack. Both stacks use the same Docker Compose project name ("localai")
so they appear together in Docker Desktop.
"""

import os
import subprocess
import shutil
import time
import argparse
import platform
import sys
import secrets
import tempfile

def run_command(cmd, cwd=None):
    """Run a shell command and print it."""
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)

def clone_supabase_repo():
    """Clone the Supabase repository using sparse checkout if not already present."""
    if not os.path.exists("supabase"):
        print("Cloning the Supabase repository...")
        run_command([
            "git", "clone", "--filter=blob:none", "--no-checkout",
            "https://github.com/supabase/supabase.git"
        ])
        os.chdir("supabase")
        run_command(["git", "sparse-checkout", "init", "--cone"])
        run_command(["git", "sparse-checkout", "set", "docker"])
        run_command(["git", "checkout", "master"])
        os.chdir("..")
    else:
        if os.path.exists("supabase/.git"):
            print("Supabase repository already exists, updating...")
            os.chdir("supabase")
            run_command(["git", "pull"])
            os.chdir("..")
        else:
            print("Supabase directory exists and is fully integrated (no .git folder). Skipping update.")

def ensure_supabase_volumes():
    """Ensure supabase/docker/volumes/ config exists (Kong + Postgres init scripts).

    These files are required for the stack to boot but are NOT committed to this
    repo, and clone_supabase_repo() skips regeneration when supabase/ has no .git
    dir. Without them, Docker bind-mounts the missing host paths as empty
    directories: Kong reads an empty kong.yml (crash loop) and the Postgres init
    SQL scripts become directories (schemas never initialize).

    Idempotent: fetches the upstream config subtree only when missing, then
    overlays the locked golden kong.yml. Never touches db/data or storage.
    """
    vol = os.path.join("supabase", "docker", "volumes")
    golden_kong = os.path.join(".golden", "backups", "kong.yml.golden")
    supabase_ref = os.environ.get("SUPABASE_REF", "master")

    required = [
        os.path.join("api", "kong.yml"),
        os.path.join("db", "roles.sql"),
        os.path.join("db", "jwt.sql"),
        os.path.join("db", "realtime.sql"),
        os.path.join("db", "_supabase.sql"),
        os.path.join("db", "logs.sql"),
        os.path.join("db", "pooler.sql"),
        os.path.join("db", "webhooks.sql"),
        os.path.join("pooler", "pooler.exs"),
    ]

    have_config = (
        os.path.isfile(os.path.join(vol, "api", "kong.yml"))
        and os.path.isfile(os.path.join(vol, "db", "roles.sql"))
        and os.path.isfile(os.path.join(vol, "pooler", "pooler.exs"))
    )

    if have_config:
        print("Supabase volumes config already present.")
    else:
        print(f"Supabase volumes config missing — fetching from upstream ({supabase_ref})...")
        tmp = tempfile.mkdtemp(prefix="supabase-vol-")
        try:
            clone_dir = os.path.join(tmp, "supabase")
            run_command([
                "git", "clone", "--filter=blob:none", "--no-checkout",
                "https://github.com/supabase/supabase.git", clone_dir,
            ])
            run_command(["git", "sparse-checkout", "init", "--cone"], cwd=clone_dir)
            run_command(["git", "sparse-checkout", "set", "docker"], cwd=clone_dir)
            run_command(["git", "checkout", supabase_ref], cwd=clone_dir)

            src = os.path.join(clone_dir, "docker", "volumes")
            os.makedirs(vol, exist_ok=True)
            # Copy config only; skip runtime data dirs (data/, storage/).
            shutil.copytree(
                src, vol, dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("data", "storage"),
            )
            print("Fetched Supabase volumes config tree.")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # Overlay the locked golden kong.yml (authoritative; matches config-guard checksum).
    if os.path.isfile(golden_kong):
        os.makedirs(os.path.join(vol, "api"), exist_ok=True)
        shutil.copyfile(golden_kong, os.path.join(vol, "api", "kong.yml"))
        print("Restored kong.yml from golden backup.")
    else:
        print("WARNING: golden kong.yml not found — using upstream kong.yml.")

    # Runtime dirs (empty; filled by data restore / first boot).
    for d in (os.path.join("db", "data"), "storage", "functions"):
        os.makedirs(os.path.join(vol, d), exist_ok=True)

    # Verify required config is in place before we try to start anything.
    missing = [f for f in required if not os.path.isfile(os.path.join(vol, f))]
    if missing:
        print("ERROR: Supabase volumes incomplete — Kong/Postgres will not boot:")
        for f in missing:
            print(f"  missing: {f}")
        sys.exit(1)
    print("Supabase volumes ready.")

def prepare_supabase_env():
    """Merge .env in root with .env.example in supabase/docker and write to .env in supabase/docker."""
    target_env_path = os.path.join("supabase", "docker", ".env")
    example_env_path = os.path.join("supabase", "docker", ".env.example")
    root_env_path = ".env"

    print("Merging .env.example with root .env to create supabase/docker/.env...")
    
    env_vars = {}

    # 1. Load defaults from .env.example
    if os.path.exists(example_env_path):
        with open(example_env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    else:
        print(f"Warning: {example_env_path} not found.")

    # 2. Override with values from root .env
    if os.path.exists(root_env_path):
        with open(root_env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    else:
        print(f"Warning: {root_env_path} not found.")

    # 3. Write merged variables to target .env
    # We'll read the example file again to preserve comments and structure as much as possible,
    # or just write out the simple key-values.
    # For Docker Compose, a simple key=value file is sufficient.
    
    with open(target_env_path, 'w') as f:
        f.write("# Generated by start_services.py - Merged configuration\n")
        f.write("# Defaults from supabase/docker/.env.example, overrides from root .env\n\n")
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    print(f"Successfully created {target_env_path}")

def stop_existing_containers(profile=None):
    print("Stopping and removing existing containers for the unified project 'localai'...")
    cmd = ["docker", "compose", "-p", "localai"]
    if profile and profile != "none":
        cmd.extend(["--profile", profile])
    cmd.extend(["-f", "docker-compose.yml", "down"])
    run_command(cmd)

def start_supabase(environment=None):
    """Start the Supabase services (using its compose file)."""
    print("Starting Supabase services...")
    cmd = ["docker", "compose", "-p", "localai", "-f", "supabase/docker/docker-compose.yml"]
    if environment and environment == "public":
        cmd.extend(["-f", "docker-compose.override.public.supabase.yml"])
    cmd.extend(["up", "-d"])
    run_command(cmd)

def start_local_ai(profile=None, environment=None):
    """Start the local AI services (using its compose file)."""
    print("Starting local AI services...")
    cmd = ["docker", "compose", "-p", "localai"]
    if profile and profile != "none":
        cmd.extend(["--profile", profile])
    cmd.extend(["-f", "docker-compose.yml"])
    if environment and environment == "private":
        cmd.extend(["-f", "docker-compose.override.private.yml"])
    if environment and environment == "public":
        cmd.extend(["-f", "docker-compose.override.public.yml"])
    cmd.extend(["up", "-d"])
    run_command(cmd)







def generate_searxng_secret_key():
    """Generate a secret key for SearXNG based on the current platform."""
    print("Checking SearXNG settings...")

    # Define paths for SearXNG settings files
    settings_path = os.path.join("searxng", "settings.yml")
    settings_base_path = os.path.join("searxng", "settings-base.yml")

    # Check if settings-base.yml exists
    if not os.path.exists(settings_base_path):
        print(f"Warning: SearXNG base settings file not found at {settings_base_path}")
        return

    # Check if settings.yml exists, if not create it from settings-base.yml
    if not os.path.exists(settings_path):
        print(f"SearXNG settings.yml not found. Creating from {settings_base_path}...")
        try:
            shutil.copyfile(settings_base_path, settings_path)
            print(f"Created {settings_path} from {settings_base_path}")
        except Exception as e:
            print(f"Error creating settings.yml: {e}")
            return
    else:
        print(f"SearXNG settings.yml already exists at {settings_path}")

    print("Generating SearXNG secret key...")

    # Detect the platform and run the appropriate command
    system = platform.system()

    try:
        if system == "Windows":
            print("Detected Windows platform, using PowerShell to generate secret key...")
            # PowerShell command to generate a random key and replace in the settings file
            ps_command = [
                "powershell", "-Command",
                "$randomBytes = New-Object byte[] 32; " +
                "(New-Object Security.Cryptography.RNGCryptoServiceProvider).GetBytes($randomBytes); " +
                "$secretKey = -join ($randomBytes | ForEach-Object { \"{0:x2}\" -f $_ }); " +
                "(Get-Content searxng/settings.yml) -replace 'ultrasecretkey', $secretKey | Set-Content searxng/settings.yml"
            ]
            subprocess.run(ps_command, check=True)

        elif system == "Darwin":  # macOS
            print("Detected macOS platform, using sed command with empty string parameter...")
            # macOS sed command requires an empty string for the -i parameter
            openssl_cmd = ["openssl", "rand", "-hex", "32"]
            random_key = subprocess.check_output(openssl_cmd).decode('utf-8').strip()
            sed_cmd = ["sed", "-i", "", f"s|ultrasecretkey|{random_key}|g", settings_path]
            subprocess.run(sed_cmd, check=True)

        else:  # Linux and other Unix-like systems
            print("Detected Linux/Unix platform, using standard sed command...")
            # Standard sed command for Linux
            openssl_cmd = ["openssl", "rand", "-hex", "32"]
            random_key = subprocess.check_output(openssl_cmd).decode('utf-8').strip()
            sed_cmd = ["sed", "-i", f"s|ultrasecretkey|{random_key}|g", settings_path]
            subprocess.run(sed_cmd, check=True)

        print("SearXNG secret key generated successfully.")

    except Exception as e:
        print(f"Error generating SearXNG secret key: {e}")
        print("You may need to manually generate the secret key using the commands:")
        print("  - Linux: sed -i \"s|ultrasecretkey|$(openssl rand -hex 32)|g\" searxng/settings.yml")
        print("  - macOS: sed -i '' \"s|ultrasecretkey|$(openssl rand -hex 32)|g\" searxng/settings.yml")
        print("  - Windows (PowerShell):")
        print("    $randomBytes = New-Object byte[] 32")
        print("    (New-Object Security.Cryptography.RNGCryptoServiceProvider).GetBytes($randomBytes)")
        print("    $secretKey = -join ($randomBytes | ForEach-Object { \"{0:x2}\" -f $_ })")
        print("    (Get-Content searxng/settings.yml) -replace 'ultrasecretkey', $secretKey | Set-Content searxng/settings.yml")



def check_and_fix_docker_compose_for_searxng():
    """Check and modify docker-compose.yml for SearXNG first run."""
    docker_compose_path = "docker-compose.yml"
    if not os.path.exists(docker_compose_path):
        print(f"Warning: Docker Compose file not found at {docker_compose_path}")
        return

    try:
        # Read the docker-compose.yml file
        with open(docker_compose_path, 'r') as file:
            content = file.read()

        # Default to first run
        is_first_run = True

        # Check if Docker is running and if the SearXNG container exists
        try:
            # Check if the SearXNG container is running
            container_check = subprocess.run(
                ["docker", "ps", "--filter", "name=searxng", "--format", "{{.Names}}"],
                capture_output=True, text=True, check=True
            )
            searxng_containers = container_check.stdout.strip().split('\n')

            # If SearXNG container is running, check inside for uwsgi.ini
            if any(container for container in searxng_containers if container):
                container_name = next(container for container in searxng_containers if container)
                print(f"Found running SearXNG container: {container_name}")

                # Check if uwsgi.ini exists inside the container
                container_check = subprocess.run(
                    ["docker", "exec", container_name, "sh", "-c", "[ -f /etc/searxng/uwsgi.ini ] && echo 'found' || echo 'not_found'"],
                    capture_output=True, text=True, check=False
                )

                if "found" in container_check.stdout:
                    print("Found uwsgi.ini inside the SearXNG container - not first run")
                    is_first_run = False
                else:
                    print("uwsgi.ini not found inside the SearXNG container - first run")
                    is_first_run = True
            else:
                print("No running SearXNG container found - assuming first run")
        except Exception as e:
            print(f"Error checking Docker container: {e} - assuming first run")

        if is_first_run and "cap_drop: - ALL" in content:
            print("First run detected for SearXNG. Temporarily removing 'cap_drop: - ALL' directive...")
            # Temporarily comment out the cap_drop line
            modified_content = content.replace("cap_drop: - ALL", "# cap_drop: - ALL  # Temporarily commented out for first run")

            # Write the modified content back
            with open(docker_compose_path, 'w') as file:
                file.write(modified_content)

            print("Note: After the first run completes successfully, you should re-add 'cap_drop: - ALL' to docker-compose.yml for security reasons.")
        elif not is_first_run and "# cap_drop: - ALL  # Temporarily commented out for first run" in content:
            print("SearXNG has been initialized. Re-enabling 'cap_drop: - ALL' directive for security...")
            # Uncomment the cap_drop line
            modified_content = content.replace("# cap_drop: - ALL  # Temporarily commented out for first run", "cap_drop: - ALL")

            # Write the modified content back
            with open(docker_compose_path, 'w') as file:
                file.write(modified_content)

    except Exception as e:
        print(f"Error checking/modifying docker-compose.yml for SearXNG: {e}")



def main():
    parser = argparse.ArgumentParser(description='Start the local AI and Supabase services.')
    parser.add_argument('--profile', choices=['cpu', 'gpu-nvidia', 'gpu-amd', 'none'], default='cpu',
                      help='Profile to use for Docker Compose (default: cpu)')
    parser.add_argument('--environment', choices=['private', 'public'], default='private',
                      help='Environment to use for Docker Compose (default: private)')
    args = parser.parse_args()

    # OpenClaw Gateway is managed by systemd (openclaw-gateway.service)
    # No need to start it here

    clone_supabase_repo()

    # Ensure Kong + Postgres init config exists before starting Supabase
    ensure_supabase_volumes()

    # Generate secrets and check configuration
    generate_searxng_secret_key()
    # prepare_openclaw_env()
    prepare_supabase_env()
    check_and_fix_docker_compose_for_searxng()
    
    # Check OpenClaw configuration
    # check_openclaw_config()

    stop_existing_containers(args.profile)

    # Start Supabase first
    start_supabase(args.environment)

    # Give Supabase some time to initialize
    print("Waiting for Supabase to initialize...")
    time.sleep(10)

    # Build OpenClaw image before starting services
    # build_openclaw_image()

    # Then start the local AI services
    start_local_ai(args.profile, args.environment)
    
    # Wait for OpenClaw to be ready
    # wait_for_openclay()
    
    print("All services started successfully!")
    print("============================================================")
    print()
    print("📊 Service URLs:")

    def _get_compose_ports():
        try:
            out = subprocess.check_output([
                "docker", "ps", "--filter", "label=com.docker.compose.project=localai",
                "--format", "{{.Names}}|{{.Ports}}"
            ], text=True)
        except Exception:
            return {}

        m = {}
        for line in out.splitlines():
            if '|' in line:
                name, ports = line.split('|', 1)
                m[name.strip()] = ports.strip()
        return m

    def _extract_host_port(ports_str, prefer_container_port=None):
        import re
        if not ports_str:
            return None
        # match host port patterns like 0.0.0.0:5678->5678/tcp
        m = re.search(r'0\.0\.0\.0:(\d+)->', ports_str)
        if m:
            return m.group(1)
        # match host->container like 5678->5678/tcp
        m = re.search(r'(\d+)->\d+/tcp', ports_str)
        if m:
            return m.group(1)
        # fallback: any bare port like 8080/tcp
        m = re.search(r'(\d+)/tcp', ports_str)
        if m:
            return m.group(1)
        return None

    ports_map = _get_compose_ports()

    def find_port_for(matches, prefer=None):
        for k, v in ports_map.items():
            for match in matches:
                if match in k:
                    hp = _extract_host_port(v, prefer)
                    if hp:
                        return hp
        return None

    entries = []
    # OpenClaw is not managed by Docker here; only show it if detected
    openclaw_port = find_port_for(["openclaw", "openclaw-gateway"]) or None
    entries.append(("OpenClaw Gateway", openclaw_port))
    entries.append(("OpenClaw Control UI", openclaw_port))

    # Try to detect Open WebUI (commonly exposed on 8080)
    webui_port = find_port_for(["webui", "open-webui", "imgproxy", "studio", "searxng"], prefer="8080")
    if not webui_port:
        # try to find any mapping to container port 8080
        for v in ports_map.values():
            if ":8080->" in v or ":8080/tcp" in v or "->8080/tcp" in v:
                webui_port = _extract_host_port(v)
                break
    entries.append(("Open WebUI", webui_port))

    entries.append(("n8n", find_port_for(["n8n"])) )
    entries.append(("Qdrant", find_port_for(["qdrant"])) )
    entries.append(("Neo4j Browser", find_port_for(["neo4j"])) )
    entries.append(("Supabase Kong", find_port_for(["kong", "supabase-kong"])) )
    entries.append(("Caddy (Proxy)", find_port_for(["caddy"])) )

    for name, port in entries:
        if port:
            print(f"  • {name}: http://localhost:{port}")
        else:
            print(f"  • {name}: not running / not exposed")

    print()
    print("📖 Documentation: docs/OPENCLAW_INTEGRATIONS.md")
    print("============================================================")

if __name__ == "__main__":
    main()
