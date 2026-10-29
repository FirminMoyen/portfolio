---
title: "Monitoring"
description: "Prometheus, Grafana and Uptime Kuma, to keep track of the lab's state: the roadmap step in progress."
summary: "Prometheus, Grafana and Uptime Kuma, to keep track of the lab's state: the roadmap step in progress."
draft: false
weight: 4
# Badge de la carte : étapes de data/roadmap.yaml (architecture §5.2).
roadmap: [monitoring]
ShowReadingTime: false
ShowPostNavLinks: false
---

Monitoring is the step in progress on the [roadmap]({{< relref "/roadmap" >}}), before automation.

## What is planned

- **Prometheus**: collecting metrics from the machines and the services.
- **Grafana**: dashboards, to read those metrics.
- **Uptime Kuma**: service availability, checked continuously.

I have already used Prometheus and Grafana in my first homelab.

## Where I am

The tools are chosen. I still have to decide where to install them in the lab, then set them up. The [journal]({{< relref "/journal" >}}) will tell how the installation goes.
