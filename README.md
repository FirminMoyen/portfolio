# firminmoyen.dev

Source code of [firminmoyen.dev](https://firminmoyen.dev), the showcase of my homelab: a small lab rebuilt from scratch since October 2026 to simulate a company's infrastructure, and documented every week in French and English.

## What's inside

- **The project**: why this homelab, and the framework I set for myself.
- **Roadmap**: the lab's steps, done, in progress and upcoming.
- **Infrastructure**: physical infrastructure, network, virtualization, monitoring, automation, and the architecture decisions.
- **Services**: what runs in the lab.
- **Journal**: one entry per week.
- **About me** and **Resume**, with a PDF version.

## How it's built

- [Hugo](https://gohugo.io) 0.165 (extended edition) and the [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme, as an unmodified submodule.
- Bilingual static site (French and English, the root redirects to English), with no cookies and no trackers.
- The lab's data (components, roadmap, home page stack) lives in `data/` and feeds the pages.
- Deployed to GitHub Pages by GitHub Actions on every push to `main`.
- The site's code (templates, styles, scripts, CI) is written with [Claude Code](https://claude.com/claude-code): I describe what I want, then review and approve every change before it is merged.

## Run it locally

```bash
git clone --recurse-submodules https://github.com/FirminMoyen/portfolio.git
cd portfolio
hugo server
```

The site is served at http://localhost:1313. `hugo server -D` also shows drafts.

## Repository layout

| Folder | Contents |
|---|---|
| `content/` | Pages and journal entries, one `.fr.md` and one `.en.md` file per page |
| `data/` | Component catalog and groups, roadmap, home page stack block, certifications |
| `layouts/` | The site's own Hugo templates |
| `assets/` | Styles, diagrams, images |
| `static/` | Files served as is: PDF resumes, icons, redirects from old URLs |
| `scripts/diagrams/` | SVG diagram generation |
| `docs/` | Site architecture and page-by-page structure (in French) |

## Contact

contact@firminmoyen.dev · [LinkedIn](https://www.linkedin.com/in/firmin-moyen-01724b264/)
