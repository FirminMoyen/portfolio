---
title: "Infrastructure"
description: "Le lab tel qu'il est aujourd'hui : deux nœuds Proxmox VE en cluster, un réseau découpé en zones derrière OPNsense, un accès à distance par VPN."
draft: false
menus:
  main:
    identifier: infrastructure
    weight: 20
---

Cette section décrit le lab tel qu'il est aujourd'hui : les machines, le réseau qui les relie, et la virtualisation qui les fait travailler ensemble. Le matériel est modeste, mais l'organisation est celle d'une entreprise : un pare-feu à l'entrée, des zones séparées, un accès à distance sans rien exposer sur Internet.

Les deux machines, PVE1 et PVE2, font tourner Proxmox VE et sont réunies en cluster. Un pare-feu OPNsense, installé en machine virtuelle sur PVE1, sépare le lab du réseau de la maison et le découpe en zones. J'y accède à distance par Tailscale, un VPN. L'une des zones est isolée du reste : j'y expérimente, par curiosité, avec un agent IA autonome.

Les choix importants sont expliqués dans les [décisions d'architecture]({{< relref "/infrastructure/decisions" >}}), et les prochaines étapes sur la [feuille de route]({{< relref "/roadmap" >}}).
