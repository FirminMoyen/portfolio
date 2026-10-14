# Structure du site — page par page

| | |
|---|---|
| Statut | Validé (v0.1), 14 octobre 2026 |
| Date | 14 octobre 2026 |
| Emplacement | `docs/structure.md` du repo `FirminMoyen/portfolio` |
| Complète | `docs/architecture.md`, en particulier ses sections URL, Sections, Modèle de contenu, Implémentation Hugo et Plan d'implémentation |
| Lecteurs | Claude Code (implémente), Firmin (valide) |

## 0. Portée

- Ce document fixe la **structure** du site : pages, URL, fichiers, types Hugo, templates, menus, fil d'Ariane, blocs de chaque page, redirections. Il ne contient **aucun contenu** : la prose appartient à Firmin (architecture §9).
- En cas d'écart avec `docs/architecture.md`, Claude Code s'arrête et le signale (architecture §0.1).
- Chaque bloc de page indique la phase du plan (architecture §15) où son rendu est implémenté.
- Aujourd'hui (§7), seuls sont créés l'arborescence, la navigation, les redirections et les archetypes. Les pages s'affichent avec les templates par défaut de PaperMod.

## 1. Principes de structure

- **URL.** Toutes les pages vivent sous `/fr/` ou `/en/` (architecture §4). Les slugs sont en anglais et identiques dans les deux langues.
- **Dossiers.** Une page est un dossier contenant `index.fr.md` et `index.en.md`. Une section a ses `_index.fr.md` et `_index.en.md`.
- **Brouillon tant que vide.** Toute page sans contenu porte `draft: true`. En production, elle n'est pas construite et n'apparaît ni dans le menu ni dans le plan du site. `hugo server -D` montre l'arborescence complète.
- **Menus dans le front matter des pages,** plus dans `hugo.toml`. Une entrée de menu n'existe que si sa page est construite : une section entre au menu automatiquement le jour où elle est publiée.
- **Titres et descriptions.** Les titres sont les libellés de ce document. La description vaut `TODO(firmin)` tant que Firmin ne l'a pas écrite ; c'est permis dans un brouillon seulement.
- **Pages d'état sans métadonnées d'article.** L'accueil, les sections, les pages de groupe et À propos n'affichent ni date, ni temps de lecture, ni navigation précédent/suivant.

## 2. Inventaire

| ID | Page | URL FR | URL EN | Source | Type | Menu (poids) | Aujourd'hui |
|---|---|---|---|---|---|---|---|
| P01 | Racine | `/` | — | Générée par Hugo | Redirection | — | Redirige vers la langue par défaut (D1) |
| P02 | Accueil | `/fr/` | `/en/` | `content/_index.{fr,en}.md` | home | Accueil / Home (10) | Publiée (existante) |
| P03 | Infrastructure | `/fr/infrastructure/` | `/en/infrastructure/` | `content/infrastructure/_index.*` | section | Infrastructure (20) | Brouillon |
| P04 | Page de groupe (×7) | `/fr/infrastructure/<groupe>/` | `/en/infrastructure/<groupe>/` | `content/infrastructure/<groupe>/index.*` | page | — | Brouillons |
| P05 | Décisions d'architecture | `/fr/infrastructure/decisions/` | `/en/infrastructure/decisions/` | `content/infrastructure/decisions/_index.*` | section | — | Brouillon |
| P06 | ADR | `…/decisions/adr-NNNN-<slug>/` | idem | Archetype `adr` | page | — | Modèle seulement |
| P07 | Services | `/fr/services/` | `/en/services/` | `content/services/_index.*` | section | Services (30) | Brouillon |
| P08 | Fiche service | `/fr/services/<id>/` | `/en/services/<id>/` | Archetype `services` | page | — | Modèle seulement |
| P09 | Devlog | `/fr/devlog/` | `/en/devlog/` | `content/devlog/_index.*` | section | Devlog (40) | Brouillon |
| P10 | Entrée devlog | `/fr/devlog/NNN-<slug>/` | idem | Archetype `devlog` | page | — | Modèle seulement |
| P11 | Incidents | `/fr/devlog/incidents/` | `/en/devlog/incidents/` | `content/devlog/incidents/_index.*` | section | — | Brouillon |
| P12 | Post-mortem | `/fr/devlog/incidents/pm-NNN-<slug>/` | idem | Archetype `postmortem` | page | — | Modèle seulement |
| P13 | À propos | `/fr/about/` | `/en/about/` | `content/about/index.*` | page | À propos / About (50) | Publiée (convertie en dossier) |
| P14 | Tags | `/fr/tags/`, `/fr/tags/<tag>/` | idem | Générées par Hugo | taxonomie | — | Automatiques ; aucun tag aujourd'hui |
| P15 | Certifications | `/fr/certifications/`, `/fr/certifications/<id>/` | idem | Générées par Hugo | taxonomie | — | Automatiques ; aucune aujourd'hui |
| P16 | Page 404 | `/fr/404.html`, `/404.html` | `/en/404.html` | Thème ; `static/404.html` à la racine | — | — | Racine : page autonome bilingue (1.1) |

Les sept groupes de P04, avec leurs libellés (architecture §6.4) :

| Dossier | Titre FR | Titre EN |
|---|---|---|
| `hardware` | Matériel | Hardware |
| `network` | Réseau | Network |
| `virtualization` | Virtualisation | Virtualization |
| `storage-backup` | Stockage et sauvegardes | Storage and backup |
| `identity-security` | Identité et sécurité | Identity and security |
| `kubernetes` | Kubernetes | Kubernetes |
| `automation` | Automatisation | Automation |

## 3. Éléments communs à toutes les pages

### 3.1 En-tête

| Élément | Comportement | Phase |
|---|---|---|
| Titre du site | Lien vers l'accueil de la langue courante | Existant |
| Menu | Entrées des pages publiées, dans l'ordre des poids (§3.5) | Aujourd'hui (1.2) |
| Sélecteur de langue | Mène à la page traduite (surcharge existante de `header.html`) | Existant |
| Bascule de thème | Clair / sombre (PaperMod) | Existant |

### 3.2 Fil d'Ariane

Affiché sur toutes les pages sauf l'accueil (`ShowBreadCrumbs`). Il suit l'arborescence : Accueil › Infrastructure › Réseau ; Accueil › Devlog › Incidents › PM-001. Activé aujourd'hui (1.2).

### 3.3 Pied de page

- Copyright.
- Lien vers le code source du site.
- Mention « ni cookies ni traceurs », dont le texte vient des fichiers i18n.
- Lien vers le flux RSS du devlog (`/<lang>/devlog/index.xml`), sur toutes les pages, affiché seulement quand le devlog est publié.

Le lien RSS est en place depuis l'étape 1.4 : `extend_footer.html` l'ajoute sous le pied de page de PaperMod. Le reste est implémenté en phase 5.2 dans le même fichier. Aucun bouton RSS à côté des titres (`ShowRssButtonInSectionTermList` désactivé).

### 3.4 Métadonnées

- `<title>` et description de chaque page ;
- liens `hreflang` vers la traduction (PaperMod) ;
- balises OpenGraph, avec une image par défaut ajoutée en phase 3.1.

### 3.5 Menu

| Identifiant | FR | EN | Cible | Poids | Apparaît |
|---|---|---|---|---|---|
| `home` | Accueil | Home | P02 | 10 | Toujours |
| `infrastructure` | Infrastructure | Infrastructure | P03 | 20 | Quand P03 est publiée (4.2) |
| `services` | Services | Services | P07 | 30 | Quand P07 est publiée (4.2) |
| `devlog` | Devlog | Devlog | P09 | 40 | Quand P09 est publiée (3.3) |
| `about` | À propos | About | P13 | 50 | Toujours |

En production, le menu se limite donc aujourd'hui à **Accueil · À propos**. Les autres entrées apparaissent seules, avec la publication de leur section.

### 3.6 Redirections des anciennes URL

Les alias de Hugo reçoivent le préfixe de langue. Avec les deux langues en sous-dossier, une URL à la racine comme `/about/` ne peut donc pas venir d'un alias. Toutes les anciennes URL sont redirigées par de petits fichiers `static/<chemin>/index.html` :

- une redirection immédiate (`<meta http-equiv="refresh">`) ;
- un lien `canonical` vers la cible ;
- `noindex` ;
- un lien cliquable.

C'est le même format que les alias de Hugo, et une seule liste à tenir : ce tableau.

| Ancienne URL | Cible aujourd'hui | Cible finale | Mise à jour à l'étape |
|---|---|---|---|
| `/about/` | `/fr/about/` | `/fr/about/` | — |
| `/journal/` | `/fr/` | `/fr/devlog/` | 3.3 |
| `/journal/proxmox-homelab-premiers-pas/` | `/fr/` | `/fr/devlog/` | 3.3 |
| `/projects/` | `/fr/` | `/fr/infrastructure/` | 4.2 |
| `/en/journal/` | `/en/` | `/en/devlog/` | 3.3 |
| `/en/journal/proxmox-homelab-first-steps/` | `/en/` | `/en/devlog/` | 3.3 |
| `/en/projects/` | `/en/` | `/en/infrastructure/` | 4.2 |
| `/tags/` | `/fr/tags/` | `/fr/tags/` | — |
| `/categories/` | `/fr/` | `/fr/` | — |
| `/en/categories/` | `/en/` | `/en/` | — |

Les deux lignes de l'article suivent D2 (§8) ; si l'article est conservé, elles changent. `/en/`, `/en/about/` et `/en/tags/` gardent leur adresse.

À l'étape 1.1, tant que `journal`, `projects` et la taxonomie `categories` existent, les redirections de la racine visent leur équivalent sous `/fr/` (`/journal/` → `/fr/journal/`…) ; l'étape 1.2 les passe à leur « cible aujourd'hui ».

Exceptions, sans redirection :

- les pages `…/page/1/`, que Hugo génère lui-même pour renvoyer vers la première page d'une liste et qui ne sont liées nulle part ;
- les flux RSS (`index.xml`) des anciennes URL : une page HTML ne peut pas rediriger un lecteur de flux.

### 3.7 Fichiers techniques

| Fichier | Origine |
|---|---|
| `/index.html` | Redirection vers la langue par défaut, générée par Hugo |
| `/404.html` | Exigé par GitHub Pages. Hugo ne le génère pas quand les deux langues sont en sous-dossier : `static/404.html`, page bilingue autonome (CSS intégré, clair et sombre, sans JavaScript, sans le style du thème) |
| `/robots.txt` | `enableRobotsTXT` |
| `/sitemap.xml` | Index des plans de site par langue (Hugo) |
| `/<lang>/index.xml`, `/<lang>/devlog/index.xml` | Flux RSS (Hugo, PaperMod) |
| `/CNAME` | `static/CNAME`, existant |

## 4. Les pages

Format de chaque fiche : identité de la page, puis ses blocs dans l'ordre d'affichage. Entre parenthèses, la source du bloc et sa phase :

- *thème* : rendu existant de PaperMod ;
- *Firmin* : prose du corps de la page ;
- *archetype* : rubriques créées par l'archetype ;
- un numéro de phase (architecture §15) : rendu implémenté par un template ou un shortcode à cette étape.

### P02 — Accueil

| | |
|---|---|
| Rôle | L'essentiel en un écran : qui, quoi, preuve d'activité, contact |
| URL | `/fr/` · `/en/` |
| Fichiers | `content/_index.fr.md`, `content/_index.en.md` |
| Type, template | home ; `layouts/home.html` (5.2). D'ici là, liste par défaut de PaperMod |
| Menu | Accueil / Home (10) |
| Aujourd'hui | Contenu actuel conservé ; entrée de menu ajoutée au front matter ; `mainSections = ["devlog"]` |

1. **Identité** : `headline`, `availability`, pitch, boutons CV, Contact (lien vers `#contact` de P13), GitHub, LinkedIn. *(front matter et Firmin ; liens dans `hugo.toml` ; 5.2)*
2. **Le lab en un coup d'œil** : schéma `lab-overview`, nombre de composants par statut, phases en cours, date de dernière vérification, lien vers P03. *(données ; 5.1 et 5.2)*
3. **Stack** : composants non retirés, groupés, avec leur badge de statut. *(catalogue ; 5.2)*
4. **Derniers devlogs** : les 3 dernières entrées, P10 ou P12 (numéro, date, titre, description). *(5.2)*
5. **Certifications** : liste et statuts. *(données ; 5.2)*

### P03 — Infrastructure

| | |
|---|---|
| Rôle | Vue d'ensemble : schéma, composants par groupe, dernières décisions |
| URL | `/fr/infrastructure/` · `/en/infrastructure/` |
| Fichiers | `content/infrastructure/_index.fr.md`, `_index.en.md` |
| Type, template | section ; `layouts/infrastructure/section.html` (4.1) |
| Menu | Infrastructure (20), dès sa publication |
| Fil d'Ariane | Accueil › Infrastructure |
| Aujourd'hui | Brouillon |

1. **En-tête** : titre, description. *(thème)*
2. **Introduction**, dont la règle de frontière entre infrastructure et services. *(Firmin)*
3. **Schéma** `lab-overview`. *(5.1)*
4. **Composants par groupe** : un tableau par groupe, dans l'ordre de `data/groups.yaml`. Colonnes : nom (lien vers sa carte dans P04), rôle, statut, où il tourne, date de vérification. *(4.1)*
5. **Dernières décisions** : les 5 ADR les plus récentes et un lien vers P05. *(4.1)*

### P04 — Page de groupe d'infrastructure (×7)

| | |
|---|---|
| Rôle | Un domaine de l'infrastructure : prose et cartes de ses composants |
| URL | `/fr/infrastructure/<groupe>/` · `/en/infrastructure/<groupe>/` |
| Fichiers | `content/infrastructure/<groupe>/index.fr.md`, `index.en.md` |
| Type, template | page ; `layouts/infrastructure/page.html` (4.1) |
| Menu | — (accès par P03) |
| Fil d'Ariane | Accueil › Infrastructure › *Groupe* |
| Aujourd'hui | 7 brouillons : titre, description `TODO(firmin)`, rubriques vides |

1. **En-tête** : titre (libellé du groupe), description. *(thème)*
2. **Rubriques** : Rôle dans le lab · Mise en œuvre · Exploitation · Limites et évolutions. *(Firmin)*
3. **Cartes des composants** : une par composant du groupe, ancrée sur `#<id>`. Chaque carte porte la fiche technique (architecture §5.4) et les liens vers le devlog, les ADR et les incidents qui la concernent. *(catalogue ; 4.1)*

### P05 — Décisions d'architecture (index)

| | |
|---|---|
| Rôle | Toutes les ADR |
| URL | `/fr/infrastructure/decisions/` · `/en/infrastructure/decisions/` |
| Fichiers | `content/infrastructure/decisions/_index.fr.md`, `_index.en.md` |
| Type, template | section ; `layouts/infrastructure/decisions/section.html` (3.2) |
| Menu | — (accès par P03) |
| Fil d'Ariane | Accueil › Infrastructure › Décisions d'architecture |
| Aujourd'hui | Brouillon |

1. **En-tête.** *(thème)*
2. **Introduction** : ce qu'est une ADR ici, les statuts. *(Firmin)*
3. **Tableau des ADR** : numéro, titre (lien), badge de statut, date, de la plus récente à la plus ancienne. *(3.2)*

### P06 — ADR

| | |
|---|---|
| URL | `/fr/infrastructure/decisions/adr-NNNN-<slug>/` |
| Fichiers | Créés par `hugo new content --kind adr …` |
| Type, template | page ; `layouts/infrastructure/decisions/page.html` (3.2) |
| Fil d'Ariane | Accueil › Infrastructure › Décisions d'architecture › ADR-NNNN |
| Aujourd'hui | Archetype seulement (1.3) |

1. **En-tête** : « ADR-0007 — titre », badge de statut, date, composants concernés (liens). *(3.2)*
2. **Bandeau** « Remplacée par ADR-xxxx » ou « Remplace ADR-xxxx », s'il y a lieu. *(3.2)*
3. **Corps** : Contexte · Options considérées · Décision · Conséquences. *(archetype)*
4. **Citée par** : les entrées devlog qui la référencent, calculées. *(3.2)*

### P07 — Services (catalogue)

| | |
|---|---|
| Rôle | Tous les services du lab |
| URL | `/fr/services/` · `/en/services/` |
| Fichiers | `content/services/_index.fr.md`, `_index.en.md` |
| Type, template | section ; `layouts/services/section.html` (4.1) |
| Menu | Services (30), dès sa publication |
| Fil d'Ariane | Accueil › Services |
| Aujourd'hui | Brouillon |

1. **En-tête.** *(thème)*
2. **Introduction.** *(Firmin)*
3. **Légende des statuts.** *(4.1)*
4. **Un tableau par groupe de services.** Colonnes : nom (lien vers P08 si elle est publiée), rôle, statut, où il tourne, exposition, date de vérification. *(catalogue ; 4.1)*

### P08 — Fiche service

| | |
|---|---|
| URL | `/fr/services/<id>/` |
| Fichiers | Créés par `hugo new content --kind services services/<id>` |
| Type, template | page ; `layouts/services/page.html` (4.1) |
| Fil d'Ariane | Accueil › Services › *Nom* |
| Aujourd'hui | Archetype seulement (1.3) |

1. **En-tête** : nom, badge de statut, rôle. *(catalogue ; 4.1)*
2. **Fiche technique** (architecture §5.4). *(catalogue ; 4.1)*
3. **Corps** : Pourquoi · Mise en œuvre · Exploitation · Limites et évolutions. *(archetype)*
4. **Liés** : entrées devlog, ADR et incidents, calculés. *(4.1)*

### P09 — Devlog (liste)

| | |
|---|---|
| Rôle | Le chemin parcouru, semaine par semaine |
| URL | `/fr/devlog/` · `/en/devlog/` |
| Fichiers | `content/devlog/_index.fr.md`, `_index.en.md` |
| Type, template | section ; `layouts/devlog/section.html` (3.1) |
| Menu | Devlog (40), dès sa publication |
| Fil d'Ariane | Accueil › Devlog |
| Aujourd'hui | Brouillon |

1. **En-tête.** *(thème)* Le flux RSS est proposé dans le pied de page (§3.3).
2. **Introduction.** *(Firmin)*
3. **Accès rapides** : Incidents (P11), Tags (P14), Certifications (P15). *(3.1)*
4. **Liste paginée par 10**, du plus récent au plus ancien : entrées P10 et P12, avec numéro (S07 ou PM-002), date, titre, description et tags. Un badge signale les post-mortems. *(3.1)*

### P10 — Entrée devlog

| | |
|---|---|
| URL | `/fr/devlog/NNN-<slug>/` |
| Fichiers | Créés par `hugo new content --kind devlog devlog/NNN-<slug>` |
| Type, template | page ; `layouts/devlog/page.html` (3.1) |
| Fil d'Ariane | Accueil › Devlog › S07 |
| Aujourd'hui | Archetype seulement (1.3) |

1. **En-tête** : « S07 · titre », date, description, tags, certifications. *(3.1)*
2. **Composants concernés et ADR liées** (liens). *(3.1)*
3. **Corps** : Objectif de la semaine · Réalisé · Problèmes et résolution · Décisions · Appris · Semaine prochaine. *(archetype)*
4. **Erratum**, facultatif, en fin d'entrée. *(Firmin)*
5. **Navigation** précédente / suivante. *(thème)*

### P11 — Incidents (liste)

| | |
|---|---|
| Rôle | Tous les post-mortems |
| URL | `/fr/devlog/incidents/` · `/en/devlog/incidents/` |
| Fichiers | `content/devlog/incidents/_index.fr.md`, `_index.en.md` |
| Type, template | section ; `layouts/devlog/incidents/section.html` (3.1) |
| Menu | — (accès par P09) |
| Fil d'Ariane | Accueil › Devlog › Incidents |
| Aujourd'hui | Brouillon |

1. **En-tête.** *(thème)*
2. **Introduction** : ce qu'est un post-mortem, les niveaux de gravité. *(Firmin)*
3. **Tableau** : numéro, titre (lien), gravité, date de l'incident, durée d'impact. *(3.1)*

### P12 — Post-mortem

| | |
|---|---|
| URL | `/fr/devlog/incidents/pm-NNN-<slug>/` |
| Fichiers | Créés par `hugo new content --kind postmortem devlog/incidents/pm-NNN-<slug>` |
| Type, template | page ; `layouts/devlog/incidents/page.html` (3.1) |
| Fil d'Ariane | Accueil › Devlog › Incidents › PM-003 |
| Aujourd'hui | Archetype seulement (1.3) |

1. **En-tête** : « PM-003 · titre », gravité, date de l'incident, durée d'impact, composants. *(3.1)*
2. **Corps** : Résumé · Impact · Chronologie · Détection · Cause racine · Résolution · Actions correctives · Ce que j'en retiens. *(archetype)*
3. **Navigation** précédente / suivante. *(thème)*

### P13 — À propos

| | |
|---|---|
| Rôle | Le projet, son auteur, le contact, la fabrication du site |
| URL | `/fr/about/` · `/en/about/` |
| Fichiers | `content/about/index.fr.md`, `index.en.md` (aujourd'hui `_index`) |
| Type, template | page ; `layouts/about/page.html` (5.2) |
| Menu | À propos / About (50) |
| Fil d'Ariane | Accueil › À propos |
| Aujourd'hui | Convertie en dossier ; contenu actuel conservé ; entrée de menu dans le front matter |

Structure cible, posée avec le contenu de Firmin en 5.3 :

| Titre FR | Titre EN | Contenu |
|---|---|---|
| ## Le projet | ## The project | ### Objectif · ### Contraintes · ### Feuille de route (shortcode `roadmap`, 5.2) |
| ## Moi | ## About me | ### Parcours · ### Certifications (shortcode `certifications`, 5.2) · ### CV (liens vers les PDF) |
| ## Contact | ## Contact | Shortcode `contact` (5.2). Le titre produit l'ancre `#contact` dans les deux langues |
| ## Ce site | ## This site | Fabrication et contrôles du site, lien vers le repo |

### P14 et P15 — Taxonomies

| | Tags | Certifications |
|---|---|---|
| Index | `/fr/tags/` : chaque terme avec son nombre de pages | `/fr/certifications/` |
| Page de terme | `/fr/tags/<tag>/` : libellé (tiré de `data/tags.yaml` en 5.2), liste des pages | `/fr/certifications/<id>/` : libellé (tiré de `data/certifications.yaml`) |
| Template | `layouts/taxonomy.html`, `layouts/term.html` (5.2) | idem |
| Aujourd'hui | Taxonomie déclarée dans `hugo.toml` ; pages générées dès qu'un terme est utilisé | idem |

### P16 — Page 404

Fournie par PaperMod sous `/fr/404.html` et `/en/404.html`. GitHub Pages sert `/404.html` à la racine, que Hugo ne génère pas avec les deux langues en sous-dossier : c'est `static/404.html`, une page bilingue autonome qui renvoie vers `/en/` et `/fr/` (choix du 14/10/2026, étape 1.1).

## 5. Arborescence après aujourd'hui

```
content/
├── _index.fr.md, _index.en.md                     P02 Accueil (publiée)
├── about/index.fr.md, index.en.md                 P13 À propos (publiée)
├── infrastructure/
│   ├── _index.fr.md, _index.en.md                 P03 (brouillon)
│   ├── hardware/index.fr.md, index.en.md          P04 (brouillon)
│   ├── network/…                                  P04 (brouillon)
│   ├── virtualization/…                           P04 (brouillon)
│   ├── storage-backup/…                           P04 (brouillon)
│   ├── identity-security/…                        P04 (brouillon)
│   ├── kubernetes/…                               P04 (brouillon)
│   ├── automation/…                               P04 (brouillon)
│   └── decisions/_index.fr.md, _index.en.md       P05 (brouillon)
├── services/_index.fr.md, _index.en.md            P07 (brouillon)
└── devlog/
    ├── _index.fr.md, _index.en.md                 P09 (brouillon)
    └── incidents/_index.fr.md, _index.en.md       P11 (brouillon)
archetypes/
├── devlog/index.fr.md, index.en.md                P10
├── postmortem/index.fr.md, index.en.md            P12
├── adr/index.fr.md, index.en.md                   P06
└── services/index.fr.md, index.en.md              P08
static/
├── CNAME                                          existant
└── <7 redirections du §3.6>/index.html
```

Supprimés : `content/journal/`, `content/projects/`, ancien article (selon D2).

## 6. Front matter de structure

**Section en brouillon** (P03, P05, P07, P09, P11). Exemple :

```yaml
---
title: "Infrastructure"
description: "TODO(firmin)"
draft: true
menus:
  main:
    identifier: infrastructure
    weight: 20
---
```

- P05 et P11 n'ont pas de clé `menus`.
- Les deux langues partagent le même `identifier` et le même `weight`.
- `title` change avec la langue lorsque le libellé diffère (Décisions d'architecture / Architecture decisions).

**Page de groupe** (P04). Exemple :

```markdown
---
title: "Réseau"
description: "TODO(firmin)"
draft: true
ShowReadingTime: false
ShowPostNavLinks: false
---

## Rôle dans le lab

## Mise en œuvre

## Exploitation

## Limites et évolutions
```

Rubriques en anglais : Role in the lab · Implementation · Operations · Limits and next steps.

**Accueil** (P02) : on ajoute seulement ceci au front matter existant.

```yaml
menus:
  main:
    identifier: home
    name: "Accueil"        # "Home" dans _index.en.md
    weight: 10
```

**À propos** (P13) : on ajoute au front matter existant `ShowReadingTime: false`, `ShowPostNavLinks: false`, et une entrée de menu `about` de poids 50, dont le nom est le titre.

## 7. Mise en œuvre aujourd'hui

Ordre retenu pour aujourd'hui : **0.1, puis la phase 1**. Les étapes 0.2 à 0.4 (CI, contrôles de publication, nettoyage) suivent à la prochaine session. D'ici là, `hugo --minify` exécuté en local fait office de contrôle (architecture §14.4). Chaque étape est une branche et une PR, avec un plan présenté avant toute écriture.

| Étape | Branche | Contenu | Critères d'acceptation |
|---|---|---|---|
| 0.1 | `docs/architecture` | `docs/architecture.md` (v0.3), `docs/structure.md` (ce document), `CLAUDE.md` (architecture, Annexe B), `.claude/rules/`, `.claude/settings.json` | `CLAUDE.md` sous 200 lignes ; la nouvelle règle sur `content/` (architecture C8) est en place, ce qui autorise les étapes suivantes |
| 1.1 | `feat/i18n-subdirs` | Langues en sous-dossier, langue par défaut (D1) ; `timeZone`, `enableRobotsTXT`, `refLinksErrorLevel` ; redirections de `static/` vers les équivalents `/fr/` des pages encore existantes | `/` redirige vers la langue choisie ; chaque ancienne URL du §3.6 redirige ; le sélecteur de langue mène à la page traduite ; présence de `/404.html` vérifiée, ou solution proposée dans la PR |
| 1.2 | `feat/sections` | Arborescence du §5 ; conversion d'À propos en dossier ; suppression de `journal` et `projects` (D2) ; menus déplacés dans le front matter (§3.5, §6) et retirés de `hugo.toml` ; taxonomies `tags` et `certifications` ; paramètres `ShowBreadCrumbs`, `ShowCodeCopyButtons`, `ShowPostNavLinks`, `mainSections = ["devlog"]` ; services tiers désactivés (`[privacy]`) ; redirections passées à leur « cible aujourd'hui » (§3.6) | Build vert, sans nouvel avertissement. **En production** (sans `-D`) : seules P02 et P13 existent, dans les deux langues, avec un menu Accueil · À propos. **Avec `-D`** : toutes les pages du §2 sont navigables, le menu compte 5 entrées dans l'ordre, le fil d'Ariane est juste, chaque page mène à sa traduction. Rien d'autre n'est écrit que les libellés de ce document et des `TODO(firmin)` |
| 1.3 | `feat/archetypes` | Archetypes de dossier `devlog`, `postmortem`, `adr`, `services`, conformes à l'architecture, Annexe A | Chaque `hugo new content --kind …` crée FR et EN en brouillon, au bon front matter et avec les bonnes rubriques. Les fichiers de test sont supprimés, pas commités |
| 1.4 | `feat/footer-rss` | Bouton RSS retiré des titres ; lien vers le flux RSS du devlog sous le pied de page (`extend_footer.html`, §3.3) ; premiers fichiers `i18n/` et `assets/css/extended/site.css` | Aucun logo RSS à côté des titres ; avec `-D`, le lien figure en bas de chaque page dans les deux langues ; en production, absent tant que le devlog est en brouillon |

Reportés à leurs phases : templates et rendu des blocs (3 à 5), modèle de données et validations (2), `enableGitInfo` (0.2, qui exige un clonage complet en CI), pied de page et fichiers i18n (5.2).

## 8. Décisions à confirmer avant de commencer

| # | Question | Recommandation | Bloque |
|---|---|---|---|
| D1 | Vers quelle langue `/` redirige-t-il ? | **Tranchée le 14/10/2026 : `en`** (architecture §17.2) | 1.1 |
| D2 | Que faire de l'article `proxmox-homelab-premiers-pas` ? | **Tranchée le 14/10/2026 : supprimé** ; ses URL redirigent comme au §3.6 | 1.2 |
