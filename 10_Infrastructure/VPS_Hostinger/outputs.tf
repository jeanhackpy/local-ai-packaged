###############################################################################
# Outputs
###############################################################################

output "instance_id" {
  description = "OCID of the compute instance"
  value       = oci_core_instance.palanthai.id
}

output "instance_public_ip" {
  description = "Public IP address (use for SSH + DNS A records)"
  value       = oci_core_instance.palanthai.public_ip
}

output "instance_private_ip" {
  description = "Private IP inside the VCN"
  value       = oci_core_instance.palanthai.private_ip
}

output "vcn_id" {
  value = oci_core_vcn.palanthai_vcn.id
}

output "subnet_id" {
  value = oci_core_subnet.palanthai_subnet.id
}

output "image_ocid" {
  description = "OCID of the Ubuntu 24.04 image used (pinned)"
  value       = var.image_ocid
}

output "shape_summary" {
  value = "${var.instance_shape} (${var.instance_ocpus} OCPU / ${var.instance_memory_gb} GB)"
}

output "next_steps" {
  description = "Post-apply instructions"
  value = <<-EOT

    Instance up. Next steps:

    1. SSH:               ssh ubuntu@${oci_core_instance.palanthai.public_ip}
    2. Run post-prov:     bash oracle_post_provisioning.sh ${oci_core_instance.palanthai.public_ip}
    3. Update DNS:        n8n.recall-agency.com → ${oci_core_instance.palanthai.public_ip}
    4. Verify:            curl -I https://n8n.recall-agency.com (after Caddy up)
  EOT
}
