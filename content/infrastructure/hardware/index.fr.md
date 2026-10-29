---
title: "Matériel"
description: "Les deux machines du lab, PVE1 et PVE2 : deux ordinateurs portables Dell reliés par un petit switch, administrés entièrement à distance."
summary: "Les deux machines du lab, PVE1 et PVE2 : deux ordinateurs portables Dell reliés par un petit switch, administrés entièrement à distance."
draft: false
weight: 1
ShowReadingTime: false
ShowPostNavLinks: false
---

Tout le lab tient sur deux ordinateurs portables Dell que j'avais déjà, reliés par un petit switch. Aucun serveur acheté pour l'occasion : c'est la contrainte du budget zéro, et un bon exercice pour tirer le meilleur de ressources limitées. Les deux machines tournent sans que j'aie besoin d'y toucher : je les administre entièrement à distance.

{{< diagram name="lab-physical" alt="Schéma physique du lab : Internet arrive par la box domestique (1er NAT) sur la VM OPNsense de PVE1 (Dell Latitude 7490, 2e NAT). PVE1 est relié par câble au switch sw-01 (5 ports), qui relie aussi PVE2 (Dell XPS 15, par un adaptateur USB-Ethernet)." >}}

## Deux portables, deux rôles

PVE1, un Dell Latitude 7490, porte l'infrastructure du lab : le pare-feu, le routeur et l'accès à distance. PVE2, un Dell XPS 15 9570, est destiné aux machines virtuelles et aux conteneurs des services. Sur les deux, Proxmox VE est installé directement sur le matériel (voir [Virtualisation]({{< relref "/infrastructure/virtualization" >}})).

## Détails techniques

- **PVE1** : Dell Latitude 7490, 4 cœurs, 16 Go de mémoire.
- **PVE2** : Dell XPS 15 9570, 6 cœurs, 32 Go de mémoire. Il n'a pas de port Ethernet intégré : il est relié au switch par un adaptateur USB-Ethernet. Son GPU NVIDIA, inutile pour l'instant, est désactivé et mis hors tension.
- **sw-01** : switch non manageable (il ne se configure pas) à 5 ports, dédié au lab.
- **Sans accès physique** : les deux machines redémarrent seules après une coupure de courant, et je les ai redémarrées à distance.

## Limites et évolutions

L'adaptateur USB-Ethernet de PVE2 a deux conséquences : il n'émet pas les trames VLAN, ce qui m'a conduit à organiser le réseau autrement (voir [Réseau]({{< relref "/infrastructure/network" >}})), et c'est par lui que passe le lien du cluster (voir [Virtualisation]({{< relref "/infrastructure/virtualization" >}})).
