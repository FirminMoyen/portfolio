# Architecture du site firminmoyen.dev

| | |
|---|---|
| Statut | Validé (v0.3), 14 octobre 2026 |
| Date | 14 octobre 2026 |
| Emplacement | `docs/architecture.md` du repo `FirminMoyen/portfolio` |
| Lecteurs | Claude Code (implémente et maintient), Firmin (valide), visiteurs du repo : ce document est public |
| Documents liés | Structure page par page : `docs/structure.md` (pages, URL, menus, blocs, redirections). Architecture et plan du lab (`docs/architecture.md` du repo `homelab`) : calendrier commun (§15 de ce plan), contenu du catalogue, ADR prévues. Règles opérationnelles : `CLAUDE.md` et `.claude/rules/` |

## Résumé

Le site présente un homelab reconstruit de zéro et documenté chaque semaine. Il doit permettre à Firmin d'être repéré pour un poste en administration systèmes et infrastructure. Il sépare deux natures de contenu :

- **l'état actuel du lab** : Infrastructure et Services, des pages mises à jour en place et générées depuis un catalogue de données unique (`data/catalog/`) ;
- **le chemin parcouru** : Devlog (une entrée par semaine), post-mortems et décisions d'architecture (ADR), des entrées datées qu'on ne réécrit pas.

L'Accueil (pitch, schéma du lab, stack, derniers devlogs, CV) et la page À propos (le projet, son auteur, les contacts) complètent l'ensemble. Le site est bilingue FR/EN et statique (Hugo + PaperMod sur GitHub Pages), sans JavaScript propre. Il se valide lui-même : le build Hugo échoue si une donnée est incohérente, une traduction manquante ou une référence cassée. La CI ajoute les contrôles que Hugo ne peut pas faire : secrets, adresses IP, métadonnées d'images, synchronisation des traductions.

---

## 0. Mode d'emploi pour Claude Code

### 0.1 Autorité des documents

- Ce document décrit la structure du site et ses raisons. `CLAUDE.md` et `.claude/rules/` contiennent les règles opérationnelles courtes et renvoient ici pour le détail.
- Si une demande contredit ce document, ne pas l'exécuter en silence. Signaler la contradiction et proposer une modification du document. Le document et le code changent dans la même PR.
- Les décisions ouvertes (§17.1) appartiennent à Firmin. Claude Code ne les tranche pas.
- Le détail page par page (fichiers, templates, menus, blocs, redirections) est dans `docs/structure.md`. Ce document le complète sans jamais le contredire.

### 0.2 Vocabulaire normatif

- **DOIT / NE DOIT PAS** : règle obligatoire ; une violation bloque la PR.
- **DEVRAIT / NE DEVRAIT PAS** : règle par défaut ; tout écart est justifié dans la description de la PR.
- **PEUT** : option.

### 0.3 Manière de travailler

- Firmin n'écrit pas le code mais valide tout. Avant de créer ou de modifier un fichier, Claude Code DOIT présenter un plan (fichiers concernés, objectif de chaque changement) et attendre son accord.
- Une étape à la fois. Une étape du §15 correspond à une branche et à une PR. Claude Code ne prend pas d'avance sur l'étape suivante.
- Commits petits, en Conventional Commits. Workflow git : §14 et `CLAUDE.md`.

### 0.4 Première action

Lire ce document en entier, puis présenter le plan de l'étape 0.1 (§15) sans écrire de fichier. Chaque décision ouverte (§17.1) est posée à Firmin au moment de l'étape qu'elle bloque, pas avant.

### 0.5 Tenir ce document à jour

Une PR qui modifie la structure (sections, schémas de données, règles de validation, CI, outillage, gouvernance) DOIT mettre à jour ce document dans la même PR et ajouter une ligne au journal (§17.2).

---

## 1. Contexte et objectifs

### 1.1 Le projet

Firmin reconstruit son homelab de zéro, avec le matériel qu'il possède déjà et sans budget. Le lab lui sert à apprendre, à préparer des certifications (CCNA, Red Hat, Terraform, Ansible, Kubernetes) et à démontrer des pratiques d'exploitation conformes aux standards du métier : sécurité, maintenance, disponibilité. Rien n'y est exposé sur Internet.

Le site est la vitrine de ce travail. Chaque semaine, Firmin le met à jour et publie un post LinkedIn qui renvoie vers l'entrée du devlog.

### 1.2 Publics

| Public | Temps | Ce qu'il cherche | Parcours type |
|---|---|---|---|
| Recruteur | moins d'une minute | Qui, quel poste, quel niveau, preuve d'activité, contact | Accueil → CV ou contact |
| Responsable technique, ingénieur | 5 à 15 minutes | Rigueur, raisonnement, capacité d'exploitation | Accueil → Infrastructure → fiche → ADR → devlog ou post-mortem → code |
| Firmin | — | La référence de son propre lab | Toutes les sections |

### 1.3 Critères de réussite

- Sur l'accueil, en un écran (desktop), un recruteur comprend le profil et voit le lab.
- Chaque affirmation technique est datée et vérifiable : lien vers le code, l'entrée devlog ou l'ADR.
- La mise à jour hebdomadaire coûte peu : Firmin donne ses notes, valide, fusionne. Les archetypes et les procédures guident le reste ; le build et la CI le contrôlent.

---

## 2. Principes d'architecture

- **P1 — L'état n'est pas l'historique.** Infrastructure et Services décrivent l'état actuel et se modifient en place. Devlog, post-mortems et ADR forment l'historique : datés, jamais réécrits (§9.3).
- **P2 — Une seule source par fait.** Le statut, l'emplacement, le mode de déploiement, la sauvegarde et la supervision d'un composant n'existent que dans `data/catalog/<id>.yaml`. Les templates les affichent ; la prose ne les répète pas.
- **P3 — Liens déclarés d'un côté, calculés de l'autre.** Une entrée devlog déclare les composants et les ADR qu'elle concerne. Les fiches et les ADR affichent les liens inverses, calculés au build.
- **P4 — Statut honnête.** Prévu, en construction, en service, retiré : un élément prévu n'est jamais présenté comme fait. Un composant n'est déclaré en service qu'avec ses réponses d'exploitation (sauvegarde, supervision, vérification datée) ; le build refuse le statut sinon (§6.3).
- **P5 — Le site se valide lui-même.** Les contrôles de cohérence vivent dans les templates (`errorf`) : `hugo --minify` échoue en local comme en CI. La CI ajoute ce que Hugo ne voit pas (§12, §13).
- **P6 — Sécurité dès la conception.** La politique de publication (§10) est écrite et contrôlée automatiquement ; ce qui ne peut pas l'être passe en revue.
- **P7 — Bilingue par construction.** Chaque page existe en FR et en EN avant fusion. Une modification dans une langue impose la même dans l'autre (§8).
- **P8 — Sobriété.** Site statique, sans JavaScript écrit pour le site : seules les fonctions de PaperMod activées par paramètre en embarquent (bascule de thème, boutons de copie du code). Aucune dépendance npm, aucun service tiers, aucun traceur. Les outils sont épinglés et vérifiés par somme de contrôle.
- **P9 — Le thème reste intact.** PaperMod reste un submodule non modifié. Le site compose avec ses partials et ses points d'extension. Toute surcharge d'un fichier du thème figure au registre (§11.7).

---

## 3. Existant et changements proposés

### 3.1 Existant (commit `7ab02d8`)

- Hugo 0.165.0 extended, thème PaperMod en submodule (commit `d3768854`, nouveau système de templates, Hugo ≥ 0.146 requis).
- Déploiement GitHub Pages par Actions à chaque push sur `main`, domaine `firminmoyen.dev`.
- Bilingue par suffixe (`.fr.md` / `.en.md`) : FR par défaut à la racine, EN sous `/en/`.
- Sections `journal` (un article du 27/08/2026 sur l'ancien lab), `projects` (vide), `about` (texte provisoire).
- Surcharge `layouts/_partials/header.html` : la bascule de langue mène à la page traduite.
- `layouts-maison/` et `assets/css/main.css` présents mais inactifs.
- `CLAUDE.md` et `.claude/settings.json` présents. Aucune CI sur les PR.

### 3.2 Changements à valider

| # | Domaine | Existant | Proposé | Raison |
|---|---|---|---|---|
| C1 | Sections | journal, projects, about | accueil, infrastructure (+ decisions), services, devlog (+ incidents), about | Architecture convenue le 12/10/2026 |
| C2 | URL | FR à la racine, EN sous `/en/` | FR sous `/fr/`, EN sous `/en/` ; la racine redirige vers la langue par défaut | La langue par défaut peut changer sans casser un seul lien (D1) |
| C3 | Ancien contenu | `journal/proxmox-homelab-premiers-pas` | Selon D2 ; `/journal/` redirige vers le devlog | Le lab décrit n'existe plus |
| C4 | Slugs | `slug` anglais différent autorisé | Même slug dans les deux langues, champ `slug` interdit | Appariement et liens prévisibles, contrôle simple |
| C5 | Organisation | Un fichier par langue | Un dossier par page (page bundle) : `index.fr.md`, `index.en.md`, images | Les images vivent avec leur page ; un archetype crée FR et EN d'une commande |
| C6 | CSS | `assets/css/main.css`, non chargé | `assets/css/extended/site.css` | C'est l'emplacement que PaperMod assemble après son propre CSS |
| C7 | JavaScript | « Aucun JavaScript côté client » | Aucun JavaScript écrit pour le site ; fonctions PaperMod activées par paramètre permises | PaperMod embarque déjà du JS (bascule de thème) |
| C8 | Règle sur `content/` | « Ne jamais créer de contenu dans content/ » | Claude Code crée la structure et met en forme ce que Firmin fournit ; il ne rédige jamais de lui-même et n'invente aucun fait (§9) | Permet l'échafaudage, la traduction et les fiches |
| C9 | CI | Déploiement seulement | CI sur PR (build, liens, publication, traductions, diagrammes), déploiement durci, Dependabot | Faire de la CI la barrière, conformément aux conventions de Firmin |
| C10 | Nettoyage | `layouts-maison/`, `assets/css/main.css` | Suppression (D5) | Inutilisés ; l'historique git les conserve |
| C11 | Gouvernance | Un `CLAUDE.md` unique | `CLAUDE.md` court, `.claude/rules/` par zone, skills de procédure | Le contexte n'est chargé que lorsqu'il sert (§14) |

---

## 4. Plan du site et URL

```
/                                             redirection vers /<langue par défaut>/ (D1)
/<lang>/                                      Accueil
/<lang>/infrastructure/                       Vue d'ensemble : schéma, composants, dernières décisions
/<lang>/infrastructure/<groupe>/              Une page par groupe d'infrastructure (§5.2)
/<lang>/infrastructure/decisions/             Index des ADR
/<lang>/infrastructure/decisions/adr-0001-<slug>/
/<lang>/services/                             Catalogue des services
/<lang>/services/<id>/                        Fiche d'un service
/<lang>/devlog/                               Toutes les entrées : hebdomadaires et post-mortems
/<lang>/devlog/001-<slug>/                    Entrée hebdomadaire
/<lang>/devlog/incidents/                     Post-mortems
/<lang>/devlog/incidents/pm-001-<slug>/
/<lang>/about/                                Le projet, l'auteur, les contacts
/<lang>/tags/<tag>/                           Tout ce qui concerne une technologie
/<lang>/certifications/<id>/                  Tout le travail lié à une certification
```

Menu, dans cet ordre : Accueil · Infrastructure · Services · Devlog · À propos (EN : Home · Infrastructure · Services · Devlog · About).

Règles :

- Les slugs sont en ASCII minuscule, en kebab-case, en anglais, et identiques dans les deux langues.
- Une URL publiée ne disparaît pas : un renommage ou une suppression DOIT laisser une redirection, à vérifier dans `public/` après build. Hugo préfixe les `aliases` de la langue de la page ; pour une URL hors des préfixes de langue, la redirection passe par un fichier `static/` (`docs/structure.md` §3.6).
- Chaque fusion sur `main` est déployée, donc aucune section vide en production. Une section sans contenu porte `draft: true`. Les entrées de menu sont déclarées dans le front matter de leur page, pas dans `hugo.toml` : une section entre au menu automatiquement le jour où elle est publiée (`docs/structure.md` §1, §3.5).

---

## 5. Sections

### 5.1 Accueil

Objectif : l'essentiel en un écran sur desktop, en deux sur mobile. Les blocs, dans l'ordre :

1. **Identité.** Nom, poste visé (`headline`), pitch de deux ou trois phrases (corps de `content/_index.<lang>.md`), une ligne de localisation et de mobilité (`availability`). Boutons : CV (PDF de la langue courante), Contact (`/about/#contact`), GitHub, LinkedIn. Les textes viennent de Firmin ; les liens de `hugo.toml`.
2. **Le lab en un coup d'œil.** Schéma `lab-overview` (§11.6), nombre de composants par statut, phases de la roadmap en cours et date de dernière vérification (la plus récente des dates `verified` du catalogue). Lien vers Infrastructure.
3. **Stack.** Composants non retirés, groupés par groupe, chacun avec son badge de statut. Calculé depuis le catalogue.
4. **Devlog.** Les trois dernières entrées (hebdomadaires et post-mortems), avec numéro, date et description.
5. **Certifications.** Statut de chacune, depuis les données.

### 5.2 Infrastructure

**Frontière entre infrastructure et services.** Est infrastructure ce dont le reste du lab dépend pour fonctionner : matériel, réseau, hyperviseur, stockage, sauvegardes, identité, cluster Kubernetes, chaîne IaC/GitOps. Est service ce qui est consommé, par Firmin ou par d'autres services, sans que le reste en dépende : supervision, applications, outils. En cas de doute, une question tranche : si ce composant s'arrête, quels autres composants cessent de fonctionner ? S'il y en a, c'est de l'infrastructure. Le champ `layer` du catalogue porte la décision ; changer de côté, c'est changer un champ.

- **Vue d'ensemble** (`/infrastructure/`) : prose courte de Firmin, schéma, tableau des composants d'infrastructure par groupe avec liens vers les pages de groupe, cinq dernières ADR.
- **Pages de groupe** (`/infrastructure/<groupe>/`) : une par groupe d'infrastructure déclaré dans `data/groups.yaml`, obligatoire dès qu'un composant du groupe est en construction ou en service (V10). Prose de Firmin, puis une carte par composant du groupe : la fiche technique (§5.4), ancrée sur `#<id>`.

### 5.3 Décisions (ADR)

- Une page par décision, numérotée en continu : ADR-0001, ADR-0002… Format : Annexe A.3.
- Statuts : `proposed`, `accepted`, `rejected`, `deprecated`, `superseded`.
- Une ADR acceptée n'est pas réécrite. Changer d'avis passe par une nouvelle ADR qui déclare `supersedes`. L'ancienne passe alors en `superseded` avec `superseded_by` : ce sont les seuls champs qui changent.
- Mérite une ADR tout choix entre de vraies alternatives aux conséquences durables : hyperviseur, topologie réseau, outil de sauvegarde, accès distant, distribution Kubernetes, outil GitOps… Un simple réglage n'en mérite pas.
- Index : numéro, titre, statut, date, du plus récent au plus ancien.
- Page : badge de statut, date, composants concernés, bandeau « remplacée par » s'il y a lieu, entrées devlog qui la citent (calculées).

### 5.4 Services

- **Catalogue** (`/services/`) : un tableau par groupe de services. Colonnes : nom (lien vers la fiche si elle existe), rôle, statut, où il tourne, exposition, date de vérification. Tout vient des données.
- **Fiche** (`/services/<id>/`) : en-tête (nom, statut, rôle), fiche technique, prose de Firmin (Annexe A.4), puis entrées devlog, ADR et post-mortems liés (calculés).

Fiche technique, rendue par le même partial pour les services et pour les cartes d'infrastructure :

| Rubrique | Source dans le catalogue |
|---|---|
| Rôle | `summary` |
| Statut | `status`, `since` |
| Où il tourne | `runtime.kind`, `runtime.host` |
| Déploiement | `deploy.method`, `deploy.code` (lien vers le repo du lab) |
| Exposition | `exposure` |
| Authentification | `auth.method`, `auth.mfa` |
| Sauvegarde | `backup.method`, `backup.frequency`, `backup.restore_tested` (« restauration non testée » si absent) |
| Supervision | `monitoring.metrics`, `monitoring.logs`, `monitoring.alerts` |
| Dépendances | `depends_on` |
| Vérifié le | `verified` |

### 5.5 Devlog

- Une entrée par semaine de travail, numérotée en continu : S1, S2… en français, W1, W2… en anglais. Le numéro compte les comptes rendus hebdomadaires, pas les semaines du calendrier. Après une semaine sans entrée, la suivante prend le numéro suivant et précise la période couverte.
- `date` = dernier jour de la semaine couverte (en pratique, le jour de publication). Une entrée rattrapée garde la date de sa semaine.
- Gabarit fixe (Annexe A.1) : Objectif, Réalisé, Problèmes et résolution, Décisions, Appris, Semaine prochaine.
- Chaque entrée déclare `components`, `adrs`, `tags` et `certifications`.
- Liste (`/devlog/`) : toutes les entrées, post-mortems compris, de la plus récente à la plus ancienne. Pour chacune : numéro (S07 ou PM-002), date, titre, description, tags. Pagination par 10, flux RSS.
- Page : numéro et titre, date, description, tags et certifications, composants concernés, ADR liées, corps, navigation précédente/suivante.
- Le post LinkedIn de la semaine résume l'entrée et y renvoie (§16.1).

### 5.6 Incidents (post-mortems)

- Rédigé pour tout incident qui a causé une perte de service ou de données, ou qui a demandé une remise en état non triviale, même auto-infligé. Ce sont souvent les plus instructifs.
- Format sans recherche de coupable (Annexe A.2) : Résumé, Impact, Chronologie, Détection, Cause racine, Résolution, Actions correctives, Ce que j'en retiens.
- Gravité : `sev1` (perte de données ou lab entièrement indisponible), `sev2` (un composant d'infrastructure ou un service indisponible), `sev3` (dégradation partielle, contournement disponible).
- Numérotation continue : PM-001, PM-002… `date` = publication, `incident_date` = début de l'incident, `impact_minutes` = durée de l'impact.
- Le corps n'est pas réécrit ; seul l'état des actions correctives évolue.
- `/devlog/incidents/` les liste. Ils figurent aussi dans la liste du devlog, avec un badge.

### 5.7 À propos

Une seule page, `/about/`, en trois parties :

1. **Le projet** : objectif, contraintes (budget nul, matériel existant, rien d'exposé), roadmap (shortcode `roadmap`), raison de la reconstruction (D2).
2. **Moi** : parcours, certifications (shortcode `certifications`), CV en FR et en EN, contact (shortcode `contact`, sous un titre « Contact » qui produit l'ancre `#contact`).
3. **Ce site** : comment il est construit et contrôlé (Hugo, CI, politique de publication), lien vers le repo, mention « ni cookies ni traceurs ».

### 5.8 Taxonomies

- `tags` : technologies et thèmes. Le vocabulaire est contrôlé dans `data/tags.yaml` ; un nouveau tag s'ajoute à ce fichier dans la même PR.
- `certifications` : les identifiants de `data/certifications.yaml`.
- Utilisées par les entrées devlog, les post-mortems et les ADR. Les pages d'état n'en ont pas besoin : le catalogue les décrit.
- Les pages de terme affichent le libellé tiré des données.

---

## 6. Modèle de données (`data/`)

Les données sont indépendantes de la langue. Toute chaîne à traduire prend la forme `{fr: "…", en: "…"}`. Tout est validé au build (§12).

### 6.1 Fichiers

| Fichier | Contenu |
|---|---|
| `data/catalog/<id>.yaml` | Un composant, d'infrastructure ou de service. Le nom du fichier est l'identifiant. |
| `data/groups.yaml` | Les groupes de chaque couche : identifiant, libellés, ordre d'affichage |
| `data/tags.yaml` | Le vocabulaire des tags |
| `data/certifications.yaml` | Les certifications |
| `data/roadmap.yaml` | Les phases du projet |

Les identifiants sont en kebab-case ASCII et ne changent pas : l'URL des fiches en dépend. Un renommage impose une redirection.

### 6.2 Catalogue : schéma

```yaml
# data/catalog/grafana.yaml — EXEMPLE ILLUSTRATIF, à ne pas recopier dans data/
name: Grafana                  # nom affiché, non traduit
layer: service                 # infrastructure | service
group: observability           # identifiant d'un groupe de cette couche (data/groups.yaml)
status: running                # planned | building | running | retired
since: 2026-11-02              # date d'entrée dans le statut actuel
summary:                       # une phrase : le rôle du composant
  fr: "Tableaux de bord des métriques et des journaux du lab."
  en: "Dashboards for the lab's metrics and logs."
runtime:
  kind: pod                    # hardware | bare-metal | vm | lxc | pod | tooling | external
  host: k8s-cluster            # identifiant (ou liste d'identifiants) du composant hôte
deploy:
  method: argocd               # manual | ansible | terraform | helm | kustomize | argocd | flux
  code: apps/grafana           # chemin dans le repo du lab (D3)
exposure: vpn                  # internal | vpn — aucune autre valeur n'est acceptée
auth:
  method: sso                  # sso | local | ssh-key | certificate | none
  mfa: true
backup:
  method: velero               # none | vzdump | pbs | velero | restic | config-export
  frequency: daily             # hourly | daily | weekly | manual
  restore_tested: 2026-11-10   # dernier test de restauration réussi
monitoring:
  metrics: true
  logs: true
  alerts: false
depends_on: [prometheus, loki] # identifiants des composants dont il dépend
verified: 2026-11-10           # dernière vérification de cette fiche contre le lab réel
```

Sens des valeurs :

- `runtime.kind` : `hardware` (appareil physique), `bare-metal` (logiciel installé directement sur le matériel, comme Proxmox VE), `vm`, `lxc`, `pod` (charge Kubernetes), `tooling` (exécuté depuis le poste de travail ou la CI, comme Terraform), `external` (hébergé hors du lab).
- `exposure` : `internal` (joignable uniquement depuis les réseaux du lab), `vpn` (joignable aussi depuis les appareils de Firmin, par le VPN maillé). Une exposition publique n'existe pas dans ce modèle : l'introduire serait un changement d'architecture, à décider par ADR.
- Ajouter une valeur à une énumération, c'est modifier ce paragraphe, les chaînes i18n et la validation dans la même PR.

### 6.3 Exigences par statut

| Champ | `planned` | `building` | `running` | `retired` |
|---|---|---|---|---|
| `name`, `layer`, `group`, `status`, `summary` | requis | requis | requis | requis |
| `runtime.kind`, `deploy.method` | — | requis | requis | — |
| `runtime.host` | — | requis pour `bare-metal`, `vm`, `lxc`, `pod` | idem | — |
| `exposure`, `auth` | — | requis pour `bare-metal`, `vm`, `lxc`, `pod` | idem | — |
| `backup`, `monitoring` | — | — | requis | — |
| `verified` | — | requis | requis | — |
| `since` | optionnel | optionnel | optionnel | requis (date de retrait) |
| Fiche publiée (couche `service`) | optionnelle | requise | requise | conservée |
| Page du groupe publiée (couche `infrastructure`) | optionnelle | requise | requise | conservée |

Tout `none` se justifie. `auth.method: none`, `backup.method: none` et une supervision entièrement à `false` exigent un champ `note: {fr, en}` dans le bloc concerné (exemple : « composant sans état »).

`deploy.method: manual` est accepté et affiché tel quel : une dette d'automatisation visible est honnête.

### 6.4 `data/groups.yaml`

L'ordre de la liste est l'ordre d'affichage. La page d'un groupe d'infrastructure (FR et EN) devient obligatoire dès qu'un de ses composants passe en construction (V10).

```yaml
infrastructure:
  - {id: hardware,          label: {fr: "Matériel",                en: "Hardware"}}
  - {id: network,           label: {fr: "Réseau",                  en: "Network"}}
  - {id: virtualization,    label: {fr: "Virtualisation",          en: "Virtualization"}}
  - {id: storage-backup,    label: {fr: "Stockage et sauvegardes", en: "Storage and backup"}}
  - {id: identity-security, label: {fr: "Identité et sécurité",    en: "Identity and security"}}
  - {id: kubernetes,        label: {fr: "Kubernetes",              en: "Kubernetes"}}
  - {id: automation,        label: {fr: "Automatisation",          en: "Automation"}}
service:
  - {id: observability,     label: {fr: "Supervision",             en: "Observability"}}
  - {id: security,          label: {fr: "Sécurité",                en: "Security"}}
  - {id: platform,          label: {fr: "Plateforme",              en: "Platform"}}
  - {id: enterprise,        label: {fr: "Services d'entreprise",   en: "Enterprise services"}}
  - {id: apps,              label: {fr: "Applications",            en: "Applications"}}
```

### 6.5 `data/tags.yaml`

Le libellé est une chaîne commune aux deux langues, ou une paire `{fr, en}`.

```yaml
proxmox:    {label: "Proxmox VE"}
kubernetes: {label: "Kubernetes"}
backup:     {label: {fr: "Sauvegarde", en: "Backup"}}
```

### 6.6 `data/certifications.yaml`

```yaml
- id: ccna                     # EXEMPLE — Firmin fournit la liste réelle
  name: "Cisco CCNA"
  status: preparing            # planned | preparing | passed
  passed_on:                   # date, requise si passed
  credential_url:              # lien de vérification (Credly…), requis si passed
```

### 6.7 `data/roadmap.yaml`

```yaml
- id: foundations              # EXEMPLE — Firmin fournit les phases réelles
  title: {fr: "…", en: "…"}
  status: in-progress          # planned | in-progress | done
  started: 2026-10-12          # requis si in-progress ou done
  finished:                    # requis si done
  goals:                       # objectifs vérifiables
    - {fr: "…", en: "…"}
```

---

## 7. Modèle de contenu (`content/`)

### 7.1 Organisation

Chaque page est un dossier (page bundle) qui contient `index.fr.md`, `index.en.md` et ses images. Les sections ont leurs `_index.fr.md` et `_index.en.md`.

```
content/
├── _index.{fr,en}.md                              accueil
├── about/index.{fr,en}.md
├── infrastructure/
│   ├── _index.{fr,en}.md
│   ├── <groupe>/index.{fr,en}.md                  un dossier par groupe d'infrastructure
│   └── decisions/
│       ├── _index.{fr,en}.md
│       └── adr-0001-<slug>/index.{fr,en}.md
├── services/
│   ├── _index.{fr,en}.md
│   └── <id>/index.{fr,en}.md                      id = identifiant du catalogue
└── devlog/
    ├── _index.{fr,en}.md
    ├── 001-<slug>/index.{fr,en}.md
    └── incidents/
        ├── _index.{fr,en}.md
        └── pm-001-<slug>/index.{fr,en}.md
```

Les numéros sont complétés par des zéros : trois chiffres pour le devlog et les post-mortems, quatre pour les ADR.

### 7.2 Front matter

Front matter en YAML (`---`), comme aujourd'hui. Toute page porte `title`, `description` et `draft`. `description` fait une ou deux phrases, 160 caractères au plus ; elle sert aux listes, à la balise meta et à l'aperçu du lien sur LinkedIn.

| Type | Champs requis en plus | Champs optionnels |
|---|---|---|
| Entrée devlog | `date`, `week`, `tags` | `components`, `adrs`, `certifications` |
| Post-mortem | `date`, `pm`, `incident_date`, `severity`, `impact_minutes` | `components`, `tags` |
| ADR | `date`, `adr`, `status` | `components`, `supersedes`, `superseded_by` (requis si `superseded`), `tags` |
| Fiche service, page de groupe | — | — (les faits viennent du catalogue) |
| Accueil | `headline`, `availability` | — |
| Sections, About | — | — |

Les champs structurés sont identiques dans les deux langues (contrôle V6) : `draft`, `date`, `week`, `pm`, `adr`, `status`, `incident_date`, `severity`, `impact_minutes`, `components`, `adrs`, `certifications`, `tags`, `supersedes`, `superseded_by`. Seuls `title`, `description` et le corps diffèrent.

### 7.3 Archetypes

Des archetypes de dossier créent les deux langues en une commande :

```
archetypes/
├── devlog/index.{fr,en}.md
├── postmortem/index.{fr,en}.md
├── adr/index.{fr,en}.md
└── services/index.{fr,en}.md
```

```
hugo new content --kind devlog devlog/007-<slug>
```

Le dossier est créé avec les deux fichiers en brouillon, selon les gabarits de l'Annexe A. Les archetypes sont des templates Go : ils NE DOIVENT PAS contenir d'appel de shortcode (`{{<`), que Hugo tenterait d'interpréter. Vérifier le comportement exact (archetype de dossier, choix par `--kind`) avec la version de Hugo épinglée.

### 7.4 Liens internes

- Vers un composant : `{{< component "grafana" >}}`. Le shortcode mène à la fiche (service) ou à l'ancre de la page de groupe (infrastructure).
- Vers une ADR ou un post-mortem : `{{< adr 1 >}}`, `{{< pm 1 >}}`.
- Vers toute autre page : `[texte]({{< relref "/devlog/001-<slug>" >}})`. Une référence cassée fait échouer le build.
- Aucune URL du site écrite en dur. Les liens externes sont permis et vérifiés chaque semaine (§13.2).

### 7.5 Images

- Dans le dossier de la page, référencées en relatif, avec un texte alternatif obligatoire (V12).
- PNG, JPG, WebP ou SVG, 1 Mo au plus (contrôle CI).
- Chaque capture est relue avant commit (§10). Aucune métadonnée GPS (contrôle CI).
- Les schémas ne sont pas des images de page : ce sont des sources D2 (§11.6).

---

## 8. Bilingue

- Langues : `fr` (Français) et `en` (English), toutes deux en sous-dossier (`defaultContentLanguageInSubdir = true`). La racine redirige vers la langue par défaut (D1).
- Langue source : le français. Firmin rédige, ou donne ses notes, en français. La version anglaise est une traduction faite par Claude Code sur demande et validée par Firmin.
- Chaque page existe dans les deux langues avant fusion (V5), avec des champs structurés identiques (V6).
- Synchronisation : une PR qui modifie `index.fr.md` DOIT modifier `index.en.md`, et inversement (contrôle CI). Le label `i18n-skip` lève ce contrôle pour un changement sans effet sur l'autre langue, comme une faute de frappe ; la PR le justifie.
- Les chaînes d'interface vivent dans `i18n/fr.yaml` et `i18n/en.yaml` ; les libellés métier dans les fichiers de données (`{fr, en}`).
- Les dates sont formatées selon la langue (`:date_long`).
- La bascule de langue mène à la page traduite (surcharge existante de `header.html`, conservée).

---

## 9. Règles de rédaction

### 9.1 Qui écrit quoi

| Contenu | Rédaction | Rôle de Claude Code |
|---|---|---|
| Prose : devlog, post-mortems, ADR, fiches, pages de groupe, accueil, À propos | Firmin, en texte ou en notes | Mettre en forme à partir des notes, sur demande ; traduire ; corriger orthographe et format |
| Données : catalogue, roadmap, certifications, tags | Firmin, par ses énoncés | Transcrire en YAML ce que Firmin énonce |
| Structure : sections, archetypes, templates, CI, outillage | Claude Code | Proposer un plan, puis implémenter après accord |

### 9.2 Aucune invention

- Claude Code NE DOIT PAS ajouter un fait absent de ce que Firmin a fourni ou de ce qui est vérifiable dans le repo du lab : ni commande, ni version, ni chiffre, ni résultat, ni difficulté, ni leçon.
- Une information manque : la demander. Dans un brouillon, la marquer `TODO(firmin): <question>`. Le build refuse tout `TODO(firmin)` dans une page publiée (V11).
- `verified` et `backup.restore_tested` ne changent que sur indication explicite de Firmin.

### 9.3 Historique immuable

- Devlog : une entrée publiée n'est pas réécrite. Une faute de frappe se corrige directement ; une erreur de fond se signale par un bloc « Erratum (date) » en fin d'entrée.
- ADR acceptée : seuls `status` et `superseded_by` changent.
- Post-mortem : seul l'état des actions correctives évolue.
- Pages d'état (Infrastructure, Services, Accueil, À propos) : mises à jour en place.

### 9.4 Traduction

- Traduire le sens, pas les mots, avec la même structure : mêmes titres, même ordre, mêmes listes.
- Ne jamais traduire le code, les commandes, les identifiants, les noms de produits ni les champs structurés.
- Ne rien ajouter, ne rien retirer, ne pas « améliorer » le texte source. Signaler une ambiguïté à Firmin plutôt que la trancher.
- Les deux fichiers arrivent dans la même PR.

### 9.5 Style

Première personne. Passé composé pour ce qui a été fait. Phrases courtes, faits plutôt qu'adjectifs, aucun superlatif. En français, les termes techniques gardent leur forme anglaise quand c'est l'usage du métier (cluster, pod, playbook). Une rubrique vide est supprimée du gabarit, sauf « Réalisé » et « Semaine prochaine ».

---

## 10. Politique de publication

Le repo et le site sont publics : tout ce qui y entre doit pouvoir être lu par n'importe qui.

| Catégorie | Autorisé | Interdit |
|---|---|---|
| Réseau | Schémas logiques, plan d'adressage privé (RFC 1918), VLAN | IP publique du domicile, IPv4 comme IPv6 ; adresses du réseau VPN (100.64.0.0/10) |
| Accès distant | Le principe et l'outil (VPN maillé, aucun port ouvert) | Points d'accès, nom du tailnet, clés, règles d'accès détaillées, ports |
| Secrets | — | Tout secret, jeton, mot de passe ou clé privée, même révoqué ou « de démonstration » |
| Images | Captures relues | Métadonnées GPS ; capture montrant IP publique, jeton, e-mail, onglet ou notification personnels |
| Données personnelles | Nom, région, e-mail de contact dédié (D4), liens professionnels | Adresse postale, téléphone, date de naissance, données de tiers (famille, appareils du foyer) |
| Code et configuration | Extraits relus, sans secret ni identifiant réel | Fichiers de configuration bruts non relus |

Contrôles :

- **Automatiques**, en CI et bloquants :
  - gitleaks sur les commits de la PR ;
  - `scripts/check-publication.sh`, qui refuse :
    - les IPv4 hors plages privées et de documentation ;
    - les IPv6 globales ;
    - les noms `*.ts.net` ;
    - les adresses e-mail hors liste autorisée ;
    - les images avec coordonnées GPS ;
    - les images de plus de 1 Mo.

  Les exceptions vivent dans `.publication-allowlist`, une par ligne, avec leur justification ; chacune est validée par Firmin.
- **En revue**, pour ce qui ne s'automatise pas : Claude Code ouvre chaque image ajoutée et signale tout contenu sensible visible, puis Firmin la vérifie (définition de terminé, §14.4).
- **En cas de fuite publiée** : procédure §16.8. Un secret publié est compromis : il se révoque, on ne se contente pas de l'effacer.

---

## 11. Implémentation Hugo

### 11.1 Configuration (`hugo.toml`)

À ajouter à l'étape 1 :

- `defaultContentLanguage` selon D1 et `defaultContentLanguageInSubdir = true` ;
- `enableGitInfo = true` : date de mise à jour tirée de git. Ajouté à l'étape 0.2, en même temps que le clonage complet en CI (`fetch-depth: 0`) ;
- `refLinksErrorLevel = "ERROR"`, `enableRobotsTXT = true`, `timeZone = "Europe/Brussels"` ;
- taxonomies : `tag = "tags"`, `certification = "certifications"` ;
- aucun menu dans `hugo.toml` : les entrées sont dans le front matter des pages (§4, `docs/structure.md` §3.5) ;
- `[params]`, en plus de l'existant :
  - `ShowCodeCopyButtons`, `ShowBreadCrumbs`, `ShowPostNavLinks`, `ShowRssButtonInSectionTermList` ;
  - `socialIcons` (GitHub, LinkedIn, e-mail) ;
  - `labRepo` (D3) ;
  - `profile` : nom, e-mail de contact, chemin du CV par langue ;
  - `images` : image OpenGraph par défaut, au format PNG 1200 × 630 ;
- Markdown : garder `unsafe = false` (pas de HTML brut dans le contenu) ; le shortcode `rawhtml` de PaperMod est interdit ;
- `[privacy]` : désactiver les services tiers intégrés.

### 11.2 Templates

Nouveau système de templates (Hugo ≥ 0.146) : un dossier de `layouts/` correspond à un chemin de pages et s'applique à tout ce qu'il contient ; le fichier le plus proche l'emporte.

```
layouts/
├── home.html                              accueil (§5.1)
├── term.html                              pages de terme, libellés depuis data/ (§5.8)
├── taxonomy.html                          liste des termes (surcharge, registre §11.7)
├── about/page.html
├── infrastructure/
│   ├── section.html                       vue d'ensemble
│   ├── page.html                          page de groupe
│   └── decisions/{section,page}.html      index et page d'ADR
├── services/{section,page}.html           catalogue et fiche
├── devlog/
│   ├── section.html                       liste (inclut les post-mortems)
│   ├── page.html                          entrée hebdomadaire
│   └── incidents/{section,page}.html      post-mortems
├── _partials/
│   ├── header.html                        surcharge existante (registre §11.7)
│   ├── extend_head.html                   point d'extension PaperMod : appelle les validations (§12)
│   ├── validate/{data,page}.html
│   ├── catalog/{fiche,table,badge,link}.html
│   ├── devlog/{item,meta}.html
│   ├── profile/links.html                 CV, e-mail, GitHub, LinkedIn : accueil, À propos, contact
│   └── backlinks.html                     liens inverses (P3)
└── _shortcodes/{diagram,component,adr,pm,roadmap,certifications,contact}.html
```

Règles :

- Les templates définissent le bloc `main` et réutilisent les partials de PaperMod (`breadcrumbs`, `post_meta`, `post_nav_links`…) pour garder un rendu homogène.
- Aucun calcul dupliqué : un partial par calcul (liens inverses, compteurs, lien vers un composant), réutilisé partout.
- Vérifier la résolution des templates dans la documentation de la version de Hugo épinglée avant de créer un fichier.

### 11.3 Shortcodes

| Shortcode | Rôle | Validation |
|---|---|---|
| `component "<id>"` | Lien vers un composant, avec son badge de statut | identifiant connu |
| `adr <n>`, `pm <n>` | Lien « ADR-0007 — titre », « PM-002 — titre » | numéro existant |
| `diagram name="<nom>" alt="<texte>"` | Schéma en version claire et sombre (§11.6) | source présente, `alt` non vide |
| `roadmap`, `certifications`, `contact` | Blocs de la page À propos, depuis les données et `hugo.toml` | — |

Le shortcode `component` et la liste des composants d'une entrée ne créent un lien que si la page cible (fiche ou page de groupe) est publiée. Sinon, ils affichent le nom et le badge sans lien. Aucun lien ne mène donc à une page absente, quel que soit l'ordre dans lequel le contenu arrive.

### 11.4 Chaînes d'interface

`i18n/fr.yaml` et `i18n/en.yaml` contiennent toutes les chaînes d'interface : statuts, valeurs des énumérations, intitulés de la fiche technique, boutons, numéros de semaine (« S%02d » / « W%02d »). Aucun texte écrit en dur dans un template.

### 11.5 CSS

Un seul fichier, `assets/css/extended/site.css`, que PaperMod ajoute après son propre CSS. Il utilise les variables du thème (`--primary`, `--secondary`, `--tertiary`, `--entry`, `--border`, `--code-bg`) pour fonctionner en clair comme en sombre. Un badge de statut porte toujours son texte, jamais la seule couleur. Aucun framework CSS.

### 11.6 Schémas

- Source en D2 (`assets/diagrams/<nom>.d2`), version épinglée (§13.1). Rendu en deux SVG commités à côté de la source, `<nom>.light.svg` et `<nom>.dark.svg`, pour qu'ils apparaissent dans le diff des PR.
- Rendu par `scripts/render-diagrams.sh`. La CI refait le rendu et échoue si les SVG commités diffèrent. Si le rendu n'est pas reproductible à l'octet près, le contrôle se limite à « rendu sans erreur et deux SVG présents », et ce document est mis à jour.
- Affichage : le shortcode `diagram` produit les deux images ; le CSS montre la bonne selon `html[data-theme]`, sans JavaScript. Le texte alternatif est obligatoire.
- Vue logique uniquement (§10).
- Premier schéma : `lab-overview`, sur l'accueil et sur la page Infrastructure.

### 11.7 Registre des surcharges du thème

| Fichier du site | Nature | Raison | À chaque mise à jour de PaperMod |
|---|---|---|---|
| `layouts/_partials/header.html` | Surcharge | Bascule de langue vers la page traduite (`.Translations`) plutôt que vers l'accueil | Comparer l'ancienne et la nouvelle version du `header.html` du thème ; reporter les changements |
| `layouts/taxonomy.html` | Surcharge | Libellés des termes depuis `data/` | Idem avec `taxonomy.html` |
| `layouts/_partials/extend_head.html` | Point d'extension prévu par le thème | Appel des validations | Vérifier qu'il est toujours inclus par `head.html` |

---

## 12. Validation au build

Les contrôles vivent dans `layouts/_partials/validate/`. `extend_head.html` les appelle : validation des données une seule fois par build (`partialCached`), validation de chaque page à son rendu. Les erreurs passent par `errorf`, les avertissements par `warnf`. Les messages sont en français, préfixés par le chemin du fichier, et donnent les valeurs attendues. Pour comparer des listes entre deux langues, comparer leurs formes sérialisées (`jsonify`).

| # | Contrôle | Niveau |
|---|---|---|
| V1 | Chaque fichier du catalogue respecte le schéma (§6.2) et les exigences de son statut (§6.3) | erreur |
| V2 | `exposure` vaut `internal` ou `vpn` | erreur |
| V3 | Les identifiants référencés existent : `runtime.host`, `depends_on`, `components`, shortcodes | erreur |
| V4 | `groups`, `tags`, `certifications`, `roadmap` : champs requis, valeurs autorisées, libellés en FR et en EN | erreur |
| V5 | Toute page publiée existe dans les deux langues | erreur |
| V6 | Champs structurés identiques en FR et en EN (§7.2) | erreur |
| V7 | `week`, `pm` et `adr` correspondent au préfixe du dossier, sont uniques et sans trou | erreur |
| V8 | Front matter requis selon le type (§7.2) ; champ `slug` absent | erreur |
| V9 | Un service `building` ou `running` a une fiche publiée ; toute fiche correspond à un service du catalogue | erreur |
| V10 | Toute page de groupe correspond à un groupe d'infrastructure déclaré ; un groupe qui contient un composant `building` ou `running` a sa page publiée | erreur |
| V11 | Aucun `TODO(firmin)` dans une page publiée | erreur |
| V12 | Toute image a un texte alternatif | erreur |
| V13 | Une ADR `superseded` a un `superseded_by` existant | erreur |
| V14 | Un composant en service non vérifié depuis plus de 60 jours | avertissement |
| V15 | `tags` et `certifications` appartiennent au vocabulaire | erreur |
| V16 | `description` dépasse 160 caractères | avertissement |

Les brouillons ne sont pas construits en production et ne sont donc pas validés : la CI construit sans `-D`.

Tests des validations (DEVRAIT) : `tests/validation/<cas>/` décrit, pour chaque règle, les fichiers ajoutés, modifiés ou supprimés, et le message attendu. `scripts/test-validation.sh` applique chaque cas à une copie temporaire du repo et vérifie que le build échoue avec ce message. Un cas de référence, valide, doit passer. Ces tests tournent en CI.

---

## 13. CI/CD et outillage

### 13.1 Versions

- Une seule source : `tools.env` (`HUGO_VERSION`, `D2_VERSION`, `GITLEAKS_VERSION`, `LYCHEE_VERSION`).
- `scripts/install-tools.sh` installe ces versions dans `.bin/` (ignoré par git). Il détecte le système (Linux en CI, poste de Firmin) et vérifie chaque archive contre la somme SHA-256 publiée.
- En local comme en CI, les scripts utilisent `.bin/`.
- `exiftool` vient du gestionnaire de paquets (apt en CI, Homebrew en local).

### 13.2 Workflows

| Fichier | Déclencheur | Rôle |
|---|---|---|
| `build.yml` | `workflow_call` | Build réutilisable : clone avec submodules et `fetch-depth: 0`, `install-tools.sh`, `hugo --minify --gc --printPathWarnings` (donc validations), présence de `public/404.html`, `public/` publié comme artefact |
| `ci.yml` | `pull_request` vers `main` | `build` ; `links` (lychee hors ligne sur `public/`, ancres comprises) ; `publication` (gitleaks sur les commits de la PR, `check-publication.sh`) ; `i18n-sync` (sauf label `i18n-skip`) ; `diagrams` ; `validation-tests` |
| `pages.yml` | push sur `main`, manuel | `build` puis déploiement Pages (workflow existant, durci) |
| `links-external.yml` | hebdomadaire, manuel | lychee en ligne sur les liens externes ; un échec déclenche la notification GitHub |
| `availability.yml` | toutes les heures, manuel | Vérifie que le site répond (HTTP 200, certificat valide) depuis l'extérieur du lab ; un échec déclenche la notification GitHub (§16.9) |

Chaque job arrive avec l'étape du §15 qui en a besoin.

PaperMod produit des liens absolus (`baseURL`). Pour la vérification hors ligne, construire avec une `baseURL` locale ou utiliser le remappage de lychee ; sinon les liens internes ne sont pas vérifiés.

### 13.3 Règles pour les workflows

- Actions épinglées par SHA, avec la version en commentaire.
- `permissions` minimales : `contents: read` par défaut ; `pages: write` et `id-token: write` pour le seul job de déploiement.
- Tout binaire téléchargé est vérifié par somme de contrôle.
- `concurrency` annule les exécutions obsolètes d'une même PR.
- Dependabot (`.github/dependabot.yml`), chaque semaine : écosystèmes `github-actions` et `gitsubmodule` (PaperMod). Hugo, D2, gitleaks et lychee se mettent à jour à la main, chaque mois (§16.5).
- Modèle de PR (`.github/pull_request_template.md`) : la définition de terminé (§14.4) sous forme de cases à cocher.

### 13.4 En local

- `.githooks/pre-commit` lance gitleaks sur les fichiers indexés et `check-publication.sh`. `scripts/setup-hooks.sh` l'active une fois par clone (`git config core.hooksPath .githooks`).
- Le hook est un confort ; la barrière reste la CI. `--no-verify` (ou `-n`) est interdit.

### 13.5 Réglages GitHub (à faire par Firmin)

- Ruleset sur `main` : PR obligatoire, jobs de `ci.yml` exigés, force-push et suppression bloqués.
- Pages : HTTPS forcé ; domaine vérifié dans les réglages du compte GitHub, ce qui empêche sa prise de contrôle par un tiers.
- Secret scanning et push protection activés (gratuits pour un repo public).
- Alertes Dependabot activées.

---

## 14. Gouvernance de Claude Code

### 14.1 Couches d'instructions

| Fichier | Contenu | Chargé |
|---|---|---|
| `CLAUDE.md` | Invariants, commandes, workflow git, définition de terminé, renvois vers ce document. Moins de 200 lignes. | À chaque session |
| `.claude/rules/content.md` (`paths: content/**, data/**, archetypes/**, static/cv/**`) | §6, §7, §9 et §10, en consignes courtes | Quand Claude Code touche ces fichiers |
| `.claude/rules/templates.md` (`paths: layouts/**, assets/**, i18n/**, hugo.toml`) | §11 et §12, en consignes courtes | Idem |
| `.claude/rules/ci.md` (`paths: .github/**, scripts/**, tools.env, .githooks/**, tests/**`) | §13, en consignes courtes | Idem |
| `.claude/skills/<nom>/SKILL.md` | Procédures du §16 | Quand Firmin les invoque |
| `docs/architecture.md` | Ce document | À la demande |

Les fichiers de règles donnent des consignes impératives courtes, chacune avec son renvoi (§). Ils ne contredisent jamais ce document.

### 14.2 Skills

Toutes portent `disable-model-invocation: true` : c'est Firmin qui les déclenche. Avant leur création (phase 6), Claude Code suit directement les procédures du §16.

| Skill | Usage | Procédure |
|---|---|---|
| `/devlog` | Entrée hebdomadaire : numéro suivant calculé, slug proposé | §16.1 |
| `/component <id>` | Ajouter un composant ou le faire évoluer | §16.2 |
| `/adr <slug>` | Nouvelle décision | §16.3 |
| `/postmortem <slug>` | Nouvel incident | §16.4 |
| `/translate <chemin>` | Traduire une page de FR vers EN | §9.4 |
| `/linkedin <n>` | Brouillon du post LinkedIn de la semaine n | §16.1 |

### 14.3 Permissions (`.claude/settings.json`)

- **Autorisé** : build et scripts du repo (`.bin/*`, `scripts/*`), lecture et workflow git sur branche (`status`, `diff`, `log`, `add`, `commit`, `switch`, `checkout`), `gh pr create`, `gh pr view`, `gh run list`, `gh run view`.
- **Interdit** : `gh pr merge`, `git push --force`, push direct sur `main`, toute modification des réglages GitHub (`gh repo edit`, `gh secret`, `gh api` en écriture).
- Les règles de permission filtrent les commandes par préfixe : elles ne distinguent pas une lecture d'une écriture par `gh api`. `gh api` est donc refusé en bloc. `git push` sans option n'est ni autorisé ni interdit : il demande confirmation à chaque fois.

### 14.4 Définition de terminé (toute PR)

1. Firmin a validé le plan avant toute écriture.
2. `hugo --minify` passe sans erreur ni nouvel avertissement.
3. `scripts/check-publication.sh` passe.
4. FR et EN sont à jour, ou le label `i18n-skip` est justifié.
5. Chaque image ajoutée a été ouverte et vérifiée (§10).
6. Revue visuelle par Firmin : Claude Code lance `hugo server` et donne la liste des pages à regarder, en FR et en EN, en thème clair et sombre.
7. Ce document est à jour si la structure change, journal compris (§17.2).
8. Branche poussée. La PR n'est ouverte qu'avec l'accord de Firmin ; Claude Code ne fusionne jamais.

---

## 15. Plan d'implémentation

Les phases se suivent dans l'ordre. Chaque étape est une branche et une PR ; son plan est présenté et validé avant toute écriture. Chaque fusion laisse le site publiable, puisque `main` est déployée.

Ordre retenu le 14/10/2026 : 0.1, puis la phase 1 (la structure, détaillée dans `docs/structure.md` §7), puis 0.2 à 0.4. Tant que la CI n'existe pas, `hugo --minify` exécuté en local fait office de contrôle (§14.4).

En attendant la phase 3, Firmin consigne ses notes de chaque semaine. Elles deviendront, dans l'ordre, les premières entrées du devlog, datées de leur semaine. La semaine S1 (12–18 octobre 2026) est celle de la planification. Le calendrier commun au site et au lab est au §15 du plan du lab.

### Phase 0 — Fondations

| Étape | Branche | Contenu | Critères d'acceptation |
|---|---|---|---|
| 0.1 | `docs/architecture` | Ce document (statut « validé ») ; `docs/structure.md` ; `CLAUDE.md` tiré de l'Annexe B, puis l'annexe retirée de ce document ; `.claude/rules/` ; `.claude/settings.json` (§14.3) | `CLAUDE.md` sous 200 lignes ; aucune contradiction entre les fichiers |
| 0.2 | `chore/ci-pipeline` | `tools.env`, `install-tools.sh`, `build.yml`, `ci.yml` (jobs `build`, `links` et `i18n-sync`), `pages.yml` durci (clonage complet, `enableGitInfo`), Dependabot, modèle de PR | CI verte sur la PR ; déploiement inchangé après fusion ; actions épinglées par SHA ; même version de Hugo en local et en CI ; un lien interne cassé fait échouer `links` ; une PR qui ne modifie qu'une langue échoue |
| 0.3 | `chore/publication-checks` | gitleaks, `check-publication.sh`, `.publication-allowlist`, hook pre-commit, job `publication` | Sur une branche jetable, une IP publique, un faux jeton et une image géolocalisée font échouer la CI |
| 0.4 | `chore/cleanup` | Selon D5 | Site identique avant et après |
| — | Firmin | Réglages GitHub (§13.5) | Fusion impossible sans CI verte |

### Phase 1 — Structure

| Étape | Branche | Contenu | Critères d'acceptation |
|---|---|---|---|
| 1.1 | `feat/i18n-subdirs` | Langues en sous-dossier, redirection de la racine (D1), redirections des anciennes URL par fichiers `static/` (`docs/structure.md` §3.6) | `/` et chaque ancienne URL redirigent ; le sélecteur de langue mène à la page traduite ; présence de `public/404.html` vérifiée |
| 1.2 | `feat/sections` | Arborescence complète de `docs/structure.md` (sections et pages de groupe en brouillon) ; menus dans le front matter ; pages existantes converties en dossiers (C5) ; `journal` et `projects` retirés, anciennes URL redirigées ; ancien article selon D2 ; ajouts à `hugo.toml` (§11.1) | Build vert. En production, seules les pages publiées et leurs entrées de menu existent. Avec `-D`, toute l'arborescence est navigable |
| 1.3 | `feat/archetypes` | Archetypes (Annexe A) | `hugo new content --kind …` crée FR et EN en brouillon, conformes aux gabarits |

### Phase 2 — Données et validation

| Étape | Branche | Contenu | Critères d'acceptation |
|---|---|---|---|
| 2.1 | `feat/data-model` | Fichiers `data/` (groupes ; vocabulaires vides ou fournis par Firmin), chaînes i18n de base, `validate/data.html` (V1 à V4, V14), tests et job `validation-tests` | Chaque règle a un cas de test qui échoue avec le message attendu |
| 2.2 | `feat/page-validation` | `validate/page.html` (V5 à V13, V15, V16), tests | Idem |

### Phase 3 — Historique : devlog, incidents, ADR (débloque la publication hebdomadaire)

| Étape | Branche | Contenu | Critères d'acceptation |
|---|---|---|---|
| 3.1 | `feat/devlog-templates` | Templates devlog et incidents, partials `devlog/*`, `backlinks`, shortcodes `component`, `adr`, `pm`, CSS, image OpenGraph par défaut | Revue visuelle en FR et EN, thèmes clair et sombre, largeur mobile ; liens inverses corrects ; un composant sans page publiée s'affiche sans lien |
| 3.2 | `feat/adr-templates` | Templates decisions | Bandeau « remplacée par » ; liens inverses |
| 3.3 | `docs/devlog-001` | Premières entrées (Firmin), leurs ADR, les composants qu'elles citent (avec fiche ou page de groupe si V9 ou V10 l'exige), entrée Devlog au menu | Entrées publiées ; aperçu LinkedIn correct (titre, description, image) ; aucun fait inventé |

Jusqu'à la phase 4, les fiches et les pages de groupe exigées par V9 et V10 s'affichent avec le template par défaut de PaperMod : leur prose est en ligne, leur fiche technique arrive en 4.1. Infrastructure et Services n'entrent au menu qu'en 4.2.

### Phase 4 — État : catalogue

| Étape | Branche | Contenu | Critères d'acceptation |
|---|---|---|---|
| 4.1 | `feat/catalog-templates` | Partials `catalog/*`, templates services et infrastructure | Revue visuelle ; les exigences par statut s'affichent comme prévu (« restauration non testée », notes des `none`) |
| 4.2 | `docs/catalog-initial` | Reste du catalogue (Firmin), prose des pages de groupe, entrées Infrastructure et Services au menu | Build vert ; aucun composant inventé |

### Phase 5 — Accueil, À propos, schémas

| Étape | Branche | Contenu | Critères d'acceptation |
|---|---|---|---|
| 5.1 | `feat/diagrams` | D2 dans `tools.env`, `render-diagrams.sh`, job `diagrams`, shortcode `diagram`, schéma `lab-overview` décrit par Firmin | Bon schéma selon le thème ; CI rouge si un SVG est périmé |
| 5.2 | `feat/home-about` | `home.html`, page About, shortcodes `roadmap`, `certifications`, `contact`, templates de taxonomie | Accueil lisible en un écran sur desktop ; libellés des tags corrects |
| 5.3 | `docs/about-home` | Textes de Firmin, CV, contacts (D4), certifications, roadmap | Aucun champ provisoire publié |

### Phase 6 — Outillage de maintenance

| Étape | Branche | Contenu | Critères d'acceptation |
|---|---|---|---|
| 6.1 | `chore/skills` | `.claude/skills/` (§14.2) | Chaque skill déroulée une fois à blanc, sans commit |
| 6.2 | `chore/external-checks` | `links-external.yml`, `availability.yml` | Exécutions manuelles vertes ; un site injoignable (URL de test) fait échouer `availability.yml` |

---

## 16. Procédures de maintenance

### 16.1 Chaque semaine : l'entrée devlog (`/devlog`, puis `/linkedin`)

1. Firmin donne ses notes de la semaine : ce qui a été fait, les problèmes, les décisions, les changements de statut, les incidents.
2. Claude Code présente son plan : numéro (le suivant), slug, composants, ADR et tags concernés, modifications du catalogue, ADR ou post-mortem à créer.
3. Après accord :
   - créer la branche `docs/devlog-<nnn>` et le dossier depuis l'archetype ;
   - mettre en forme l'entrée française à partir des notes, sans rien ajouter (les questions deviennent des `TODO(firmin)`) ;
   - mettre à jour le catalogue ;
   - créer les ADR et post-mortems éventuels (§16.3, §16.4) ;
   - traduire en anglais.
4. Contrôles : `hugo --minify`, `check-publication.sh`, inspection des images.
5. `hugo server` : Claude Code donne à Firmin les URL de l'entrée et des pages modifiées, en FR et en EN.
6. Après validation : commits, push, accord de Firmin avant d'ouvrir la PR, CI verte. Firmin fusionne et le site est déployé.
7. LinkedIn : Claude Code propose un brouillon tiré de l'entrée, dans la langue choisie par Firmin. Trois à cinq lignes : un résultat concret, un problème résolu, le lien. Aucun fait absent de l'entrée. Firmin vérifie l'aperçu du lien avec le Post Inspector de LinkedIn, puis publie lui-même.

### 16.2 Cycle de vie d'un composant (`/component`)

- **Nouveau** : entrée `planned` avec les champs minimaux.
- **Passage à `building`** : `runtime`, `deploy`, `exposure`, `auth`, `verified` ; pour un service, création de la fiche (archetype `services`).
- **Passage à `running`** : `backup`, `monitoring`, `since`, `verified`. Le build refuse le statut s'il manque une réponse.
- **Test de restauration réussi** : `backup.restore_tested`, sur indication de Firmin.
- **Retrait** : statut `retired` et `since`. La fiche reste en ligne, puisqu'elle fait partie de l'histoire du lab ; le composant sort du schéma.
- **Changement de topologie** (hôte, dépendances, réseau) : le schéma `lab-overview` est mis à jour dans la même PR.
- Toute évolution est mentionnée dans l'entrée devlog de la semaine.

### 16.3 Décision (`/adr`)

Numéro suivant. Statut `proposed` ou `accepted`. Firmin fournit le contexte, les options, la décision et les conséquences ; Claude Code met en forme et relie les composants. Si la nouvelle ADR en remplace une, l'ancienne est mise à jour dans la même PR (`status`, `superseded_by`).

### 16.4 Incident (`/postmortem`)

Rédigé dans la semaine de l'incident, à partir de la chronologie et des faits fournis par Firmin. Les actions correctives prennent la forme d'une liste de cases à cocher. L'entrée devlog de la semaine y renvoie. L'état des actions est mis à jour ensuite, au fil de leur réalisation.

### 16.5 Chaque mois (première semaine)

- Composants non vérifiés depuis plus de 60 jours (avertissements V14) : les revoir avec Firmin et mettre à jour `verified`.
- PR Dependabot : actions ; PaperMod selon le §16.6.
- Rapport des liens externes.
- Versions des outils (Hugo, D2, gitleaks, lychee) : lire les notes de version, mettre à jour `tools.env`, vérifier que le build ne produit aucun nouvel avertissement.

### 16.6 Mise à jour de PaperMod

1. Lire les commits du thème depuis le commit épinglé : changements incompatibles, version minimale de Hugo.
2. Pour chaque fichier du registre (§11.7), comparer l'ancienne et la nouvelle version du thème et reporter les changements dans la surcharge.
3. Build, revue visuelle (deux langues, deux thèmes), fusion.

### 16.7 Changement d'architecture

Sections, schémas, validations, CI, outillage : mise à jour de ce document et ligne au journal (§17.2) dans la même PR. Si des URL changent, redirections.

### 16.8 Fuite publiée

1. Révoquer ou changer immédiatement ce qui a fui (secret, clé, accès). Réécrire l'historique git ne suffit pas : forks, caches et archives en gardent une copie.
2. Retirer l'élément du site et du repo.
3. Rédiger un post-mortem.

### 16.9 Exploitation hors du repo

Le site dépend de comptes et de services extérieurs au repo. C'est là qu'est sa vraie surface d'attaque.

- **Comptes** (GitHub, Cloudflare comme registraire et DNS, Proton pour la messagerie du domaine, LinkedIn) :
  - second facteur fort : clé d'accès ou clé matérielle ;
  - codes de secours dans le gestionnaire de mots de passe et sur papier ;
  - aucune session ouverte sur un appareil partagé.
- **Domaine.** Renouvellement automatique activé, verrou de transfert, moyen de paiement à jour. Une expiration couperait à la fois le site et la messagerie professionnelle.
- **DNS.**
  - DNSSEC activé.
  - Enregistrements CAA limités aux autorités utilisées : Let's Encrypt pour GitHub Pages.
  - SPF, DKIM et DMARC vérifiés. DMARC passe en `quarantine`, puis en `reject` une fois les rapports propres.
  - Enregistrements inventoriés, puis gérés en code dans le repo du lab : Terraform, après un import dont le plan ne propose aucun changement.
- **Disponibilité.** Deux sondes :
  - interne : la supervision du lab vérifie la réponse HTTP et l'expiration du certificat ;
  - externe et indépendante du lab : `availability.yml` (§13.2).
- **Revue annuelle, en janvier.** Comptes et seconds facteurs, jetons et leur portée, date de renouvellement du domaine, enregistrements DNS, règles de protection de `main`, secrets du repo GitHub (il ne doit y en avoir aucun).
- **Incident.** Site injoignable, domaine ou compte compromis :
  1. révoquer les sessions et les jetons, changer les mots de passe ;
  2. vérifier les enregistrements DNS et les membres du repo ;
  3. rédiger un post-mortem.

---

## 17. Décisions

### 17.1 Ouvertes (Firmin tranche)

| # | Question | Recommandation | Bloque |
|---|---|---|---|
| D1 | Vers quelle langue redirige `/` : `fr` ou `en` ? | `en` : un recruteur non francophone ne lit pas une page en français, alors que l'inverse est rare dans l'IT. Ce choix reste réversible sans casser de lien (C2). | 1.1 |
| D2 | Que faire de l'article `proxmox-homelab-premiers-pas` (lab d'avant la reconstruction) : le supprimer ou l'archiver ? | Le supprimer et expliquer la reconstruction dans « Le projet ». L'article décrit des VM exposées directement sur le réseau local, à l'opposé de la posture visée. | 1.2 |
| D3 | Repo du lab : nom, public ou privé ? | `FirminMoyen/homelab`, public, avec les secrets chiffrés (SOPS/age) : les fiches peuvent alors pointer vers le code (plan du lab, LD9). En attendant, `deploy.code` reste vide. | Liens « code » des fiches |
| D4 | Contact public : adresse principale ou alias dédié ? | Un alias dédié sur le domaine, remplaçable en cas de spam. CV public sans adresse, téléphone ni date de naissance. | 5.3 |
| D5 | Supprimer `layouts-maison/` et `assets/css/main.css` ? | Oui : l'historique git les conserve. | 0.4 |

### 17.2 Journal des décisions du site

| Date | Décision | Référence |
|---|---|---|
| 2026-10-12 | Sections accueil, infrastructure, services, devlog, about ; ADR sous infrastructure ; catalogue en données | Échange de cadrage |
| 2026-10-14 | Architecture v0.1 (ce document) | PR de l'étape 0.1 |
| 2026-10-14 | v0.2 : exploitation hors du repo (§16.9), sonde de disponibilité externe, repo du lab proposé (D3), lien vers le calendrier commun | Plan du lab |
| 2026-10-14 | v0.3 : structure page par page (`docs/structure.md`) ; menus dans le front matter et sections en brouillon tant qu'elles sont vides ; redirections par fichiers `static/` ; ordre du jour : 0.1, puis phase 1, puis 0.2 à 0.4 | `docs/structure.md` |
| 2026-10-14 | v0.3 validée et commitée ; annexe B retirée (`CLAUDE.md` devient la source) ; `.claude/rules/` et permissions (§14.3, précisions sur `gh api` et `git push`) ; tableau du §11.3 corrigé ; `docs/structure.md` v0.1 ajouté | PR de l'étape 0.1 |

---

## 18. Hors périmètre, pour plus tard

- **Catalogue généré depuis le repo du lab.** Le schéma du §6.2 est le contrat : le lab produirait `data/catalog/` et le site le consommerait au build.
- **Schéma généré depuis le catalogue** (`runtime.host`, `depends_on`).
- **Images OpenGraph par entrée**, générées par le traitement d'images de Hugo.
- **Recherche** (fonction intégrée à PaperMod), si le nombre d'entrées le justifie.
- **En-têtes de sécurité** (CSP, HSTS) : impossibles à définir sur GitHub Pages. Il faudrait passer par un proxy Cloudflare ou par un autre hébergeur ; à décider plus tard.
- **Mesure d'audience** sans cookie.
- **Commits signés.**

---

## Annexe A — Gabarits

Les gabarits ci-dessous montrent les fichiers tels que l'archetype les crée. L'archetype remplit la date et met `draft: true`. Les commentaires HTML guident la rédaction ; ils restent invisibles sur le site.

### A.1 Entrée devlog — `devlog/<nnn>-<slug>/index.fr.md`

```markdown
---
title: ""
date: 2026-10-18
draft: true
description: ""
week: 1
components: []
adrs: []
tags: []
certifications: []
---

## Objectif de la semaine

## Réalisé

## Problèmes et résolution
<!-- Pour chaque problème : symptôme, diagnostic, cause, solution. -->

## Décisions
<!-- Une phrase par décision, avec le lien vers son ADR. -->

## Appris

## Semaine prochaine
```

Rubriques en anglais : Goal of the week, Done, Problems and fixes, Decisions, Learned, Next week.

### A.2 Post-mortem — `devlog/incidents/pm-<nnn>-<slug>/index.fr.md`

```markdown
---
title: ""
date: 2026-11-05
draft: true
description: ""
pm: 1
incident_date: 2026-11-03
severity: sev3
impact_minutes: 0
components: []
tags: []
---

## Résumé

## Impact
<!-- Ce qui ne fonctionnait plus, pendant combien de temps, données perdues ou non. -->

## Chronologie

| Heure | Événement |
|---|---|

## Détection
<!-- Comment l'incident a été remarqué, et ce qui aurait permis de le voir plus tôt. -->

## Cause racine

## Résolution

## Actions correctives
- [ ] Action — échéance

## Ce que j'en retiens
```

Rubriques en anglais : Summary, Impact, Timeline, Detection, Root cause, Resolution, Corrective actions, Takeaways.

### A.3 ADR — `infrastructure/decisions/adr-<nnnn>-<slug>/index.fr.md`

```markdown
---
title: ""
date: 2026-10-20
draft: true
description: ""
adr: 1
status: proposed
components: []
supersedes:
superseded_by:
tags: []
---

## Contexte
<!-- Le problème à résoudre et les contraintes : matériel, budget, sécurité, temps. -->

## Options considérées

### Option 1 — …
<!-- Avantages, inconvénients. -->

### Option 2 — …

## Décision

## Conséquences
<!-- Positives, négatives, ce qu'il faudra surveiller ou réexaminer. -->
```

Rubriques en anglais : Context, Options considered, Decision, Consequences.

### A.4 Fiche service — `services/<id>/index.fr.md`

La fiche technique vient du catalogue ; la page ne contient que la prose.

```markdown
---
title: ""
draft: true
description: ""
---

## Pourquoi
<!-- Le besoin auquel ce service répond, et pourquoi celui-ci plutôt qu'un autre (lien ADR s'il existe). -->

## Mise en œuvre

## Exploitation
<!-- Mises à jour, sauvegarde et restauration, supervision : ce que la fiche technique ne dit pas. -->

## Limites et évolutions
```

Rubriques en anglais : Why, Implementation, Operations, Limits and next steps. Les pages de groupe d'infrastructure suivent la même trame, avec « Rôle dans le lab » à la place de « Pourquoi ».
