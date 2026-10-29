---
title: "Journal"
description: "La reconstruction du lab racontée semaine par semaine : ce que j'ai construit, ce qui a résisté, ce que j'ai choisi et pourquoi."
draft: false
menus:
  main:
    identifier: journal
    weight: 40
---

Chaque semaine, je raconte ici où en est le lab : ce que j'ai construit, ce qui a résisté, ce que j'ai choisi et pourquoi. Chaque entrée se termine par un encadré « En bref » qui résume les composants, les étapes et les décisions.

## L'histoire jusqu'ici

De 2022 à 2026, j'ai fait tourner un premier homelab. En octobre 2026, je l'ai entièrement effacé : c'était une bonne occasion de tout documenter depuis le début et de repartir sur de bonnes bases.

La semaine 1 pose les fondations sur une seule machine : un hyperviseur, un pare-feu qui isole le lab de la maison, et un accès à distance sans rien exposer sur Internet. La semaine 2 ajoute une seconde machine, réunit les deux en cluster, et découpe le réseau en zones, sans les VLAN que le matériel refusait. Prochain chapitre : une stack de monitoring, avant d'automatiser le lab avec Ansible et Terraform.
