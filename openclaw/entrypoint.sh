#!/bin/sh
# Entrypoint script to substitute environment variables in openclaw.json
# This script preserves the placeholder version for Git while creating a runtime version

CONFIG_FILE="/home/node/.openclaw/openclaw.json"
RUNTIME_CONFIG="/tmp/openclaw.json.runtime"
AUTH_FILE="/home/node/.openclaw/agents/main/agent/auth-profiles.json"

# Function to fill placeholders in config file
fill_config_placeholders() {
    local input_file="$1"
    local output_file="$2"
    envsubst < "$input_file" > "$output_file"
}

# Check if config file exists with placeholders
if [ -f "$CONFIG_FILE" ]; then
    if grep -q '\${[A-Z_]*}' "$CONFIG_FILE" 2>/dev/null; then
        echo "Found placeholder config - generating runtime version..."
        fill_config_placeholders "$CONFIG_FILE" "$RUNTIME_CONFIG"
        
        # Replace only the env section in the original file to preserve user modifications
        # while keeping placeholders for Git
        echo "Injecting secrets into runtime config..."
        cp "$RUNTIME_CONFIG" "$CONFIG_FILE.runtime"
    else
        echo "Config already filled - using as-is"
    fi
else
    echo "Warning: Config file not found"
fi

# Generate auth-profiles.json with API keys
cat > "$AUTH_FILE" << EOF
{
    "nvidia:default": {
        "provider": "nvidia",
        "mode": "api_key",
        "apiKey": "${NVIDIA_API_KEY}"
    },
    "openrouter:default": {
        "provider": "openrouter",
        "mode": "api_key",
        "apiKey": "${OPENROUTER_API_KEY}"
    },
    "ollama:default": {
        "provider": "ollama",
        "mode": "api_key"
    },
    "ollama-cloud:default": {
        "provider": "ollama-cloud",
        "mode": "api_key",
        "apiKey": "${OLLAMA_API_KEY}"
    }
}
EOF
echo "Generated auth-profiles.json"

# Fix permissions for node user
chown -R node:node /home/node/.openclaw

# Start OpenClaw as node user
exec su -c "openclaw gateway run" node
