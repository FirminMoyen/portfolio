---
title: "Network"
description: "The lab's network: separated from the home by an OPNsense firewall, split into zones, reachable remotely through a VPN with no open port."
summary: "The lab's network: separated from the home by an OPNsense firewall, split into zones, reachable remotely through a VPN with no open port."
draft: false
weight: 2
ShowReadingTime: false
ShowPostNavLinks: false
---

The network protects the home from the lab, and each part of the lab from the others. A firewall, OPNsense, routes traffic between the zones and applies each zone's rules. To work remotely, I use a VPN.

{{< diagram name="lab-network" alt="Lab network diagram: the home router (1st NAT) and my devices (VPN tunnel) reach OPNsense (firewall and router, 2nd NAT), which serves the infrastructure zone (OPNsense, PVE1, PVE2), the isolated zone and the upcoming zones, one /24 per use, without VLANs." >}}

## A lab separated from the home

The lab shares the home's internet connection, but not its network. OPNsense, a firewall widely used in companies, runs as a virtual machine on PVE1 and separates the lab network from the home network. A configuration mistake or a compromised machine in the lab must not be able to reach the home. The choice and the options set aside are explained in [ADR-0002]({{< relref "/infrastructure/decisions/adr-0002-lab-isolated-opnsense" >}}).

## Zones, without VLANs

The lab is split into zones: separate subnets, one per purpose, each with its own rules.

In a company, these zones are usually separated with VLANs: virtual networks that share the same cables but that the switch keeps sealed off from each other. That was my plan. The hardware did not allow it: the switch, being unmanaged, cannot enforce VLANs, and above all PVE2's USB-Ethernet adapter does not send VLAN frames.

So I kept the zones, without the VLANs. They share the same physical network, and the Proxmox firewall enforces their boundaries at the level of each virtual machine: it checks the machine's addresses and applies its zone's rules to it.

## An isolated zone

The first zone is isolated from the rest of the lab: there, out of curiosity, I experiment with an autonomous AI agent. The zone gives it access to the internet, but neither to the home nor to the rest of the lab, and I checked this from the virtual machine that lives there.

## Remote access

To administer the lab from outside, I use Tailscale, a VPN: an encrypted tunnel between my devices and the lab. I chose it after comparing it with Headscale and NetBird ([ADR-0001]({{< relref "/infrastructure/decisions/adr-0001-remote-access-tailscale" >}})). It requires no port open to the internet, and it gives access to the lab network only, never to the home network. The administration interfaces are not exposed to the internet: I reach them through this VPN.

## Technical details

- **Addressing**: the lab uses the `10.42.0.0/16` range, with one /24 per zone. The infrastructure zone, `10.42.0.0/24`, hosts OPNsense, PVE1 and PVE2. The isolated zone is `10.42.50.0/24`.
- **Internet access**: double NAT (network address translation, which lets private addresses go out under a single address), through the home router and then OPNsense, with no port forwarded to the lab.
- **DNS**: the internal domain is a subdomain of firminmoyen.dev, resolved only inside the lab.
- **Zones**: one /24 subnet per zone, on the same physical network. OPNsense routes between the zones with one gateway address per zone. The Proxmox firewall is enabled on each VM: it filters IP and MAC addresses and applies a rule group specific to the zone.
- **Why no VLANs**: above all, no VLAN frames leaving PVE2's USB-Ethernet adapter, confirmed with frame captures, and no link in its vendor-specific mode. Unmanaged sw-01 switch. Options set aside:
  - A VXLAN virtual network, kept as a possible next step.
  - A flat network.
  - Zones limited to PVE1.
  - Another adapter, ruled out by the zero budget.
- **Isolated zone**: outbound internet access allowed, home network and the rest of the lab unreachable, rules logged. An Ubuntu Server 26.04 LTS VM runs there, on PVE2, reachable only over SSH with a key. The experiment runs in it under an account without administrator rights. Tests from the VM: the internet answers, neither the home network nor the infrastructure zone (including the administration of OPNsense and of both hosts) answers, and a spoofed address is blocked.
- **VPN**: Tailscale runs on OPNsense as a subnet router (the VPN's entry point into the lab network) and advertises only the lab's route, `10.42.0.0/16`.

## Limits and next steps

- The zones share the same physical network: they are not isolated at layer 2, the layer of Ethernet frames. This is an accepted limit. A VXLAN virtual network remains a possible next step.
- On FreeBSD, the system OPNsense is built on, the Tailscale plugin runs in userspace, so OPNsense's firewall does not see traffic coming from the VPN. For now, isolation of that traffic relies on the VPN's access policy and on advertising only the lab's route. One option is under study: moving the subnet router into a Linux VM, behind the firewall.
- Improvement under consideration: two-factor authentication on OPNsense's administration interface.
