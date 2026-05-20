# PSB Method — Reference

## Research Sources

### freeCodeCamp: How to Write a Good README File
- Lead with project title + one-line description
- Include: motivation/why, installation, usage, contributing, license
- Visuals (GIF/screenshot) after title, before text
- Keep concise — link to detailed docs elsewhere

### DEV.to: GitHub README Best Practices (60k+ Stars Analysis)
- 30-second readability test: visitors understand what + why in 30 seconds
- Feature tables beat bullet lists (scannable)
- Copy-paste quick start (2-3 lines max)
- Projects with 60k+ stars (AFFiNE, Supabase, Excalidraw) share: clear value prop + visual demo + 30-second setup + feature table
- Length sweet spot: 500-1500 words
- Common mistakes: wall of text, missing visuals, complex setup, no motivation, outdated info

### jehna/readme-best-practices
- Template structure: title, description, getting started, prerequisites, installing, tests, deployment, built with, contributing, authors, license, acknowledgments
- Use plain language assuming reader doesn't know your project

### Tilburg Science Hub
- Include: project description, methodology, repository overview, dependencies, how to run
- Motivation section: explain which problem is solved

### othneildrew/Best-README-Template
- Table of contents for long READMEs
- About The Project with screenshot
- Built With section listing technologies
- Getting Started with prerequisites and installation
- Roadmap with checkboxes
- Contact and acknowledgments

## PSB Method Synthesis

The PSB Method distills these sources into a three-section framework:

| Section | Maps To | Why First |
|---------|---------|-----------|
| **Problem** | Motivation, Why, About | Emotional hook — makes reader care |
| **Solution** | Description, Architecture, Built With | Conceptual model — makes reader understand |
| **Built** | Repository Overview, Features, Components | Proof — makes reader trust |

The key insight from the 60k+ star analysis: projects that front-load WHY before WHAT get dramatically more engagement. PSB enforces this ordering.

## Validation Criteria (from research)

1. **30-second test:** Can a first-time visitor understand what the project does and why in 30 seconds?
2. **Copy-paste test:** Can someone install and try it in under 5 lines of commands?
3. **Accuracy test:** Does every component/feature mentioned actually exist in the repo?
4. **Freshness test:** Are version numbers and descriptions current?
5. **Scanability test:** Can someone skim the README (headers + tables only) and get 80% of the information?
