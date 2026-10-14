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

## Context
<!-- The problem to solve and the constraints: hardware, budget, security, time. -->

## Options considered

### Option 1 — …
<!-- Pros, cons. -->

### Option 2 — …

## Decision

## Consequences
<!-- Positive, negative, what to monitor or revisit. -->
