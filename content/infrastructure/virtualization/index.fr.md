---
title: "Virtualisation"
description: "Proxmox VE, l'hyperviseur du lab : en service sur PVE1, puis sur PVE2, avant un cluster à deux nœuds sans haute disponibilité."
summary: "Proxmox VE, l'hyperviseur du lab : en service sur PVE1, puis sur PVE2, avant un cluster à deux nœuds sans haute disponibilité."
draft: false
weight: 3
ShowReadingTime: false
ShowPostNavLinks: false
---

## Rôle dans le lab

Proxmox VE est l'hyperviseur du lab. Il est en service sur PVE1, où il fait tourner OPNsense en VM.

## Mise en œuvre

J'ai installé Proxmox VE directement sur PVE1, avec ZFS sur le seul disque de la machine et le dépôt no-subscription.

## Exploitation

Interfaces d'administration non exposées sur Internet, accessibles par le VPN. Celle de Proxmox VE utilise des comptes locaux, sans 2FA.

L'étape en cours porte sur l'administration à distance sans accès physique : durcissement de l'hôte et test de redémarrage complet à distance.

## Limites et évolutions

Après PVE1, j'installerai Proxmox VE sur PVE2, puis je réunirai les deux nœuds dans un cluster Proxmox, sans haute disponibilité. Avec deux nœuds, si l'un s'arrête, l'autre perd le quorum.
