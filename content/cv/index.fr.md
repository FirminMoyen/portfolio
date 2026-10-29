---
title: "CV"
description: "CV de Firmin Moyen, administrateur systèmes : expériences, compétences, formation et certification."
ShowReadingTime: false
ShowPostNavLinks: false
headline: "Administrateur systèmes · Infrastructure Windows et Linux, automatisation, DevOps"
sidebar:
  - title: "Contact"
    items:
      - kind: email
      - kind: linkedin
      - kind: website
      - text: "Belgique"
      - text: "Permis B"
      - text: "Disponible immédiatement"
        strong: true
  - title: "Compétences"
    items:
      - label: "Systèmes"
        text: "Windows Server, Active Directory, GPO, Linux, Proxmox VE, VMware ESXi, Docker"
      - label: "Automatisation et CI/CD"
        text: "Terraform, Ansible, GitHub Actions, GitLab CI/CD, Jenkins, Git"
      - label: "Monitoring et ticketing"
        text: "Prometheus, Grafana, osTicket"
      - label: "Réseau et services"
        text: "DNS (Bind9), Apache, Nginx, Tailscale, formation niveau Cisco CCNA"
      - label: "Scripting"
        text: "Bash, Python, JavaScript"
      - label: "Méthodes"
        text: "Agile, Scrum"
  - title: "Formation"
    items:
      - label: "Bachelier en technologie de l'informatique"
        text: "EPHEC, Louvain-la-Neuve · 2019 – 2024"
      - label: "Sciences physiques"
        text: "UCLouvain · 2018 – 2019"
  - title: "Certification"
    items:
      - label: "LPIC-1 (Linux)"
        text: "En préparation, objectif fin 2026"
  - title: "Langues"
    items:
      - text: "Français : langue maternelle"
      - text: "Anglais : courant (C1)"
---

## Profil

Administrateur systèmes junior, bachelier en technologie de l'informatique (EPHEC). Expérience en administration Windows Server et Active Directory sur un parc multisite, en automatisation d'infrastructure (Terraform, Ansible, CI/CD) et en monitoring (Prometheus, Grafana). De 2022 à 2026, j'ai maintenu un cluster Proxmox en haute disponibilité. Je reconstruis aujourd'hui mon homelab de zéro et je le documente chaque semaine. Recherche un poste d'administrateur systèmes en Belgique ou au Luxembourg.

## Expériences professionnelles

### Expérience internationale au Canada (PVT)

*Montréal, Canada · 09/2025 – 09/2026*

- Conseiller de vente Home Cinéma chez Best Buy puis agent au comptoir chez Desjardins. Service client en environnement bilingue français et anglais.

### Administrateur systèmes, équipe support

*Administration communale de Virton · 11/2024 – 08/2025*

- Administration de 2 domaines Active Directory : comptes, groupes, stratégies de groupe (GPO), serveurs Windows Server.
- Maintenance et support d'un parc de plus de 200 postes répartis sur 4 sites, et d'une dizaine de serveurs.
- Conception et déploiement d'une solution de monitoring (Prometheus, Grafana) et de ticketing (osTicket) en Infrastructure as Code (Terraform, Ansible, GitHub Actions), pour un meilleur suivi et une résolution plus rapide des incidents.

### Stagiaire, équipe projet

*BCE · Broadcasting Center Europe, Luxembourg-Kirchberg · 11/2023 – 06/2024*

- Développement en Python d'un plugin pour l'IPAM interne et conteneurisation de l'application avec Docker.
- Conception et mise en place du workflow Git et des pipelines CI/CD de l'équipe.

### Stagiaire, équipe IT Expertise in Health Data

*Luxembourg Institute of Health · 02/2023 – 06/2023*

- Développement d'un tableau de bord de monitoring de la base de données du Registre national du cancer (R, technologies web).

## Projet personnel : homelab

### Reconstruction documentée

*Depuis 10/2026 · {{< site-link >}}*

- Reconstruction de zéro, documentée chaque semaine en français et en anglais : journal, décisions d'architecture.
- Deux nœuds Proxmox VE en cluster, pare-feu OPNsense qui isole le lab du réseau domestique et le découpe en zones.
- Accès distant par Tailscale (VPN WireGuard), aucun service exposé publiquement.
- En cours : monitoring avec Prometheus, Grafana et Uptime Kuma, puis automatisation avec Ansible et Terraform.

### Premier homelab

*2022 – 2026*

- Cluster Proxmox VE en haute disponibilité, monitoring avec Prometheus et Grafana, services auto-hébergés.
- Entièrement effacé en octobre 2026 pour tout documenter depuis le début et repartir sur de bonnes bases.
