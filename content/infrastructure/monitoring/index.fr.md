---
title: "Monitoring"
description: "Prometheus, Grafana et Uptime Kuma, pour suivre l'état du lab : l'étape en cours de la feuille de route."
summary: "Prometheus, Grafana et Uptime Kuma, pour suivre l'état du lab : l'étape en cours de la feuille de route."
draft: false
weight: 4
# Badge de la carte : étapes de data/roadmap.yaml (architecture §5.2).
roadmap: [monitoring]
ShowReadingTime: false
ShowPostNavLinks: false
---

Le monitoring est l'étape en cours de la [feuille de route]({{< relref "/roadmap" >}}), avant l'automatisation.

## Ce qui est prévu

- **Prometheus** : la collecte des métriques des machines et des services.
- **Grafana** : les tableaux de bord, pour lire ces métriques.
- **Uptime Kuma** : la disponibilité des services, vérifiée en continu.

J'ai déjà utilisé Prometheus et Grafana dans mon premier homelab.

## Où j'en suis

Les outils sont choisis. Il me reste à décider où les installer dans le lab, puis à les mettre en place. Le [journal]({{< relref "/journal" >}}) racontera l'installation.
