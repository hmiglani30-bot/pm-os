# PM-OS

A Claude Code plugin that runs an 11-stage AI agent pipeline — taking a product idea from raw research through adversarial review to a working HTML prototype and eng-ready deck, all in one command.

## What PM-OS Is (and Isn't)

PM-OS is a **personal PM operating system** for senior PMs who use Claude Code. It automates the artifact-generation chain (research → PRD → design → prototype → eng package) while preserving context between stages. It is not a team collaboration tool, not a SaaS product, not a replacement for PM judgment. The pipeline generates artifacts and stress-tests them adversarially — the PM makes the decisions. It runs on Claude Code because the plugin system gives agents access to web research, file generation, and iterative prototyping in a single environment.

## The Problem

PMs spend weeks cycling between docs: writing research in one tool, drafting PRDs in another, getting feedback over email, hand-building mockups, then scrambling to package it all for an eng meeting. Each handoff loses context. Research findings don't make it into the PRD. PRD decisions don't survive into the prototype. By the time engineering sees it, the artifact is a telephone-game version of the original insight.

## The Solution

PM-OS replaces the multi-tool, multi-week workflow with a single pipeline command. Each stage is a specialized AI agent that reads the previous stage's output, produces a versioned artifact, and passes structured context forward. An adversarial gate (Gandalf) stress-tests the strategy with 12 scored questions before design begins. A second gate (Adversarial Debate) generates new ideas through structured argument. The prototype builder produces a working Cloudscape HTML demo — not a mockup, a clickable product. Every artifact is version-controlled with git commits per stage, so you can diff any two stages to see exactly what changed.

The pipeline runs in two modes — **interactive** (pause after each stage for human review) or **autonomous** (run end-to-end, flag open questions at the end) — and three depth levels: **quick** (research + PRD + prototype), **standard** (adds adversarial gate + design + launch readiness), or **deep** (full 11-stage pipeline with debate, validation, eng alignment).

## What's Built

### Pipeline Stages (11 stages, executed sequentially)

| Stage | Agent | What It Does | Version | Depth |
|-------|-------|-------------|---------|-------|
| 0 | Setup | Creates working directory, pipeline state, stage-notes log | — | all |
| 0.5 | Current State Auditor | Examines existing product UX, maps pain points, inventories competitor interaction patterns | v0.2.0 | all |
| 1 | Researcher | Deep competitive analysis, capability evolution timelines, interaction pattern benchmarking | v0.5.0 | all |
| 2 | PRD Writer | Customer-first PRD with thesis preservation, context reconciliation, evidence tags, self-eval sidecar | v3.0.0 | all |
| 3 | Gandalf | Adversarial strategy gate — 12 scored questions, hybrid rubric + evidence scoring, max 3 rounds | v0.3.0 | standard+ |
| 3.5 | Adversarial Debate | 5-round structured debate between 5 expert personas, produces new ideas through argument | v0.1.0 | deep |
| 4 | Designer | UX/experience design with product navigation map, 5-minute demo script, Cloudscape component mapping | v0.3.0 | standard+ |
| 5 | Prototype Builder | Single-file HTML prototype in Vision Mode (maximalist, demoable) or Spec Mode (production-faithful) | v0.3.0 | all |
| 5.5 | Validation Planner | Assumption map, prototype test plan (5 usability tasks), go/pivot criteria for external validation | v0.1.0 | deep |
| 6 | Launch Readiness | Eng handoff: sprint breakdown, acceptance criteria, RACI, phased rollout, monitoring, rollback plan | v0.2.0 | standard+ |
| 6.5 | Eng Alignment Packager | 30-minute meeting package — structured doc + PPTX deck with live prototype walkthrough script | v0.1.0 | deep |
| 7 | Post-Launch Evaluator | Compares production metrics against predictions, produces iteration backlog (deferred, 30+ days post-GA) | v0.1.0 | deep |

### Utility Skills

| Skill | What It Does | Version |
|-------|-------------|---------|
| Research Librarian | Shared web research capability callable by any agent | v0.1.0 |
| Visual Explainer | Explanation-led interactive HTML explainers with typed concept maps, structural analogies, scenario quizzes, and narrative arcs | v1.0.0 |
| Context Fusion | Synthesizes context across all pipeline artifacts, flags contradictions and gaps | v0.1.0 |
| Validation Planner | Assumption mapping, prototype test plans, go/pivot criteria for external validation | v0.1.0 |
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

## Commands

### Pipeline Commands (run multiple stages)

| Command | What It Does |
|---------|-------------|
| `/pm-pipeline [topic]` | Full pipeline orchestrator — supports `--mode` and `--depth` flags |
| `/pm-deep [topic]` | Shortcut for full 11-stage pipeline (interactive, deep) |
| `/pm-standard [topic]` | Shortcut for 7-stage pipeline (skips debate, eng alignment, post-launch) |
| `/pm-fast [topic]` | Shortcut for 5-stage pipeline (research → PRD → prototype) |

### Individual Skill Commands (run one stage)

| Command | What It Does |
|---------|-------------|
| `/research [topic]` | Run competitive/market research |
| `/write-prd [topic]` | Write a PRD from research artifacts |
| `/build-prototype [topic]` | Build a single-file HTML prototype |
| `/debate [topic or PRD]` | Run multi-persona adversarial debate |
| `/visual-explainer [topic]` | Generate interactive HTML visual explainer |
| `/context-fusion [topic]` | Synthesize context across all pipeline artifacts |

## How It Works

```
/pm-pipeline [topic] --mode interactive --depth deep
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
                                          └→ Stage 5.5 (Validation Checkpoint) → validation-plan-v1.md
                                               └→ Stage 6 (Launch Readiness) → launch-readiness-v1.md
                                                    └→ Stage 6.5 (Eng Alignment) → eng-alignment-v1.md + .pptx
```

Four feedback loops run as non-blocking side effects — the pipeline always moves forward. Every stage commits to git, so you can `git diff` between any two stages.

## Who Reads What

Different stakeholders consume different pipeline artifacts:

| Stakeholder | Primary Artifact | What to Focus On |
|------------|-----------------|-----------------|
| PM (you) | All artifacts | Full pipeline — this is your operating system |
| Engineering Lead | `launch-readiness-v1.md` | Eng spec, sprint breakdown, acceptance criteria, tech debt |
| Designer | `design-spec-v1.md` + `prototype-v1.html` | Navigation map, interaction states, Cloudscape mapping |
| Director / VP | `eng-alignment-v1.pptx` | 10-slide deck with demo walkthrough and "The Ask" |
| Other PMs | `research-v1.md` + `prd-v1.md` | Market context, competitive landscape, JTBD, solution lineage |
| QA / Test | `launch-readiness-v1.md` | Acceptance criteria (GIVEN/WHEN/THEN), phased rollout gates |

## Quick Start

```bash
# Clone the repo
git clone https://github.com/hmiglani30-bot/pm-os.git

# Option A: Install as a Claude Code plugin (recommended)
# In Claude Code, run: /install-plugin /path/to/pm-os

# Option B: Copy to your Claude Code plugins directory
cp -r pm-os ~/.claude/plugins/pm-os
```

Then in Claude Code or Cowork:
```
/pm-pipeline AI Adoption Control Plane --mode interactive --depth deep
/pm-pipeline session replay improvements --mode autonomous --depth quick
```

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

## Usage by Platform

**Cowork (Desktop App):** Install the plugin, then use slash commands directly in chat. Pipeline artifacts appear as downloadable files. Best for interactive mode where you review each stage.

**Claude Code (CLI):** Install with `/install-plugin /path/to/pm-os`. Run commands from any directory — artifacts are written to the current working directory. Best for autonomous mode and deep pipeline runs.

**Dispatch:** Start a task with the pipeline command. Dispatch routes it to a Cowork session with the mounted folder. Good for kicking off long runs while you do other work.

**Chat (claude.ai):** Skills are available if the plugin is installed to your account. Limited to skills that don't require file system access (research, debate). Prototyping and artifact generation work better in Cowork or Claude Code.

## Contributing

To add a new pipeline stage:
1. Create `skills/[stage-name]/SKILL.md` with frontmatter (name, description, version)
2. Add reference files in `skills/[stage-name]/references/` if needed
3. Wire it into `commands/pm-pipeline.md` at the appropriate stage position
4. Add context pruning rules (what inputs it receives, what outputs it produces)
5. Run the pipeline end-to-end to validate

To improve an existing skill: edit the SKILL.md, bump the version, and add an entry to the Eval Learnings Log at the bottom of the file.
