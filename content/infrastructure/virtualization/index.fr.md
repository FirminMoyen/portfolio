---
title: "Virtualisation"
description: "Proxmox VE, l'hyperviseur du lab : en service sur Hermes, puis sur Atlas, avant un cluster à deux nœuds sans haute disponibilité."
draft: false
weight: 3
ShowReadingTime: false
ShowPostNavLinks: false
---

## Rôle dans le lab

Proxmox VE est l'hyperviseur du lab. Il est en service sur Hermes, où il fait tourner OPNsense en VM.

## Mise en œuvre

J'ai installé Proxmox VE directement sur Hermes, avec ZFS sur le seul disque de la machine et le dépôt no-subscription.

## Exploitation

Interfaces d'administration non exposées sur Internet, accessibles par le VPN. Celle de Proxmox VE utilise des comptes locaux, sans 2FA.

Les sauvegardes et la supervision ne sont pas encore en place : je les ai reportées.

L'étape en cours porte sur l'administration à distance sans accès physique : durcissement de l'hôte et test de redémarrage complet à distance.

## Limites et évolutions

Après Hermes, j'installerai Proxmox VE sur Atlas, puis je réunirai les deux nœuds dans un cluster Proxmox, sans haute disponibilité. Avec deux nœuds, si l'un s'arrête, l'autre perd le quorum.
