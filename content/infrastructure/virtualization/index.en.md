---
title: "Virtualization"
description: "Proxmox VE, the lab's hypervisor: PVE1 and PVE2 joined in a two-node cluster, administered entirely remotely."
summary: "Proxmox VE, the lab's hypervisor: PVE1 and PVE2 joined in a two-node cluster, administered entirely remotely."
draft: false
weight: 3
ShowReadingTime: false
ShowPostNavLinks: false
---

Virtualization makes it possible to run several virtual machines (VMs) on a single physical machine. In the lab, that is the job of Proxmox VE, a hypervisor installed directly on PVE1 and PVE2. The two machines are joined in a cluster: I administer them as a single whole, from a single interface.

## A two-node cluster

In a cluster, the nodes vote to check that enough of them can see each other to make decisions: this is the quorum. A node that loses quorum can no longer start or change its VMs. With two nodes, there is a trap: if one stops, the other is left alone with half of the votes, and loses quorum.

So I gave two votes to PVE1, which carries the firewall, and only one to PVE2. If PVE2 stops, PVE1 keeps quorum on its own and can restart the firewall. If PVE1 stops, PVE2 loses quorum. The quorum test passed.

The cluster has neither high availability (HA, which would automatically restart a failed node's VMs on the other node) nor a QDevice (a small external arbiter that would add an extra vote).

## Administered without physical access

I do not need to be in front of the machines to administer them: I have rebooted them remotely, with no physical intervention. The Proxmox firewall is active on both hosts: anything not explicitly allowed in is denied.

## Technical details

- **PVE1**: Proxmox VE 9.2 (kernel 7.0), installed directly on the hardware. ZFS (a file system that checks data integrity) on the machine's single disk, with its in-memory cache, the ARC, capped at 1 GB. No-subscription repository (Proxmox updates without a subscription).
- **PVE2**: Proxmox VE, installed directly on the hardware.
- **Cluster**: two nodes, without HA or QDevice. PVE1 has two votes, PVE2 one. Quorum test passed.
- **Proxmox firewall**: active on both hosts, with an inbound policy that denies by default. Also enabled on each VM (see [Network]({{< relref "/infrastructure/network" >}})). The rules themselves are not published.
- **Access**: administration interfaces not exposed to the internet, reachable through the VPN.

## Limits and next steps

- The cluster has a single link, on the lab network, and it goes through PVE2's USB-Ethernet adapter: its latency stays below the threshold Proxmox requires on average, with little margin.
- PVE1 remains a single point of failure: it carries the firewall and the majority of the votes ([ADR-0002]({{< relref "/infrastructure/decisions/adr-0002-lab-isolated-opnsense" >}})).
- Improvement under consideration: two-factor authentication on Proxmox VE's administration interface.
