---
title: "Objectifs et contraintes du projet"
date: 2026-10-25
draft: false
description: "Pourquoi je construis ce homelab, où je veux aller, et le cadre que je me suis fixé."
tags: []
---

## Pourquoi ce homelab

Je construis ce homelab pour apprendre en pratiquant. Lire une documentation ne suffit pas : il faut installer, casser, réparer, et comprendre pourquoi. Le lab me sert aussi à préparer mes certifications, à commencer par la LPIC-1, que je vise pour fin 2026.

C'est enfin une vitrine. Tout ce que j'y fais est documenté ici, pour montrer concrètement ce que je sais faire et comment je travaille.

## Mes objectifs

- **Appliquer les pratiques du métier**, la sécurité en tête. Le lab est construit comme une infrastructure d'entreprise, pas comme un bac à sable.
- **Avancer pas à pas.** Chaque technologie est apprise, mise en place et documentée avant de passer à la suivante.
- **Tout documenter publiquement**, en français et en anglais : un journal chaque semaine, et une décision d'architecture écrite pour chaque choix important.

## Où je veux aller

Aujourd'hui, le lab tourne sur un premier nœud Proxmox VE, derrière un pare-feu OPNsense, avec un accès distant par VPN. La suite :

- un cluster Proxmox à deux nœuds ;
- Kubernetes ;
- une approche GitOps complète ;
- un environnement mixte Windows et Linux, qui reprend des pratiques d'entreprise.

L'ordre des étapes après le cluster n'est pas encore fixé. La [feuille de route]({{< relref "/infrastructure" >}}#lab-roadmap) montre où j'en suis.

## Le cadre que je me suis fixé

- **Du matériel que j'avais déjà** : deux ordinateurs portables Dell et un petit switch. C'est une contrainte, mais aussi un bon exercice : tirer le meilleur de ressources limitées.
- **Rien n'est exposé sur Internet.** J'accède au lab à distance par VPN, sans aucun port ouvert.
- **Un temps limité.** Je préfère une progression régulière à une progression rapide.
- **Ce qui est publié est relu.** Avant d'arriver ici, chaque information du lab passe une relecture, pour qu'aucun détail sensible ne sorte.
