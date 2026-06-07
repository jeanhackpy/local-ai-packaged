###############################################################################
# Networking — VCN, Public Subnet, IGW, Route Table, Security List
###############################################################################

resource "oci_core_vcn" "palanthai_vcn" {
  compartment_id = var.tenancy_ocid
  cidr_blocks    = [var.vcn_cidr]
  display_name   = "palanthai-vcn"
  dns_label      = "palanthai"

  freeform_tags = local.common_tags
}

resource "oci_core_internet_gateway" "palanthai_igw" {
  compartment_id = var.tenancy_ocid
  vcn_id         = oci_core_vcn.palanthai_vcn.id
  display_name   = "palanthai-igw"
  enabled        = true

  freeform_tags = local.common_tags
}

resource "oci_core_route_table" "palanthai_rt" {
  compartment_id = var.tenancy_ocid
  vcn_id         = oci_core_vcn.palanthai_vcn.id
  display_name   = "palanthai-rt"

  route_rules {
    destination       = "0.0.0.0/0"
    network_entity_id = oci_core_internet_gateway.palanthai_igw.id
  }

  freeform_tags = local.common_tags
}

resource "oci_core_security_list" "palanthai_sl" {
  compartment_id = var.tenancy_ocid
  vcn_id         = oci_core_vcn.palanthai_vcn.id
  display_name   = "palanthai-sl"

  # === Ingress (inbound) ===
  ingress_security_rules {
    description = "SSH (fail2ban-protected; tighten via ssh_ingress_cidr once Tailscale is up)"
    source      = var.ssh_ingress_cidr
    source_type = "CIDR_BLOCK"
    protocol    = "6" # TCP
    tcp_options {
      min = 22
      max = 22
    }
  }

  ingress_security_rules {
    description = "HTTP for Caddy / Let's Encrypt"
    source      = "0.0.0.0/0"
    source_type = "CIDR_BLOCK"
    protocol    = "6"
    tcp_options {
      min = 80
      max = 80
    }
  }

  ingress_security_rules {
    description = "HTTPS for Caddy / Let's Encrypt"
    source      = "0.0.0.0/0"
    source_type = "CIDR_BLOCK"
    protocol    = "6"
    tcp_options {
      min = 443
      max = 443
    }
  }

  ingress_security_rules {
    description = "HTTP/3 (QUIC) for Caddy"
    source      = "0.0.0.0/0"
    source_type = "CIDR_BLOCK"
    protocol    = "17" # UDP
    udp_options {
      min = 443
      max = 443
    }
  }

  # === Egress (outbound) ===
  egress_security_rules {
    description      = "Allow all outbound (Docker pulls, apt, etc.)"
    destination      = "0.0.0.0/0"
    destination_type = "CIDR_BLOCK"
    protocol         = "all"
  }

  freeform_tags = local.common_tags
}

resource "oci_core_subnet" "palanthai_subnet" {
  compartment_id            = var.tenancy_ocid
  vcn_id                    = oci_core_vcn.palanthai_vcn.id
  cidr_block                = var.subnet_cidr
  display_name              = "palanthai-public-subnet"
  dns_label                 = "public"
  route_table_id            = oci_core_route_table.palanthai_rt.id
  security_list_ids         = [oci_core_security_list.palanthai_sl.id]
  prohibit_public_ip_on_vnic = false # we WANT public IPs

  freeform_tags = local.common_tags
}
