---
title: "Virtualisation"
description: "Proxmox VE, l'hyperviseur du lab : PVE1 et PVE2 réunis dans un cluster à deux nœuds, administrés entièrement à distance."
summary: "Proxmox VE, l'hyperviseur du lab : PVE1 et PVE2 réunis dans un cluster à deux nœuds, administrés entièrement à distance."
draft: false
weight: 3
ShowReadingTime: false
ShowPostNavLinks: false
---

La virtualisation permet de faire tourner plusieurs machines virtuelles (VM) sur une seule machine physique. Dans le lab, c'est le rôle de Proxmox VE, un hyperviseur installé directement sur PVE1 et PVE2. Les deux machines sont réunies en cluster : je les administre comme un seul ensemble, depuis une seule interface.

## Un cluster à deux nœuds

Dans un cluster, les nœuds votent pour vérifier qu'ils sont assez nombreux à se voir pour prendre des décisions : c'est le quorum. Un nœud qui perd le quorum ne peut plus démarrer ni modifier ses VM. Avec deux nœuds, il y a un piège : si l'un s'arrête, l'autre se retrouve seul avec la moitié des votes, et perd le quorum.

J'ai donc donné deux votes à PVE1, qui porte le pare-feu, et un seul à PVE2. Si PVE2 s'arrête, PVE1 garde seul le quorum et peut relancer le pare-feu. Si PVE1 s'arrête, PVE2 perd le quorum. Le test de quorum est réussi.

Le cluster n'a ni haute disponibilité (HA, qui relancerait automatiquement sur l'autre nœud les VM d'un nœud en panne), ni QDevice (un petit arbitre externe qui ajouterait un vote supplémentaire).

## Administré sans accès physique

Je n'ai pas besoin d'être devant les machines pour les administrer : je les ai redémarrées à distance, sans intervention physique. Le pare-feu de Proxmox est actif sur les deux hôtes : tout ce qui n'est pas explicitement autorisé à entrer est refusé.

## Détails techniques

- **PVE1** : Proxmox VE 9.2 (noyau 7.0), installé directement sur le matériel. ZFS (un système de fichiers qui vérifie l'intégrité des données) sur le seul disque de la machine, avec son cache en mémoire, l'ARC, plafonné à 1 Go. Dépôt no-subscription (les mises à jour de Proxmox sans abonnement).
- **PVE2** : Proxmox VE, installé directement sur le matériel.
- **Cluster** : deux nœuds, sans HA ni QDevice. PVE1 a deux votes, PVE2 un seul. Test de quorum réussi.
- **Pare-feu de Proxmox** : actif sur les deux hôtes, avec une politique entrante qui refuse par défaut. Activé aussi sur chaque VM (voir [Réseau]({{< relref "/infrastructure/network" >}})). Le détail des règles n'est pas publié.
- **Accès** : interfaces d'administration non exposées sur Internet, joignables par le VPN.

## Limites et évolutions

- Le cluster n'a qu'un lien, sur le réseau du lab, et il passe par l'adaptateur USB-Ethernet de PVE2 : sa latence reste en moyenne sous le seuil demandé par Proxmox, avec peu de marge.
- PVE1 reste un point unique de défaillance : il porte le pare-feu et la majorité des votes ([ADR-0002]({{< relref "/infrastructure/decisions/adr-0002-lab-isolated-opnsense" >}})).
- Amélioration envisagée : la double authentification sur l'interface d'administration de Proxmox VE.
