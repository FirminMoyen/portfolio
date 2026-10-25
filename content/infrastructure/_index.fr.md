---
title: "Infrastructure"
description: "L'infrastructure du homelab : matériel, réseau et virtualisation."
draft: false
menus:
  main:
    identifier: infrastructure
    weight: 20
---

Cette section décrit l'infrastructure du lab, c'est-à-dire ce dont le reste du lab dépend pour fonctionner. Ce qui est consommé sans que le reste en dépende relève des services. En cas de doute, une question tranche : si ce composant s'arrête, quels autres composants cessent de fonctionner ?

Aujourd'hui, le lab tourne sur un seul nœud, PVE1, avec Proxmox VE. Un pare-feu OPNsense, en VM sur PVE1, isole le lab du réseau domestique. J'accède au lab à distance par Tailscale, sans aucun port ouvert sur Internet. Un second nœud, PVE2, puis un cluster Proxmox à deux nœuds sont prévus.

L'infrastructure est répartie en trois groupes : matériel, réseau et virtualisation.

## Feuille de route

Les étapes, dans l'ordre. La chronologie se lit dans le journal, semaine par semaine. Après le cluster, l'ordre n'est pas encore fixé.

{{< roadmap >}}
