---
title: "À propos de moi"
description: "Firmin Moyen, administrateur systèmes junior : parcours, homelab, façon de travailler et contact."
ShowReadingTime: false
ShowPostNavLinks: false
aliases: ["/about/"]
menus:
  main:
    identifier: about
    weight: 50
headline: "Administrateur systèmes · Infrastructure Windows et Linux, automatisation, DevOps"
availability: "Belgique · Recherche un poste en Belgique ou au Luxembourg · Français : langue maternelle, anglais : courant (C1) · Disponible immédiatement"
---

Je suis administrateur systèmes junior. J'ai administré deux domaines Active Directory, assuré le support d'un parc de plus de 200 postes répartis sur quatre sites, et déployé du monitoring en Infrastructure as Code.

Aujourd'hui, je reconstruis mon homelab de zéro, en le documentant sur ce site.

## Mon parcours

J'ai fait mon bachelier en technologie de l'informatique à l'EPHEC, à Louvain-la-Neuve. Mes deux stages, au Luxembourg, étaient côté développement : au Luxembourg Institute of Health, puis chez BCE (Broadcasting Center Europe), où j'ai aussi travaillé avec des conteneurs et des pipelines CI/CD.

Puis sur le terrain, à l'administration communale de Virton, comme administrateur systèmes dans l'équipe support. J'ai ensuite passé un an au Canada, avec un permis vacances-travail (PVT), à travailler au service de la clientèle, en français et en anglais.

Le détail de chaque poste est dans mon [CV]({{< relref "/cv" >}}).

## Mon homelab

C'est là que j'apprends en pratiquant. J'ai fait tourner un premier lab de 2022 à 2026. En octobre 2026, je l'ai entièrement effacé pour en construire un nouveau : c'était une bonne occasion de tout documenter depuis le début et de repartir sur de bonnes bases.

Ce nouveau lab, je le construis avec le matériel que j'ai déjà. Il tourne sur deux nœuds Proxmox VE réunis en cluster, derrière un pare-feu OPNsense qui l'isole du réseau domestique et le découpe en zones. Je l'administre à distance par un VPN, sans rien exposer sur Internet.

Il me sert aussi à préparer la LPIC-1, que je vise pour fin 2026. [Le projet]({{< relref "/project" >}}) en dit plus sur ses objectifs et son cadre, et le [journal]({{< relref "/journal" >}}) raconte sa construction, semaine par semaine.

## Ma façon de travailler

- Documenter au fur et à mesure.
- Justifier mes choix importants et ce qu'ils impliquent, dans des [décisions d'architecture]({{< relref "/infrastructure/decisions" >}}) ou dans le journal.
- Vérifier par des tests plutôt que de supposer.
- Ne pas avoir peur de se tromper : c'est le but de ce lab.
- Adapter au mieux le projet aux limites du matériel.
