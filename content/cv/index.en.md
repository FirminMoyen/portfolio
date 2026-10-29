---
title: "Resume"
description: "Resume of Firmin Moyen, systems administrator: experience, skills, education and certification."
ShowReadingTime: false
ShowPostNavLinks: false
headline: "Systems Administrator · Windows and Linux infrastructure, automation, DevOps"
sidebar:
  - title: "Contact"
    items:
      - kind: email
      - kind: linkedin
      - kind: website
      - text: "Belgium"
      - text: "Driving licence (B)"
      - text: "Available immediately"
        strong: true
  - title: "Skills"
    items:
      - label: "Systems"
        text: "Windows Server, Active Directory, GPO, Linux, Proxmox VE, VMware ESXi, Docker"
      - label: "Automation and CI/CD"
        text: "Terraform, Ansible, GitHub Actions, GitLab CI/CD, Jenkins, Git"
      - label: "Monitoring and ticketing"
        text: "Prometheus, Grafana, osTicket"
      - label: "Networking and services"
        text: "DNS (Bind9), Apache, Nginx, Tailscale, Cisco CCNA-level training"
      - label: "Scripting"
        text: "Bash, Python, JavaScript"
      - label: "Methodologies"
        text: "Agile, Scrum"
  - title: "Education"
    items:
      - label: "Bachelor's degree in Information Technology"
        text: "EPHEC, Louvain-la-Neuve · 2019 – 2024"
      - label: "Physics"
        text: "UCLouvain · 2018 – 2019"
  - title: "Certification"
    items:
      - label: "LPIC-1 (Linux)"
        text: "In progress, target end of 2026"
  - title: "Languages"
    items:
      - text: "French: native"
      - text: "English: fluent (C1)"
---

## Profile

Junior systems administrator with a bachelor's degree in Information Technology (EPHEC). Experience administering Windows Server and Active Directory across a multi-site estate, automating infrastructure (Terraform, Ansible, CI/CD) and setting up monitoring (Prometheus, Grafana). Ran a high-availability Proxmox cluster from 2022 to 2026. Now rebuilding my homelab from scratch and documenting it every week. Looking for a systems administrator role in Belgium or Luxembourg.

## Professional experience

### International experience in Canada (Working Holiday)

*Montreal, Canada · 09/2025 – 09/2026*

- Home theatre sales advisor at Best Buy, then counter agent at Desjardins. Customer service in a bilingual French and English environment.

### Systems Administrator, IT support team

*Municipality of Virton, Belgium · 11/2024 – 08/2025*

- Administered 2 Active Directory domains: users, groups, Group Policy (GPO) and Windows Servers.
- Maintained and supported a fleet of 200+ workstations across 4 sites, plus around ten servers.
- Designed and deployed a monitoring (Prometheus, Grafana) and ticketing (osTicket) solution as Infrastructure as Code (Terraform, Ansible, GitHub Actions), improving incident tracking and speeding up resolution.

### Intern, project team

*BCE · Broadcasting Center Europe, Luxembourg-Kirchberg · 11/2023 – 06/2024*

- Developed a Python plugin for the internal IPAM and containerised the application with Docker.
- Designed and implemented the team's Git workflow and CI/CD pipelines.

### Intern, IT Expertise in Health Data team

*Luxembourg Institute of Health · 02/2023 – 06/2023*

- Built a monitoring dashboard for the National Cancer Registry database (R, web technologies).

## Personal project: homelab

### Documented rebuild

*Since 10/2026 · {{< site-link >}}*

- Rebuilt from scratch, documented every week in French and English: journal, architecture decisions.
- Two Proxmox VE nodes in a cluster, an OPNsense firewall that isolates the lab from the home network and splits it into zones.
- Remote access via Tailscale (WireGuard VPN), with no services exposed to the internet.
- In progress: monitoring with Prometheus, Grafana and Uptime Kuma, then automation with Ansible and Terraform.

### First homelab

*2022 – 2026*

- High-availability Proxmox VE cluster, monitoring with Prometheus and Grafana, self-hosted services.
- Wiped entirely in October 2026 to document everything from the start and rebuild on solid foundations.
