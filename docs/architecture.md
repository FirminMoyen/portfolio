# Architecture du site firminmoyen.dev

| | |
|---|---|
| Statut | Validé (v0.3), 14 octobre 2026 ; mis à jour le 29 octobre 2026 (refonte « regard recruteur », §17.2) |
| Date | 14 octobre 2026 |
| Emplacement | `docs/architecture.md` du repo `FirminMoyen/portfolio` |
| Lecteurs | Claude Code (implémente et maintient), Firmin (valide), visiteurs du repo : ce document est public |
| Documents liés | Structure page par page : `docs/structure.md` (pages, URL, menus, blocs, redirections). Architecture et plan du lab (`docs/architecture.md` du repo `homelab`) : calendrier commun (§15 de ce plan), contenu du catalogue, ADR prévues. Règles opérationnelles : `CLAUDE.md` et `.claude/rules/` |

## Résumé

Le site présente un homelab reconstruit de zéro et documenté chaque semaine. Il doit permettre à Firmin d'être repéré pour un poste en administration systèmes et infrastructure. Il sépare deux natures de contenu :

- **l'état actuel du lab** : Infrastructure et Services, des pages mises à jour en place et générées depuis un catalogue de données unique (`data/catalog/`) ;
- **le chemin parcouru** : Journal (une entrée par semaine), post-mortems et décisions d'architecture (ADR), des entrées datées qu'on ne réécrit pas.

L'Accueil (le projet : présentation, ligne d'identité avec boutons CV et contact, schéma du lab, stack, dernières entrées du journal), la page Le projet (pourquoi, où il en est, où il va, le cadre), la page À propos de moi (l'auteur : profil, parcours en récit, homelab, façon de travailler, ce qu'il cherche, contact) et la page CV (la référence factuelle : compétences, dates, missions, formation, certifications) complètent l'ensemble. Le site est bilingue FR/EN et statique (Hugo + PaperMod sur GitHub Pages), sans JavaScript propre. Il se valide lui-même : le build Hugo échoue si une donnée est incohérente, une traduction manquante ou une référence cassée. La CI ajoute les contrôles que Hugo ne peut pas faire : secrets, adresses IP, métadonnées d'images, synchronisation des traductions.

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
- Une étape à la fois : Claude Code ne prend pas d'avance sur l'étape suivante.
- Une session de travail = une branche, qui peut couvrir plusieurs étapes du §15. Un commit à chaque changement ; PR en fin de session, sur demande de Firmin.
- Commits petits, en Conventional Commits. Workflow git : §14 et `CLAUDE.md`.

### 0.4 Première action

Lire ce document en entier, puis présenter le plan de l'étape 0.1 (§15) sans écrire de fichier. Chaque décision ouverte (§17.1) est posée à Firmin au moment de l'étape qu'elle bloque, pas avant.

### 0.5 Tenir ce document à jour

Une PR qui modifie la structure (sections, schémas de données, règles de validation, CI, outillage, gouvernance) DOIT mettre à jour ce document dans la même PR et ajouter une ligne à l'historique des décisions (§17.2).

---

## 1. Contexte et objectifs

### 1.1 Le projet

Firmin reconstruit son homelab de zéro, avec le matériel qu'il possède déjà et sans budget. Le lab lui sert à apprendre, à préparer des certifications (CCNA, Red Hat, Terraform, Ansible, Kubernetes) et à démontrer des pratiques d'exploitation conformes aux standards du métier : sécurité, maintenance, disponibilité. Rien n'y est exposé sur Internet.

Le site est la vitrine de ce travail. Chaque semaine, Firmin le met à jour et publie un post LinkedIn qui renvoie vers l'entrée du journal.

### 1.2 Publics

| Public | Temps | Ce qu'il cherche | Parcours type |
|---|---|---|---|
| Recruteur | moins d'une minute | Qui, quel poste, quel niveau, preuve d'activité, contact | Accueil → À propos de moi → CV ou contact |
| Responsable technique, ingénieur | 5 à 15 minutes | Rigueur, raisonnement, capacité d'exploitation | Accueil → Infrastructure → fiche → ADR → journal ou post-mortem → code |
| Firmin | — | La référence de son propre lab | Toutes les sections |

### 1.3 Critères de réussite

- Sur l'accueil, en un écran (desktop), un recruteur comprend le profil et voit le lab.
- Chaque affirmation technique est datée et vérifiable : lien vers le code, l'entrée du journal ou l'ADR.
- La mise à jour hebdomadaire coûte peu : Firmin donne ses notes, valide, fusionne. Les archetypes et les procédures guident le reste ; le build et la CI le contrôlent.

---

## 2. Principes d'architecture

- **P1 — L'état n'est pas l'historique.** Infrastructure et Services décrivent l'état actuel et se modifient en place. Journal, post-mortems et ADR forment l'historique : datés, jamais réécrits (§9.3).
- **P2 — Une seule source par fait.** Le statut, l'emplacement, le mode de déploiement, la sauvegarde et la supervision d'un composant n'existent que dans `data/catalog/<id>.yaml`. Les templates les affichent. La prose peut citer les faits importants (modèle d'une machine, nombre de nœuds, version…) pour rester lisible, à condition de rester cohérente avec le catalogue, qui reste la source de vérité des statuts (décision de Firmin du 28/10/2026).
- **P3 — Liens déclarés d'un côté, calculés de l'autre.** Une entrée du journal déclare les composants et les ADR qu'elle concerne. Les fiches et les ADR affichent les liens inverses, calculés au build.
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
| C1 | Sections | journal, projects, about | accueil, infrastructure (+ decisions), services, journal (+ incidents), about | Architecture convenue le 12/10/2026 |
| C2 | URL | FR à la racine, EN sous `/en/` | FR sous `/fr/`, EN sous `/en/` ; la racine redirige vers la langue par défaut | La langue par défaut peut changer sans casser un seul lien (D1) |
| C3 | Ancien contenu | `journal/proxmox-homelab-premiers-pas` | Selon D2 ; `/journal/` redirige vers la nouvelle section Journal | Le lab décrit n'existe plus |
| C4 | Slugs | `slug` anglais différent autorisé | Même slug dans les deux langues, champ `slug` interdit | Appariement et liens prévisibles, contrôle simple |
| C5 | Organisation | Un fichier par langue | Un dossier par page (page bundle) : `index.fr.md`, `index.en.md`, images | Les images vivent avec leur page ; un archetype crée FR et EN d'une commande |
| C6 | CSS | `assets/css/main.css`, non chargé | `assets/css/extended/site.css` | C'est l'emplacement que PaperMod assemble après son propre CSS |
| C7 | JavaScript | « Aucun JavaScript côté client » | Aucun JavaScript écrit pour le site ; fonctions PaperMod activées par paramètre permises | PaperMod embarque déjà du JS (bascule de thème) |
| C8 | Règle sur `content/` | « Ne jamais créer de contenu dans content/ » | Claude Code crée la structure et rédige la prose à partir des faits fournis par Firmin ou vérifiables dans le repo du lab, sous la validation de Firmin (décision du 28/10/2026 ; à l'origine, il mettait seulement en forme) ; il n'invente aucun fait (§9) | Permet l'échafaudage, la traduction, les fiches et une prose lisible par un recruteur |
| C9 | CI | Déploiement seulement | CI sur PR (build, liens, publication, traductions, diagrammes), déploiement durci, Dependabot | Faire de la CI la barrière, conformément aux conventions de Firmin |
| C10 | Nettoyage | `layouts-maison/`, `assets/css/main.css` | Suppression (D5) | Inutilisés ; l'historique git les conserve |
| C11 | Gouvernance | Un `CLAUDE.md` unique | `CLAUDE.md` court, `.claude/rules/` par zone, skills de procédure | Le contexte n'est chargé que lorsqu'il sert (§14) |

---

## 4. Plan du site et URL

```
/                                             redirection vers /<langue par défaut>/ (D1)
/<lang>/                                      Accueil
/<lang>/project/                              Le projet : pourquoi, où il en est, où il va, le cadre (§5.9)
/<lang>/roadmap/                              Feuille de route : les étapes du lab et leur statut (§5.10)
/<lang>/infrastructure/                       Vue d'ensemble : schéma, composants, dernières décisions
/<lang>/infrastructure/<groupe>/              Une page par groupe d'infrastructure, plus Monitoring et Automatisation (§5.2)
/<lang>/infrastructure/decisions/             Index des ADR
/<lang>/infrastructure/decisions/adr-0001-<slug>/
/<lang>/services/                             Les services, en cartes avec leur statut (§5.4)
/<lang>/services/<id>/                        Page d'un service
/<lang>/journal/                               Toutes les entrées : hebdomadaires et post-mortems
/<lang>/journal/001-<slug>/                    Entrée hebdomadaire
/<lang>/journal/incidents/                     Post-mortems
/<lang>/journal/incidents/pm-001-<slug>/
/<lang>/about-me/                             L'auteur : profil, parcours, homelab, façon de travailler, contact (§5.7)
/<lang>/cv/                                   CV HTML : la référence factuelle (compétences, dates, missions, formation, certifications) (§5.7)
/<lang>/tags/<tag>/                           Tout ce qui concerne une technologie (index /tags/ non généré tant qu'aucun tag n'est utilisé, §5.8)
/<lang>/certifications/<id>/                  Tout le travail lié à une certification (idem)
```

Menu, dans cet ordre : Accueil · Le projet · Infrastructure · Services · Journal · À propos de moi (EN : Home · The project · Infrastructure · Services · Journal · About me). La feuille de route n'y figure pas : on l'atteint par des liens (§5.10). Services, en brouillon du 28 au 29/10/2026, est publiée avec ses deux premières pages (§5.4). Sur petit écran, les entrées passent à la ligne au lieu de défiler (§11.5).

Règles :

- Les slugs sont en ASCII minuscule, en kebab-case, en anglais, et identiques dans les deux langues.
- Une URL publiée ne disparaît pas : un renommage ou une suppression DOIT laisser une redirection, à vérifier dans `public/` après build. Hugo préfixe les `aliases` de la langue de la page ; pour une URL hors des préfixes de langue, la redirection passe par un fichier `static/` (`docs/structure.md` §3.6).
- Chaque fusion sur `main` est déployée, donc aucune page vide ni aucun `TODO(firmin)` en production. Une page sans contenu porte `draft: true` ; seules les sections du menu peuvent être publiées avant leur contenu, avec une description et un court message « en construction » (`docs/structure.md` §1). Les entrées de menu sont déclarées dans le front matter de leur page, pas dans `hugo.toml` : une section entre au menu automatiquement le jour où elle est publiée (`docs/structure.md` §1, §3.5).

---

## 5. Sections

### 5.1 Accueil

Objectif : présenter le **projet**, et dire en une ligne **qui** le mène (décision de Firmin du 28/10/2026 : un recruteur doit savoir chez qui il est sans quitter l'accueil). Le détail sur Firmin reste sur la page À propos de moi (§5.7). L'essentiel en un écran sur desktop, en deux sur mobile. Un bloc sans donnée est masqué plutôt qu'affiché vide. Les blocs, dans l'ordre :

1. **Le projet.** Deux ou trois phrases (corps de `content/_index.<lang>.md`) : un homelab reconstruit de zéro, documenté chaque semaine, ce qu'il sert à apprendre et à démontrer. Juste en dessous, une ligne d'identité : nom (`params.profile.name`), poste visé et pays recherchés (champ `identity` du front matter de l'accueil). Puis deux boutons : « CV » (page CV, ou le PDF à défaut) et « Me contacter » (ancre `#contact` de la page À propos de moi). Puis les liens « Le projet » et « À propos de moi ».
2. **Le lab en un coup d'œil.** Schéma `lab-overview` (§11.6), marqué « architecture cible » tant qu'aucun composant n'est en service ; phase en cours de la feuille de route, avec un lien vers sa page (§5.10). Les compteurs de composants par statut sont retirés (25/10/2026) : ils reviendront avec les services. Liens : Infrastructure, Services. La dernière entrée du journal n'y figure pas : le bloc 4 la montre déjà.
3. **Stack.** Les briques du lab par thème (Infrastructure, Réseau, Monitoring, Services), dans l'ordre de `data/stack.yaml` (§6.8) : pour chacune, son nom, son rôle dans le lab en une ligne, et son statut (« En service », « En cours » ou « À venir »). Le statut se lit dans le catalogue ou la feuille de route. Le titre d'un thème mène à sa page quand elle est publiée, et un lien « Feuille de route complète » vers sa page (§5.10) ferme le bloc. Quatre colonnes côte à côte sur desktop, deux sur tablette, une sur mobile, avec un rôle de quelques mots (décision de Firmin du 29/10/2026 : montrer ce qui tourne et ce qui vient, plutôt qu'une liste de composants qui répétait le schéma).
4. **Journal.** Les trois dernières entrées, comptes rendus et post-mortems confondus : numéro (S06, PM-001), date, titre, description. Liens : le journal complet, les incidents, le flux RSS.

Ne figurent pas sur l'accueil : le reste de ce qui concerne Firmin (À propos de moi ; compétences et certifications dans le CV), le détail technique (Infrastructure et Services), les ADR (Infrastructure), la liste complète des incidents (Journal).

### 5.2 Infrastructure

**Frontière entre infrastructure et services.** Est infrastructure ce dont le reste du lab dépend pour fonctionner : matériel, réseau, hyperviseur, stockage, sauvegardes, identité, cluster Kubernetes, chaîne IaC/GitOps. Est service ce qui est consommé, par Firmin ou par d'autres services, sans que le reste en dépende : supervision, applications, outils. En cas de doute, une question tranche : si ce composant s'arrête, quels autres composants cessent de fonctionner ? S'il y en a, c'est de l'infrastructure. Le champ `layer` du catalogue porte la décision ; changer de côté, c'est changer un champ.

La règle de frontière sert au classement (champ `layer`) ; elle n'est pas expliquée aux visiteurs (28/10/2026). Exception décidée par Firmin le 29/10/2026 : le monitoring a sa page dans Infrastructure, à côté de l'automatisation.

- **Vue d'ensemble** (`/infrastructure/`) : une introduction humaine (ce qu'est le lab aujourd'hui, en deux paragraphes), schéma, tableau des composants d'infrastructure par groupe avec liens vers les pages de groupe, cinq dernières ADR. L'introduction renvoie vers la feuille de route, qui a sa propre page depuis le 29/10/2026 (§5.10).
- **Cartes et badges** (décision de Firmin du 29/10/2026) : la vue d'ensemble montre une carte par page de la section, dans l'ordre de leur `weight` : Infrastructure physique, Réseau, Virtualisation, Monitoring, Automatisation, puis Décisions d'architecture. Chaque carte porte le badge de la feuille de route (Fait, En cours, À venir), calculé depuis les étapes que la page liste dans son champ `roadmap` : une étape en cours, ou un mélange d'étapes faites et à venir, donne En cours. Décisions d'architecture n'a pas de badge. Gabarit `infrastructure/section.html`, partials `section/overview.html`, `section/cards.html` et `section/card-badge.html`, avec le balisage des cartes de PaperMod.
- **Infrastructure physique** : l'ancienne page Matériel, renommée le 29/10/2026 (décision de Firmin). Son adresse ne change pas : `/infrastructure/hardware/`.
- **Monitoring et Automatisation** (`/infrastructure/monitoring/`, `/infrastructure/automation/`, 29/10/2026) : deux pages courtes qui disent seulement ce qui est prévu et où en est l'étape, tant que rien n'est installé. Elles ne sont pas des groupes de `data/groups.yaml` : elles n'ont encore aucun composant.
- **Pages de groupe** (`/infrastructure/<groupe>/`) : une par groupe d'infrastructure déclaré dans `data/groups.yaml`, obligatoire dès qu'un composant du groupe est en construction ou en service (V10). Trame (28/10/2026) : deux ou trois phrases d'ouverture (ce que c'est, pourquoi ça compte), quelques sections en langage simple où chaque terme technique est expliqué une fois, puis « Détails techniques » et « Limites et évolutions » (Annexe A.4). Ensuite, une carte par composant du groupe : la fiche technique (§5.4), ancrée sur `#<id>`.

### 5.3 Décisions (ADR)

- Une page par décision, numérotée en continu : ADR-0001, ADR-0002… Format : Annexe A.3.
- Statuts : `proposed`, `accepted`, `rejected`, `deprecated`, `superseded`.
- Une ADR acceptée n'est pas réécrite. Changer d'avis passe par une nouvelle ADR qui déclare `supersedes`. L'ancienne passe alors en `superseded` avec `superseded_by` : ce sont les seuls champs qui changent.
- Mérite une ADR tout choix entre de vraies alternatives aux conséquences durables : hyperviseur, topologie réseau, outil de sauvegarde, accès distant, distribution Kubernetes, outil GitOps… Un simple réglage n'en mérite pas.
- Index : numéro, titre, statut, date, du plus récent au plus ancien.
- Page : badge de statut, date, composants concernés, bandeau « remplacée par » s'il y a lieu, entrées du journal qui la citent (calculées).

### 5.4 Services

- **État (29/10/2026)** : section publiée, revenue au menu, avec deux pages : OpenBot (`/services/openbot/`, en service) et Lab LPIC-1 (`/services/lpic-1-lab/`, à venir). Décision de Firmin : une vue d'ensemble en cartes avec badge, sur le modèle d'Infrastructure (§5.2). Un service n'est pas une étape de la feuille de route : son statut est le champ `status` de sa page (`running`, `building` ou `planned`), affiché avec les libellés du bloc Stack (En service, En cours, À venir). Le catalogue en tableau et la fiche technique ci-dessous restent la cible, quand les services seront décrits dans `data/catalog/`.
- **Catalogue** (`/services/`) : un tableau par groupe de services. Colonnes : nom (lien vers la fiche si elle existe), rôle, statut, où il tourne, exposition, date de vérification. Tout vient des données.
- **Fiche** (`/services/<id>/`) : en-tête (nom, statut, rôle), fiche technique, prose de Firmin (Annexe A.4), puis entrées du journal, ADR et post-mortems liés (calculés).

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

### 5.5 Journal

- Une entrée par semaine de travail, numérotée en continu : S1, S2… en français, W1, W2… en anglais. Le numéro compte les comptes rendus hebdomadaires, pas les semaines du calendrier. Après une semaine sans entrée, la suivante prend le numéro suivant et précise la période couverte.
- `date` = dernier jour de la semaine couverte (en pratique, le jour de publication). Une entrée rattrapée garde la date de sa semaine.
- Le journal raconte une histoire (décision de Firmin du 28/10/2026). Gabarit narratif (Annexe A.1) : un titre en forme de tournant ou de question ; un chapeau de deux ou trois phrases ; un à trois récits courts (le problème, ce que j'ai essayé, ce que j'ai choisi et pourquoi avec le lien vers la décision, la limite que j'accepte) ; « Ce que j'en retiens », dans les mots de Firmin ; « La suite » ; un encadré « En bref » pour les techniciens (composants, étapes, décisions). Le chapeau sert de résumé dans les listes (`<!--more-->`). Les entrées d'avant le 28/10/2026 suivaient l'ancien gabarit (Objectif, Réalisé, Problèmes et résolution, Décisions, Appris, Semaine prochaine).
- Chaque entrée déclare `components`, `adrs`, `tags` et `certifications`.
- Liste (`/journal/`) : toutes les entrées, post-mortems compris, de la plus récente à la plus ancienne. Pour chacune : date, titre (une entrée hebdomadaire commence par « Semaine N — » / « Week N — », un post-mortem garde son numéro PM-002), description, tags. Pagination par 10, flux RSS.
- Page : numéro et titre, date, description, tags et certifications, composants concernés, ADR liées, corps, navigation précédente/suivante.
- Le post LinkedIn de la semaine résume l'entrée et y renvoie (§16.1).

### 5.6 Incidents (post-mortems)

- Rédigé pour tout incident qui a causé une perte de service ou de données, ou qui a demandé une remise en état non triviale, même auto-infligé. Ce sont souvent les plus instructifs.
- Format sans recherche de coupable (Annexe A.2) : Résumé, Impact, Chronologie, Détection, Cause racine, Résolution, Actions correctives, Ce que j'en retiens.
- Gravité : `sev1` (perte de données ou lab entièrement indisponible), `sev2` (un composant d'infrastructure ou un service indisponible), `sev3` (dégradation partielle, contournement disponible).
- Numérotation continue : PM-001, PM-002… `date` = publication, `incident_date` = début de l'incident, `impact_minutes` = durée de l'impact.
- Le corps n'est pas réécrit ; seul l'état des actions correctives évolue.
- `/journal/incidents/` les liste. Ils figurent aussi dans la liste du journal, avec un badge.

### 5.7 À propos de moi

**Règle de partage (décision de Firmin du 29/10/2026) : le CV dit *quoi*, À propos de moi dit *qui*.** À propos de moi présente la personne : son parcours en récit, son homelab, sa façon de travailler, le contact. Le CV est la seule référence factuelle : compétences, dates, missions, formation, langues, certifications. À propos de moi NE DOIT PAS dupliquer la liste des compétences ni le détail des postes ; elle renvoie au CV. Exception : le paragraphe d'introduction PEUT citer en une phrase les chiffres clés de l'expérience (domaines, parc, sites), comme accroche.

Une seule page, `/about-me/` (titre « À propos de moi » / « About me »), consacrée à Firmin et à lui seul :

1. **Profil** : photo ronde (`params.profile.photo`, partial `profile/photo.html`, 30/10/2026), nom, poste visé (`headline`), ligne pratique (`availability`) : région plutôt que commune (§10), mobilité, langues, disponibilité. Boutons : CV (page CV, ou le PDF de la langue courante à défaut, sans adresse, téléphone ni date de naissance), GitHub, LinkedIn, depuis `params.profile`.
2. **Présentation** : corps de la page, en récit, en paragraphes courts : une introduction, puis « Mon parcours » (le fil des études et des postes, sans le détail des missions, qui renvoie au CV), « Mon homelab » (pourquoi il existe, l'ancien lab au passé, les briques importantes en une phrase, liens vers Le projet et le journal) et « Ma façon de travailler » (une liste courte de principes, sans exemples), en dernière section. Le type de poste recherché n'a pas de section propre : la ligne `availability` du profil le porte (décision de Firmin du 29/10/2026).
3. **Contact** : partial `profile/contact.html`, rendu par le template juste après le corps de la page, en fin de page, sous un titre « Contact » qui porte l'ancre `#contact` (visée par le bouton « Me contacter » de l'accueil). E-mail depuis `params.contactEmail`, LinkedIn depuis `params.profile`. Le shortcode `contact` prévu à l'origine n'est pas créé : un partial garde l'ordre des blocs.

Le bloc Certifications (partial `profile/certifications.html`, depuis `data/certifications.yaml`) est retiré le 29/10/2026 : la certification visée figure dans le CV, et « Mon homelab » la cite.

**Page CV** (`/<lang>/cv/`, `content/cv/index.<lang>.md`, template `cv/page.html`) : la version HTML du CV, avec le téléchargement du PDF de la langue courante. Colonne latérale depuis le front matter (`sidebar` : contact, compétences, formation, certification, langues) ; corps : profil, expériences professionnelles avec leurs dates et leurs missions, projet personnel. Hors du menu : on l'atteint par les boutons « CV » de l'accueil et d'À propos de moi. Les PDF de `static/cv/` sont l'impression de cette page (décision de Firmin du 29/10/2026) : une page A4 par langue, grâce aux styles `@media print` de `site.css`, sans en-tête ni pied de page. Les liens vers le site passent par `params.siteDomain` (shortcode `site-link`), pour que l'impression depuis le serveur de dev ne contienne pas `localhost`. L'en-tête montre la photo ronde, comme À propos de moi. Dans la colonne Contact, le domaine porte la mention « Portfolio : », et la ligne LinkedIn est masquée à l'impression, inutile sur papier (décisions de Firmin du 30/10/2026). Pour les refaire : `hugo server`, puis Chrome sans en-têtes ni pieds de page (`--headless --no-pdf-header-footer --print-to-pdf`) sur `/fr/cv/` et `/en/cv/`, puis vérifier l'absence de `localhost` et de toute adresse personnelle.

`params.contactEmail` est l'unique source de l'adresse de contact : page À propos de moi, rubrique Contact du CV HTML, pied de page.

Le projet (objectif, contraintes) est présenté côté projet, sur la page Le projet (§5.9), et ses étapes sur la page Feuille de route (§5.10) ; la fabrication du site (code source, « sans cookies ni traceurs », crédit Hugo et PaperMod) dans le pied de page.

### 5.8 Taxonomies

- `tags` : technologies et thèmes. Le vocabulaire est contrôlé dans `data/tags.yaml` ; un nouveau tag s'ajoute à ce fichier dans la même PR.
- `certifications` : les identifiants de `data/certifications.yaml`.
- Utilisées par les entrées du journal, les post-mortems et les ADR. Les pages d'état n'en ont pas besoin : le catalogue les décrit.
- Les pages de terme affichent le libellé tiré des données.
- Tant qu'aucune page n'utilise de tag ni de certification, les pages d'index (`/<lang>/tags/`, `/<lang>/certifications/`) ne sont pas générées : `disableKinds = ["taxonomy"]` dans `hugo.toml` (28/10/2026). La ligne est retirée le jour où le premier terme est utilisé. La redirection racine `/tags/` vise `/fr/` en attendant.

### 5.9 Le projet

Une page, `/<lang>/project/` (« Le projet » / « The project »), au menu entre Accueil et Infrastructure (poids 15). Elle remplace la section Divers et son unique article, « Objectifs et contraintes du projet » (28/10/2026) ; les anciennes adresses `/<lang>/misc/` et `/<lang>/misc/project-goals-constraints/` y redirigent (alias). Page d'état, mise à jour en place : pourquoi un homelab, pourquoi repartir de zéro, où en est le lab, la suite, le cadre que Firmin s'est fixé. « La suite » donne seulement l'étape en cours et la suivante, puis renvoie à la feuille de route (§5.10) pour le reste, sans la répéter (décision de Firmin du 29/10/2026).

### 5.10 Feuille de route

Une page, `/<lang>/roadmap/` (« Feuille de route » / « Roadmap »), hors du menu. Décisions de Firmin du 29/10/2026 : la feuille de route quitte la page Infrastructure, qui décrit le lab tel qu'il est, pour une page à elle. Comme les décisions d'architecture, elle n'a pas d'entrée au menu : on l'atteint par des liens, là où le texte en parle. Page d'état, mise à jour en place, sans date, temps de lecture ni navigation. Elle contient une introduction, la liste des étapes (shortcode `roadmap`, §6.7), puis « Plus loin » : ce qui vient après la dernière étape, dans un ordre pas encore fixé, et ce qui avance en parallèle, hors feuille de route.

Y renvoient : la phase en cours et le bloc Stack de l'accueil (§5.1), l'introduction d'Infrastructure, « La suite » de Le projet et des entrées du journal. L'ancienne ancre `/infrastructure/#lab-roadmap` n'existe plus : la page Infrastructure reste en place et renvoie vers la feuille de route.

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
| `data/stack.yaml` | Le bloc Stack de l'accueil : thèmes et briques, avec leur rôle (§6.8) |

Les identifiants sont en kebab-case ASCII et ne changent pas : l'URL des fiches en dépend. Un renommage impose une redirection.

### 6.2 Catalogue : schéma

```yaml
# data/catalog/grafana.yaml — EXEMPLE ILLUSTRATIF, à ne pas recopier dans data/
name: Grafana                  # nom affiché : chaîne commune, ou paire {fr, en} s'il se traduit
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
| `backup`, `monitoring` | — | — | optionnels (décision du 25/10/2026) : renseignés quand ils sont en place | — |
| `verified` | — | requis | requis | — |
| `since` | optionnel | optionnel | optionnel | requis (date de retrait) |
| Fiche publiée (couche `service`) | optionnelle | requise | requise | conservée |
| Page du groupe publiée (couche `infrastructure`) | optionnelle | requise | requise | conservée |

Tout `none` se justifie. `auth.method: none`, `backup.method: none` et une supervision entièrement à `false` exigent un champ `note: {fr, en}` dans le bloc concerné (exemple : « composant sans état »).

`deploy.method: manual` est accepté et affiché tel quel : une dette d'automatisation visible est honnête.

### 6.4 `data/groups.yaml`

L'ordre de la liste est l'ordre d'affichage. La page d'un groupe d'infrastructure (FR et EN) devient obligatoire dès qu'un de ses composants passe en construction (V10).

Les groupes d'infrastructure sont fixés par D6 (tranchée le 25/10/2026, §17.2) : trois groupes, dans cet ordre. Les autres groupes de la proposition de départ (stockage et sauvegardes, identité et sécurité, Kubernetes, automatisation) seront ajoutés quand ils auront du contenu. Aucun groupe de services n'est déclaré tant qu'aucun service n'existe : la liste `service` reste vide.

```yaml
infrastructure:
  - {id: hardware,          label: {fr: "Infrastructure physique", en: "Physical infrastructure"}}
  - {id: network,           label: {fr: "Réseau",                  en: "Network"}}
  - {id: virtualization,    label: {fr: "Virtualisation",          en: "Virtualization"}}
service: []
```

Proposition de départ pour les groupes encore à venir (à ajouter le jour où ils ont du contenu) :

```yaml
infrastructure:
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

Depuis le 29/10/2026, aucun template ne lit ce fichier : le bloc Certifications d'À propos de moi est retiré, et la certification visée figure dans le CV (§5.7). Il reste le vocabulaire prévu de la taxonomie `certifications` (§5.8).

### 6.7 `data/roadmap.yaml`

```yaml
- id: foundations              # EXEMPLE — Firmin fournit les phases réelles
  title: {fr: "…", en: "…"}
  status: in-progress          # planned | in-progress | done
  goals:                       # objectifs vérifiables
    - {fr: "…", en: "…"}
```

La feuille de route ne porte pas de dates (décision de Firmin du 25/10/2026) : la chronologie se lit dans le journal, semaine par semaine. Les étapes donnent seulement l'ordre et le statut. Elle s'affiche sur la page Feuille de route (§5.10) par le shortcode `roadmap` ; l'étape en cours montre ses objectifs. Une étape `planned` s'affiche dans la liste comme « À venir » (libellé du 29/10/2026, qui remplace « Prévu » partout sur le site, badges et légendes des schémas compris) ; seule une étape `in-progress` apparaît sur l'accueil comme « Phase en cours ».

### 6.8 `data/stack.yaml`

```yaml
- id: network                       # thème, dans l'ordre d'affichage
  label: {fr: "Réseau", en: "Network"}
  link: /infrastructure/network     # facultatif : page du thème, si elle est publiée
  items:
    - name: "OPNsense"
      role: {fr: "…", en: "…"}      # une ligne : ce que la brique fait dans le lab
      components: [fw-01]           # statut lu dans le catalogue (premier composant)
    - name: {fr: "…", en: "…"}
      role: {fr: "…", en: "…"}
      roadmap: monitoring           # ou : statut lu dans la feuille de route
    - name: "…"
      role: {fr: "…", en: "…"}
      page: /services/openbot       # ou : statut lu dans le champ `status` d'une page
    - name: "…"
      role: {fr: "…", en: "…"}
      status: planned               # ou : statut propre, seulement hors catalogue, feuille de route et pages
```

Une brique est une technologie ou un ensemble, pas forcément un composant du catalogue. Son statut a une seule source (P2) : le catalogue (`components`), sinon la feuille de route (`roadmap` : `done` → en service, `in-progress` → en cours, `planned` → à venir), sinon le champ `status` de la page désignée par `page` (un service, 29/10/2026), sinon son propre champ `status` (`running`, `building` ou `planned`), réservé aux briques qui n'existent nulle part ailleurs. Un rôle ne cite que des faits publiés ailleurs sur le site (§9.2).

---

## 7. Modèle de contenu (`content/`)

### 7.1 Organisation

Chaque page est un dossier (page bundle) qui contient `index.fr.md`, `index.en.md` et ses images. Les sections ont leurs `_index.fr.md` et `_index.en.md`.

```
content/
├── _index.{fr,en}.md                              accueil
├── about-me/index.{fr,en}.md
├── project/index.{fr,en}.md                       Le projet (§5.9)
├── cv/index.{fr,en}.md                            CV HTML
├── infrastructure/
│   ├── _index.{fr,en}.md
│   ├── <groupe>/index.{fr,en}.md                  un dossier par groupe d'infrastructure
│   └── decisions/
│       ├── _index.{fr,en}.md
│       └── adr-0001-<slug>/index.{fr,en}.md
├── services/
│   ├── _index.{fr,en}.md
│   └── <id>/index.{fr,en}.md                      id = identifiant du catalogue
└── journal/
    ├── _index.{fr,en}.md
    ├── 001-<slug>/index.{fr,en}.md
    └── incidents/
        ├── _index.{fr,en}.md
        └── pm-001-<slug>/index.{fr,en}.md
```

Les numéros sont complétés par des zéros : trois chiffres pour le journal et les post-mortems, quatre pour les ADR.

### 7.2 Front matter

Front matter en YAML (`---`), comme aujourd'hui. Toute page porte `title`, `description` et `draft`. `description` fait une ou deux phrases, 160 caractères au plus ; elle sert aux listes, à la balise meta et à l'aperçu du lien sur LinkedIn.

| Type | Champs requis en plus | Champs optionnels |
|---|---|---|
| Entrée du journal | `date`, `week`, `tags` | `components`, `adrs`, `certifications` |
| Post-mortem | `date`, `pm`, `incident_date`, `severity`, `impact_minutes` | `components`, `tags` |
| ADR | `date`, `adr`, `status` | `components`, `supersedes`, `superseded_by` (requis si `superseded`), `tags` |
| Fiche service, page de groupe | — | — (les faits viennent du catalogue) |
| À propos de moi | `headline`, `availability` | — |
| Accueil, sections | — | — |

Les champs structurés sont identiques dans les deux langues (contrôle V6) : `draft`, `date`, `week`, `pm`, `adr`, `status`, `incident_date`, `severity`, `impact_minutes`, `components`, `adrs`, `certifications`, `tags`, `supersedes`, `superseded_by`. Seuls `title`, `description` et le corps diffèrent.

### 7.3 Archetypes

Des archetypes de dossier créent les deux langues en une commande :

```
archetypes/
├── journal/index.{fr,en}.md
├── postmortem/index.{fr,en}.md
├── adr/index.{fr,en}.md
└── services/index.{fr,en}.md
```

```
hugo new content --kind journal journal/007-<slug>
```

Le dossier est créé avec les deux fichiers en brouillon, selon les gabarits de l'Annexe A. La date est celle du jour ; le numéro (`week`, `pm`, `adr`) est lu dans le nom du dossier, zéros de tête retirés (`007-…` → 7). Les champs qu'un archetype ne peut pas connaître restent vides plutôt que de recevoir une valeur d'exemple : la validation (V8) bloque la publication tant qu'ils ne sont pas remplis. Les archetypes sont des templates Go : ils NE DOIVENT PAS contenir d'appel de shortcode (`{{<`), que Hugo tenterait d'interpréter. Vérifier le comportement exact (archetype de dossier, choix par `--kind`) avec la version de Hugo épinglée.

### 7.4 Liens internes

- Vers un composant : `{{< component "grafana" >}}`. Le shortcode mène à la fiche (service) ou à l'ancre de la page de groupe (infrastructure).
- Vers une ADR ou un post-mortem : `{{< adr 1 >}}`, `{{< pm 1 >}}`.
- Vers toute autre page : `[texte]({{< relref "/journal/001-<slug>" >}})`. Une référence cassée fait échouer le build.
- Aucune URL du site écrite en dur. Les liens externes sont permis et vérifiés chaque semaine (§13.2).

### 7.5 Images

- Dans le dossier de la page, référencées en relatif, avec un texte alternatif obligatoire (V12).
- PNG, JPG, WebP ou SVG, 1 Mo au plus (contrôle CI).
- Chaque capture est relue avant commit (§10). Aucune métadonnée GPS (contrôle CI).
- Les schémas ne sont pas des images de page : ils sont conçus dans Claude Design et exportés en SVG (§11.6).

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
| Prose : journal, post-mortems, ADR, fiches, pages de groupe, accueil, Le projet, À propos de moi | Firmin fournit les faits (notes, texte, repo du lab) et valide | Rédiger la prose à partir de ces faits, sous la validation de Firmin (décision du 28/10/2026) ; traduire ; corriger orthographe et format. « Ce que j'en retiens » reste dans les mots de Firmin |
| Données : catalogue, roadmap, certifications, tags | Firmin, par ses énoncés | Transcrire en YAML ce que Firmin énonce |
| Structure : sections, archetypes, templates, CI, outillage | Claude Code | Proposer un plan, puis implémenter après accord |

### 9.2 Aucune invention

- Claude Code NE DOIT PAS ajouter un fait absent de ce que Firmin a fourni ou de ce qui est vérifiable dans le repo du lab : ni commande, ni version, ni chiffre, ni résultat, ni difficulté, ni leçon.
- Une information manque : la demander. Dans un brouillon, la marquer `TODO(firmin): <question>`. Le build refuse tout `TODO(firmin)` dans une page publiée (V11).
- `verified` et `backup.restore_tested` ne changent que sur indication explicite de Firmin.
- **Exception temporaire (décidée par Firmin le 14/10/2026).** Le site est publié avec du contenu d'exemple fictif, marqué « EXEMPLE » / « (exemple) » : présentation, profil, catalogue, groupes, feuille de route, certifications, schéma, entrées du journal, post-mortem, fiches et pages de groupe. Un bandeau en haut de chaque page (`params.underConstruction`) signale que le contenu est provisoire et en partie fictif. Ce contenu est remplacé par les vraies données de Firmin, et le bandeau retiré, au plus tard à la première vraie entrée du journal (3.3). **Close le 25/10/2026** : tout le contenu d'exemple est retiré ou remplacé, le bandeau est désactivé (`underConstruction = false`).

### 9.3 Historique immuable

- Journal : une entrée publiée n'est pas réécrite. Une faute de frappe se corrige directement ; une erreur de fond se signale par un bloc « Erratum (date) » en fin d'entrée.
- **Exception (décidée par Firmin le 28/10/2026).** L'entrée de la semaine 1 est réécrite en récit selon le nouveau gabarit (Annexe A.1), avec les mêmes faits et son erratum conservé en fin d'entrée : le site n'avait pas encore été partagé. Les rubriques « Ce que j'en retiens » des semaines 1 et 2 attendent les mots de Firmin.
- ADR acceptée : seuls `status` et `superseded_by` changent.
- **Exception (décidée par Firmin le 29/10/2026).** Le retrait des points-virgules (§9.5) s'applique aussi aux ADR acceptées et aux entrées du journal déjà écrites, sans changement de sens.
- **Exception (décidée par Firmin le 29/10/2026).** Le remplacement de « supervision » par « monitoring » (§9.5) s'applique aussi aux ADR acceptées (ADR-0002), sans changement de sens.
- Post-mortem : seul l'état des actions correctives évolue.
- Pages d'état (Infrastructure, Services, Accueil, À propos de moi) : mises à jour en place.

### 9.4 Traduction

- Traduire le sens, pas les mots, avec la même structure : mêmes titres, même ordre, mêmes listes.
- Ne jamais traduire le code, les commandes, les identifiants, les noms de produits ni les champs structurés.
- Ne rien ajouter, ne rien retirer, ne pas « améliorer » le texte source. Signaler une ambiguïté à Firmin plutôt que la trancher.
- Les deux fichiers arrivent dans la même PR.

### 9.5 Style

Première personne. Passé composé pour ce qui a été fait. Paragraphes humains et concrets, dans le ton de l'introduction de l'accueil : lisibles en 30 secondes par un recruteur non technique, sans rien omettre d'important pour un responsable technique. Chaque terme technique est expliqué simplement à sa première apparition dans la page (quorum, VLAN, VPN, NAT, ZFS…) ; le détail va dans « Détails techniques » ou dans l'encadré « En bref ». Pas de répétition d'une page à l'autre : une limite se décrit une fois et les autres pages y renvoient. Un résultat vérifié se formule comme tel (« l'isolation est testée »), pas comme une intention. Phrases courtes, faits plutôt qu'adjectifs, aucun superlatif. En français, les termes techniques gardent leur forme anglaise quand c'est l'usage du métier (cluster, pod, playbook). Une rubrique vide est supprimée du gabarit, sauf « La suite » ; « Ce que j'en retiens » est retirée tant que Firmin n'a pas donné ses mots. Le site ne mentionne pas d'aide à la rédaction. Pas de point-virgule dans la prose du site, en français comme en anglais (décision de Firmin du 29/10/2026) : couper en deux phrases, ou utiliser une virgule, un deux-points ou une liste. En français, on écrit « monitoring » (ou « observabilité »), jamais « supervision » (décision de Firmin du 29/10/2026). Les noms de champs du catalogue (`monitoring`) ne changent pas.

---

## 10. Politique de publication

Le repo et le site sont publics : tout ce qui y entre doit pouvoir être lu par n'importe qui.

| Catégorie | Autorisé | Interdit |
|---|---|---|
| Réseau | Schémas logiques, plan d'adressage privé (RFC 1918), VLAN ; adresses de l'infrastructure du lab : passerelle OPNsense et nœuds Proxmox (exception décidée par Firmin le 29/10/2026 : adresses privées, injoignables depuis Internet) | IP publique du domicile, IPv4 comme IPv6 ; adresses du réseau VPN (100.64.0.0/10) ; adresses des VM hors infrastructure du lab (dont la zone isolée) |
| Accès distant | Le principe et l'outil (VPN maillé, aucun port ouvert) | Points d'accès, nom du tailnet, clés, règles d'accès détaillées, ports |
| Arrivée d'Internet (exceptions décidées par Firmin le 25/10/2026) | Le lab sort par une box internet domestique, avec un double NAT (box, puis OPNsense) ; Internet arrive sur le pare-feu OPNsense de PVE1 | Fournisseur et modèle de la box ; toute adresse du réseau domestique ; nom des interfaces et des ponts ; accès de secours |
| Secrets | — | Tout secret, jeton, mot de passe ou clé privée, même révoqué ou « de démonstration » |
| Agent IA de la zone isolée (exception décidée par Firmin le 29/10/2026) | Le nom du logiciel (OpenBot), sans le dire « open source » | Service de comptes et relais, compte, abonnement, adresse et règles de la VM |
| Images | Captures relues | Métadonnées GPS ; capture montrant IP publique, jeton, e-mail, onglet ou notification personnels |
| Données personnelles | Nom, région, e-mail de contact dédié (D4), liens professionnels, et la photo de profil sur À propos de moi et le CV (exception décidée par Firmin le 30/10/2026 : image recadrée, sans métadonnées) | Adresse postale, téléphone, date de naissance, données de tiers (famille, appareils du foyer) |
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
  - `ShowCodeCopyButtons`, `ShowBreadCrumbs`, `ShowPostNavLinks` (pas de bouton RSS à côté des titres : le flux du journal est proposé dans le pied de page) ;
  - `socialIcons` (GitHub, LinkedIn, e-mail) ;
  - `labRepo` (D3) ;
  - `profile` : nom, liens GitHub et LinkedIn, chemin du CV par langue, affichés sur la page À propos de moi et sur l'accueil ;
  - `contactEmail` : l'adresse de contact, unique source pour la page À propos de moi, le CV HTML et le pied de page (28/10/2026) ;
  - `author` (balise meta `author`) et `hideAuthor` (pas de nom d'auteur répété sous chaque page) ;
  - `siteRepo` : lien vers le code source du site, dans le pied de page ;
  - `hideFooter` : le pied de page de PaperMod est remplacé par celui du site (§11.7) ;
  - `images` : image OpenGraph par défaut, au format PNG 1200 × 630, une par langue (`[languages.<lang>.params]`, fichiers `static/og-image.<lang>.png` : fond uni, monogramme, nom, poste, site ; générées le 28/10/2026 avec Swift/AppKit, sans métadonnées) ;
- `title = "Firmin Moyen · Homelab"` : le nom d'abord (28/10/2026) ;
- `disableKinds = ["taxonomy"]` tant qu'aucun tag ni certification n'est utilisé (§5.8) ;
- Markdown : garder `unsafe = false` (pas de HTML brut dans le contenu) ; le shortcode `rawhtml` de PaperMod est interdit ;
- `[privacy]` : désactiver les services tiers intégrés.

### 11.2 Templates

Nouveau système de templates (Hugo ≥ 0.146) : un dossier de `layouts/` correspond à un chemin de pages et s'applique à tout ce qu'il contient ; le fichier le plus proche l'emporte.

```
layouts/
├── home.html                              accueil (§5.1)
├── term.html                              pages de terme, libellés depuis data/ (§5.8)
├── taxonomy.html                          liste des termes (surcharge, registre §11.7)
├── about-me/page.html                     profil, présentation, contact (§5.7)
├── cv/page.html                           CV HTML ; colonne Contact alimentée par hugo.toml (`kind`)
├── infrastructure/
│   ├── section.html                       vue d'ensemble
│   ├── page.html                          page de groupe
│   └── decisions/{section,page}.html      index et page d'ADR
├── services/section.html                  cartes des services (§5.4) ; la fiche (page.html) reste à faire
├── journal/
│   ├── section.html                       liste (inclut les post-mortems)
│   ├── page.html                          entrée hebdomadaire
│   └── incidents/{section,page}.html      post-mortems
├── _partials/
│   ├── header.html                        surcharge existante (registre §11.7)
│   ├── extend_head.html                   point d'extension PaperMod : appelle les validations (§12)
│   ├── extend_footer.html                 point d'extension PaperMod : pied de page du site (nom, contact, source, RSS, crédit)
│   ├── validate/{data,page}.html
│   ├── catalog/{fiche,table,badge,link}.html   badge et link en place depuis 5.2a
│   ├── home/{intro,lab,stack,stack-list,journal}.html   blocs de l'accueil : le projet (5.2a)
│   ├── profile/{intro,links,contact,cv-url}.html   page À propos de moi ; cv-url sert aussi l'accueil
│   ├── l10n.html                          valeur {fr, en} d'un champ de données dans la langue courante
│   ├── journal/{item,meta}.html
│   └── backlinks.html                     liens inverses (P3)
└── _shortcodes/{diagram,component,adr,pm,roadmap}.html
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
| `roadmap` | Feuille de route, depuis les données. Le contact est rendu par le template de À propos de moi (partial `profile/contact.html`) ; les certifications figurent dans le CV (§5.7) | — |

Le shortcode `component` et la liste des composants d'une entrée ne créent un lien que si la page cible (fiche ou page de groupe) est publiée. Sinon, ils affichent le nom et le badge sans lien. Aucun lien ne mène donc à une page absente, quel que soit l'ordre dans lequel le contenu arrive.

### 11.4 Chaînes d'interface

`i18n/fr.yaml` et `i18n/en.yaml` contiennent toutes les chaînes d'interface : statuts, valeurs des énumérations, intitulés de la fiche technique, boutons, numéros de post-mortem (« PM-%03d »). Le numéro de semaine est écrit dans le titre de l'entrée, prérempli par l'archetype. Aucun texte écrit en dur dans un template.

### 11.5 CSS

Un seul fichier, `assets/css/extended/site.css`, que PaperMod ajoute après son propre CSS. Il utilise les variables du thème (`--primary`, `--secondary`, `--tertiary`, `--entry`, `--border`, `--code-bg`) pour fonctionner en clair comme en sombre. Un badge de statut porte toujours son texte, jamais la seule couleur. Aucun framework CSS.

Sur petit écran (768 px et moins), le menu passe à la ligne au lieu de défiler hors de l'écran (PaperMod : `nowrap` et `overflow-x`), et l'en-tête prend des lignes plus basses (28/10/2026). Les entrées du journal ont un encadré « En bref » : titre `## En bref {.brief}` et la liste qui le suit.

Style retenu le 15/10/2026 : « éditorial ». Fond papier, grande typographie, un seul accent (bleu), cartes à bordure fine, badges en pastilles teintées. `site.css` redéfinit les variables de PaperMod pour le clair et pour le sombre (y compris sans JavaScript, `data-theme="auto"`). Le thème suit le système du visiteur (`defaultTheme = "auto"`), et la bascule de PaperMod reste disponible. Polices du système, aucune police externe (P8).

### 11.6 Schémas

- Conception dans Claude Design (décision de Firmin du 25/10/2026) : chaque schéma est dessiné et validé par Firmin sur un canvas privé, une planche par langue. Le canvas n'est pas lié depuis le site.
- Sources : chaque planche validée est copiée telle quelle dans `scripts/diagrams/src/<nom>.<lang>.dc.html`. Toute modification passe d'abord par le canvas, puis la planche est recopiée.
- Export : `python3 scripts/diagrams/render.py` convertit chaque source en deux SVG commités, `assets/diagrams/<nom>.<lang>.light.svg` et `.dark.svg` (correspondance des couleurs claires et sombres dans le script), pour qu'ils apparaissent dans le diff des PR. SVG statiques : aucune police externe (P8), aucun script, aucune image embarquée ; titre accessible inclus.
- Relecture : chaque schéma passe par `publication-reviewer` avant sa PR, comme tout contenu issu du lab.
- Affichage : l'accueil et le shortcode `diagram` (`{{</* diagram name="<nom>" alt="…" */>}}`) choisissent les SVG de la langue de la page ; le CSS montre la bonne version selon `html[data-theme]`, sans JavaScript. Un clic ouvre le SVG en pleine taille. Le texte alternatif est obligatoire ; le shortcode échoue au build s'il manque, ou si un SVG manque.
- Vue logique et câblage du lab uniquement (§10, y compris ses exceptions).
- Schémas : `lab-overview` (accueil), `lab-network` (page Réseau), `lab-physical` (page Infrastructure physique).

### 11.7 Registre des surcharges du thème

| Fichier du site | Nature | Raison | À chaque mise à jour de PaperMod |
|---|---|---|---|
| `layouts/_partials/header.html` | Surcharge | Bascule de langue vers la page traduite (`.Translations`) plutôt que vers l'accueil ; bandeau « site en construction » en tête (`construction-banner.html`) | Comparer l'ancienne et la nouvelle version du `header.html` du thème ; reporter les changements |
| `layouts/taxonomy.html` | Surcharge | Libellés des termes depuis `data/` | Idem avec `taxonomy.html` |
| `layouts/_partials/extend_head.html` | Point d'extension prévu par le thème | Appel des validations | Vérifier qu'il est toujours inclus par `head.html` |
| `layouts/_partials/extend_footer.html` | Point d'extension prévu par le thème | Pied de page complet du site (nom, contact, code source, flux RSS du journal, « sans cookies ni traceurs », crédit discret à Hugo et PaperMod, sans lien de suivi) ; celui de PaperMod est masqué par `params.hideFooter` (28/10/2026) | Vérifier que `footer.html` respecte toujours `hideFooter` et inclut toujours ce partial et ses scripts |

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
- Dependabot (`.github/dependabot.yml`), chaque semaine : écosystèmes `github-actions` et `gitsubmodule` (PaperMod). Hugo, gitleaks et lychee se mettent à jour à la main, chaque mois (§16.5).
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
| `/journal` | Entrée hebdomadaire : numéro suivant calculé, slug proposé | §16.1 |
| `/component <id>` | Ajouter un composant ou le faire évoluer | §16.2 |
| `/adr <slug>` | Nouvelle décision | §16.3 |
| `/postmortem <slug>` | Nouvel incident | §16.4 |
| `/translate <chemin>` | Traduire une page de FR vers EN | §9.4 |
| `/linkedin <n>` | Brouillon du post LinkedIn de la semaine n | §16.1 |

### 14.3 Permissions (`.claude/settings.json`)

- **Autorisé** : build et scripts du repo (`.bin/*`, `scripts/*`), lecture et workflow git sur branche (`status`, `diff`, `log`, `add`, `commit`, `switch`, `checkout`), `gh pr create`, `gh pr view`, `gh run list`, `gh run view`.
- **Interdit** : `git push --force`, push direct sur `main`, toute modification des réglages GitHub (`gh repo edit`, `gh secret`, `gh api` en écriture).
- Les règles de permission filtrent les commandes par préfixe : elles ne distinguent pas une lecture d'une écriture par `gh api`. `gh api` est donc refusé en bloc. `git push` sans option et `gh pr merge` ne sont ni autorisés ni interdits : ils demandent confirmation à chaque fois. Claude Code ne fusionne une PR que sur demande explicite de Firmin.

### 14.4 Définition de terminé (toute PR)

1. Firmin a validé le plan avant toute écriture.
2. `hugo --minify` passe sans erreur ni nouvel avertissement.
3. `scripts/check-publication.sh` passe.
4. FR et EN sont à jour, ou le label `i18n-skip` est justifié.
5. Chaque image ajoutée a été ouverte et vérifiée (§10).
6. Revue visuelle par Firmin : Claude Code lance `hugo server` et donne la liste des pages à regarder, en FR et en EN, en thème clair et sombre.
7. Ce document est à jour si la structure change, historique des décisions compris (§17.2).
8. Branche poussée. La PR n'est ouverte qu'avec l'accord de Firmin, en fin de session ; elle n'est fusionnée par Claude Code que sur sa demande explicite.

---

## 15. Plan d'implémentation

Les phases se suivent dans l'ordre. Le plan de chaque étape est présenté et validé avant toute écriture ; les étapes d'une même session partagent une branche et une PR (§0.3). Chaque fusion laisse le site publiable, puisque `main` est déployée.

Ordre retenu le 14/10/2026 : 0.1, puis la phase 1 (la structure, détaillée dans `docs/structure.md` §7), puis 0.2 à 0.4. Tant que la CI n'existe pas, `hugo --minify` exécuté en local fait office de contrôle (§14.4).

En attendant la phase 3, Firmin consigne ses notes de chaque semaine. Elles deviendront, dans l'ordre, les premières entrées du journal, datées de leur semaine. La semaine S1 (12–18 octobre 2026) est celle de la planification. Le calendrier commun au site et au lab est au §15 du plan du lab.

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
| 1.4 | `feat/footer-rss` | Lien RSS du journal dans le pied de page au lieu d'un bouton à côté des titres (`docs/structure.md` §3.3) | Aucun logo RSS dans les titres ; lien absent en production tant que le journal est en brouillon |
| 1.5 | `feat/journal-rename` | Section « Devlog » renommée « Journal » : contenu, archetype, URL, menu, pied de page, documents | Plus aucun « devlog » hors de l'historique des décisions ; `/en/journal/` redirige tant que la section est en brouillon |
| 1.6 | `feat/placeholder-sections` | Infrastructure, Services et Journal publiées « en construction » (`docs/structure.md` §1) ; redirections à leur cible finale | Menu à 5 entrées en production ; aucune page vide ni `TODO(firmin)` publié |
| 1.7 | `feat/remove-infra-groups` | Les 7 pages de groupe retirées ; liste des groupes en décision ouverte (D6) | Aucune page de groupe dans le repo ; build vert |

### Phase 2 — Données et validation

| Étape | Branche | Contenu | Critères d'acceptation |
|---|---|---|---|
| 2.1 | `feat/data-model` | Fichiers `data/` (groupes ; vocabulaires vides ou fournis par Firmin), chaînes i18n de base, `validate/data.html` (V1 à V4, V14), tests et job `validation-tests` | Chaque règle a un cas de test qui échoue avec le message attendu |
| 2.2 | `feat/page-validation` | `validate/page.html` (V5 à V13, V15, V16), tests | Idem |

### Phase 3 — Historique : journal, incidents, ADR (débloque la publication hebdomadaire)

| Étape | Branche | Contenu | Critères d'acceptation |
|---|---|---|---|
| 3.1 | `feat/journal-templates` | Templates du journal et des incidents, partials `journal/*`, `backlinks`, shortcodes `component`, `adr`, `pm`, CSS, image OpenGraph par défaut | Revue visuelle en FR et EN, thèmes clair et sombre, largeur mobile ; liens inverses corrects ; un composant sans page publiée s'affiche sans lien |
| 3.2 | `feat/adr-templates` | Templates decisions | Bandeau « remplacée par » ; liens inverses |
| 3.3 | `docs/journal-001` | Premières entrées (Firmin), leurs ADR, les composants qu'elles citent (avec fiche ou page de groupe si V9 ou V10 l'exige), message « en construction » retiré du Journal | Entrées publiées ; aperçu LinkedIn correct (titre, description, image) ; aucun fait inventé |

Jusqu'à la phase 4, les fiches et les pages de groupe exigées par V9 et V10 s'affichent avec le template par défaut de PaperMod : leur prose est en ligne, leur fiche technique arrive en 4.1. Infrastructure, Services et Journal sont au menu depuis l'étape 1.6, avec un message « en construction ».

### Phase 4 — État : catalogue

| Étape | Branche | Contenu | Critères d'acceptation |
|---|---|---|---|
| 4.1 | `feat/catalog-templates` | Partials `catalog/*`, templates services et infrastructure | Revue visuelle ; les exigences par statut s'affichent comme prévu (« restauration non testée », notes des `none`) |
| 4.2 | `docs/catalog-initial` | Reste du catalogue (Firmin), prose des pages de groupe, message « en construction » retiré d'Infrastructure et de Services | Build vert ; aucun composant inventé |

### Phase 5 — Accueil, À propos, schémas

| Étape | Branche | Contenu | Critères d'acceptation |
|---|---|---|---|
| 5.1 | `feat/diagrams` | Shortcode `diagram`, job `diagrams` (quatre SVG présents et valides par schéma, export à jour). Le schéma `lab-overview` est livré en avance (25/10/2026) selon §11.6 | Bon schéma selon la langue et le thème ; CI rouge si un SVG manque ou est périmé |
| 5.2a | `feat/home` | `home.html` et ses blocs (§5.1), badges et liens du catalogue, chaînes i18n, `params.profile` ; anticipé le 14/10/2026, avant les phases 2 à 4 | Sans données, accueil identique en production ; avec des données d'exemple locales, les cinq blocs s'affichent en FR et en EN, clair et sombre |
| 5.2 | `feat/home-about` | Page About, shortcodes `roadmap`, `certifications`, `contact`, templates de taxonomie | Accueil lisible en un écran sur desktop ; libellés des tags corrects |
| 5.3 | `docs/about-home` | Textes de Firmin, CV, contacts (D4), certifications, roadmap | Aucun champ provisoire publié |

### Phase 6 — Outillage de maintenance

| Étape | Branche | Contenu | Critères d'acceptation |
|---|---|---|---|
| 6.1 | `chore/skills` | `.claude/skills/` (§14.2) | Chaque skill déroulée une fois à blanc, sans commit |
| 6.2 | `chore/external-checks` | `links-external.yml`, `availability.yml` | Exécutions manuelles vertes ; un site injoignable (URL de test) fait échouer `availability.yml` |

---

## 16. Procédures de maintenance

### 16.1 Chaque semaine : l'entrée du journal (`/journal`, puis `/linkedin`)

1. Firmin donne ses notes de la semaine : ce qui a été fait, les problèmes, les décisions, les changements de statut, les incidents.
2. Claude Code présente son plan : numéro (le suivant), slug, composants, ADR et tags concernés, modifications du catalogue, ADR ou post-mortem à créer.
3. Après accord :
   - créer la branche `docs/journal-<nnn>` et le dossier depuis l'archetype ;
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
- **Passage à `running`** : `since`, `verified` (`backup` et `monitoring` dès qu'ils sont en place). Le build refuse le statut s'il manque une réponse.
- **Test de restauration réussi** : `backup.restore_tested`, sur indication de Firmin.
- **Retrait** : statut `retired` et `since`. La fiche reste en ligne, puisqu'elle fait partie de l'histoire du lab ; le composant sort du schéma.
- **Changement de topologie** (hôte, dépendances, réseau) : le schéma `lab-overview` est mis à jour dans la même PR.
- Toute évolution est mentionnée dans l'entrée du journal de la semaine.

### 16.3 Décision (`/adr`)

Numéro suivant. Statut `proposed` ou `accepted`. Firmin fournit le contexte, les options, la décision et les conséquences ; Claude Code met en forme et relie les composants. Si la nouvelle ADR en remplace une, l'ancienne est mise à jour dans la même PR (`status`, `superseded_by`).

### 16.4 Incident (`/postmortem`)

Rédigé dans la semaine de l'incident, à partir de la chronologie et des faits fournis par Firmin. Les actions correctives prennent la forme d'une liste de cases à cocher. L'entrée du journal de la semaine y renvoie. L'état des actions est mis à jour ensuite, au fil de leur réalisation.

### 16.5 Chaque mois (première semaine)

- Composants non vérifiés depuis plus de 60 jours (avertissements V14) : les revoir avec Firmin et mettre à jour `verified`.
- PR Dependabot : actions ; PaperMod selon le §16.6.
- Rapport des liens externes.
- Versions des outils (Hugo, gitleaks, lychee) : lire les notes de version, mettre à jour `tools.env`, vérifier que le build ne produit aucun nouvel avertissement.

### 16.6 Mise à jour de PaperMod

1. Lire les commits du thème depuis le commit épinglé : changements incompatibles, version minimale de Hugo.
2. Pour chaque fichier du registre (§11.7), comparer l'ancienne et la nouvelle version du thème et reporter les changements dans la surcharge.
3. Build, revue visuelle (deux langues, deux thèmes), fusion.

### 16.7 Changement d'architecture

Sections, schémas, validations, CI, outillage : mise à jour de ce document et ligne à l'historique des décisions (§17.2) dans la même PR. Si des URL changent, redirections.

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
| D1 | Vers quelle langue redirige `/` : `fr` ou `en` ? | **Tranchée le 14/10/2026 : `en`** (§17.2). Un recruteur non francophone ne lit pas une page en français, alors que l'inverse est rare dans l'IT. Ce choix reste réversible sans casser de lien (C2). | 1.1 |
| D2 | Que faire de l'article `proxmox-homelab-premiers-pas` (lab d'avant la reconstruction) : le supprimer ou l'archiver ? | **Tranchée le 14/10/2026 : supprimé** (§17.2). Le supprimer et expliquer la reconstruction dans « Le projet ». L'article décrit des VM exposées directement sur le réseau local, à l'opposé de la posture visée. | 1.2 |
| D3 | Repo du lab : nom, public ou privé ? | `FirminMoyen/homelab`, public, avec les secrets chiffrés (SOPS/age) : les fiches peuvent alors pointer vers le code (plan du lab, LD9). En attendant, `deploy.code` reste vide. | Liens « code » des fiches |
| D4 | Contact public : adresse principale ou alias dédié ? | **Tranchée le 28/10/2026 : adresse dédiée sur le domaine, `contact@firminmoyen.dev`, opérationnelle** (§17.2). Remplaçable en cas de spam. CV public sans adresse, téléphone ni date de naissance. | 5.3 |
| D5 | Supprimer `layouts-maison/` et `assets/css/main.css` ? | Oui : l'historique git les conserve. | 0.4 |
| D6 | Quels groupes d'infrastructure (identifiants, libellés, ordre) ? | **Tranchée le 25/10/2026 : `hardware`, `network`, `virtualization`** (§6.4, §17.2). Les autres groupes de la proposition seront ajoutés quand ils auront du contenu. | 2.1 (`data/groups.yaml`), pages de groupe |

### 17.2 Historique des décisions du site

| Date | Décision | Référence |
|---|---|---|
| 2026-10-12 | Sections accueil, infrastructure, services, devlog, about ; ADR sous infrastructure ; catalogue en données | Échange de cadrage |
| 2026-10-14 | Architecture v0.1 (ce document) | PR de l'étape 0.1 |
| 2026-10-14 | v0.2 : exploitation hors du repo (§16.9), sonde de disponibilité externe, repo du lab proposé (D3), lien vers le calendrier commun | Plan du lab |
| 2026-10-14 | v0.3 : structure page par page (`docs/structure.md`) ; menus dans le front matter et sections en brouillon tant qu'elles sont vides ; redirections par fichiers `static/` ; ordre du jour : 0.1, puis phase 1, puis 0.2 à 0.4 | `docs/structure.md` |
| 2026-10-14 | v0.3 validée et commitée ; annexe B retirée (`CLAUDE.md` devient la source) ; `.claude/rules/` et permissions (§14.3, précisions sur `gh api` et `git push`) ; tableau du §11.3 corrigé ; `docs/structure.md` v0.1 ajouté | PR de l'étape 0.1 |
| 2026-10-14 | D1 : `/` redirige vers `en`. Langues en sous-dossier ; anciennes URL redirigées par `static/`, `/tags/` et `/categories/` comprises ; pages `…/page/1/` et flux RSS en exception (`docs/structure.md` §3.6) ; `/404.html` racine fourni par `static/404.html` (P16) | PR de l'étape 1.1 |
| 2026-10-14 | D2 : ancien article supprimé, ses URL redirigées. Arborescence de `docs/structure.md` §5 en brouillon ; menus dans le front matter ; taxonomies `tags` et `certifications` ; fil d'Ariane ; services tiers désactivés (`[privacy]`) | PR de l'étape 1.2 |
| 2026-10-14 | Archetypes de dossier `devlog`, `postmortem`, `adr`, `services` ; numéro tiré du nom du dossier ; champs du post-mortem inconnus laissés vides (Annexe A.2) | PR de l'étape 1.3 |
| 2026-10-14 | Flux RSS : lien vers le flux du devlog sous le pied de page (`extend_footer.html`, registre §11.7) plutôt qu'un bouton à côté du titre de chaque section ; premiers fichiers `i18n/` et `site.css` | PR de l'étape 1.4 |
| 2026-10-14 | La section « Devlog » devient « Journal » (`/<lang>/journal/`, archetype `journal`, skill `/journal`, branches `docs/journal-<nnn>`) ; le §17.2 devient « Historique des décisions du site » pour éviter le double sens. Les lignes précédentes gardent le terme de leur date | PR de l'étape 1.5 |
| 2026-10-14 | Infrastructure, Services et Journal publiées avant leur contenu, avec une description et un message « en construction » : le menu montre les cinq sections dès maintenant. Les sous-pages restent en brouillon ; redirections passées à leur cible finale | PR de l'étape 1.6 |
| 2026-10-14 | Groupes d'infrastructure non décidés : les 7 pages de groupe sont retirées, la liste du §6.4 devient une proposition et D6 est ouverte | PR de l'étape 1.7 |
| 2026-10-14 | Accueil (§5.1) refondu et implémenté en avance (5.2a) : blocs masqués sans données, stack limitée aux composants en service ou en construction (les prévus sont comptés), ligne d'état avec la dernière semaine plutôt que la dernière vérification, `params.profile` | PR de l'étape 5.2a |
| 2026-10-14 | Exception à §9.2 décidée par Firmin : contenu d'exemple fictif publié pour montrer le rendu, sous un bandeau « site en construction » sur chaque page ; Décisions d'architecture et Incidents publiées « en construction ». À retirer au plus tard en 3.3 | PR du bandeau |
| 2026-10-15 | L'accueil ne présente plus que le projet ; tout ce qui concerne Firmin (profil, CV, certifications, contact) passe sur la page « À propos de moi » / « About me », déplacée de `/about/` à `/about-me/` (alias Hugo pour `/fr/about/` et `/en/about/`, redirection `static/` pour `/about/`) | PR `feat/about-me` |
| 2026-10-15 | Style « éditorial » (proposition C) : palette claire et sombre redéfinie dans `site.css`, chiffres clés en cartes sur l'accueil, thème par défaut selon le système du visiteur, bascule clair/sombre conservée | PR `feat/style-editorial` |
| 2026-10-15 | Gouvernance (décidée et modifiée par Firmin) : une branche et une PR par session de travail, un commit à chaque changement, PR en fin de session sur demande ; Claude Code peut fusionner sur demande explicite (`gh pr merge` retiré des interdits, confirmation à chaque fois) | PR `feat/style-editorial` |
| 2026-10-25 | D6 : trois groupes d'infrastructure, dans cet ordre : `hardware` (Matériel / Hardware), `network` (Réseau / Network), `virtualization` (Virtualisation / Virtualization). Les autres groupes de la proposition du §6.4 seront ajoutés quand ils auront du contenu ; aucun groupe de services tant qu'aucun service n'existe | PR `docs/first-public-content` |
| 2026-10-25 | Fin de l'exception à §9.2 : contenu d'exemple retiré, vraies données publiées (catalogue, groupes, feuille de route, ADR-0001 et 0002, journal 001), bandeau « site en construction » désactivé | PR `docs/first-public-content` |
| 2026-10-25 | Feuille de route sans dates (§6.7) : `started` et `finished` retirés du schéma, la chronologie vit dans le journal ; l'entrée 001 couvre tout ce qui a été fait avant le 25/10/2026 | PR `docs/first-public-content` |
| 2026-10-25 | Schémas conçus dans Claude Design au lieu de D2 (§11.6) : canvas privé validé par Firmin, export SVG par langue et par thème via `scripts/diagrams/`. Premier schéma : `lab-overview` sur l'accueil | PR `docs/first-public-content` |
| 2026-10-25 | Noms publics des nœuds : PVE1 et PVE2, seuls utilisés sur le site et dans ce repo (les noms internes restent dans le repo privé du lab). Identifiants du catalogue alignés : `pve1`, `pve2` (matériel), `proxmox-pve1` (hyperviseur). Exception à l'historique immuable : ADR-0002 et journal 001, publiés le jour même et avant l'annonce du site, sont réécrits avec ces noms. Switch corrigé : 5 ports. Schémas `lab-network` et `lab-physical`, shortcode `diagram`, export par `scripts/diagrams/render.py` ; accueil élargi à `--nav-width` pour la lisibilité du schéma. Exceptions de publication sur l'arrivée d'Internet (§10) | PR `docs/diagrams-pve-naming` |
| 2026-10-25 | Section Incidents repassée en brouillon tant qu'aucun incident n'existe. Titre des entrées du journal : « Semaine N — … » (« Week N — … »), prérempli par l'archetype ; le préfixe S01 disparaît de l'accueil | PR `docs/diagrams-pve-naming` |
| 2026-10-25 | Feuille de route affichée sur la page Infrastructure (shortcode `roadmap`, livré en avance sur 5.2) ; compteurs par statut retirés de l'accueil ; résumé explicite (`summary`) pour les pages de groupe | PR `docs/diagrams-pve-naming` |
| 2026-10-25 | Sauvegardes et supervision : plus mentionnées sur le site tant qu'elles ne sont pas en place ; `backup` et `monitoring` deviennent optionnels dans le catalogue (§6.3) | PR `docs/diagrams-pve-naming` |
| 2026-10-25 | Stack de l'accueil : titres de groupe plus marqués et seuls cliquables (vers la page du groupe) ; composants listés sans lien | PR `docs/diagrams-pve-naming` |
| 2026-10-25 | Nouvelle section Divers (`/misc/`, menu 45, archetype `misc`) pour les articles qui n'entrent ni dans l'infrastructure ni dans les services ; premier article : objectifs et contraintes du projet. Accueil : texte d'introduction réécrit | PR `docs/diagrams-pve-naming` |
| 2026-10-28 | Refonte « regard recruteur » (décisions de Firmin) : Claude Code rédige la prose à partir des faits existants, sous la validation de Firmin (§9.1, C8) ; P2 précisé : la prose peut citer les faits importants (modèles, nombre de nœuds…) si elle reste cohérente avec `data/catalog/`, source de vérité des statuts ; style (§9.5) : paragraphes humains, termes techniques expliqués une fois, détail dans « Détails techniques », pas de répétition, résultats vérifiés plutôt qu'intentions | PR `feat/refonte-site` |
| 2026-10-28 | Journal narratif : nouveau gabarit (Annexe A.1, archetype `journal`, §5.5) : titre en tournant ou en question, chapeau, un à trois récits, « Ce que j'en retiens » (mots de Firmin), « La suite », encadré « En bref » ; champs du front matter inchangés. Exception à §9.3 : semaine 1 réécrite en récit, mêmes faits, erratum conservé (site pas encore partagé). « Ce que j'en retiens » retirée des entrées 001 et 002 en attendant les mots de Firmin | PR `feat/refonte-site` |
| 2026-10-28 | Identité sur l'accueil (§5.1) : titre du site « Firmin Moyen · Homelab », auteur dans les méta, ligne d'identité (nom, administrateur systèmes junior, poste recherché en Belgique ou au Luxembourg), boutons « CV » et « Me contacter ». Le site ne mentionne pas d'aide à la rédaction | PR `feat/refonte-site` |
| 2026-10-28 | Ancien lab présenté au passé (2022-2026 : cluster Proxmox en haute disponibilité, supervision Prometheus et Grafana, services auto-hébergés), sans détail, sur À propos de moi, le CV HTML, Le projet et le journal ; la raison du redémarrage est donnée dans les mots de Firmin. L'agent IA n'est mentionné que brièvement : le récit porte sur la zone isolée | PR `feat/refonte-site` |
| 2026-10-28 | D4 tranchée : `contact@firminmoyen.dev`, opérationnelle. Un seul paramètre, `params.contactEmail`, utilisé par À propos de moi (partial `profile/contact.html`, ancre `#contact`, à la place du shortcode `contact`), la rubrique Contact du CV HTML (`kind: email`) et le pied de page | PR `feat/refonte-site` |
| 2026-10-28 | Navigation : Services repassée en brouillon tant qu'aucun service n'existe ; section Divers et archetype `misc` supprimés ; page « Le projet » (`/project/`, menu 15, §5.9), qui reprend l'article « Objectifs et contraintes du projet » mis à jour, avec alias depuis `/misc/` et `/misc/project-goals-constraints/` ; index des taxonomies non générés tant qu'ils sont vides (`disableKinds`, §5.8), redirection `/tags/` vers `/fr/` ; menu qui passe à la ligne sur mobile (§11.5) | PR `feat/refonte-site` |
| 2026-10-28 | Pied de page du site dans `extend_footer.html` (nom, contact, code source, RSS, « sans cookies ni traceurs », crédit Hugo et PaperMod sans lien de suivi), celui de PaperMod masqué (`hideFooter`, §11.7) ; image Open Graph par langue (§11.1) ; nom de composant traduisible (`name: {fr, en}`, §6.2), « Cluster Proxmox » / « Proxmox cluster » ; pages de groupe en trame ouverture, Détails techniques, Limites et évolutions (§5.2, Annexe A.4) ; index des ADR sans le paragraphe sur les statuts ; feuille de route : « Zones réseau et zone isolée » (fait) et « Automatiser le lab avec Ansible » (prévu) | PR `feat/refonte-site` |
| 2026-10-29 | À propos de moi et CV sans doublon (décision de Firmin, §5.7) : le CV dit *quoi* (seule référence factuelle : compétences, dates, missions, formation, certifications), À propos de moi dit *qui* (parcours en un paragraphe qui renvoie au CV, homelab, façon de travailler, ce que je cherche, contact). Liste « Mes compétences » retirée d'À propos de moi ; bloc Certifications retiré (partial `profile/certifications.html`, ses chaînes i18n et ses règles CSS supprimés) ; `data/certifications.yaml` conservé, plus lu par aucun template (§6.6) | PR `feat/refonte-site` |
| 2026-10-29 | Pas de point-virgule dans la prose du site, en français comme en anglais (décision de Firmin, §9.5) : remplacé par un point, une virgule, un deux-points ou une liste, sans changement de sens. Exception à §9.3 : le retrait s'applique aussi aux ADR acceptées (0001, 0002) et aux entrées du journal déjà écrites (001, 002). Commentaire de l'archetype `journal` (et Annexe A.1) aligné | PR `feat/refonte-site` |
| 2026-10-29 | À propos de moi retravaillée (décision de Firmin, §5.7) : section « Ce que je cherche » retirée (la ligne `availability` porte le poste recherché), « Ma façon de travailler » réécrite en liste courte de principes, texte découpé en paragraphes courts et espacement des titres, paragraphes et listes augmenté sur cette page (`.profile-pitch`) | PR `feat/refonte-site` |
| 2026-10-29 | Monitoring avant l'automatisation (décision de Firmin) : nouvelle étape « Mettre en place une stack de monitoring » dans `data/roadmap.yaml`, avant l'étape Ansible, qui devient « Automatiser le lab avec Ansible et Terraform » ; Le projet, le CV, le journal (index et entrée 002, pas encore publiée) alignés. Aucun outil de monitoring nommé pour le nouveau lab tant qu'il n'est pas choisi. Vocabulaire (§9.5) : « monitoring » ou « observabilité » au lieu de « supervision » dans les pages FR, ADR-0002 comprise (exception à §9.3) | PR `feat/refonte-site` |
| 2026-10-29 | Publication (§10) : les adresses de l'infrastructure du lab (passerelle OPNsense, nœuds Proxmox) deviennent publiables (décision de Firmin), les adresses des VM hors infrastructure restent interdites. Schéma réseau : « supervision » remplacé par « monitoring » (§9.5) | PR `feat/refonte-site` |
| 2026-10-29 | Accueil, bloc Stack (§5.1, §6.8) : briques par thème (Infrastructure, Réseau, Monitoring, Services) avec leur rôle et leur statut, depuis le nouveau `data/stack.yaml` ; partial `home/stack-list.html` supprimé. Monitoring avec Prometheus et Grafana passe « En cours » dans `data/roadmap.yaml` (décision de Firmin). Lab LPIC-1 annoncé « À venir », hors feuille de route. Libellé « À venir » au lieu de « Prévu » partout (badges, feuille de route, légendes des schémas) | PR `feat/refonte-site` |
| 2026-10-29 | Bloc Stack : une brique par outil (Prometheus, Grafana, Uptime Kuma, Ansible, Terraform), rôles réduits à quelques mots, quatre thèmes côte à côte sur desktop (deux sur tablette, un sur mobile). Uptime Kuma ajouté à l'étape monitoring. La VM de la zone isolée s'affiche « OpenBot server » : nom du logiciel publiable (exception décidée par Firmin, §10) | PR `feat/refonte-site` |
| 2026-10-29 | CV en PDF refaits depuis la page CV (styles d'impression, shortcode `site-link`) : adresse dédiée, contenu à jour, une page par langue ; les anciens PDF affichaient une adresse personnelle. Corrections de la relecture de publication : pare-feu de Proxmox « sur chaque VM des zones », plus de double authentification d'OPNsense « envisagée » (fait : aucune), monitoring « En cours » sur Le projet et le CV, légende anglaise des schémas « Running » | PR `feat/refonte-site` |
| 2026-10-29 | Feuille de route sur sa propre page, `/<lang>/roadmap/` (§5.10), hors du menu et atteinte par des liens, comme les décisions d'architecture (décision de Firmin). La page Infrastructure n'affiche plus la liste et y renvoie. Liens de l'accueil, de Le projet et du journal vers la nouvelle page, ancre `#lab-roadmap` retirée | PR `feat/site-sections` |
| 2026-10-29 | Infrastructure (§5.2) : « Matériel » devient « Infrastructure physique » (adresse inchangée), nouvelles pages Monitoring et Automatisation (ce qui est prévu, où en est l'étape), cartes de la vue d'ensemble avec le badge de la feuille de route (champ `roadmap` des pages). Le monitoring a sa page dans Infrastructure (exception à la frontière du §5.2). Services publiée (§5.4) avec OpenBot (en service) et Lab LPIC-1 (à venir), cartes avec badge (champ `status`). Bloc Stack : thèmes Monitoring et Services reliés à leurs pages, statuts des services lus dans leurs pages (champ `page`, §6.8). Décisions de Firmin | PR `feat/site-sections` |
| 2026-10-30 | Accueil : le premier paragraphe dit le but du lab, simuler une infrastructure d'entreprise, et « un petit labo » évite la répétition d'« infrastructure ». CV (§5.7) : « Portfolio : » devant le domaine du site, LinkedIn masqué à l'impression, PDF refaits. Photo de profil ronde sur À propos de moi et le CV, nouvelle exception de publication (§10). Décisions de Firmin | PR `feat/home-intro`, PR `fix/home-and-cv` |

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

Les gabarits ci-dessous montrent les fichiers tels que l'archetype les crée (`archetypes/`). L'archetype remplit la date et le numéro, et met `draft: true`. Les commentaires HTML guident la rédaction ; ils restent invisibles sur le site.

### A.1 Entrée du journal — `journal/<nnn>-<slug>/index.fr.md`

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

<!-- Titre : un tournant ou une question. Chapeau, sans titre : deux ou trois phrases (où en était le lab, ce qui a changé cette semaine). -->

<!--more-->

## Récit
<!-- Un à trois récits courts, chacun sous un titre parlant. Pour chacun : le problème, ce que j'ai essayé, ce que j'ai choisi et pourquoi (lien vers la décision), la limite que j'accepte. -->

## Ce que j'en retiens
<!-- Les mots de Firmin. Rubrique retirée tant qu'il ne les a pas donnés. -->

## La suite

## En bref {.brief}
<!-- Pour les techniciens. -->

- **Composants** : 
- **Étapes** : 
- **Décisions** : 
```

Rubriques en anglais : Story, What I take away, What's next, In brief (**Components**, **Steps**, **Decisions**). `<!--more-->` fait du chapeau le résumé affiché dans les listes ; `{.brief}` donne à « En bref » son encadré (§11.5). Gabarit en vigueur depuis le 28/10/2026 ; l'ancien (Objectif de la semaine, Réalisé, Problèmes et résolution, Décisions, Appris, Semaine prochaine) n'est plus utilisé.

### A.2 Post-mortem — `journal/incidents/pm-<nnn>-<slug>/index.fr.md`

```markdown
---
title: ""
date: 2026-11-05
draft: true
description: ""
pm: 1
incident_date:         # AAAA-MM-JJ, début de l'incident / start of the incident
severity:              # sev1 | sev2 | sev3
impact_minutes:
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

Rubriques en anglais : Why, Implementation, Operations, Limits and next steps.

Les pages de groupe d'infrastructure suivent depuis le 28/10/2026 une trame plus lisible : deux ou trois phrases d'ouverture sans titre (ce que c'est, pourquoi ça compte) ; une à quatre sections en langage simple, sous des titres parlants, où chaque terme technique est expliqué une fois ; « Détails techniques » (liste des faits) ; « Limites et évolutions ». En anglais : Technical details, Limits and next steps.
