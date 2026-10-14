---
paths:
  - ".github/**"
  - "scripts/**"
  - "tools.env"
  - ".githooks/**"
  - "tests/**"
---

# CI/CD et outillage

Détail : `docs/architecture.md` §13.

## Versions (§13.1)
- Une seule source de versions : `tools.env`. Les outils s'installent dans `.bin/` par `scripts/install-tools.sh`.
- Tout binaire téléchargé est vérifié contre sa somme SHA-256 publiée.
- En local comme en CI, les scripts utilisent `.bin/`.

## Workflows (§13.2, §13.3)
- Actions épinglées par SHA, version en commentaire.
- `permissions` minimales : `contents: read` par défaut ; `pages: write` et `id-token: write` pour le seul job de déploiement.
- `concurrency` annule les exécutions obsolètes d'une même PR.
- Build : clone avec submodules et `fetch-depth: 0` ; `hugo --minify --gc --printPathWarnings` ; vérifier `public/404.html`.
- Vérification des liens hors ligne : `baseURL` locale ou remappage lychee, sinon les liens internes ne sont pas vérifiés.
- Chaque job arrive avec l'étape du §15 qui en a besoin ; ne pas anticiper.

## En local (§13.4)
- Le hook pre-commit est un confort ; la barrière reste la CI. `--no-verify` (ou `-n`) interdit.

## Réglages GitHub (§13.5)
- Réservés à Firmin : ne jamais les modifier (`gh repo edit`, `gh secret`, `gh api`).
