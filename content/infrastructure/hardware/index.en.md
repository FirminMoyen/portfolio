---
title: "Hardware"
description: "The lab's machines: PVE1, running, and PVE2, planned."
draft: false
weight: 1
ShowReadingTime: false
ShowPostNavLinks: false
---

## Role in the lab

The lab relies on two Dell laptops. PVE1 carries the lab's infrastructure: firewall, router and remote access. PVE2 will carry the VMs and containers for services.

## Implementation

{{< diagram name="lab-physical" alt="Lab physical diagram: the internet comes in through the home router (1st NAT) to the OPNsense VM on PVE1 (Dell Latitude 7490, 2nd NAT); PVE1 is cabled to the sw-01 switch (5 ports), which will connect PVE2 (Dell XPS 15, planned)." >}}

PVE1 is running: Proxmox VE is installed directly on the hardware (see the Virtualization page). PVE2 is not installed yet.

## Operations

Backups and monitoring are not in place yet: I have deferred them.

## Limits and next steps

Until PVE2 is installed, PVE1 is the lab's only node. Installing Proxmox VE on PVE2 is the next step after the current one, before the two nodes are joined in a cluster.
