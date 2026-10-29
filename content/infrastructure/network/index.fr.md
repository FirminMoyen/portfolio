---
title: "Réseau"
description: "Le réseau du lab : séparé de la maison par un pare-feu OPNsense, découpé en zones, joignable à distance par VPN sans aucun port ouvert."
summary: "Le réseau du lab : séparé de la maison par un pare-feu OPNsense, découpé en zones, joignable à distance par VPN sans aucun port ouvert."
draft: false
weight: 2
# Badge de la carte : étapes de data/roadmap.yaml (architecture §5.2).
roadmap: [opnsense-network, remote-access, network-zones]
ShowReadingTime: false
ShowPostNavLinks: false
---

Le réseau protège la maison du lab, et chaque partie du lab des autres. Un pare-feu, OPNsense, route le trafic entre les zones et applique les règles de chacune. Pour travailler à distance, j'utilise un VPN.

{{< diagram name="lab-network" alt="Schéma réseau du lab : la box domestique (1er NAT) et mes appareils (tunnel VPN) rejoignent OPNsense (pare-feu et routeur, 2e NAT), qui dessert la zone d'infrastructure (OPNsense, PVE1, PVE2), la zone isolée et les zones à venir, une /24 par usage, sans VLAN." >}}

## Un lab séparé de la maison

Le lab partage la connexion Internet de la maison, mais pas son réseau. OPNsense, un pare-feu répandu en entreprise, tourne en machine virtuelle sur PVE1 et sépare le réseau du lab de celui de la maison. Une erreur de configuration ou une machine compromise dans le lab ne doit pas pouvoir toucher la maison. Le choix et les options écartées sont expliqués dans l'[ADR-0002]({{< relref "/infrastructure/decisions/adr-0002-lab-isolated-opnsense" >}}).

## Des zones, sans VLAN

Le lab est découpé en zones : des sous-réseaux séparés, un par usage, chacun avec ses propres règles.

En entreprise, on sépare d'habitude ces zones avec des VLAN : des réseaux virtuels qui partagent les mêmes câbles, mais que le switch garde étanches entre eux. C'était mon plan. Le matériel ne l'a pas permis : le switch, non manageable, ne peut pas faire respecter les VLAN, et surtout l'adaptateur USB-Ethernet de PVE2 n'émet pas les trames VLAN.

J'ai donc gardé les zones, sans les VLAN. Elles partagent le même réseau physique, et c'est le pare-feu de Proxmox qui fait respecter leurs frontières au niveau de chaque machine virtuelle : il vérifie ses adresses et lui applique les règles de sa zone.

## Une zone isolée

La première zone est isolée du reste du lab : j'y expérimente, par curiosité, avec un agent IA autonome. La zone lui donne accès à Internet, mais ni à la maison ni au reste du lab, et je l'ai vérifié depuis la machine virtuelle qui s'y trouve.

## L'accès à distance

Pour administrer le lab depuis l'extérieur, j'utilise Tailscale, un VPN : un tunnel chiffré entre mes appareils et le lab. Je l'ai choisi après l'avoir comparé à Headscale et à NetBird ([ADR-0001]({{< relref "/infrastructure/decisions/adr-0001-remote-access-tailscale" >}})). Il ne demande d'ouvrir aucun port sur Internet, et il donne accès au réseau du lab uniquement, jamais à celui de la maison. Les interfaces d'administration ne sont pas exposées sur Internet : je les atteins par ce VPN.

## Détails techniques

- **Adressage** : le lab utilise la plage `10.42.0.0/16`, avec un /24 par zone. La zone d'infrastructure, `10.42.0.0/24`, accueille OPNsense, PVE1 et PVE2. La zone isolée est `10.42.50.0/24`.
- **Sortie sur Internet** : double NAT (traduction d'adresses, qui fait sortir des adresses privées sous une seule adresse), par la box de la maison puis par OPNsense, sans aucune redirection de port vers le lab.
- **DNS** : le domaine interne est un sous-domaine de firminmoyen.dev, résolu uniquement dans le lab.
- **Zones** : un sous-réseau /24 par zone, sur le même réseau physique. OPNsense route entre les zones avec une adresse de passerelle par zone. Le pare-feu de Proxmox est activé sur chaque VM des zones : il filtre les adresses IP et MAC et applique un groupe de règles propre à la zone.
- **Pourquoi pas de VLAN** : surtout, absence de trames VLAN en sortie de l'adaptateur USB-Ethernet de PVE2, constatée par des captures de trames, et aucun lien dans son mode propre au fabricant. Switch sw-01 non manageable. Options écartées :
  - Un réseau virtuel VXLAN, gardé comme évolution possible.
  - Un réseau à plat.
  - Des zones limitées à PVE1.
  - Un autre adaptateur, exclu par le budget zéro.
- **Zone isolée** : sortie sur Internet autorisée, réseau domestique et reste du lab injoignables, règles journalisées. Une VM Ubuntu Server 26.04 LTS y tourne, sur PVE2, administrée en SSH, par clé uniquement. L'expérience y tourne sous un compte sans droits d'administration. Tests depuis la VM : Internet répond, ni le réseau domestique ni la zone d'infrastructure (administration d'OPNsense et des deux hôtes comprise) ne répondent, et une adresse usurpée est bloquée.
- **VPN** : Tailscale tourne sur OPNsense en subnet router (le point d'entrée du VPN dans le réseau du lab) et annonce la seule route du lab, `10.42.0.0/16`.

## Limites et évolutions

- Les zones partagent le même réseau physique : elles ne sont pas isolées au niveau 2, celui des trames Ethernet. C'est une limite assumée. Un réseau virtuel VXLAN reste une évolution possible.
- Sous FreeBSD, le système d'OPNsense, le plugin Tailscale fonctionne en espace utilisateur : le pare-feu d'OPNsense ne voit donc pas le trafic venu du VPN. Pour l'instant, le cloisonnement de ce trafic repose sur la politique d'accès du VPN et sur l'annonce de la seule route du lab. Une piste est à l'étude : déplacer le subnet router dans une VM Linux, derrière le pare-feu.
- L'interface d'administration d'OPNsense n'a pas de double authentification.
