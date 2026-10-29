---
title: "Semaine 2 — Un second nœud, et un plan B pour le réseau"
date: 2026-10-28
draft: false
description: "PVE2 rejoint le lab, les deux nœuds forment un cluster, et le réseau se découpe en zones sans VLAN, faute de matériel compatible."
week: 2
components: [pve2, proxmox-pve2, proxmox-cluster, fw-01, tailscale]
adrs: [2]
tags: []
certifications: []
---

La semaine 1 avait posé les fondations sur une seule machine. Cette semaine, le lab est passé à deux : PVE2 a rejoint PVE1, les deux forment maintenant un cluster, et le réseau s'est découpé en zones. Pas comme prévu : le matériel a refusé les VLAN, et il a fallu trouver un autre chemin.

<!--more-->

## Un second nœud, et un cluster

PVE2 est un Dell XPS 15 9570 : 6 cœurs, 32 Go de mémoire, mais aucun port Ethernet. Je l'ai relié au switch par un adaptateur USB-Ethernet, j'ai désactivé et mis hors tension son GPU NVIDIA, inutile ici, et j'ai installé Proxmox VE. Comme PVE1, il redémarre seul après une coupure de courant, et je l'ai redémarré à distance. Avec le pare-feu de Proxmox actif sur les deux hôtes, qui refuse par défaut tout ce qui entre sans autorisation, l'étape « administration sans accès physique » est terminée.

Restait à réunir les deux machines. Un cluster à deux nœuds cache un piège : les nœuds votent pour garder le quorum, le droit de prendre des décisions, et si l'un s'arrête, l'autre se retrouve seul avec la moitié des votes. Il perd alors le quorum et ne peut plus démarrer ses VM. J'ai donné deux votes à PVE1, qui porte le pare-feu, et un seul à PVE2 : si PVE2 s'arrête, PVE1 garde seul le quorum et peut relancer le pare-feu. Le test de quorum est réussi. Le cluster n'a ni haute disponibilité ni QDevice, un arbitre externe qui ajouterait un vote supplémentaire (voir [Virtualisation]({{< relref "/infrastructure/virtualization" >}})).

Les limites que j'accepte : si PVE1 s'arrête, PVE2 perd le quorum. Et le cluster n'a qu'un lien, qui passe par l'adaptateur USB de PVE2 : sa latence reste en moyenne sous le seuil demandé par Proxmox, mais avec peu de marge.

## Des zones sans VLAN

Le plan de la semaine 1 prévoyait des zones séparées par des VLAN, ces réseaux virtuels qui partagent les mêmes câbles mais restent étanches entre eux. Le matériel a dit non. Le switch, non manageable, ne peut pas faire respecter les VLAN, et surtout l'adaptateur USB-Ethernet de PVE2 n'émet pas les trames VLAN : je l'ai vérifié par des captures de trames, et son mode propre au fabricant ne monte même pas de lien.

J'ai écarté les autres options :

- Un réseau virtuel VXLAN, qui transporterait les zones dans un tunnel par-dessus le réseau existant, et que je garde comme évolution possible.
- Un réseau à plat.
- Des zones limitées à PVE1.
- Un autre adaptateur, exclu par le budget zéro.

J'ai choisi des zones routées. Chaque zone a son propre sous-réseau, sur le même réseau physique, et OPNsense route entre elles avec une passerelle par zone. Le pare-feu de Proxmox, activé sur chaque VM des zones, fait respecter les frontières : il filtre les adresses IP et MAC de la machine et lui applique les règles de sa zone. Le détail est sur la page [Réseau]({{< relref "/infrastructure/network" >}}). La limite que j'accepte : sans VLAN, les zones ne sont pas isolées au niveau 2, celui des trames Ethernet.

La première zone créée est une zone isolée, où j'expérimente, par curiosité, avec un agent IA autonome. Elle sort sur Internet, mais la maison et le reste du lab lui sont injoignables, et ses règles sont journalisées. J'y ai installé une VM Ubuntu Server 26.04 LTS sur PVE2, joignable uniquement en SSH par clé. L'expérience y tourne sous un compte sans droits d'administration. Depuis cette VM, j'ai vérifié que tout tient : Internet répond, ni le réseau domestique ni la zone d'infrastructure (administration d'OPNsense et des deux hôtes comprise) ne répondent, et une adresse usurpée est bloquée.

## La route que je croyais élargie

En semaine 1, j'avais élargi la route annoncée par le VPN à tout le réseau du lab, `10.42.0.0/16`. Du moins, je le croyais : elle était restée limitée à la zone d'infrastructure, `10.42.0.0/24`. Je l'ai corrigée le 28 octobre. Elle couvre maintenant tout le lab, et un erratum le signale dans l'[entrée de la semaine 1]({{< relref "/journal/001-rebuild" >}}).

## La suite

Prochaine étape de la [feuille de route]({{< relref "/roadmap" >}}) : mettre en place une stack de monitoring. Jusqu'ici, j'ai tout installé et configuré à la main : l'automatisation avec Ansible et Terraform viendra ensuite.

## En bref {.brief}

- **Composants** : PVE2 (Dell XPS 15 9570, 6 cœurs, 32 Go), Proxmox VE sur PVE2, cluster Proxmox à deux nœuds, pare-feu de Proxmox, OPNsense, Tailscale.
- **Étapes** :
  - Proxmox VE sur PVE2.
  - Pare-feu de Proxmox actif sur les deux hôtes, entrées refusées par défaut.
  - Redémarrage à distance.
  - Cluster à deux nœuds (PVE1 : deux votes, PVE2 : un), test de quorum réussi.
  - Zones routées sans VLAN, un /24 par zone.
  - Zone isolée `10.42.50.0/24` et sa VM Ubuntu Server 26.04 LTS, tests d'isolation réussis.
  - Route du VPN corrigée en `10.42.0.0/16`.
- **Décisions** : zones routées plutôt que VLAN, avec le pare-feu de Proxmox sur chaque VM des zones (voir [Réseau]({{< relref "/infrastructure/network" >}})). Deux votes pour PVE1, un pour PVE2 (voir [Virtualisation]({{< relref "/infrastructure/virtualization" >}})).
- **Limites acceptées** : pas d'isolation de niveau 2 entre les zones. Un seul lien de cluster, avec peu de marge de latence.
