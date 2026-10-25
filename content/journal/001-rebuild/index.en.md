---
title: "Rebuild: Proxmox, OPNsense and remote access"
date: 2026-10-25
draft: false
description: "The lab starts again from scratch: Proxmox VE on PVE1, the lab network behind OPNsense, remote access through Tailscale."
week: 1
components: [pve1, proxmox-pve1, fw-01, tailscale]
adrs: [1, 2]
tags: []
certifications: []
---

This first entry covers the period since mid-October 2026.

## Goal of the week

Rebuild the lab from scratch, starting with the hypervisor, the lab network and remote access.

## Done

- In mid-October 2026, I started rebuilding the lab from scratch.
- Installed Proxmox VE 9.2 on PVE1.
- OPNsense as a VM on PVE1, and the lab network `10.42.0.0/24`. The previous lab already used this principle, a virtualised OPNsense in front of a network of the lab's own; the rebuild keeps it.
- Remote access through Tailscale, with a subnet router on OPNsense.
- **Tailscale plugin limit on FreeBSD.** On FreeBSD, the Tailscale plugin runs in userspace, so OPNsense's firewall does not see traffic coming from the VPN. For now, isolation relies on the VPN's access policy and on advertising only the lab's route. One option is under study: moving the subnet router into a Linux VM, behind the firewall.
- Tests over 4G: the lab is reachable, the home network is not.

## Problems and fixes

- **Widening the advertised route.** The route advertised by the subnet router covered `10.42.0.0/24`. I widened it to `10.42.0.0/16`, to cover future zones: one /24 zone per use, whose VLAN number matches the third octet.

## Decisions

- The lab is isolated from the home network behind an OPNsense VM on PVE1: [ADR-0002]({{< relref "/infrastructure/decisions/adr-0002-lab-isolated-opnsense" >}}).
- Remote access to the lab goes through Tailscale: [ADR-0001]({{< relref "/infrastructure/decisions/adr-0001-remote-access-tailscale" >}}).

## Next steps

- Finish step 4 of the roadmap: host hardening and a full remote reboot test.
- Install Proxmox VE on PVE2.
- Form the two-node Proxmox cluster, without HA.
