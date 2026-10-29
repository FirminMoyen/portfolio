---
title: "Week {{ index (split .File.ContentBaseName "-") 0 | strings.TrimLeft "0" | int }} — "
date: {{ now.Format "2006-01-02" }}
draft: true
description: ""
week: {{ index (split .File.ContentBaseName "-") 0 | strings.TrimLeft "0" | int }}
components: []
adrs: []
tags: []
certifications: []
---

<!-- Title: a turning point or a question. Lead, without a heading: two or three sentences (where the lab stood, what changed this week). -->

<!--more-->

## Story
<!-- One to three short stories, each under a telling heading. For each: the problem, what I tried, what I chose and why (link to the decision), the limit I accept. -->

## What I take away
<!-- Firmin's own words. Section removed until he has given them. -->

## What's next

## In brief {.brief}
<!-- For technical readers. -->

- **Components**: 
- **Steps**: 
- **Decisions**: 
