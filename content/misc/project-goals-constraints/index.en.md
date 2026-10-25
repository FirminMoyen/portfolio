---
title: "Project goals and constraints"
date: 2026-10-25
draft: false
description: "Why I am building this homelab, where I want to take it, and the framework I set for myself."
tags: []
---

## Why this homelab

I am building this homelab to learn by doing. Reading documentation is not enough: you have to install, break, fix, and understand why. The lab also helps me prepare for my certifications, starting with the LPIC-1, which I am aiming for by the end of 2026.

It is also a showcase. Everything I do in it is documented here, to show concretely what I can do and how I work.

## My goals

- **Apply professional practices**, with security first. The lab is built like a company's infrastructure, not like a sandbox.
- **Move forward step by step.** Each technology is learned, set up and documented before moving on to the next.
- **Document everything publicly**, in French and in English: a journal entry every week, and a written architecture decision for every important choice.

## Where I want to go

Today, the lab runs on a first Proxmox VE node, behind an OPNsense firewall, with remote access through a VPN. Next:

- a two-node Proxmox cluster;
- Kubernetes;
- a full GitOps approach;
- a mixed Windows and Linux environment that reproduces company practices.

The order of the steps after the cluster is not set yet. The [roadmap]({{< relref "/infrastructure" >}}#lab-roadmap) shows where I am.

## The framework I set for myself

- **Hardware I already had**: two Dell laptops and a small switch. It is a constraint, but also a good exercise: getting the most out of limited resources.
- **Nothing is exposed to the internet.** I reach the lab remotely through a VPN, with no open port.
- **Limited time.** I prefer steady progress to fast progress.
- **What gets published is reviewed.** Before it reaches this site, every piece of information from the lab goes through a review, so that no sensitive detail gets out.
