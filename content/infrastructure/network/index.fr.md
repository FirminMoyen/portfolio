---
title: "Réseau"
description: "Le réseau du lab : isolé du réseau domestique derrière OPNsense, accessible à distance par Tailscale, sans port ouvert sur Internet."
draft: false
weight: 2
ShowReadingTime: false
ShowPostNavLinks: false
---

## Rôle dans le lab

Le réseau isole le lab du réseau domestique. OPNsense, en VM sur PVE1, est le pare-feu et le routeur du lab. Le switch sw-01 est dédié au lab. Tailscale fournit l'accès distant.

## Mise en œuvre

{{< diagram name="lab-network" alt="Schéma réseau du lab : la box domestique (1er NAT) et mes appareils (tunnel VPN) rejoignent OPNsense (fw-01, 2e NAT, passerelle 10.42.0.1), qui dessert la zone infrastructure 10.42.0.0/24 (fw-01 .1, PVE1 .2, PVE2 .3 prévu) et les zones à venir, une par usage, VLAN égal au 3e octet." >}}

Le lab sort sur Internet par la box domestique : il y a donc un double NAT, la box puis OPNsense. Aucun port n'est redirigé vers le lab.

Le lab utilise la plage `10.42.0.0/16`, découpée en une zone /24 par usage. Le numéro de VLAN reprend le troisième octet. La zone `10.42.0.0/24` est celle de l'infrastructure physique : OPNsense en `.1`, PVE1 en `.2`, PVE2 en `.3`.

Le domaine DNS interne est un sous-domaine de firminmoyen.dev, résolu uniquement dans le lab.

Pour l'accès distant, j'ai choisi Tailscale après l'avoir comparé à Headscale et à NetBird. Tailscale tourne sur OPNsense en subnet router et annonce la route `10.42.0.0/16`. Le VPN donne accès au réseau du lab uniquement, jamais au réseau domestique. Aucun port n'est ouvert sur Internet.

## Exploitation

Interfaces d'administration non exposées sur Internet, accessibles par le VPN. Celle d'OPNsense utilise des comptes locaux, sans 2FA.

Les sauvegardes et la supervision ne sont pas encore en place : je les ai reportées.

## Limites et évolutions

Sous FreeBSD, le plugin Tailscale fonctionne en espace utilisateur : le pare-feu d'OPNsense ne voit donc pas le trafic venu du VPN. Le cloisonnement repose pour l'instant sur la politique d'accès du VPN et sur l'annonce de la seule route du lab. Une piste est à l'étude : déplacer le subnet router dans une VM Linux, derrière le pare-feu.
