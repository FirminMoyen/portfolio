---
paths:
  - "layouts/**"
  - "assets/**"
  - "i18n/**"
  - "hugo.toml"
---

# Templates, styles et configuration

Détail : `docs/architecture.md` §11, §12.

## Configuration (§11.1)
- `hugo.toml` ne change que dans le cadre d'un plan validé.
- Aucun menu dans `hugo.toml` : les entrées sont dans le front matter des pages (§4).
- Garder `unsafe = false` ; le shortcode `rawhtml` de PaperMod est interdit.

## Templates (§11.2)
- Nouveau système de templates (Hugo ≥ 0.146) : vérifier la résolution dans la documentation de la version épinglée avant de créer un fichier.
- Définir le bloc `main` ; réutiliser les partials de PaperMod (`breadcrumbs`, `post_meta`, `post_nav_links`…).
- Un partial par calcul (liens inverses, compteurs, lien vers un composant), jamais dupliqué.
- Ne jamais modifier `themes/PaperMod/`. Toute surcharge d'un fichier du thème s'inscrit au registre §11.7, dans la même PR.

## Shortcodes (§11.3)
- `component` ne crée un lien que si la page cible est publiée ; sinon nom et badge sans lien.

## Chaînes d'interface (§11.4)
- Tout texte d'interface dans `i18n/fr.yaml` et `i18n/en.yaml`. Aucun texte en dur dans un template.

## CSS (§11.5)
- Un seul fichier : `assets/css/extended/site.css`. Aucun framework.
- Utiliser les variables du thème (`--primary`, `--secondary`, `--tertiary`, `--entry`, `--border`, `--code-bg`) pour le clair et le sombre.
- Un badge de statut porte toujours son texte, jamais la seule couleur.
- Aucun JavaScript écrit pour le site (P8).

## Schémas (§11.6)
- Source D2 dans `assets/diagrams/<nom>.d2`, rendus `<nom>.light.svg` et `<nom>.dark.svg` commités. Vue logique uniquement.

## Validation au build (§12)
- Contrôles dans `layouts/_partials/validate/`, appelés depuis `extend_head.html` (données via `partialCached`).
- `errorf` pour une erreur, `warnf` pour un avertissement. Messages en français, préfixés par le chemin du fichier, avec les valeurs attendues.
- Comparer des listes entre langues par `jsonify`.
- Chaque règle V1 à V16 a son cas de test dans `tests/validation/`.
