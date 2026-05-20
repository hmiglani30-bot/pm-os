# PM-OS

A Claude Code plugin that runs a 10-stage AI agent pipeline — taking a product idea from raw research through adversarial review to a working HTML prototype and eng-ready deck, all in one command.

## The Problem

PMs spend weeks cycling between docs: writing research in one tool, drafting PRDs in another, getting feedback over email, hand-building mockups, then scrambling to package it all for an eng meeting. Each handoff loses context. Research findings don't make it into the PRD. PRD decisions don't survive into the prototype. By the time engineering sees it, the artifact is a telephone-game version of the original insight.

## The Solution

PM-OS replaces the multi-tool, multi-week workflow with a single pipeline command. Each stage is a specialized AI agent that reads the previous stage's output, produces a versioned artifact, and passes structured context forward. An adversarial gate (Gandalf) stress-tests the strategy with 12 scored questions before design begins. A second gate (Adversarial Debate) generates new ideas through structured argument. The prototype builder produces a working Cloudscape HTML demo — not a mockup, a clickable product. Every artifact is version-controlled with git commits per stage, so you can diff any two stages to see exactly what changed.

The pipeline runs in two modes: **interactive** (pause after each stage for human review) or **autonomous** (run end-to-end, flag open questions at the end).

## What's Built

### Pipeline Stages (10 stages, executed sequentially)

| Stage | Agent | What It Does | Version |
|-------|-------|-------------|---------|
| 0 | Setup | Creates working directory, pipeline state, stage-notes log | — |
| 0.5 | Current State Auditor | Examines existing product UX, maps pain points, inventories competitor interaction patterns | v0.2.0 |
| 1 | Researcher | Deep competitive analysis, capability evolution timelines, interaction pattern benchmarking | v0.5.0 |
| 2 | PRD Writer | Customer-first PRD with dual-scope boundary (Eng v1 + Proto v1), 25 MECE FAQs, solution lineage | v0.4.0 |
| 3 | Gandalf | Adversarial strategy gate — 12 scored questions, hybrid rubric + evidence scoring, max 3 rounds | v0.3.0 |
| 3.5 | Adversarial Debate | 5-round structured debate between 5 expert personas, produces new ideas through argument | v0.1.0 |
| 4 | Designer | UX/experience design with product navigation map, 5-minute demo script, Cloudscape component mapping | v0.3.0 |
| 5 | Prototype Builder | Single-file HTML prototype in Vision Mode (maximalist, demoable) or Spec Mode (production-faithful) | v0.3.0 |
| 6 | Launch Readiness | Eng handoff: sprint breakdown, acceptance criteria, RACI, phased rollout, monitoring, rollback plan | v0.2.0 |
| 6.5 | Eng Alignment Packager | 30-minute meeting package — structured doc + PPTX deck with live prototype walkthrough script | v0.1.0 |
| 7 | Post-Launch Evaluator | Compares production metrics against predictions, produces iteration backlog (deferred, 30+ days post-GA) | v0.1.0 |

### Utility Skills

| Skill | What It Does | Version |
|-------|-------------|---------|
| Research Librarian | Shared web research capability callable by any agent | v0.1.0 |
| Visual Explainer | Interactive HTML explainers with narration, diagrams, quizzes, and progressive disclosure | v0.2.0 |
| README Writer | Generates and validates READMEs using the PSB Method (Problem-Solution-Built) | v0.1.0 |

### Reference Files

| Reference | Location | Purpose |
|-----------|----------|---------|
| FAQ Framework | `skills/prd-writer/references/faq-framework.md` | Calibrates the 25 MECE FAQ categories and complexity tiers |
| Scoring Methodology | `skills/gandalf/references/scoring-methodology.md` | Gandalf's hybrid rubric + evidence scoring system |
| Consumer Design Patterns | `skills/designer/references/consumer-patterns.md` | Spotify + Stripe hybrid patterns |
| Enterprise Design Patterns | `skills/designer/references/enterprise-patterns.md` | Salesforce + Datadog hybrid patterns |
| Cloudscape Components | `skills/designer/references/cloudscape-components.md` | AWS Cloudscape Design System component catalog |
| Eval Method | `skills/researcher/references/eval-method.md` | Research quality self-evaluation rubric |
| PSB Method | `skills/readme-writer/references/psb-method.md` | README best practices research synthesis |
| Component Library | `skills/visual-explainer/references/component-library.md` | Visual explainer HTML component patterns |

## How It Works

```
/pm-pipeline [topic] --mode interactive
```

```
Stage 0 (Setup)
  └→ Stage 0.5 (Current State Audit) → current-state-v1.md
       └→ Stage 1 (Research) → research-v1.md
            └→ Stage 2 (PRD) → prd-v1.md
                 └→ Stage 3 (Gandalf Gate) → gandalf-evaluation-v1.md
                      └→ Stage 3.5 (Adversarial Debate) → debate-v1.md + debate-v1.pdf
                           └→ Stage 4 (Designer) → design-spec-v1.md
                                ├→ [parallel] Loop 1: Design patches PRD experience section
                                └→ Stage 5 (Prototype) → prototype-v1.html
                                     ├→ [side effect] Loop 2: Fidelity report → Designer
                                     └→ Loop 3: Prototype patches PRD → prd-v[final].md
                                          └→ Stage 6 (Launch Readiness) → launch-readiness-v1.md
                                               └→ Stage 6.5 (Eng Alignment) → eng-alignment-v1.md + .pptx
```

Four feedback loops run as non-blocking side effects — the pipeline always moves forward. Every stage commits to git, so you can `git diff` between any two stages.

## Quick Start

1. Install this as a Claude Code plugin (copy the repo to your plugins directory or install via `.plugin` file)
2. Run: `/pm-pipeline AI Adoption Control Plane --mode interactive`
3. The pipeline creates a working directory and walks you through each stage

## Example Output

The `eval-runs/ai-adoption-control-plane/` directory contains a complete pipeline run that produced:

| Artifact | Words | Description |
|----------|-------|-------------|
| `research-v1.md` | ~8,000 | Competitive landscape, capability evolution, interaction pattern benchmarking |
| `prd-v2.md` | ~7,000 | Customer-first PRD with dual-scope boundary and 25 FAQs |
| `gandalf-evaluation-v2.md` | ~3,000 | 12-question adversarial evaluation with scores |
| `design-spec-v3.md` | ~6,000 | Cloudscape UX spec with navigation map and demo script |
| `prototype-v3.html` | 100KB | Working single-file Cloudscape HTML prototype |
| `launch-readiness-v3.md` | ~5,800 | Sprint breakdown, RACI, rollout plan, monitoring |

## Architecture Credits

| Pattern | Source | How It's Used |
|---------|--------|---------------|
| Discovery & competitive analysis | [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | Researcher's progressive specificity and assumption surfacing |
| Context pruning & file-based state | [sdi2200262/agentic-project-management](https://github.com/sdi2200262/agentic-project-management) | Pipeline state management, stage-notes cross-stage learning log |
| Adversarial scoring | [coleam00/adversarial-dev](https://github.com/coleam00/adversarial-dev) | Gandalf's rubric + evidence hybrid scoring, max retry limits |

## Contributing

To add a new pipeline stage:
1. Create `skills/[stage-name]/SKILL.md` with frontmatter (name, description, version)
2. Add reference files in `skills/[stage-name]/references/` if needed
3. Wire it into `commands/pm-pipeline.md` at the appropriate stage position
4. Add context pruning rules (what inputs it receives, what outputs it produces)
5. Run the pipeline end-to-end to validate

To improve an existing skill: edit the SKILL.md, bump the version, and add an entry to the Eval Learnings Log at the bottom of the file.
