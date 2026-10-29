---
title: "Accès distant au lab par Tailscale"
date: 2026-10-25
draft: false
description: "Pourquoi j'accède au lab à distance par Tailscale plutôt que par Headscale ou NetBird, sans aucun port ouvert sur Internet."
adr: 1
status: accepted
components: [tailscale, fw-01]
supersedes:
superseded_by:
tags: []
---

## Contexte

Je dois pouvoir administrer le lab à distance, y compris depuis mon téléphone. Contraintes :

- **Rien d'exposé publiquement** : aucun port ouvert sur Internet vers le lab.
- **Budget zéro** : uniquement le matériel que je possède déjà, aucun abonnement payant, pas de serveur loué (VPS).
- **Sécurité de niveau entreprise** : authentification forte, contrôle d'accès explicite (moindre privilège), segmentation entre le lab et le réseau domestique.
- **Un seul utilisateur** pour l'instant : moi.

La décision a été prise mi-octobre 2026, au démarrage de la reconstruction du lab (ordre d'installation : Proxmox, réseau OPNsense, puis Tailscale). Cette ADR est rédigée a posteriori, le 25 octobre 2026.

## Options considérées

Les trois options sont des réseaux superposés (overlay) fondés sur WireGuard, avec un plan de contrôle qui distribue les clés et la politique d'accès, et des clients qui établissent des tunnels directs entre eux quand c'est possible (par relais sinon). Aucune n'impose d'ouvrir un port entrant vers le lab.

### Option 1 — Tailscale (plan de contrôle hébergé par Tailscale)

- **Avantages**
  - Installation simple : pas de serveur de coordination à installer ni à maintenir. Plugin disponible pour OPNsense.
  - Contrôle d'accès complet dans la politique d'accès du VPN.
  - Applications mobiles officielles (iOS, Android).
  - Plan gratuit « Personal » pour un usage personnel non commercial, suffisant pour un seul utilisateur ([tarifs](https://tailscale.com/pricing/), [FAQ](https://tailscale.com/kb/1251/pricing-faq)).
- **Inconvénients**
  - Le plan de contrôle est un service SaaS : l'identité, la distribution des clés et la politique d'accès dépendent d'un tiers.
  - Le plan gratuit a des limites (nombre d'utilisateurs, fonctionnalités) qui pourraient compter si le lab s'ouvre à d'autres personnes.

### Option 2 — Headscale (plan de contrôle Tailscale auto-hébergé)

- **Avantages**
  - Logiciel libre, réimplémentation du serveur de coordination de Tailscale. Il utilise les clients officiels Tailscale ([documentation](https://github.com/juanfont/headscale/blob/main/docs/about/features.md)).
  - Aucune dépendance à un SaaS pour le plan de contrôle.
- **Inconvénients**
  - Un serveur de plus à installer, sécuriser, sauvegarder et mettre à jour.
  - Pour joindre le lab depuis la 4G, le serveur de coordination doit être joignable depuis Internet : soit on l'expose depuis la maison (contraire à « rien d'exposé »), soit on le place sur un serveur loué (contraire au budget zéro).
  - Fonctionnalités en retrait par rapport au service officiel : le projet vise l'usage personnel et ne couvre pas tout le périmètre de Tailscale.

### Option 3 — NetBird (hébergé ou auto-hébergé)

- **Avantages**
  - Logiciel libre (licence BSD-3), auto-hébergeable, avec une offre hébergée. Politiques d'accès par groupes et règles, contrôles de posture des appareils. Clients iOS et Android ([dépôt](https://github.com/netbirdio/netbird), [documentation](https://docs.netbird.io)).
- **Inconvénients**
  - En auto-hébergé : même problème que Headscale. La documentation d'installation demande une VM joignable publiquement (nom de domaine, TCP 80/443, UDP 3478).
  - En version hébergée : même dépendance à un SaaS que Tailscale.
- **Pourquoi je l'ai placé derrière Tailscale** :
  1. En auto-hébergé, NetBird demande un serveur joignable depuis Internet (ports ouverts ou VPS), ce qui est contraire à « rien d'exposé » et au budget zéro.
  2. Pas de plugin OPNsense, alors que Tailscale s'installe directement sur OPNsense par un plugin.
  3. Maturité et communauté : Tailscale est plus répandu, mieux documenté, avec plus de retours d'expérience.
- **Note factuelle (vérifiée le 25 octobre 2026)** : un plugin `os-netbird` existe aujourd'hui dans le dépôt officiel d'OPNsense, inclus à partir d'OPNsense 25.7.3 selon la documentation NetBird ([guide OPNsense](https://docs.opnsense.org/manual/how-tos/netbird.html), [guide NetBird](https://docs.netbird.io/get-started/install/opnsense)). Il crée une interface `wt0` qui peut être assignée et filtrée par les règles du pare-feu OPNsense. Les politiques NetBird ne créent pas ces règles automatiquement. La raison 2 est conservée telle que je l'ai donnée. Elle serait à revoir si l'accès distant est réexaminé.

## Décision

**Tailscale**, avec le plan de contrôle hébergé par Tailscale.

Les critères qui ont fait pencher la balance :

1. La facilité d'installation.
2. Les fonctionnalités de contrôle d'accès.
3. Les applications mobiles.

### Mise en œuvre retenue

- **Subnet router sur OPNsense** (plugin Tailscale), qui annonce uniquement le réseau du lab, `10.42.0.0/16`. Le réseau domestique n'est pas annoncé.
- **Politique d'accès** restreinte. Son contenu n'est pas publié.
- **Validation** : tests depuis la 4G réussis. Le lab est joignable, le réseau domestique ne l'est pas.

## Conséquences

**Positives**

- Aucun port entrant ouvert sur Internet : la surface exposée n'augmente pas.
- Accès depuis le téléphone et l'ordinateur sans infrastructure supplémentaire.
- Le VPN donne accès au lab et seulement au lab : seule la route `10.42.0.0/16` est annoncée.

**Négatives et risques**

- **Dépendance à un service tiers** : le plan de contrôle est hébergé par Tailscale. Une panne ou un changement des conditions du service peut affecter l'accès distant. Headscale reste une porte de sortie possible, puisqu'il reprend les mêmes clients.
- **Le pare-feu ne filtre pas le trafic du VPN.** Sous FreeBSD, le plugin Tailscale fonctionne en espace utilisateur : le pare-feu d'OPNsense ne voit donc pas le trafic venu du VPN. Le cloisonnement repose pour l'instant sur la politique d'accès du VPN et sur l'annonce de la seule route du lab. Une piste est à l'étude : déplacer le subnet router dans une VM Linux, derrière le pare-feu.

**À réexaminer**

- La piste ci-dessus : la question reste ouverte, cette ADR ne la tranche pas.
- La politique d'accès du VPN : à revoir à chaque nouvelle zone ou nouvel appareil.
