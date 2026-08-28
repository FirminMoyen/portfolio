# CLAUDE.md

Site de documentation d'infrastructure (homelab Proxmox/Ansible), généré avec Hugo.

## Commandes

- Serveur de dev : `hugo server -D` (inclut les brouillons, rechargement à chaud)
- Build de production : `hugo --minify`
- Sortie du build : `public/` (généré, ignoré par git, ne pas éditer à la main)

## Structure

- `hugo.toml` — configuration du site (langue, menu, titre)
- `content/` — pages et articles Markdown
  - `content/_index.md` — page d'accueil
  - `content/journal/` — notes datées (interventions, incidents, découvertes)
  - `content/projects/` — pages projets d'infrastructure
  - `content/about/` — page à propos
  - chaque section a un `_index.md` avec `title` et `description`
- `layouts/` — templates Go (`_default/baseof.html`, `list.html`, `single.html`, `index.html`)
- `assets/css/main.css` — feuille de style unique, traitée via Hugo Pipes

## Front matter des articles

```yaml
---
title: "Titre de l'article"
date: 2026-08-27
draft: false
---
```

- `title` : requis
- `date` : requis, format `AAAA-MM-JJ`
- `draft` : `true`/`false`, requis (les brouillons n'apparaissent pas en build classique)

## Règles

- Aucune dépendance npm, aucun framework CSS, aucun JavaScript côté client.
- Ne jamais modifier `hugo.toml` sans demande explicite.
- Ne jamais créer de contenu dans `content/` — les articles sont écrits par l'utilisateur.
- Un seul fichier CSS dans `assets/` (`assets/css/main.css`), pas de découpage en modules.
- Toujours vérifier que `hugo --minify` passe sans erreur avant de considérer une tâche terminée.
