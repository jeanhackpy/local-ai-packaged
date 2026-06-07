###############################################################################
# Compute — A1.Flex ARM instance (Always Free)
###############################################################################

resource "oci_core_instance" "palanthai" {
  compartment_id      = var.tenancy_ocid
  availability_domain = local.ad_name
  display_name        = var.instance_display_name
  shape               = var.instance_shape

  shape_config {
    ocpus         = var.instance_ocpus
    memory_in_gbs = var.instance_memory_gb
  }

  source_details {
    source_type               = "image"
    source_id                 = var.image_ocid
    boot_volume_size_in_gbs   = var.boot_volume_size_gb
  }

  create_vnic_details {
    subnet_id                 = oci_core_subnet.palanthai_subnet.id
    display_name              = "palanthai-vnic"
    assign_public_ip          = true
    private_ip                = "10.0.1.10"
    skip_source_dest_check    = false
  }

  metadata = {
    ssh_authorized_keys = file(pathexpand(var.ssh_public_key_path))

    # Cloud-init — first boot setup. Idempotent.
    user_data = base64encode(<<-EOF
      #cloud-config
      package_update: true
      package_upgrade: true
      packages:
        - docker.io
        - docker-compose-plugin
        - fail2ban
        - ufw
        - curl
        - git
        - jq
        - unzip
        - unattended-upgrades
      runcmd:
        # Minimal bootstrap only. Firewall, fail2ban, swap, Tailscale and the
        # stack are owned by oracle_post_provisioning.sh (single source of truth)
        # to avoid two systems fighting over UFW rules.
        - systemctl enable --now docker
        - usermod -aG docker ubuntu
    EOF
    )
  }

  freeform_tags = local.common_tags

  # Don't recreate instance on user_data tweak — just re-run
  lifecycle {
    ignore_changes = [
      metadata["user_data"],
    ]
  }
}
