---
title: "Matériel"
description: "Les machines du lab : PVE1, en service, et PVE2, prévu."
summary: "Les machines du lab : PVE1, en service, et PVE2, prévu."
draft: false
weight: 1
ShowReadingTime: false
ShowPostNavLinks: false
---

## Rôle dans le lab

Le lab repose sur deux ordinateurs portables Dell. PVE1 porte l'infrastructure du lab : pare-feu, routeur et accès distant. PVE2 portera les VM et les conteneurs des services.

## Mise en œuvre

{{< diagram name="lab-physical" alt="Schéma physique du lab : Internet arrive par la box domestique (1er NAT) sur la VM OPNsense de PVE1 (Dell Latitude 7490, 2e NAT) ; PVE1 est relié par câble au switch sw-01 (5 ports), qui reliera PVE2 (Dell XPS 15, prévu)." >}}

PVE1 est en service : Proxmox VE y est installé directement sur le matériel (voir la page Virtualisation). PVE2 n'est pas encore installé.

## Exploitation

Les sauvegardes et la supervision ne sont pas encore en place : je les ai reportées.

## Limites et évolutions

Tant que PVE2 n'est pas installé, PVE1 est le seul nœud du lab. L'installation de Proxmox VE sur PVE2 est la prochaine étape après celle en cours, avant la mise en cluster des deux nœuds.
