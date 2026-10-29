---
title: "Physical infrastructure"
description: "The lab's two machines, PVE1 and PVE2: two Dell laptops connected by a small switch, administered entirely remotely."
summary: "The lab's two machines, PVE1 and PVE2: two Dell laptops connected by a small switch, administered entirely remotely."
draft: false
weight: 1
# Badge de la carte : étapes de data/roadmap.yaml (architecture §5.2).
roadmap: [proxmox-pve1, proxmox-pve2]
ShowReadingTime: false
ShowPostNavLinks: false
---

The whole lab fits on two Dell laptops I already had, connected by a small switch. No server was bought for it: that is the zero-budget constraint, and a good exercise in getting the most out of limited resources. Both machines run without my having to touch them: I administer them entirely remotely.

{{< diagram name="lab-physical" alt="Lab physical diagram: the internet comes in through the home router (1st NAT) to the OPNsense VM on PVE1 (Dell Latitude 7490, 2nd NAT). PVE1 is cabled to the sw-01 switch (5 ports), which also connects PVE2 (Dell XPS 15, through a USB-Ethernet adapter)." >}}

## Two laptops, two roles

PVE1, a Dell Latitude 7490, carries the lab's infrastructure: the firewall, the router and remote access. PVE2, a Dell XPS 15 9570, is meant for the virtual machines and containers for services. On both, Proxmox VE is installed directly on the hardware (see [Virtualization]({{< relref "/infrastructure/virtualization" >}})).

## Technical details

- **PVE1**: Dell Latitude 7490, 4 cores, 16 GB of memory.
- **PVE2**: Dell XPS 15 9570, 6 cores, 32 GB of memory. It has no built-in Ethernet port: it is connected to the switch through a USB-Ethernet adapter. Its NVIDIA GPU, not needed for now, is disabled and powered off.
- **sw-01**: unmanaged switch (it cannot be configured) with 5 ports, dedicated to the lab.
- **No physical access needed**: both machines restart on their own after a power outage, and I have rebooted them remotely.

## Limits and next steps

PVE2's USB-Ethernet adapter has two consequences: it does not send VLAN frames, which led me to organise the network differently (see [Network]({{< relref "/infrastructure/network" >}})), and the cluster link goes through it (see [Virtualization]({{< relref "/infrastructure/virtualization" >}})).
