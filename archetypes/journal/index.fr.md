---
title: "Semaine {{ index (split .File.ContentBaseName "-") 0 | strings.TrimLeft "0" | int }} — "
date: {{ now.Format "2006-01-02" }}
draft: true
description: ""
week: {{ index (split .File.ContentBaseName "-") 0 | strings.TrimLeft "0" | int }}
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
