---
title: "Hardware"
description: "The lab's machines: Hermes, running, and Atlas, planned."
draft: false
weight: 1
ShowReadingTime: false
ShowPostNavLinks: false
---

## Role in the lab

The lab relies on two Dell laptops. Hermes carries the lab's infrastructure and connectivity. Atlas will carry the workloads.

## Implementation

Hermes is running: Proxmox VE is installed directly on the hardware (see the Virtualization page). Atlas is not installed yet.

## Operations

Backups and monitoring are not in place yet: I have deferred them.

## Limits and next steps

Until Atlas is installed, Hermes is the lab's only node. Installing Proxmox VE on Atlas is the next step after the current one, before the two nodes are joined in a cluster.
