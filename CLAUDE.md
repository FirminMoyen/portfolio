# CLAUDE.md

Site portfolio du homelab de Firmin : Hugo + PaperMod, GitHub Pages, https://firminmoyen.dev.
Référence : `docs/architecture.md` ; structure page par page : `docs/structure.md`.
Lire la section concernée avant toute modification
de structure, de template, de données, de CI ou d'outillage.

## Manière de travailler
- Firmin valide tout : présenter un plan (fichiers, objectif de chaque changement) et attendre
  son accord avant de créer ou de modifier un fichier.
- Une étape à la fois (architecture §15) : une session de travail = une branche ; un commit à chaque changement ; PR en fin de session, sur demande
- Si une demande contredit docs/architecture.md : s'arrêter, le signaler, proposer la
  modification du document.
- Les décisions ouvertes (architecture §17.1) appartiennent à Firmin.

## Commandes
- Développement : `hugo server` (`-D` pour voir les brouillons)
- Build et validations : `hugo --minify`
- Sortie du build : `public/` (généré, ignoré par git, ne pas éditer à la main)
- Nouveau contenu : `hugo new content --kind <journal|postmortem|adr|services> <chemin>`
  (ex. `journal/007-<slug>` ; crée FR et EN en brouillon)

## Invariants
- Aucune invention : aucun fait absent des notes de Firmin ou du repo du lab. Information
  manquante : demander, ou écrire `TODO(firmin): …` (bloque la publication).
- Les faits d'un composant vivent dans `data/catalog/<id>.yaml`, jamais dans la prose.
- Historique immuable : journal, ADR et post-mortems ne se réécrivent pas
  (erratum, nouvelle ADR, état des actions).
- Bilingue : toute page existe en FR et en EN ; une modification se reporte dans l'autre
  langue, dans la même PR.
- Publication (architecture §10) : aucun secret, aucune IP publique, aucun détail d'accès
  distant, aucune image géolocalisée. Ouvrir et inspecter chaque image ajoutée.
- Ne jamais modifier `themes/PaperMod/`. Toute surcharge s'inscrit au registre (§11.7).
- Aucun JavaScript écrit pour le site, aucune dépendance npm, aucun service tiers.
- `hugo.toml` ne change que dans le cadre d'un plan validé.

## Définition de terminé
Voir architecture §14.4 : plan validé, build sans erreur ni nouvel avertissement,
contrôle de publication, FR et EN à jour, images vérifiées, revue visuelle par Firmin,
document d'architecture à jour si la structure change.

## Workflow git
- Partir de `main` à jour ; ne jamais travailler directement sur `main`.
- Une branche par tâche : `feat/`, `fix/`, `chore/`, `docs/` (le contenu du site passe par `docs/`).
- Commits petits, en Conventional Commits.
- Jamais `--no-verify`, jamais de force-push.
- Pousser la branche, puis demander l'accord de Firmin avant d'ouvrir la PR.
- Fusionner une PR seulement sur demande explicite de Firmin. Revenir sur main après l’ouverture ou la fusion de chaque PR.
