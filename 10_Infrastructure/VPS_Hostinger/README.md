# Palanthai Oracle Cloud Singapore — Terraform

Infrastructure-as-code for the **palanthai-oracle** VM.Standard.A1.Flex instance (Always Free tier, Singapore).

## Resources deployed

- **VCN** `palanthai-vcn` (10.0.0.0/16)
- **Public subnet** (10.0.1.0/24) with Internet Gateway + default route
- **Security List** with ports 22 (SSH) / 80 / 443 (TCP) + 443 (UDP/QUIC)
- **Compute** `palanthai-oracle` — 4 OCPU / 24 GB / 200 GB, Ubuntu 24.04 LTS
- **Public IP** assigned (Reserved, stable across reboots)

## Prerequisites

```bash
brew install oci-cli hashicorp/tap/terraform
oci setup config   # creates ~/.oci/config
```

## Setup

```bash
cd /Users/phil/Documents/Factory/COMMAND&CONTROL/10_Infrastructure/VPS_Hostinger/oracle
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars → set tenancy_ocid
```

Or use env var (safer):
```bash
export TF_VAR_tenancy_ocid="ocid1.tenancy.oc1..aaaaaaaaxxx"
```

## Usage

```bash
terraform init
terraform plan
terraform apply
terraform output instance_public_ip
```

## ⚠️ Don't run `apply` for the first instance — capacity is full

Singapore AD-1 ARM A1.Flex is at 0% capacity ~99% of the time. Use **`oci_hunter.sh`** to grab the first instance, then **`terraform import`** to manage it from then on.

## Importing an oci_hunter-created instance

```bash
# After oci_hunter succeeds, get the OCID + public IP from the script output
terraform import oci_core_instance.palanthai <INSTANCE_OCID>
terraform output instance_public_ip  # confirm import worked
```

## Why both oci_hunter.sh and Terraform?

- **`oci_hunter.sh`** = first-shot capacity grab. Aggressive retry logic with macOS notifications. Used for the *initial* instance.
- **Terraform** = stateful reproducibility. Once the instance exists, Terraform owns the config. Re-apply in 5 min if the VM dies or you want to recreate the network.
- **Recommendation**: oci_hunter → import to Terraform → day-to-day ops via Terraform.

## State management

Local state by default (`terraform.tfstate`). For team / multi-machine, enable OCI Object Storage backend (uncomment in `provider.tf`). **NEVER commit `terraform.tfstate`** — already in `.gitignore`.

## Resource rationale

| Resource | Value | Why |
|---|---|---|
| Shape | VM.Standard.A1.Flex | Always Free ARM (max 4 OCPU / 24 GB per instance) |
| OCPUs | 4 | Max for single A1.Flex |
| RAM | 24 GB | Max for single A1.Flex |
| Boot | 200 GB | Max free tier; needed for Docker + Ollama + backups |
| AD | AD-1 | Same as oci_hunter; try AD-2/AD-3 if AD-1 is full |
