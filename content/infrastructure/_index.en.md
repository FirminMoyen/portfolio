---
title: "Infrastructure"
description: "The homelab's infrastructure: hardware, network and virtualization."
draft: false
menus:
  main:
    identifier: infrastructure
    weight: 20
---

This section describes the lab's infrastructure, that is, what the rest of the lab depends on to work. What is consumed without the rest depending on it belongs to services. When in doubt, one question decides: if this component stops, which other components stop working?

Today, the lab runs on a single node, Hermes, with Proxmox VE. An OPNsense firewall, in a VM on Hermes, isolates the lab from the home network. I reach the lab remotely through Tailscale, with no port open to the internet. A second node, Atlas, then a two-node Proxmox cluster are planned.

The infrastructure is split into three groups: hardware, network and virtualization.
