---
title: ""
date: {{ now.Format "2006-01-02" }}
draft: true
description: ""
week: {{ index (split .File.ContentBaseName "-") 0 | strings.TrimLeft "0" | int }}
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
