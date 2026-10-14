---
title: ""
date: {{ now.Format "2006-01-02" }}
draft: true
description: ""
adr: {{ index (split .File.ContentBaseName "-") 1 | strings.TrimLeft "0" | int }}
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
