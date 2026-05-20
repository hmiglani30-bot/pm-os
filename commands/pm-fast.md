---
description: Quick PM pipeline — research, PRD, and prototype in one shot
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Agent
argument-hint: "[idea or topic]"
---

# PM-OS Fast Mode

This is a shortcut for `/pm-pipeline $ARGUMENTS --mode interactive --depth quick`.

Run the PM pipeline in **quick mode** for `$ARGUMENTS`. This is the fast path for exploring ideas, internal pitches, and early-stage thinking.

## What This Command Does

1. **Ask the user** (if not already provided in the argument):
   - One-sentence concept
   - Target customer/persona
   - Why now (what changed?)
   - Known competitors (if any)
   - Prototype style (default: Cloudscape)

2. **Run these stages only:**
   - Stage 0: Setup (create working directory)
   - Stage 0.5: Current State Audit (or Adjacent State Audit if greenfield)
   - Stage 1: Research (competitive landscape, market context)
   - Stage 2: PRD (one-pager style — shorter than deep mode, focus on problem + solution + scope)
   - Stage 5: Prototype (Vision Mode — reads PRD directly, no design spec)

3. **Generate PDFs** for every markdown artifact:
   - After each stage produces a `.md` file, convert it to PDF using the `pdf` skill
   - PDF naming: `[artifact-name].pdf` (e.g., `research-v1.pdf`, `prd-v1.pdf`)
   - Present both the MD (for pipeline consumption) and PDF (for human reading) to the user

4. **Deliver to user:**
   - Present each artifact as it's produced (interactive — don't wait until the end)
   - For the prototype: validate it opens, check JS console, verify interactivity
   - Final summary: list all artifacts with links

## Stages Skipped (and Why)

| Skipped Stage | Why |
|--------------|-----|
| Gandalf (Stage 3) | Quick exploration doesn't need adversarial gate |
| Adversarial Debate (Stage 3.5) | No debate needed for early-stage |
| Designer (Stage 4) | Prototype reads PRD directly |
| Validation Planner (Stage 5.5) | No external validation for quick explorations |
| Launch Readiness (Stage 6) | Not heading to eng yet |
| Eng Alignment (Stage 6.5) | Not heading to eng yet |
| Post-Launch (Stage 7) | Nothing launched |

## The Prompt This Command Sends to the Pipeline

When you type `/pm-fast AI Adoption Command Center`, this is equivalent to the orchestrator receiving:

```
Topic: AI Adoption Command Center
Mode: interactive
Depth: quick
Stages: 0 → 0.5 → 1 → 2 → 5
PDF output: yes (every markdown artifact gets a companion PDF)
Feedback loops: none
```

The orchestrator will:
1. Create `pipeline-ai-adoption-command-center/`
2. Run Current State Auditor → produce `current-state-v1.md` + `current-state-v1.pdf`
3. Run Researcher → produce `research-v1.md` + `research-v1.pdf`
4. Run PRD Writer → produce `prd-v1.md` + `prd-v1.pdf`
5. Run Prototype Builder (Vision Mode, no design spec) → produce `prototype-v1.html`
6. Present all artifacts to the user

## Upgrade Path

At any point during or after the run, the user can say:
- **"go deeper"** → continues with Gandalf (Stage 3), then Designer (Stage 4), then re-runs Prototype with design spec
- **"go standard"** → adds Gandalf + Designer + Launch Readiness
- **"go deep"** → runs remaining stages (Debate, Validation, Eng Alignment)

The pipeline resumes from where it stopped — it does not re-run completed stages.
