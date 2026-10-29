---
title: "Infrastructure"
description: "The lab as it is today: two Proxmox VE nodes in a cluster, a network split into zones behind OPNsense, remote access through a VPN."
draft: false
menus:
  main:
    identifier: infrastructure
    weight: 20
---

This section describes the lab as it is today: the machines, the network that connects them, and the virtualization that makes them work together. The hardware is modest, but the organisation is a company's: a firewall at the entrance, separate zones, remote access with nothing exposed to the internet.

The two machines, PVE1 and PVE2, run Proxmox VE and are joined in a cluster. An OPNsense firewall, installed as a virtual machine on PVE1, separates the lab from the home network and splits it into zones. I reach it remotely through Tailscale, a VPN. One of the zones is isolated from the rest: there, out of curiosity, I experiment with an autonomous AI agent.

The important choices are explained in the [architecture decisions]({{< relref "/infrastructure/decisions" >}}), and the next steps on the [roadmap]({{< relref "/roadmap" >}}).
