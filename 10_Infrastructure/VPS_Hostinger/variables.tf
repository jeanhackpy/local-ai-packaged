###############################################################################
# Variables
###############################################################################

variable "region" {
  description = "OCI region (Home Region, immutable after account creation)"
  type        = string
  default     = "ap-singapore-1"
}

variable "tenancy_ocid" {
  description = "OCID of the tenancy (root compartment)"
  type        = string
  # Read from environment: TF_VAR_tenancy_ocid (recommended for secrets)
}

variable "ssh_public_key_path" {
  description = "Path to SSH public key for instance access"
  type        = string
  default     = "~/.ssh/id_ed25519.pub"
}

variable "instance_display_name" {
  description = "Display name for the compute instance"
  type        = string
  default     = "palanthai-oracle"
}

variable "instance_shape" {
  description = "Shape for the compute instance (Always Free ARM)"
  type        = string
  default     = "VM.Standard.A1.Flex"
}

variable "instance_ocpus" {
  description = "Number of OCPUs (max 4 per A1.Flex instance, Always Free)"
  type        = number
  default     = 4

  validation {
    condition     = var.instance_ocpus >= 1 && var.instance_ocpus <= 4
    error_message = "A1.Flex allows 1-4 OCPUs."
  }
}

variable "instance_memory_gb" {
  description = "Memory in GB (max 24 per A1.Flex instance, Always Free)"
  type        = number
  default     = 24

  validation {
    condition     = var.instance_memory_gb >= 1 && var.instance_memory_gb <= 24
    error_message = "A1.Flex allows 1-24 GB RAM."
  }
}

variable "boot_volume_size_gb" {
  description = "Boot volume size in GB (max 200 for Always Free)"
  type        = number
  default     = 200

  validation {
    condition     = var.boot_volume_size_gb >= 50 && var.boot_volume_size_gb <= 200
    error_message = "Boot volume must be 50-200 GB."
  }
}

variable "vcn_cidr" {
  description = "CIDR block for the VCN"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR block for the public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "ssh_ingress_cidr" {
  description = "CIDR allowed to reach SSH (22). Default open + fail2ban; tighten to your IP or the Tailscale CIDR (100.64.0.0/10) once Tailscale is connected, to avoid lockout."
  type        = string
  default     = "0.0.0.0/0"
}

variable "image_ocid" {
  description = "Pinned Ubuntu 24.04 ARM image OCID (reproducible rebuild; matches the live instance). This is the image oci_hunter.sh used to land palanthai-oracle."
  type        = string
  default     = "ocid1.image.oc1.ap-singapore-1.aaaaaaaaihkypxmfxzeyjevj3eutgzlnqjazicn27goya2lpr3mdmg5to2tq"
}
