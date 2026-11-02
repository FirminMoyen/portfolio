---
title: "Infrastructure"
description: "Le lab tel qu'il est aujourd'hui : deux nœuds Proxmox VE en cluster, un réseau découpé en zones derrière OPNsense, un accès à distance par VPN."
draft: false
menus:
  main:
    identifier: infrastructure
    weight: 20
---

Cette section décrit le lab tel qu'il est aujourd'hui : un matériel modeste, organisé comme dans une entreprise. Les deux machines, PVE1 et PVE2, font tourner Proxmox VE et sont réunies en cluster. Un pare-feu OPNsense, en machine virtuelle sur PVE1, sépare le lab du réseau de la maison et le découpe en zones. L'une d'elles est isolée du reste : j'y expérimente, par curiosité, avec un agent IA autonome. J'accède au lab à distance par Tailscale, un VPN, sans rien exposer sur Internet. Les choix importants sont expliqués dans les [décisions d'architecture]({{< relref "/infrastructure/decisions" >}}), et les prochaines étapes sur la [feuille de route]({{< relref "/roadmap" >}}).
