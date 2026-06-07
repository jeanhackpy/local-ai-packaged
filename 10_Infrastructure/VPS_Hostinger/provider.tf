###############################################################################
# OCI Provider — Palanthai Oracle Cloud Free Tier (Singapore)
###############################################################################

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    oci = {
      source  = "oracle/oci"
      version = "~> 5.0"
    }
  }

  # Optional: remote state on OCI Object Storage
  # backend "s3" {
  #   bucket   = "terraform-state"
  #   key      = "palanthai-oracle.tfstate"
  #   region   = "ap-singapore-1"
  #   endpoint = "https://<namespace>.compat.objectstorage.ap-singapore-1.oraclecloud.com"
  #   ...
  # }
}

provider "oci" {
  region = var.region
  # Auth via OCI CLI config (~/.oci/config) or instance principals
  # config_file = "~/.oci/config"
  # profile     = "DEFAULT"
}

###############################################################################
# Data sources
###############################################################################

data "oci_identity_availability_domains" "ads" {
  compartment_id = var.tenancy_ocid
}

# Pinned via var.image_ocid (see variables.tf) for reproducible rebuilds.
# This data source is also known to break `terraform import` (provider schema
# self-reference bug), so it is intentionally disabled. Re-enable only if you
# want "newest image" behaviour instead of a pinned OCID.
# data "oci_identity_images" "ubuntu_2404" {
#   compartment_id           = var.tenancy_ocid
#   operating_system         = "Canonical Ubuntu"
#   operating_system_version = "24.04"
#   shape                    = "VM.Standard.A1.Flex"
#   sort_by                  = "TIMECREATED"
#   sort_order               = "DESC"
# }

###############################################################################
# Locals
###############################################################################

locals {
  # AD-1 is what oci_hunter uses. If full, switch to AD-2 or AD-3.
  ad_name = "JCSA:AP-SINGAPORE-1-AD-1"

  common_tags = {
    project     = "palanthai"
    environment = "production"
    managed_by  = "terraform"
    migrated_at = formatdate("YYYY-MM-DD", timestamp())
  }
}
