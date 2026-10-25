---
title: "Virtualization"
description: "Proxmox VE, the lab's hypervisor: running on Hermes, then on Atlas, before a two-node cluster without high availability."
draft: false
weight: 3
ShowReadingTime: false
ShowPostNavLinks: false
---

## Role in the lab

Proxmox VE is the lab's hypervisor. It is running on Hermes, where it runs OPNsense in a VM.

## Implementation

I installed Proxmox VE directly on Hermes, with ZFS on the machine's single disk and the no-subscription repository.

## Operations

Administration interfaces are not exposed to the internet and are reachable through the VPN. Proxmox VE's uses local accounts, without 2FA.

Backups and monitoring are not in place yet: I have deferred them.

The current step is about remote administration without physical access: host hardening and a full remote reboot test.

## Limits and next steps

After Hermes, I will install Proxmox VE on Atlas, then join the two nodes in a Proxmox cluster, without high availability. With two nodes, if one stops, the other loses quorum.
