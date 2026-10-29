---
title: "Lab isolated from the home network behind OPNsense"
date: 2026-10-25
draft: false
description: "Why the lab is isolated from the home network behind a virtualised OPNsense firewall, and the options that were ruled out."
adr: 2
status: accepted
components: [fw-01, proxmox-pve1, sw-01]
supersedes:
superseded_by:
tags: []
---

## Context

The lab shares the home's Internet connection. It will host experimental VMs, test zones and services, some of which will be deliberately broken or misconfigured along the way.

My needs:

- **Protect the home network**: a configuration mistake or a compromised VM in the lab must not affect the home.
- **Learn a professional firewall**: zones, rules, NAT, as in a company.

Constraints: zero budget (existing hardware: PVE1, PVE2, the unmanaged switch sw-01), nothing publicly exposed.

The previous lab already used this principle: a virtualised OPNsense in front of a network of the lab's own. The rebuild keeps it.

The decision was made in mid-October 2026, when the lab rebuild started. This ADR was written after the fact, on 25 October 2026.

## Options considered

### Option 1 — Lab directly on the home network

- **Pros**: no network configuration, nothing to maintain.
- **Cons**: no isolation. A compromised VM or a mistake (DHCP, addressing) directly affects the home's devices. Nothing to learn on the firewall side.
- Ruled out: contrary to both needs.

### Option 2 — Isolation with the Proxmox firewall alone, without a dedicated router

- **Pros**: no extra VM. Filtering built into Proxmox, at host and VM level.
- **Cons**: the Proxmox firewall filters host and VM traffic, but does not act as a perimeter router-firewall (routing between zones, NAT, DHCP/DNS per zone, single gateway). It does not teach the target skill: zones, rules and NAT on a dedicated firewall.
- Ruled out: does not meet the need to learn a professional firewall.

### Option 3 — Dedicated physical router-firewall

- **Pros**: hardware separation, independent of the hypervisors. No single point shared with a virtualisation machine.
- **Cons**: buying hardware.
- Ruled out: zero budget.

## Decision

**The lab is isolated from the home network behind an OPNsense VM (fw-01) on PVE1.**

### Chosen implementation

- OPNsense, as a VM on PVE1, is the lab's firewall and router. The switch sw-01 is dedicated to the lab.
- Lab network `10.42.0.0/16`, one /24 zone per use. The VLAN number matches the subnet's third octet.

## Consequences

**Positive**

- Traffic between the lab and the home network goes through explicit firewall rules.
- A realistic learning ground: zones, rules, NAT, VLANs, on a firewall widely used in companies.
- The zone-based addressing plan prepares the segmentation of future uses (monitoring, Windows, Linux, networking, Kubernetes).

**Negative and risks**

- **Single point of failure**: OPNsense is a VM on PVE1. If PVE1 or the VM goes down, the lab loses its gateway: Internet, routing between zones, and remote access through the subnet router (see [ADR-0001]({{< relref "/infrastructure/decisions/adr-0001-remote-access-tailscale" >}})).
- **Unmanaged switch**: sw-01 does not handle VLANs. Carrying several zones to PVE2 is not solved. The question remains open, this ADR does not settle it.

**To revisit**

- Carrying the zones to PVE2, when the next zones are created.
- The gateway's resilience, if the lab becomes more important (accepted today for budget reasons).
