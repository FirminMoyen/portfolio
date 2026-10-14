---
title: ""
date: {{ now.Format "2006-01-02" }}
draft: true
description: ""
pm: {{ index (split .File.ContentBaseName "-") 1 | strings.TrimLeft "0" | int }}
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
