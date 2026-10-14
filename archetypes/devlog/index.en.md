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

## Goal of the week

## Done

## Problems and fixes
<!-- For each problem: symptom, diagnosis, cause, fix. -->

## Decisions
<!-- One sentence per decision, with the link to its ADR. -->

## Learned

## Next week
