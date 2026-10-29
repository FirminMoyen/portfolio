---
title: "Journal"
description: "The lab's rebuild told week by week: what I built, what pushed back, what I chose and why."
draft: false
menus:
  main:
    identifier: journal
    weight: 40
---

Every week, I share here where the lab stands: what I built, what pushed back, what I chose and why. Each entry ends with an "In brief" box that sums up the components, the steps and the decisions.

## The story so far

From 2022 to 2026, I ran a first homelab. In October 2026, I wiped it entirely: it was a good opportunity to document everything from the start and to rebuild on solid foundations.

Week 1 lays the foundations on a single machine: a hypervisor, a firewall that isolates the lab from the home, and remote access with nothing exposed to the internet. Week 2 adds a second machine, joins the two in a cluster, and splits the network into zones, without the VLANs the hardware refused. Next chapter: a monitoring stack, before automating the lab with Ansible and Terraform.
