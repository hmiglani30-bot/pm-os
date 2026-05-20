# PM Pipeline Plugin

Multi-agent PM workflow pipeline for product development. Runs 6 stages sequentially, with adversarial quality gates and versioned artifacts at every step.

## Pipeline Stages

| Stage | Agent | Input | Output |
|-------|-------|-------|--------|
| 1 | Researcher | Topic | `research-v1.md` |
| 2 | Strategy & PRD Writer | Research | `prd-v1.md` (25 MECE FAQs) |
| 3 | Gandalf (Strategy Gate) | PRD | `gandalf-evaluation-v1.md` (hybrid scoring) |
| 4 | UX/Experience Designer | PRD + Evaluation | `design-spec-v1.md` |
| 5 | Prototype Builder | Design Spec | `prototype-v1.html` (Cloudscape) |
| 6 | Launch Readiness | All artifacts | `launch-readiness-v1.md` |

## Utility Agent
- **Research Librarian** — shared web research capability callable by any agent

## Usage

```
/pm-pipeline transaction search improvements
/pm-pipeline session replay cross-sell --mode autonomous
```

**Modes:**
- `interactive` (default) — pauses after each stage for human review
- `autonomous` — runs end-to-end, flags open questions at the end

## Design Patterns

- **Consumer products** → Spotify + Stripe hybrid (personalization + trust-first)
- **Enterprise products** → Salesforce + Datadog hybrid (contextual surfacing + information density)
- **AWS products** → Always Cloudscape Design System

## Components

- 1 orchestrator command (`/pm-pipeline`)
- 7 skills (researcher, prd-writer, gandalf, designer, prototype-builder, launch-readiness, research-librarian)
- Design pattern references (consumer, enterprise, Cloudscape)
- Gandalf scoring methodology reference
- 25 MECE FAQ framework reference

## Architecture Credits

- Discovery & competitive analysis patterns: phuryn/pm-skills
- Context-pruning & file-based state: sdi2200262/agentic-project-management
- Adversarial scoring system: coleam00/adversarial-dev
