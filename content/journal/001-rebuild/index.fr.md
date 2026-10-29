---
title: "Semaine 1 — Repartir de zéro"
date: 2026-10-25
draft: false
description: "Le lab repart de zéro : un premier nœud Proxmox VE, un pare-feu OPNsense qui l'isole de la maison, un accès à distance sans aucun port ouvert."
week: 1
components: [pve1, proxmox-pve1, fw-01, tailscale]
adrs: [1, 2]
tags: []
certifications: []
---

En octobre 2026, j'ai effacé le homelab que je faisais tourner depuis 2022 : c'était une bonne occasion de tout documenter depuis le début et de repartir sur de bonnes bases. Mi-octobre, j'ai démarré la reconstruction, de zéro. Cette première entrée couvre la période depuis ce démarrage : les fondations, sur une seule machine, PVE1.

<!--more-->

## Séparer le lab de la maison

Le lab partage la connexion Internet de la maison. Il va accueillir des machines d'expérimentation, dont certaines seront volontairement cassées ou mal configurées : une erreur ou une machine compromise ne doit pas pouvoir toucher le réseau de la maison. Je voulais aussi apprendre un pare-feu comme en entreprise : zones, règles, NAT.

Brancher le lab directement sur le réseau de la maison aurait été le plus simple, mais sans aucune isolation. Le pare-feu intégré à Proxmox filtre les machines, mais ne joue pas le rôle d'un routeur-pare-feu à l'entrée du réseau. Un pare-feu physique dédié demandait d'acheter du matériel. J'ai donc choisi OPNsense, en machine virtuelle sur PVE1, devant un réseau propre au lab : c'est le principe qu'utilisait déjà mon lab précédent, et la reconstruction le reprend ([ADR-0002]({{< relref "/infrastructure/decisions/adr-0002-lab-isolated-opnsense" >}})).

J'ai d'abord installé Proxmox VE 9.2 sur PVE1, puis OPNsense en VM, avec le réseau du lab, `10.42.0.0/24`. La limite que j'accepte : OPNsense tourne sur PVE1, donc si PVE1 tombe, le lab perd sa passerelle.

## Administrer à distance sans rien ouvrir

Je dois pouvoir administrer le lab de n'importe où, y compris depuis mon téléphone, sans ouvrir de port sur Internet et sans payer de serveur. J'ai comparé trois VPN : Tailscale, Headscale et NetBird. En auto-hébergé, Headscale et NetBird demandent un serveur joignable depuis Internet : des ports ouverts à la maison, ou un serveur loué. J'ai choisi Tailscale pour sa facilité d'installation, son contrôle d'accès et ses applications mobiles ([ADR-0001]({{< relref "/infrastructure/decisions/adr-0001-remote-access-tailscale" >}})).

Tailscale tourne sur OPNsense en subnet router, le point d'entrée du VPN dans le réseau du lab. Les tests depuis la 4G sont concluants : le lab est joignable, le réseau de la maison ne l'est pas.

La limite que j'accepte : le plan de contrôle de Tailscale est hébergé par un tiers. Une autre limite est apparue en route : sous FreeBSD, le plugin Tailscale tourne en espace utilisateur, et le pare-feu d'OPNsense ne voit pas le trafic du VPN. Le détail et la piste à l'étude sont sur la page [Réseau]({{< relref "/infrastructure/network" >}}).

## Préparer les zones

Le réseau du lab est prévu en zones : une zone /24 par usage, dont le numéro de VLAN reprend le troisième octet. La route annoncée par le VPN couvrait `10.42.0.0/24`. Je l'ai élargie à `10.42.0.0/16`, pour couvrir les futures zones.

## La suite

Terminer l'étape 4 de la [feuille de route]({{< relref "/infrastructure" >}}#lab-roadmap) : administrer le lab sans accès physique, avec le durcissement de l'hôte et un test de redémarrage complet à distance. Ensuite, installer Proxmox VE sur PVE2 et réunir les deux machines dans un cluster à deux nœuds, sans haute disponibilité.

## En bref {.brief}

- **Composants** : PVE1, Proxmox VE 9.2, OPNsense, Tailscale.
- **Étapes** : Proxmox VE 9.2 sur PVE1, OPNsense en VM sur PVE1 et réseau du lab `10.42.0.0/24`, Tailscale en subnet router sur OPNsense, route annoncée élargie à `10.42.0.0/16` (voir l'erratum), tests depuis la 4G.
- **Décisions** : lab isolé de la maison derrière OPNsense ([ADR-0002]({{< relref "/infrastructure/decisions/adr-0002-lab-isolated-opnsense" >}})) et accès distant par Tailscale ([ADR-0001]({{< relref "/infrastructure/decisions/adr-0001-remote-access-tailscale" >}})).

**Erratum (28 octobre 2026).** La route annoncée était en réalité restée limitée à `10.42.0.0/24`. Je l'ai corrigée le 28 octobre 2026 : elle couvre maintenant `10.42.0.0/16`.
