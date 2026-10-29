---
title: "OpenBot"
description: "A server for autonomous AI agents, which I experiment with out of curiosity in an isolated zone of the lab."
summary: "A server for autonomous AI agents, which I experiment with out of curiosity in an isolated zone of the lab."
draft: false
weight: 1
# Badge de la carte, hors feuille de route (architecture §5.4) : running | building | planned.
status: running
ShowReadingTime: false
ShowPostNavLinks: false
---

OpenBot runs autonomous AI agents: they run commands themselves on the machine that hosts them. I experiment with it out of curiosity, in a zone of the lab isolated from the rest.

## Why an isolated zone

The software gives its agents full access to the machine it runs on. Protection therefore has to come from outside: OpenBot runs in a separate virtual machine, under an account without administrator rights, in a zone that reaches the internet but sees neither the home nor the rest of the lab (see [Network]({{< relref "/infrastructure/network" >}})).

## Technical details

- **Machine**: an Ubuntu Server VM on PVE2, in the isolated zone `10.42.50.0/24`.
- **Administration**: over SSH, with keys only.
- **Isolation**: checked from the VM. The internet answers, neither the home network nor the infrastructure zone does.

## Limits and next steps

OpenBot is still a preview release. How to keep it up to date is not decided yet.
