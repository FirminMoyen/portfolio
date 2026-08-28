---
title: "Proxmox: first steps on the homelab"
date: 2026-08-27
draft: false
slug: "proxmox-homelab-first-steps"
---

Initial setup of a Proxmox VE node on the homelab, ahead of automation via
Ansible.

## Installation

Installed from the official ISO image, on a dedicated NVMe disk. Network
configured as a bridge (`vmbr0`) to expose VMs directly on the LAN.

```bash
# Check the installed version
pveversion

# List cluster nodes (a single node here)
pvecm nodes
```

## Storage

Two storage types configured:

- `local-lvm` for VM disks (thin provisioning)
- `local` for ISOs and container templates

## Next steps

- Provisioning VMs via the Proxmox API from Ansible
- Setting up a Prometheus exporter for node monitoring
- Automated backups to external storage
