---
paths:
  - "content/**"
  - "data/**"
  - "archetypes/**"
  - "static/cv/**"
---

# Contenu et données

Détail : `docs/architecture.md` §6, §7, §9, §10.

## Données (§6)
- Un composant = un fichier `data/catalog/<id>.yaml` ; l'identifiant est le nom du fichier, en kebab-case ASCII, et ne change pas (§6.1).
- Respecter le schéma et les énumérations du §6.2. `exposure` vaut `internal` ou `vpn`, rien d'autre.
- Respecter les exigences par statut (§6.3). Tout `none` (auth, backup, supervision entièrement à `false`) exige un `note: {fr, en}`.
- Chaîne à traduire dans les données : `{fr: "…", en: "…"}`.
- Nouveau tag : l'ajouter à `data/tags.yaml` dans la même PR (§5.8).
- `verified` et `backup.restore_tested` ne changent que sur indication explicite de Firmin (§9.2).

## Contenu (§7)
- Une page = un dossier avec `index.fr.md` et `index.en.md` ; une section = `_index.fr.md` et `_index.en.md` (§7.1).
- Numéros complétés par des zéros : 3 chiffres (journal, post-mortems), 4 (ADR).
- Front matter YAML : `title`, `description` (160 caractères au plus), `draft`, plus les champs requis par type (§7.2). Champ `slug` interdit.
- Champs structurés identiques en FR et en EN ; seuls `title`, `description` et le corps diffèrent (§7.2).
- Aucune URL du site en dur : shortcodes `component`, `adr`, `pm`, ou `relref` (§7.4).
- Images dans le dossier de la page, texte alternatif obligatoire, 1 Mo au plus (§7.5).
- Archetypes : aucun appel de shortcode (`{{<`) (§7.3).

## Rédaction (§9)
- Claude Code crée la structure de `content/` (dossiers, front matter, rubriques vides, libellés de `docs/structure.md`, `TODO(firmin)` dans les brouillons) ; il met en forme, traduit et corrige ce que Firmin fournit ; il ne rédige jamais de prose de lui-même (C8, §9.1).
- Aucun fait inventé : ni commande, ni version, ni chiffre, ni résultat, ni leçon. Information manquante : demander ou `TODO(firmin): <question>` (§9.2).
- Historique immuable : journal (erratum daté), ADR acceptée (seuls `status` et `superseded_by`), post-mortem (seul l'état des actions) (§9.3).
- Traduction : le sens, même structure ; ne jamais traduire code, commandes, identifiants, noms de produits, champs structurés ; ne rien ajouter ni retirer (§9.4).
- Style : première personne, passé composé, phrases courtes, aucun superlatif (§9.5).
- Toute modification de `index.fr.md` se reporte dans `index.en.md`, dans la même PR (§8).

## Publication (§10)
- Interdits : IP publique (v4 et v6), adresses VPN (100.64.0.0/10), nom du tailnet, ports et règles d'accès, tout secret même révoqué, métadonnées GPS, données personnelles hors nom, région, e-mail dédié et liens professionnels.
- Ouvrir chaque image ajoutée et signaler tout contenu sensible visible.
- Fuite publiée : révoquer d'abord (§16.8).
