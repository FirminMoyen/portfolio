---
title: "The project"
description: "Why I am rebuilding this homelab from scratch, where it stands, where it is going, and the framework I set for myself."
draft: false
ShowReadingTime: false
ShowPostNavLinks: false
aliases: ["/misc/", "/misc/project-goals-constraints/"]
menus:
  main:
    identifier: project
    weight: 15
---

This homelab is my training ground as a systems administrator: two laptops and a small switch, organised like a company's infrastructure. I have been rebuilding it from scratch since October 2026, and every week I share what I do in it, what pushes back and what I decide.

## Why a homelab

I am building this homelab to learn by doing. Reading documentation is not enough: you have to install, break, fix, and understand why. The lab also helps me prepare for my certifications, starting with the LPIC-1, which I am aiming for by the end of 2026.

It is also a showcase: everything I do in it is documented here, to show concretely what I can do and how I work.

## Why start again from scratch

From 2022 to 2026, I ran a first homelab: a high-availability Proxmox cluster, monitored with Prometheus and Grafana, with self-hosted services. In October 2026, I wiped it entirely. It was a good opportunity to document everything from the start and to rebuild on solid foundations.

## Where the lab stands

Today, two Proxmox VE nodes, PVE1 and PVE2, form a cluster. An OPNsense firewall separates the lab from the home network and splits it into zones, each with its own rules. I administer everything remotely through a VPN, with nothing exposed to the internet. One of the zones is isolated from the rest: there, out of curiosity, I experiment with an autonomous AI agent.

The details are on the [Infrastructure]({{< relref "/infrastructure" >}}) page, and the journey so far is in the [journal]({{< relref "/journal" >}}).

## What's next

In progress: monitoring the lab with Prometheus, Grafana and Uptime Kuma. So far, I have installed and configured everything by hand: the step after that will be automating the lab with Ansible and Terraform. Further ahead, in an order not set yet: Kubernetes, a full GitOps approach, and a mixed Windows and Linux environment that reproduces company practices. The [roadmap]({{< relref "/roadmap" >}}) shows where I am.

## The framework I set for myself

The lab applies professional practices, with security first: it is built like a company's infrastructure, not like a sandbox. I move forward step by step: each technology is learned, set up and documented before moving on to the next.

I work with hardware I already had, with no budget: two Dell laptops and a small switch. It is a constraint, but also a good exercise: getting the most out of limited resources. Nothing is exposed to the internet. My time is limited, and I prefer steady progress to fast progress.

Everything is documented publicly, in French and in English: a journal entry every week, and every important choice written down with the options set aside, in an architecture decision or in the journal. Before it reaches this site, every piece of information from the lab goes through a review, so that no sensitive detail gets out.
