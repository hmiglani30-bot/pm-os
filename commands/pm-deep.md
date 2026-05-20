---
description: Full PM pipeline — all 11 stages including debate, validation, and eng alignment deck
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Agent
argument-hint: "[idea or topic]"
---

# PM-OS Deep Mode

This is a shortcut for `/pm-pipeline $ARGUMENTS --mode interactive --depth deep`.

Run the PM pipeline in **deep mode** for `$ARGUMENTS`. This is the full pipeline for high-stakes bets, new product areas, and cross-org alignment initiatives.

## What This Command Does

1. **Ask the user** (if not already provided in the argument):
   - One-sentence concept
   - Target customer/persona
   - Why now (what changed?)
   - Known competitors (if any)
   - Prototype style (default: Cloudscape)

2. **Run ALL 11 stages:**
   - Stage 0: Setup (create working directory)
   - Stage 0.5: Current State Audit (or Adjacent State Audit if greenfield)
   - Stage 1: Research (deep competitive analysis, capability evolution timelines)
   - Stage 2: PRD (full customer-first PRD with dual-scope boundary, 25 MECE FAQs)
   - Stage 3: Gandalf (adversarial strategy gate — 12 scored questions, max 3 rounds)
   - Stage 3.5: Adversarial Debate (5-round structured debate between 5 expert personas)
   - Stage 4: Designer (UX/experience design with Cloudscape component mapping)
   - Stage 5: Prototype (Spec Mode — reads design spec, production-faithful)
   - Stage 5.5: Validation Planner (assumption map, 5 usability tasks, go/pivot/kill criteria)
   - Stage 6: Launch Readiness (eng spec, sprint breakdown, acceptance criteria, rollout plan)
   - Stage 6.5: Eng Alignment Packager (30-min meeting doc + PPTX deck with demo script)

3. **All feedback loops run:**
   - Loop 1: Design → PRD (Stage 4→2): patch PRD with designed experience
   - Loop 2: Prototype → Design Critique (Stage 5→4): fidelity report if < 90%
   - Loop 3: Prototype → PRD Final (Stage 5→2): canonical prototype experience → prd-v[final]

4. **Generate PDFs** for every markdown artifact:
   - After each stage produces a `.md` file, convert it to PDF using the `pdf` skill
   - PDF naming: `[artifact-name].pdf` (e.g., `research-v1.pdf`, `prd-v1.pdf`)
   - Present both the MD (for pipeline consumption) and PDF (for human reading) to the user

5. **Generate PPTX** for eng alignment:
   - Stage 6.5 produces `eng-alignment-v1.pptx` in addition to the markdown + PDF

6. **Deliver to user:**
   - Present each artifact as it's produced (interactive — don't wait until the end)
   - For the prototype: validate it opens, check JS console, verify interactivity
   - At Stage 5.5: PAUSE for external validation (user runs interviews, usability tests)
   - Final summary: list all artifacts with links

## No Stages Skipped

Deep mode runs everything. Stage 7 (Post-Launch Evaluator) is the only deferred stage — it triggers 30+ days after GA or when the user says "evaluate launch."

## The Prompt This Command Sends to the Pipeline

When you type `/pm-deep AI Adoption Command Center`, this is equivalent to the orchestrator receiving:

```
Topic: AI Adoption Command Center
Mode: interactive
Depth: deep
Stages: 0 → 0.5 → 1 → 2 → 3 → 3.5 → 4 → 5 → 5.5 → 6 → 6.5
PDF output: yes (every markdown artifact gets a companion PDF)
PPTX output: yes (Stage 6.5)
Feedback loops: Loop 1 (4→2), Loop 2 (5→4), Loop 3 (5→2)
```

The orchestrator will:
1. Create `pipeline-ai-adoption-command-center/`
2. Run Current State Auditor → `current-state-v1.md` + `.pdf`
3. Run Researcher → `research-v1.md` + `.pdf`
4. Run PRD Writer → `prd-v1.md` + `.pdf`
5. Run Gandalf Gate → `gandalf-evaluation-v1.md` + `.pdf` → update PRD → `prd-v2.md` + `.pdf`
6. Run Adversarial Debate → `debate-v1.md` + `.pdf`
7. Run Designer → `design-spec-v1.md` + `.pdf` → [Loop 1] → `prd-v3.md` + `.pdf`
8. Run Prototype Builder → `prototype-v1.html` → [Loop 2] → [Loop 3] → `prd-v[final].md` + `.pdf`
9. Run Validation Planner → `validation-plan-v1.md` + `.pdf` → **PAUSE for external validation**
10. Run Launch Readiness → `launch-readiness-v1.md` + `.pdf`
11. Run Eng Alignment Packager → `eng-alignment-v1.md` + `.pdf` + `eng-alignment-v1.pptx`
12. Present all artifacts to the user

## Downgrade Path

At any point during the run, the user can say:
- **"go standard"** → skip Debate, Validation, Eng Alignment stages
- **"go quick"** → skip everything remaining, jump to prototype if not yet built
