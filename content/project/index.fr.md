---
title: "Le projet"
description: "Pourquoi je reconstruis ce homelab de zéro, où il en est, où il va, et le cadre que je me suis fixé."
draft: false
ShowReadingTime: false
ShowPostNavLinks: false
aliases: ["/misc/", "/misc/project-goals-constraints/"]
menus:
  main:
    identifier: project
    weight: 15
---

Ce homelab est mon terrain d'entraînement d'administrateur systèmes : deux ordinateurs portables et un petit switch, organisés comme une infrastructure d'entreprise. Je le reconstruis de zéro depuis octobre 2026, et je raconte chaque semaine ce que j'y fais, ce qui résiste et ce que je décide.

## Pourquoi un homelab

Je construis ce homelab pour apprendre en pratiquant. Lire une documentation ne suffit pas : il faut installer, casser, réparer, et comprendre pourquoi. Le lab me sert aussi à préparer mes certifications, à commencer par la LPIC-1, que je vise pour fin 2026.

C'est enfin une vitrine : tout ce que j'y fais est documenté ici, pour montrer concrètement ce que je sais faire et comment je travaille.

## Pourquoi repartir de zéro

De 2022 à 2026, j'ai fait tourner un premier homelab : un cluster Proxmox en haute disponibilité, avec du monitoring par Prometheus et Grafana, avec des services auto-hébergés. En octobre 2026, je l'ai entièrement effacé. C'était une bonne occasion de tout documenter depuis le début et de repartir sur de bonnes bases.

## Où en est le lab

Aujourd'hui, deux nœuds Proxmox VE, PVE1 et PVE2, forment un cluster. Un pare-feu OPNsense sépare le lab du réseau de la maison et le découpe en zones, chacune avec ses propres règles. J'administre le tout à distance par un VPN, sans rien exposer sur Internet. L'une des zones est isolée du reste : j'y expérimente, par curiosité, avec un agent IA autonome.

Le détail est sur la page [Infrastructure]({{< relref "/infrastructure" >}}), et le chemin parcouru dans le [journal]({{< relref "/journal" >}}).

## La suite

En cours : le monitoring du lab, avec Prometheus, Grafana et Uptime Kuma. Jusqu'ici, j'ai tout installé et configuré à la main : l'étape suivante sera d'automatiser le lab avec Ansible et Terraform. Plus loin, dans un ordre qui n'est pas encore fixé : Kubernetes, une approche GitOps complète, et un environnement mixte Windows et Linux qui reprend des pratiques d'entreprise. La [feuille de route]({{< relref "/roadmap" >}}) montre où j'en suis.

## Le cadre que je me suis fixé

Le lab applique les pratiques du métier, la sécurité en tête : il est construit comme une infrastructure d'entreprise, pas comme un bac à sable. J'avance pas à pas : chaque technologie est apprise, mise en place et documentée avant de passer à la suivante.

Je travaille avec le matériel que j'avais déjà, sans budget : deux ordinateurs portables Dell et un petit switch. C'est une contrainte, mais aussi un bon exercice : tirer le meilleur de ressources limitées. Rien n'est exposé sur Internet. Mon temps est limité, et je préfère une progression régulière à une progression rapide.

Tout est documenté publiquement, en français et en anglais : un journal chaque semaine, et chaque choix important écrit avec les options écartées, dans une décision d'architecture ou dans le journal. Avant d'arriver ici, chaque information du lab passe une relecture, pour qu'aucun détail sensible ne sorte.
