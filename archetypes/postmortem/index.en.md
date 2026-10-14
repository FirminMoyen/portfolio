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

## Summary

## Impact
<!-- What stopped working, for how long, whether data was lost. -->

## Timeline

| Time | Event |
|---|---|

## Detection
<!-- How the incident was noticed, and what would have shown it sooner. -->

## Root cause

## Resolution

## Corrective actions
- [ ] Action — due date

## Takeaways
