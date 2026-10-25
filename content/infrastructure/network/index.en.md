---
title: "Network"
description: "The lab's network: isolated from the home network behind OPNsense, reachable remotely through Tailscale, with no port open to the internet."
draft: false
weight: 2
ShowReadingTime: false
ShowPostNavLinks: false
---

## Role in the lab

The network isolates the lab from the home network. OPNsense, in a VM on PVE1, is the lab's firewall and router. The sw-01 switch is dedicated to the lab. Tailscale provides remote access.

## Implementation

{{< diagram name="lab-network" alt="Lab network diagram: the home router (1st NAT) and my devices (VPN tunnel) reach OPNsense (fw-01, 2nd NAT, gateway 10.42.0.1), which serves the infrastructure zone 10.42.0.0/24 (fw-01 .1, PVE1 .2, PVE2 .3 planned) and the upcoming zones, one per use, VLAN equal to the 3rd octet." >}}

The lab reaches the internet through the home router, so there is a double NAT: the router, then OPNsense. No port is forwarded to the lab.

The lab uses the `10.42.0.0/16` range, split into one /24 zone per purpose. The VLAN number matches the third octet. The `10.42.0.0/24` zone is the physical infrastructure: OPNsense at `.1`, PVE1 at `.2`, PVE2 at `.3`.

The internal DNS domain is a subdomain of firminmoyen.dev, resolved only inside the lab.

For remote access, I chose Tailscale after comparing it with Headscale and NetBird. Tailscale runs on OPNsense as a subnet router and advertises the `10.42.0.0/16` route. The VPN gives access to the lab network only, never to the home network. No port is open to the internet.

## Operations

Administration interfaces are not exposed to the internet and are reachable through the VPN. OPNsense's web interface uses local accounts, without 2FA.

Backups and monitoring are not in place yet: I have deferred them.

## Limits and next steps

On FreeBSD, the Tailscale plugin runs in userspace, so OPNsense's firewall does not see traffic coming from the VPN. For now, isolation relies on the VPN's access policy and on advertising only the lab's route. One option is under study: moving the subnet router into a Linux VM, behind the firewall.
