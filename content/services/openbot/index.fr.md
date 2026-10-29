---
title: "OpenBot"
description: "Un serveur d'agents IA autonomes, que j'expérimente par curiosité dans une zone isolée du lab."
summary: "Un serveur d'agents IA autonomes, que j'expérimente par curiosité dans une zone isolée du lab."
draft: false
weight: 1
# Badge de la carte, hors feuille de route (architecture §5.4) : running | building | planned.
status: running
ShowReadingTime: false
ShowPostNavLinks: false
---

OpenBot fait tourner des agents IA autonomes : ils exécutent eux-mêmes des commandes sur la machine qui les héberge. J'y expérimente par curiosité, dans une zone du lab isolée du reste.

## Pourquoi une zone isolée

Le logiciel donne à ses agents un accès complet à la machine où il tourne. La protection doit donc venir de l'extérieur : OpenBot tourne dans une machine virtuelle à part, sous un compte sans droits d'administration, dans une zone qui sort sur Internet mais ne voit ni la maison ni le reste du lab (voir [Réseau]({{< relref "/infrastructure/network" >}})).

## Détails techniques

- **Machine** : une VM Ubuntu Server sur PVE2, dans la zone isolée `10.42.50.0/24`.
- **Accès** : administration uniquement en SSH par clé.
- **Isolation** : vérifiée depuis la VM. Internet répond, le réseau domestique et le reste du lab ne répondent pas.

## Limites et évolutions

OpenBot est encore en préversion. La façon de le mettre à jour reste à décider.
