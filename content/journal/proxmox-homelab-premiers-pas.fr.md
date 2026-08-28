---
title: "Proxmox : premiers pas sur le homelab"
date: 2026-08-27
draft: false
---

Mise en place initiale d'un nœud Proxmox VE sur le homelab, avant
automatisation via Ansible.

## Installation

Installation depuis l'image ISO officielle, sur un disque NVMe dédié. Réseau
configuré en bridge (`vmbr0`) pour exposer les VMs directement sur le LAN.

```bash
# Vérifier la version installée
pveversion

# Lister les nœuds du cluster (ici un seul nœud)
pvecm nodes
```

## Stockage

Deux types de stockage configurés :

- `local-lvm` pour les disques des VMs (thin provisioning)
- `local` pour les ISOs et templates de conteneurs

## Prochaines étapes

- Provisioning des VMs via l'API Proxmox depuis Ansible
- Mise en place d'un exporter Prometheus pour le monitoring du nœud
- Sauvegardes automatisées vers un stockage externe
