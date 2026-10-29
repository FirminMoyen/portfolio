---
title: "Week 2 — A second node, and a plan B for the network"
date: 2026-10-28
draft: false
description: "PVE2 joins the lab, the two nodes form a cluster, and the network is split into zones without VLANs, for lack of compatible hardware."
week: 2
components: [pve2, proxmox-pve2, proxmox-cluster, fw-01, tailscale]
adrs: [2]
tags: []
certifications: []
---

Week 1 laid the foundations on a single machine. This week, the lab went from one machine to two: PVE2 joined PVE1, the two now form a cluster, and the network was split into zones. Not as planned: the hardware refused VLANs, and I had to find another way.

<!--more-->

## A second node, and a cluster

PVE2 is a Dell XPS 15 9570: 6 cores, 32 GB of memory, but no Ethernet port. I connected it to the switch through a USB-Ethernet adapter, disabled and powered off its NVIDIA GPU, not needed here, and installed Proxmox VE. Like PVE1, it restarts on its own after a power outage, and I have rebooted it remotely. With the Proxmox firewall active on both hosts, denying by default anything that comes in without permission, the "remote administration without physical access" step is done.

What remained was to join the two machines. A two-node cluster hides a trap: the nodes vote to keep quorum, the right to make decisions, and if one stops, the other is left alone with half of the votes. It then loses quorum and can no longer start its VMs. I gave two votes to PVE1, which carries the firewall, and only one to PVE2: if PVE2 stops, PVE1 keeps quorum on its own and can restart the firewall. The quorum test passed. The cluster has neither high availability nor a QDevice, an external arbiter that would add an extra vote (see [Virtualization]({{< relref "/infrastructure/virtualization" >}})).

The limits I accept: if PVE1 stops, PVE2 loses quorum. And the cluster has a single link, which goes through PVE2's USB adapter: its latency stays below the threshold Proxmox requires on average, but with little margin.

## Zones without VLANs

The week 1 plan had zones separated by VLANs, those virtual networks that share the same cables but stay sealed off from each other. The hardware said no. The switch, being unmanaged, cannot enforce VLANs, and above all PVE2's USB-Ethernet adapter does not send VLAN frames: I checked it with frame captures, and its vendor-specific mode does not even bring a link up.

I set the other options aside:

- A VXLAN virtual network, which would carry the zones in a tunnel over the existing network, and which I keep as a possible next step.
- A flat network.
- Zones limited to PVE1.
- Another adapter, ruled out by the zero budget.

I chose routed zones. Each zone has its own subnet, on the same physical network, and OPNsense routes between them with one gateway per zone. The Proxmox firewall, enabled on each zone VM, enforces the boundaries: it filters the machine's IP and MAC addresses and applies its zone's rules to it. The details are on the [Network]({{< relref "/infrastructure/network" >}}) page. The limit I accept: without VLANs, the zones are not isolated at layer 2, the layer of Ethernet frames.

The first zone I created is an isolated zone, where I experiment, out of curiosity, with an autonomous AI agent. It can reach the internet, but the home and the rest of the lab are unreachable from it, and its rules are logged. I installed an Ubuntu Server 26.04 LTS VM in it, on PVE2, reachable only over SSH with a key. The experiment runs in it under an account without administrator rights. From this VM, I checked that everything holds: the internet answers, neither the home network nor the infrastructure zone (including the administration of OPNsense and of both hosts) answers, and a spoofed address is blocked.

## The route I thought I had widened

In week 1, I had widened the route advertised by the VPN to the whole lab network, `10.42.0.0/16`. Or so I thought: it had remained limited to the infrastructure zone, `10.42.0.0/24`. I fixed it on 28 October. It now covers the whole lab, and an erratum says so in the [week 1 entry]({{< relref "/journal/001-rebuild" >}}).

## What's next

Next step on the [roadmap]({{< relref "/roadmap" >}}): setting up a monitoring stack. So far, I have installed and configured everything by hand: automation with Ansible and Terraform will come after that.

## In brief {.brief}

- **Components**: PVE2 (Dell XPS 15 9570, 6 cores, 32 GB), Proxmox VE on PVE2, two-node Proxmox cluster, Proxmox firewall, OPNsense, Tailscale.
- **Steps**:
  - Proxmox VE on PVE2.
  - Proxmox firewall active on both hosts, inbound denied by default.
  - Remote reboot.
  - Two-node cluster (PVE1: two votes, PVE2: one), quorum test passed.
  - Routed zones without VLANs, one /24 per zone.
  - Isolated zone `10.42.50.0/24` and its Ubuntu Server 26.04 LTS VM, isolation tests passed.
  - VPN route fixed to `10.42.0.0/16`.
- **Decisions**: routed zones rather than VLANs, with the Proxmox firewall on each zone VM (see [Network]({{< relref "/infrastructure/network" >}})). Two votes for PVE1, one for PVE2 (see [Virtualization]({{< relref "/infrastructure/virtualization" >}})).
- **Limits accepted**: no layer 2 isolation between zones. A single cluster link, with little latency margin.
