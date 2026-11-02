---
title: "Infrastructure"
description: "The lab as it is today: two Proxmox VE nodes in a cluster, a network split into zones behind OPNsense, remote access through a VPN."
draft: false
menus:
  main:
    identifier: infrastructure
    weight: 20
---

This section describes the lab as it is today: modest hardware, organised the way a company would do it. The two machines, PVE1 and PVE2, run Proxmox VE and are joined in a cluster. An OPNsense firewall, running as a virtual machine on PVE1, separates the lab from the home network and splits it into zones. One of them is isolated from the rest: there, out of curiosity, I experiment with an autonomous AI agent. I reach the lab remotely through Tailscale, a VPN, with nothing exposed to the internet. The important choices are explained in the [architecture decisions]({{< relref "/infrastructure/decisions" >}}), and the next steps on the [roadmap]({{< relref "/roadmap" >}}).
