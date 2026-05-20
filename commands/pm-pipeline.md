---
description: Run the multi-agent PM pipeline (interactive or autonomous, at variable depth)
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Agent
argument-hint: "[feature-or-topic] [--mode interactive or autonomous] [--depth quick or standard or deep]"
---

# PM Pipeline Orchestrator

Run the full PM pipeline for `$ARGUMENTS`. Parse the arguments:
- The feature/topic is everything before flags (or the entire argument if no flags)
- `--mode interactive` (default): pause after each stage for human review
- `--mode autonomous`: run all stages end-to-end, flag open questions for human at the end
- `--depth quick|standard|deep` (default: deep): controls how many stages run

## Pipeline Depth Modes

Not every product question needs 10 stages. The `--depth` flag selects a stage subset:

| Depth | Stages Run | Use When | Artifacts Produced |
|-------|-----------|----------|-------------------|
| **quick** | 0 → 0.5 → 1 → 2 → 5 | Exploring an idea, quick prototype, internal pitch | current-state, research, one-pager PRD, prototype (Vision Mode) |
| **standard** | 0 → 0.5 → 1 → 2 → 3 → 4 → 5 → 6 | Serious feature work, eng handoff needed | All quick artifacts + Gandalf gate, design spec, launch readiness |
| **deep** | All 10 stages | High-stakes bets, cross-org alignment, new product areas | Full pipeline including debate, eng alignment deck, post-launch eval |

### Depth Behavior Rules
- **quick** skips Gandalf, Debate, Designer, Launch Readiness, Eng Alignment, Post-Launch. The Prototype Builder still runs in Vision Mode but reads the PRD directly (no design spec). Feedback loops 1-3 are skipped.
- **standard** skips Adversarial Debate (Stage 3.5), Eng Alignment Packager (Stage 6.5), and Post-Launch Evaluator (Stage 7). All feedback loops run.
- **deep** runs everything. This is the default.
- If no `--depth` flag is provided, default to **deep**.
- The user can upgrade depth mid-run: "go deeper" at any interactive pause triggers the remaining stages from the current point.

## Pipeline Architecture

11 stages (7 primary + 4 half-stages), executed sequentially (Stage 7 is deferred). Each stage produces a versioned artifact in the working directory. Feedback loops run as post-stage side effects (non-blocking) — the pipeline always moves forward. After each stage, an incremental git commit is made and cross-stage notes are appended to `stage-notes.md`.

### Stage 0: Setup
1. Create a working directory: `pipeline-[topic-slug]/`
2. Create `pipeline-state.md` with: topic, mode, timestamp, status per stage, feedback loop tracking
3. Create `stage-notes.md` — cross-stage learning log (see State Management below)
4. Read any existing artifacts if resuming (resume from last complete stage — see Resume Protocol)

### Stage 0.5: Current State Audit
Invoke the `current-state-auditor` skill. Pass the topic + any existing product assets (screenshots, HTML source, docs, known pain points).
- Output: `current-state-v1.md` — what exists today, user pain map, adjacent product inventory, grounding constraints
- If truly greenfield (no existing product): produces a lighter "Adjacent State Audit" of related features
- The Grounding Constraints section is a required input for Stage 1
- **After completion:** Append key findings to `stage-notes.md` under `## Stage 0.5 Notes`

### Stage 1: Research
Invoke the `researcher` skill. Pass the topic + `current-state-v1.md` (Grounding Constraints section is required reading).
- Output: `research-v1.md` — competitor landscape, capability evolution, quantitative data, market context
- The researcher uses the `research-librarian` skill for web lookups
- The researcher MUST read the Grounding Constraints from Stage 0.5 before starting web research
- **After completion:** Append key findings to `stage-notes.md` under `## Stage 1 Notes`

### Stage 2: Strategy & PRD
Invoke the `prd-writer` skill. Pass `research-v1.md` as input.
- Output: `prd-v1.md` — customer-first PRD with persona, JTBD, problem depth, solution, 25 MECE FAQs
- The PRD is a living document — Stages 3, 4, and 5 may patch it with feedback (see Feedback Loops)
- If interactive mode: pause and show the user the PRD, ask for feedback. Apply feedback → `prd-v2.md`
- **After completion:** Append key decisions to `stage-notes.md` under `## Stage 2 Notes`

### Stage 3: Gandalf (Strategy & Problem Gate)
Invoke the `gandalf` skill. Pass the latest PRD version.
- Gandalf asks 12 predefined critique questions about strategy/problem framing (including Q12: Product Completeness)
- PRD Writer agent must answer each question, researching further if needed (via research-librarian)
- Hybrid scoring: rubric (1-5 per dimension) + evidence (specific data cited)
- Max 3 rounds for the entire stage
- Pass threshold: 10/12 questions pass (score >= 3)
- Output: `gandalf-evaluation-v1.md` — scores, evidence, pass/fail verdict, open questions flagged for human
- If any questions remain unanswered after 3 rounds, flag them and MOVE FORWARD (pipeline never blocks)
- Update the PRD with Gandalf's approved changes → `prd-v[next].md`
- **After completion:** Append scores and flags to `stage-notes.md` under `## Stage 3 Notes`

### Stage 3.5: Adversarial Debate
Invoke the `adversarial-debate` skill. Pass the latest PRD + research + Gandalf evaluation.
- 5-round structured debate between 5 expert personas (Skeptic, Customer Advocate, Competitor Watcher, Builder's Advocate, Orchestrator)
- Output: `debate-v1.md` (1200+ words, feeds downstream) AND `debate-v1.pdf` (content-matched, human-readable)
- The debate is generative (produces new ideas through argument), not just evaluative (unlike Gandalf)
- Round 4 Convergence identifies consensus items, productive disagreements, resolved/unresolved concerns
- Round 5 produces ranked recommendations with confidence levels
- **PDF generation:** Use `md_to_pdf.py` to convert MD → PDF. Verify word count >= 1200 and PDF/MD content match.
- **After completion:** Append key findings to `stage-notes.md` under `## Stage 3.5 Notes`
- The debate does NOT modify the PRD — it informs subsequent stages (Designer reads the "Synthesis for Downstream Stages" section)

### Stage 4: UX/Experience Design
Invoke the `designer` skill. Pass the approved PRD + Gandalf evaluation + debate synthesis (from Stage 3.5).
- Sequence: first principles → reality check → checklist
- Output: `design-spec-v1.md` — end-to-end experience design, layout rationale, alternatives considered
- Same scoring pattern as Gandalf (hybrid scoring, 3 rounds max) but focused on experience quality
- If interactive mode: pause for human review
- **After completion:** Append design decisions to `stage-notes.md` under `## Stage 4 Notes`
- **Feedback (4→2):** After design spec is finalized, the Designer writes an "End-to-End Experience" section summarizing the designed user journey. The PRD Writer agent patches this into the PRD's experience section → `prd-v[next].md`. This runs in parallel with Stage 5 starting.

### Stage 5: Prototype
Invoke the `prototype-builder` skill in **Vision Mode** (default). Pass the approved design spec + PRD dual-scope table + Researcher interaction patterns.
- Vision Mode builds a maximalist prototype covering ALL Proto v1 scope (including placeholder pages for v2/v3 features)
- Output: `prototype-v1.html` — single-file Cloudscape HTML prototype with full navigation surface
- Validate: render check, JS error check, interactivity check, **demo script walkability check**, navigation surface comparison vs competitors
- If interactive mode: pause for human review and iteration
- **After completion:** Append fidelity results to `stage-notes.md` under `## Stage 5 Notes`
- **Feedback (5→4 critique):** After prototype is validated, the Prototype Builder emits a "Fidelity Report" comparing what was built vs what the design spec specified, with a fidelity score (0-100%). If fidelity score < 90%, the Designer reviews the report and updates the design spec to reconcile gaps → `design-spec-v[next].md`. This runs as a side effect, not a blocker.
- **Feedback (5→2 final):** After prototype is finalized (including any fidelity-driven updates), the Prototype Builder patches the PRD's "End-to-End Experience" section with the canonical prototype experience (what was actually built and validated) → `prd-v[final].md`. This is the last PRD update in the pipeline.

### Stage 5.5: Validation Checkpoint
Invoke the `validation-planner` skill. Pass the validated prototype + latest PRD + Gandalf flags.
- Output: `validation-plan-v1.md` — assumption map, prototype test plan (5 usability tasks), go/pivot criteria
- In interactive mode: pause for the PM to run external validation (user interviews, stakeholder reviews, usability tests). Pipeline resumes when the user provides results or says "proceed."
- In autonomous mode: emit the validation plan, flag "external validation pending" in pipeline-state.md, and proceed to Stage 6.
- **After completion:** Append validation plan summary to `stage-notes.md` under `## Stage 5.5 Notes`
- This stage does NOT validate the artifacts — it produces the plan for the PM to validate the product hypothesis externally.

### Stage 6: Launch Readiness
Invoke the `launch-readiness` skill. Pass all approved artifacts (using the latest versions, including feedback-patched PRD and design spec).
- Output: `launch-readiness-v1.md` — eng spec, acceptance criteria, phased rollout, success metrics, meeting deck outline
- **After completion:** Append key findings to `stage-notes.md` under `## Stage 6 Notes`

### Stage 6.5: Engineering Alignment Package
Invoke the `eng-alignment-packager` skill. Pass all pipeline artifacts (latest versions).
- Output: `eng-alignment-v1.md` (structured 30-minute meeting doc with demo script) AND `eng-alignment-v1.pptx` (10-12 slide presentation deck)
- Distills the full pipeline output (~31K words across 6+ artifacts) into a 30-minute meeting package
- Includes live prototype walkthrough script with exact clicks and talking points
- "The Ask" section makes the meeting actionable (go/no-go, eng lead assignment, spike scope)
- **After completion:** Append summary to `stage-notes.md` under `## Stage 6.5 Notes`

### Stage 7: Post-Launch Evaluation (DEFERRED)
Invoke the `post-launch-evaluator` skill. This stage does NOT run automatically after Stage 6.

**Trigger conditions (any one):**
- User says "evaluate launch", "post-launch review", "how did it do", "did it work", or "post-mortem metrics"
- A scheduled task fires 30+ days after GA date recorded in `pipeline-state.md`

**Context pruning:** Stage 7 receives only:
- `launch-readiness-v[N].md` — Sections 5 (Phased Rollout), 11 (Success Metrics), and 13 (Risk Register) only
- `prd-v[final].md` — JTBD list and North Star metric only
- Post-launch metrics provided by the user or fetched from production telemetry
- Incident/feedback log (if available)

Do NOT pass full artifacts. Strip everything except the sections listed above before invoking the skill.

- Output: `post-launch-eval-v1.md` — verdict, metric scorecard, rollout gate audit, risk calibration, JTBD validation, iteration backlog
- **Feedback (7→1, next cycle):** When the Iteration Backlog contains ≥1 item, the orchestrator offers to start a new pipeline cycle. The backlog seeds the next cycle's Stage 1 (Researcher) with the highest-impact item as "Decision to Inform." See Loop 4 below.

## Feedback Loops

Feedback loops are post-stage side effects. They do NOT block the primary pipeline sequence. Where possible, feedback patches run in parallel with the next stage.

### Loop 1: Design → PRD (Stage 4→2)

| Property | Value |
|----------|-------|
| **Trigger** | Designer finalizes `design-spec-v1.md` |
| **What gets sent back** | An "End-to-End Experience" section: the designed user journey with key screens, interactions, transitions, and rationale for experience decisions |
| **What gets updated** | PRD → "End-to-End Experience" section. PRD Writer agent patches this section (adds if missing, replaces if exists) |
| **Version increment** | `prd-v[current+1].md` (e.g., if PRD is at v3 after Gandalf, this produces v4) |
| **Parallelism** | Runs in parallel with Stage 5 startup — prototype builder uses the design spec, not the PRD experience section |

### Loop 2: Prototype → Design Critique (Stage 5→4)

| Property | Value |
|----------|-------|
| **Trigger** | Prototype Builder completes validation of `prototype-v1.html` AND fidelity score < 90% |
| **What gets sent back** | "Fidelity Report": per-component comparison of design spec vs prototype, deviation list, fidelity score, recommended design spec updates |
| **What gets updated** | `design-spec-v[next].md` — Designer reviews the fidelity report and reconciles: updates specs that were intentionally simplified during build, flags specs that need prototype rework in a future iteration |
| **Version increment** | `design-spec-v[current+1].md` |
| **Parallelism** | Runs as a side effect after Stage 5 validation. Does NOT trigger a prototype rebuild — deviations are documented for future iterations |

### Loop 3: Prototype → PRD Final (Stage 5→2)

| Property | Value |
|----------|-------|
| **Trigger** | Prototype is finalized (validated, fidelity review complete if triggered) |
| **What gets sent back** | Canonical prototype experience: what the prototype actually does, key flows as built, any deviations from the design spec with rationale |
| **What gets updated** | PRD → "End-to-End Experience" section (replaces the Stage 4 version with the as-built version) |
| **Version increment** | `prd-v[final].md` — this is the last PRD version in the pipeline. Marked as `[final]` in pipeline-state.md |
| **Parallelism** | Must complete before Stage 6 starts — Launch Readiness needs the final PRD |

### Loop 4: Post-Launch → Research (Stage 7→1, next cycle)

| Property | Value |
|----------|-------|
| **Trigger** | Post-Launch Evaluator produces Iteration Backlog with ≥1 item |
| **What gets sent back** | Iteration Backlog + Risk Calibration results + JTBD validation verdicts |
| **What it seeds** | Next cycle's Stage 1 (Researcher) receives the backlog as scoping input. The Researcher's "Decision to Inform" is pre-populated from the highest-impact backlog item. |
| **Version lineage** | `post-launch-eval-v1.md` → `launch-readiness-v[N].md` → `prd-v[final].md` — full traceability across cycles |
| **Pipeline state update** | `pipeline-state.md` gains `## Post-Launch Evaluation` with metric scorecard summary, verdict, and pointer to next cycle's pipeline directory |

### Feedback Loop Ordering

```
Stage 0.5 completes → git commit → append stage-notes
  └─ Stage 1 starts (Researcher reads Grounding Constraints)

Stage 1 completes → git commit → append stage-notes
  └─ Stage 2 starts

Stage 2 completes → git commit → append stage-notes
  └─ Stage 3 starts

Stage 3 completes → git commit → append stage-notes
  └─ Stage 3.5 starts (Adversarial Debate)

Stage 3.5 completes → git commit → append stage-notes
  └─ Stage 4 starts (Designer reads debate synthesis)

Stage 4 completes → git commit → append stage-notes
  ├─ [parallel] Loop 1 fires (4→2): patch PRD with designed experience
  └─ [parallel] Stage 5 starts: build prototype from design spec

Stage 5 completes → git commit → append stage-notes
  ├─ [side effect] Loop 2 fires (5→4): fidelity report, update design spec if < 90%
  └─ [after Loop 2] Loop 3 fires (5→2): patch PRD with canonical prototype experience → prd-v[final].md

Stage 5.5 starts (Validation Checkpoint) → git commit → append stage-notes
  └─ In interactive mode: PAUSE for external validation. In autonomous mode: flag and continue.

Stage 6 starts after Loop 3 completes (needs final PRD) → git commit → append stage-notes

Stage 6.5 starts (Eng Alignment Package) → git commit → append stage-notes

Stage 7 runs DEFERRED (user trigger or 30+ days post-GA)
  └─ [on completion] Loop 4 fires (7→1): iteration backlog seeds next cycle's Researcher
```

## State Management

After each stage completes:
1. Update `pipeline-state.md` with: stage completed, artifact version, scores (if applicable), timestamp
2. Version all artifacts (v1, v2, v3...) — never overwrite, always increment
3. Track feedback loop status: which loops have fired, which artifact versions they produced, fidelity score if applicable
4. Mark the PRD version lineage: which stage/loop produced each version (e.g., `prd-v3 [gandalf]`, `prd-v4 [design-feedback]`, `prd-v[final] [prototype-feedback]`)
5. If interactive mode: present the artifact to the user with a summary of what was produced
6. **Incremental git commit** (GNHF pattern): After each stage completes, commit the stage's artifacts with a descriptive message:
   ```
   git add [stage artifacts] pipeline-state.md stage-notes.md
   git commit -m "Stage [N]: [stage-name] complete — [1-line summary of output]"
   ```
   This creates a rollback point per stage. If a later stage fails or produces bad output, the user can `git log` to see exactly what each stage produced and `git diff` between stages.
7. **Append to `stage-notes.md`** (GNHF pattern): After each stage, append a brief section with:
   - Key decisions made
   - Surprising findings
   - What the next stage should pay attention to
   - Any corrections to assumptions from earlier stages
   This is the cross-stage learning log — later stages read earlier notes to benefit from accumulated context.

### stage-notes.md Format

```markdown
# Stage Notes — Cross-Stage Learning Log

## Stage 0.5 Notes (Current State Audit)
- [Key finding 1]
- [Key finding 2]
- **For Researcher:** [specific guidance]

## Stage 1 Notes (Research)
- [Key finding 1]
- [Surprising market data]
- **For PRD Writer:** [specific guidance]

## Stage 2 Notes (PRD)
...
```

Each stage reads ALL prior notes before starting. This prevents context loss between stages and enables later stages to course-correct based on earlier discoveries.

### Resume Protocol (GNHF pattern)

When resuming a pipeline (e.g., after a session timeout, error, or conversation restart):

1. Read `pipeline-state.md` to identify the last completed stage
2. Read `stage-notes.md` to reconstruct cross-stage context
3. Check git log: `git log --oneline` to verify artifact state matches pipeline-state
4. Resume from the NEXT stage after the last completed one — do not re-run completed stages
5. If the last stage is marked "IN_PROGRESS" in pipeline-state, re-run it from scratch (partial artifacts are unreliable)

This means the pipeline can survive context window exhaustion, session timeouts, and manual interruptions without losing progress.

### Feedback Loop State Tracking

`pipeline-state.md` includes a feedback section:
```
## Feedback Loops
| Loop | Status | Trigger Artifact | Output Artifact | Fidelity Score |
|------|--------|-----------------|-----------------|----------------|
| 4→2 (design→PRD) | pending/complete | design-spec-v1.md | prd-v4.md | — |
| 5→4 (prototype→design) | pending/complete/skipped | prototype-v1.html | design-spec-v2.md | 87% |
| 5→2 (prototype→PRD) | pending/complete | prototype-v1.html | prd-v[final].md | — |
| 7→1 (post-launch→research) | deferred/complete | post-launch-eval-v1.md | [next cycle pipeline dir] | — |
```

## Context Pruning (borrowed from agentic-pm)

When handing off between stages, pass ONLY what the next stage needs. Note: the PRD is a living document updated by feedback loops — always pass the latest version.

- Stage 0.5 gets: topic string + existing product assets (screenshots, HTML, docs)
- Stage 1 gets: current-state-v1.md (Grounding Constraints section required) + topic string
- Stage 2 gets: research-v1.md (full) + current-state (Pain Map summary)
- Stage 3 gets: latest prd version (full) + research-v1.md (summary only)
- Stage 3.5 gets: latest prd version (full) + research (full) + gandalf-evaluation (full)
- Stage 4 gets: latest prd version (full) + gandalf-evaluation (full) + debate synthesis section + research (summary)
- Stage 5 gets: design-spec (full) + prd (executive summary only)
- Loop 1 (4→2): design-spec "End-to-End Experience" section → PRD Writer
- Loop 2 (5→4): fidelity report (full) → Designer + design-spec (full)
- Loop 3 (5→2): prototype canonical experience summary → PRD Writer + latest prd version
- Stage 5.5 gets: prototype path + latest prd version (full) + gandalf-evaluation (flags section only)
- Stage 6 gets: all artifacts (executive summaries) + design-spec latest version (full) + prd-v[final] (full) + prototype path + validation-plan (if exists)
- Stage 6.5 gets: ALL artifacts (latest versions) — this is the terminal packaging stage, it reads everything
- Stage 7 gets: launch-readiness (Sections 5, 11, 13 only) + prd-v[final] (JTBD list + North Star only) + user-provided post-launch metrics + incident log (if available)
- Loop 4 (7→1, next cycle): iteration backlog + risk calibration + JTBD verdicts → next cycle's Researcher

## Autonomous Mode Governance

When running `--mode autonomous`, the pipeline makes decisions without pausing. This section classifies which decisions the model can make, which it proposes, and which require human approval.

### Model Decides (no pause)
- Proceed to next stage after current stage completes
- Proceed past failed Gandalf questions (flag them, move forward)
- Choose artifact version numbers
- Select which feedback loops to trigger based on scores
- Generate all artifacts and stage-notes entries
- Make git commits per stage

### Model Proposes (flags for human at end)
- Scope changes to PRD (additions or cuts discovered during later stages)
- Design spec deviations from PRD intent
- Prototype features that deviate from design spec (logged in fidelity report)
- Validation checkpoint findings that suggest pivot
- Any assumption with confidence < Medium

### Human Must Approve (pipeline pauses even in autonomous mode)
- Final go/no-go on launch readiness (Stage 6 completion)
- External validation results (Stage 5.5 — cannot be auto-generated)
- Merging iteration backlog into next pipeline cycle (Loop 4)

All flags are collected in `pipeline-state.md` under `## Autonomous Mode Flags` and presented as a summary when the pipeline completes.

## PDF Generation (Mandatory)

Every markdown artifact produced by any stage MUST have a companion PDF generated immediately after the markdown is written. This ensures human-readable output at every step.

### Rules
1. **When:** After each stage writes its `.md` artifact (and after any feedback-loop version bump produces a new `.md`)
2. **How:** Use the `pdf` skill to convert markdown → PDF
3. **Naming:** Same base name as the markdown file: `research-v1.md` → `research-v1.pdf`, `prd-v[final].md` → `prd-v[final].pdf`
4. **Delivery:** In interactive mode, present BOTH the MD link and PDF link to the user after each stage
5. **Git:** PDFs are committed alongside their markdown source in the same stage commit
6. **Scope:** Applies to ALL depth modes (quick, standard, deep)

### What Gets a PDF

| Artifact | Stage | Gets PDF? |
|----------|-------|-----------|
| `current-state-v[N].md` | 0.5 | Yes |
| `research-v[N].md` | 1 | Yes |
| `prd-v[N].md` (every version) | 2 + feedback loops | Yes |
| `gandalf-evaluation-v[N].md` | 3 | Yes |
| `debate-v[N].md` | 3.5 | Yes |
| `design-spec-v[N].md` | 4 + feedback loops | Yes |
| `prototype-v[N].html` | 5 | No (already HTML) |
| `validation-plan-v[N].md` | 5.5 | Yes |
| `launch-readiness-v[N].md` | 6 | Yes |
| `eng-alignment-v[N].md` | 6.5 | Yes (also gets PPTX) |
| `post-launch-eval-v[N].md` | 7 | Yes |

### PDF Quality Check
After generating each PDF, verify:
- File exists and is non-zero bytes
- Page count is reasonable (not 0, not 500)
- Content matches the markdown source (spot-check first and last sections)

## Error Handling

- If any stage fails, log the error in pipeline-state.md and continue to the next stage
- If a feedback loop fails, log it in pipeline-state.md with status "failed" and continue — loops are non-blocking
- Never block the pipeline. Flag issues for human review.
- In autonomous mode, collect all flags and present them at the end
