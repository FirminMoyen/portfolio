---
title: "About me"
description: "Firmin Moyen, junior systems administrator: background, homelab, how I work and contact."
ShowReadingTime: false
ShowPostNavLinks: false
aliases: ["/about/"]
menus:
  main:
    identifier: about
    weight: 50
headline: "Systems Administrator · Windows and Linux infrastructure, automation, DevOps"
availability: "Belgium · Looking for a role in Belgium or Luxembourg · French: native, English: fluent (C1) · Available immediately"
---

I am a junior systems administrator. I have administered two Active Directory domains, supported a fleet of more than 200 workstations across four sites, and deployed monitoring as Infrastructure as Code.

Today, I am rebuilding my homelab from scratch, documenting it on this site.

## My background

I did my bachelor's degree in Information Technology at EPHEC, in Louvain-la-Neuve. My two internships, in Luxembourg, were on the development side: at the Luxembourg Institute of Health, then at BCE (Broadcasting Center Europe), where I also worked with containers and CI/CD pipelines.

Then came hands-on work in the field, as a systems administrator in the IT support team of the Municipality of Virton. I then spent a year in Canada on a Working Holiday visa, working in customer service, in French and in English.

The details of each role are in my [resume]({{< relref "/cv" >}}).

## My homelab

This is where I learn by doing. I ran a first lab from 2022 to 2026. In October 2026, I wiped it entirely to build a new one: it was a good opportunity to document everything from the start and to rebuild on solid foundations.

I am building this new lab with hardware I already have. It runs on two Proxmox VE nodes joined in a cluster, behind an OPNsense firewall that isolates it from my home network and splits it into zones. I administer it remotely through a VPN, with nothing exposed to the internet.

It also helps me prepare for the LPIC-1, which I am aiming for by the end of 2026. [The project]({{< relref "/project" >}}) says more about its goals and framework, and the [journal]({{< relref "/journal" >}}) tells how it is being built, week by week.

## How I work

- Document as I go.
- Justify my important choices and what they imply, in [architecture decisions]({{< relref "/infrastructure/decisions" >}}) or in the journal.
- Check with tests rather than assume.
- Not be afraid of getting things wrong: that is what this lab is for.
- Fit the project as well as I can to the limits of the hardware.
