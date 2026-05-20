---
description: Standard PM pipeline — research through launch readiness with adversarial gate
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Agent
argument-hint: "[idea or topic]"
---

# PM-OS Standard Mode

This is a shortcut for `/pm-pipeline $ARGUMENTS --mode interactive --depth standard`.

Run the PM pipeline in **standard mode** for `$ARGUMENTS`. This is the production path for serious feature work that needs eng handoff.

## What This Command Does

1. **Ask the user** (if not already provided in the argument):
   - One-sentence concept
   - Target customer/persona
   - Why now (what changed?)
   - Known competitors (if any)
   - Prototype style (default: Cloudscape)

2. **Run these stages:**
   - Stage 0: Setup (create working directory)
   - Stage 0.5: Current State Audit (or Adjacent State Audit if greenfield)
   - Stage 1: Research (competitive landscape, market context)
   - Stage 2: PRD (full customer-first PRD with dual-scope boundary, 25 MECE FAQs)
   - Stage 3: Gandalf (adversarial strategy gate — 12 scored questions, pass threshold 10/12)
   - Stage 4: Designer (UX/experience design with Cloudscape component mapping)
   - Stage 5: Prototype (Spec Mode — reads design spec, production-faithful)
   - Stage 6: Launch Readiness (eng spec, sprint breakdown, acceptance criteria, rollout plan)

3. **Feedback loops that run:**
   - Loop 1: Design → PRD (Stage 4→2): patch PRD with designed experience
   - Loop 2: Prototype → Design Critique (Stage 5→4): fidelity report if < 90%
   - Loop 3: Prototype → PRD Final (Stage 5→2): canonical prototype experience → prd-v[final]

4. **Generate PDFs** for every markdown artifact:
   - After each stage produces a `.md` file, convert it to PDF using the `pdf` skill
   - PDF naming: `[artifact-name].pdf` (e.g., `research-v1.pdf`, `prd-v1.pdf`, `gandalf-evaluation-v1.pdf`)
   - Present both the MD (for pipeline consumption) and PDF (for human reading) to the user

5. **Deliver to user:**
   - Present each artifact as it's produced (interactive — don't wait until the end)
   - For the prototype: validate it opens, check JS console, verify interactivity
   - Final summary: list all artifacts with links

## Stages Skipped (and Why)

| Skipped Stage | Why |
|--------------|-----|
| Adversarial Debate (Stage 3.5) | Reserved for high-stakes bets — standard features don't need multi-persona debate |
| Validation Planner (Stage 5.5) | External validation is for deep-mode cross-org initiatives |
| Eng Alignment Packager (Stage 6.5) | Launch Readiness doc is sufficient for standard eng handoff |
| Post-Launch (Stage 7) | Nothing launched yet — runs deferred |

## The Prompt This Command Sends to the Pipeline

When you type `/pm-standard AI Adoption Command Center`, this is equivalent to the orchestrator receiving:

```
Topic: AI Adoption Command Center
Mode: interactive
Depth: standard
Stages: 0 → 0.5 → 1 → 2 → 3 → 4 → 5 → 6
PDF output: yes (every markdown artifact gets a companion PDF)
Feedback loops: Loop 1 (4→2), Loop 2 (5→4), Loop 3 (5→2)
```

The orchestrator will:
1. Create `pipeline-ai-adoption-command-center/`
2. Run Current State Auditor → produce `current-state-v1.md` + `current-state-v1.pdf`
3. Run Researcher → produce `research-v1.md` + `research-v1.pdf`
4. Run PRD Writer → produce `prd-v1.md` + `prd-v1.pdf`
5. Run Gandalf Gate → produce `gandalf-evaluation-v1.md` + `gandalf-evaluation-v1.pdf` → update PRD → `prd-v2.md` + `prd-v2.pdf`
6. Run Designer → produce `design-spec-v1.md` + `design-spec-v1.pdf` → [Loop 1] patch PRD → `prd-v3.md` + `prd-v3.pdf`
7. Run Prototype Builder (Spec Mode) → produce `prototype-v1.html` → [Loop 2] fidelity report → [Loop 3] patch PRD → `prd-v[final].md` + `prd-v[final].pdf`
8. Run Launch Readiness → produce `launch-readiness-v1.md` + `launch-readiness-v1.pdf`
9. Present all artifacts to the user

## Upgrade Path

At any point during or after the run, the user can say:
- **"go deep"** → continues with Adversarial Debate (Stage 3.5), Validation Planner (Stage 5.5), Eng Alignment (Stage 6.5)

The pipeline resumes from where it stopped — it does not re-run completed stages.

## Downgrade Path

If mid-run the user realizes standard is overkill:
- **"go quick"** → skip remaining stages after current one completes, jump to prototype if not yet built
