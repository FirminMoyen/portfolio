---
title: "Lab isolé du réseau domestique derrière OPNsense"
date: 2026-10-25
draft: false
description: "Pourquoi le lab est isolé du réseau domestique derrière un pare-feu OPNsense virtualisé, et les options écartées."
adr: 2
status: accepted
components: [fw-01, proxmox-pve1, sw-01]
supersedes:
superseded_by:
tags: []
---

## Contexte

Le lab partage la connexion Internet de la maison. Il va accueillir des VM d'expérimentation, des zones de test et des services dont certains seront volontairement cassés ou mal configurés au cours de l'apprentissage.

Mes besoins :

- **Protéger le réseau domestique** : une erreur de configuration ou une VM compromise dans le lab ne doit pas toucher la maison.
- **Apprendre un pare-feu professionnel** : zones, règles, NAT, comme en entreprise.

Contraintes : budget zéro (matériel existant : PVE1, PVE2, le switch non manageable sw-01), rien d'exposé publiquement.

Le lab précédent utilisait déjà ce principe : OPNsense virtualisé devant un réseau propre au lab. La reconstruction le reprend.

La décision a été prise mi-octobre 2026, au démarrage de la reconstruction du lab. Cette ADR est rédigée a posteriori, le 25 octobre 2026.

## Options considérées

### Option 1 — Lab directement sur le réseau domestique

- **Avantages** : aucune configuration réseau, rien à maintenir.
- **Inconvénients** : aucune isolation. Une VM compromise ou une erreur (DHCP, adressage) touche directement les appareils de la maison. Rien à apprendre côté pare-feu.
- Écartée : contraire aux deux besoins.

### Option 2 — Isolation avec le seul pare-feu Proxmox, sans routeur dédié

- **Avantages** : pas de VM supplémentaire. Filtrage intégré à Proxmox, au niveau des hôtes et des VM.
- **Inconvénients** : le pare-feu Proxmox filtre le trafic des hôtes et des VM, mais ne remplit pas le rôle d'un routeur-pare-feu de périmètre (routage entre zones, NAT, DHCP/DNS par zone, passerelle unique). Il n'apprend pas le métier visé : zones, règles et NAT sur un pare-feu dédié.
- Écartée : ne répond pas au besoin d'apprentissage d'un pare-feu professionnel.

### Option 3 — Routeur-pare-feu physique dédié

- **Avantages** : séparation matérielle, indépendante des hyperviseurs. Pas de point unique partagé avec une machine de virtualisation.
- **Inconvénients** : achat de matériel.
- Écartée : budget zéro.

## Décision

**Le lab est isolé du réseau domestique derrière une VM OPNsense (fw-01) sur PVE1.**

### Mise en œuvre retenue

- OPNsense, en VM sur PVE1, est le pare-feu et le routeur du lab. Le switch sw-01 est dédié au lab.
- Réseau du lab `10.42.0.0/16`, une zone /24 par usage. Le numéro de VLAN reprend le troisième octet du sous-réseau.

## Conséquences

**Positives**

- Les flux entre le lab et le réseau domestique passent par des règles explicites du pare-feu.
- Terrain d'apprentissage réaliste : zones, règles, NAT, VLAN, sur un pare-feu répandu en entreprise.
- Le plan d'adressage par zones prépare la segmentation des futurs usages (monitoring, Windows, Linux, réseau, Kubernetes).

**Négatives et risques**

- **Point unique de défaillance** : OPNsense est une VM sur PVE1. Si PVE1 ou la VM tombe, le lab perd sa passerelle : Internet, routage entre zones, et l'accès distant par le subnet router (voir [ADR-0001]({{< relref "/infrastructure/decisions/adr-0001-remote-access-tailscale" >}})).
- **Switch non manageable** : sw-01 ne gère pas les VLAN. Le transport de plusieurs zones vers PVE2 n'est pas résolu. La question reste ouverte, cette ADR ne la tranche pas.

**À réexaminer**

- Le transport des zones vers PVE2, au moment de créer les prochaines zones.
- La résilience de la passerelle, si le lab prend de l'importance (aujourd'hui acceptée par budget).
