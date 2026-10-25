---
title: "Remote access to the lab through Tailscale"
date: 2026-10-25
draft: false
description: "Why I reach the lab remotely through Tailscale rather than Headscale or NetBird, with no port open to the Internet."
adr: 1
status: accepted
components: [tailscale, fw-01]
supersedes:
superseded_by:
tags: []
---

## Context

I need to manage the lab remotely, including from my phone. Constraints:

- **Nothing publicly exposed**: no port open from the Internet to the lab.
- **Zero budget**: only hardware I already own, no paid subscription, no rented server (VPS).
- **Enterprise-grade security**: strong authentication, explicit access control (least privilege), segmentation between the lab and the home network.
- **A single user** for now: me.

The decision was made in mid-October 2026, when the lab rebuild started (installation order: Proxmox, OPNsense network, then Tailscale). This ADR was written after the fact, on 25 October 2026.

## Options considered

All three options are WireGuard-based overlay networks, with a control plane that distributes keys and the access policy, and clients that set up direct tunnels between each other when possible (through a relay otherwise). None of them requires opening an inbound port to the lab.

### Option 1 — Tailscale (control plane hosted by Tailscale)

- **Pros**
  - Simple setup: no coordination server to install or maintain; a plugin is available for OPNsense.
  - Full access control in the VPN's access policy.
  - Official mobile apps (iOS, Android).
  - Free "Personal" plan for personal, non-commercial use, enough for a single user ([pricing](https://tailscale.com/pricing/), [FAQ](https://tailscale.com/kb/1251/pricing-faq)).
- **Cons**
  - The control plane is a SaaS: identity, key distribution and the access policy depend on a third party.
  - The free plan has limits (number of users, features) that could matter if the lab opens up to other people.

### Option 2 — Headscale (self-hosted Tailscale control plane)

- **Pros**
  - Free software, a reimplementation of Tailscale's coordination server; uses the official Tailscale clients ([documentation](https://github.com/juanfont/headscale/blob/main/docs/about/features.md)).
  - No dependency on a SaaS for the control plane.
- **Cons**
  - One more server to install, secure, back up and update.
  - To reach the lab over 4G, the coordination server must be reachable from the Internet: either it is exposed from home (contrary to "nothing exposed"), or it runs on a rented server (contrary to the zero budget).
  - Fewer features than the official service: the project targets personal use and does not cover Tailscale's full scope.

### Option 3 — NetBird (hosted or self-hosted)

- **Pros**
  - Free software (BSD-3 licence), self-hostable, with a hosted offering; access policies based on groups and rules, device posture checks; iOS and Android clients ([repository](https://github.com/netbirdio/netbird), [documentation](https://docs.netbird.io)).
- **Cons**
  - Self-hosted: same problem as Headscale; the installation documentation requires a publicly reachable VM (domain name, TCP 80/443, UDP 3478).
  - Hosted: same SaaS dependency as Tailscale.
- **Why I ranked it behind Tailscale**:
  1. self-hosted, NetBird requires a server reachable from the Internet (open ports or a VPS), which is contrary to "nothing exposed" and to the zero budget;
  2. no OPNsense plugin, whereas Tailscale installs directly on OPNsense through a plugin;
  3. maturity and community: Tailscale is more widespread and better documented, with more field reports.
- **Factual note (checked on 25 October 2026)**: an `os-netbird` plugin now exists in OPNsense's official repository, included from OPNsense 25.7.3 according to the NetBird documentation ([OPNsense guide](https://docs.opnsense.org/manual/how-tos/netbird.html), [NetBird guide](https://docs.netbird.io/get-started/install/opnsense)). It creates a `wt0` interface that can be assigned and filtered by OPNsense's firewall rules; NetBird policies do not create these rules automatically. Reason 2 is kept as I gave it; it would need revisiting if remote access is reconsidered.

## Decision

**Tailscale**, with the control plane hosted by Tailscale.

The criteria that tipped the balance:

1. ease of setup;
2. the access control features;
3. the mobile apps.

### Chosen implementation

- **Subnet router on OPNsense** (Tailscale plugin), advertising only the lab's network, `10.42.0.0/16`; the home network is not advertised.
- **Access policy**: restrictive. Its content is not published.
- **Validation**: tests over 4G succeeded; the lab is reachable, the home network is not.

## Consequences

**Positive**

- No inbound port open to the Internet; the exposed surface does not grow.
- Access from the phone and the computer with no extra infrastructure.
- The VPN gives access to the lab and only to the lab: only the `10.42.0.0/16` route is advertised.

**Negative and risks**

- **Dependency on a third-party service**: the control plane is hosted by Tailscale. An outage or a change in the service's terms can affect remote access; Headscale remains a possible way out, since it uses the same clients.
- **The firewall does not filter VPN traffic.** On FreeBSD, the Tailscale plugin runs in userspace, so OPNsense's firewall does not see traffic coming from the VPN. For now, isolation relies on the VPN's access policy and on advertising only the lab's route. One option is under study: moving the subnet router into a Linux VM, behind the firewall.

**To revisit**

- The option above: the question remains open, this ADR does not settle it.
- The VPN's access policy: to review with every new zone or new device.
