---
title: "Reconstruction : Proxmox, OPNsense et accès distant"
date: 2026-10-25
draft: false
description: "Le lab repart de zéro : Proxmox VE sur Hermes, réseau du lab derrière OPNsense, accès distant par Tailscale."
week: 1
components: [hermes, pve1, fw-01, tailscale]
adrs: [1, 2]
tags: []
certifications: []
---

Cette première entrée couvre la période depuis mi-octobre 2026.

## Objectif de la semaine

Reconstruire le lab de zéro, en commençant par l'hyperviseur, le réseau du lab et l'accès distant.

## Réalisé

- Mi-octobre 2026, j'ai démarré la reconstruction du lab de zéro ; l'ancien lab a été effacé.
- Installation de Proxmox VE 9.2 sur Hermes.
- OPNsense en VM sur Hermes, et réseau du lab `10.42.0.0/24`. Le lab précédent utilisait déjà ce principe, OPNsense virtualisé devant un réseau propre au lab ; la reconstruction le reprend.
- Accès distant par Tailscale, avec un subnet router sur OPNsense.
- **Mode netstack imposé sous FreeBSD.** Sous FreeBSD, le plugin Tailscale fonctionne en espace utilisateur : le pare-feu d'OPNsense ne voit donc pas le trafic venu du VPN. Le cloisonnement repose pour l'instant sur la politique d'accès du VPN et sur l'annonce de la seule route du lab. Une piste est à l'étude : déplacer le subnet router dans une VM Linux, derrière le pare-feu.
- Tests depuis la 4G : le lab est joignable, le réseau domestique ne l'est pas.

## Problèmes et résolution

- **Élargissement de la route annoncée.** La route annoncée par le subnet router couvrait `10.42.0.0/24`. Je l'ai élargie à `10.42.0.0/16`, pour couvrir les futures zones : une zone /24 par usage, dont le numéro de VLAN reprend le troisième octet.

## Décisions

- Le lab est isolé du réseau domestique derrière une VM OPNsense sur Hermes : [ADR-0002]({{< relref "/infrastructure/decisions/adr-0002-lab-isolated-opnsense" >}}).
- L'accès distant au lab passe par Tailscale : [ADR-0001]({{< relref "/infrastructure/decisions/adr-0001-remote-access-tailscale" >}}).

## Semaine prochaine

- Terminer l'étape 4 de la feuille de route : durcissement de l'hôte et test de redémarrage complet à distance.
- Installer Proxmox VE sur Atlas.
