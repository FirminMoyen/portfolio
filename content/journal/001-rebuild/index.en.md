---
title: "Week 1 — Starting again from scratch"
date: 2026-10-25
draft: false
description: "The lab starts again from scratch: a first Proxmox VE node, an OPNsense firewall that isolates it from the home, remote access with no open port."
week: 1
components: [pve1, proxmox-pve1, fw-01, tailscale]
adrs: [1, 2]
tags: []
certifications: []
---

In October 2026, I wiped the homelab I had been running since 2022: it was a good opportunity to document everything from the start and to rebuild on solid foundations. In mid-October, I started the rebuild, from scratch. This first entry covers the period since then: the foundations, on a single machine, PVE1.

<!--more-->

## Separating the lab from the home

The lab shares the home's internet connection. It will host experimental machines, some of them deliberately broken or misconfigured: a mistake or a compromised machine must not be able to reach the home network. I also wanted to learn a firewall the way companies use one: zones, rules, NAT.

Plugging the lab straight into the home network would have been the simplest option, but with no isolation at all. The firewall built into Proxmox filters the machines, but does not act as a router-firewall at the network's edge. A dedicated physical firewall meant buying hardware. So I chose OPNsense, as a virtual machine on PVE1, in front of a network of the lab's own: my previous lab already used this principle, and the rebuild keeps it ([ADR-0002]({{< relref "/infrastructure/decisions/adr-0002-lab-isolated-opnsense" >}})).

I first installed Proxmox VE 9.2 on PVE1, then OPNsense as a VM, with the lab network, `10.42.0.0/24`. The limit I accept: OPNsense runs on PVE1, so if PVE1 goes down, the lab loses its gateway.

## Remote administration without opening anything

I need to be able to administer the lab from anywhere, including from my phone, without opening a port to the internet and without paying for a server. I compared three VPNs: Tailscale, Headscale and NetBird. Self-hosted, Headscale and NetBird need a server reachable from the internet: ports open at home, or a rented server. I chose Tailscale for its ease of installation, its access control and its mobile apps ([ADR-0001]({{< relref "/infrastructure/decisions/adr-0001-remote-access-tailscale" >}})).

Tailscale runs on OPNsense as a subnet router, the VPN's entry point into the lab network. The tests over 4G are conclusive: the lab is reachable, the home network is not.

The limit I accept: Tailscale's control plane is hosted by a third party. Another limit showed up along the way: on FreeBSD, the Tailscale plugin runs in userspace, and OPNsense's firewall does not see the VPN's traffic. The details and the option under study are on the [Network]({{< relref "/infrastructure/network" >}}) page.

## Preparing the zones

The lab network is planned in zones: one /24 zone per use, whose VLAN number matches the third octet. The route advertised by the VPN covered `10.42.0.0/24`. I widened it to `10.42.0.0/16`, to cover the future zones.

## What's next

Finish step 4 of the [roadmap]({{< relref "/roadmap" >}}): administering the lab without physical access, with host hardening and a full remote reboot test. Then install Proxmox VE on PVE2 and join the two machines in a two-node cluster, without high availability.

## In brief {.brief}

- **Components**: PVE1, Proxmox VE 9.2, OPNsense, Tailscale.
- **Steps**: Proxmox VE 9.2 on PVE1, OPNsense as a VM on PVE1 and the lab network `10.42.0.0/24`, Tailscale as a subnet router on OPNsense, advertised route widened to `10.42.0.0/16` (see the erratum), tests over 4G.
- **Decisions**: lab isolated from the home behind OPNsense ([ADR-0002]({{< relref "/infrastructure/decisions/adr-0002-lab-isolated-opnsense" >}})) and remote access through Tailscale ([ADR-0001]({{< relref "/infrastructure/decisions/adr-0001-remote-access-tailscale" >}})).

**Erratum (28 October 2026).** The advertised route had in fact remained limited to `10.42.0.0/24`. I fixed it on 28 October 2026: it now covers `10.42.0.0/16`.
