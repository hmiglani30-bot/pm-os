---
description: Run the multi-agent PM pipeline (interactive or autonomous)
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Agent
argument-hint: "[feature-or-topic] [--mode interactive or autonomous]"
---

# PM Pipeline Orchestrator

Run the full PM pipeline for `$ARGUMENTS`. Parse the arguments:
- The feature/topic is everything before `--mode` (or the entire argument if no mode flag)
- `--mode interactive` (default): pause after each stage for human review
- `--mode autonomous`: run all stages end-to-end, flag open questions for human at the end

## Pipeline Architecture

7 stages, executed sequentially (Stage 7 is deferred). Each stage produces a versioned artifact in the working directory. Feedback loops run as post-stage side effects (non-blocking) — the pipeline always moves forward.

### Stage 0: Setup
1. Create a working directory: `pipeline-[topic-slug]/`
2. Create `pipeline-state.md` with: topic, mode, timestamp, status per stage, feedback loop tracking
3. Read any existing artifacts if resuming

### Stage 1: Research
Invoke the `researcher` skill. Pass the topic.
- Output: `research-v1.md` — competitor landscape, capability evolution, quantitative data, market context
- The researcher uses the `research-librarian` skill for web lookups

### Stage 2: Strategy & PRD
Invoke the `prd-writer` skill. Pass `research-v1.md` as input.
- Output: `prd-v1.md` — customer-first PRD with persona, JTBD, problem depth, solution, 25 MECE FAQs
- The PRD is a living document — Stages 3, 4, and 5 may patch it with feedback (see Feedback Loops)
- If interactive mode: pause and show the user the PRD, ask for feedback. Apply feedback → `prd-v2.md`

### Stage 3: Gandalf (Strategy & Problem Gate)
Invoke the `gandalf` skill. Pass the latest PRD version.
- Gandalf asks 10 predefined critique questions about strategy/problem framing
- PRD Writer agent must answer each question, researching further if needed (via research-librarian)
- Hybrid scoring: rubric (1-5 per dimension) + evidence (specific data cited)
- Max 3 rounds for the entire stage
- Pass threshold: 8/10 questions pass (score >= 3)
- Output: `gandalf-evaluation-v1.md` — scores, evidence, pass/fail verdict, open questions flagged for human
- If any questions remain unanswered after 3 rounds, flag them and MOVE FORWARD (pipeline never blocks)
- Update the PRD with Gandalf's approved changes → `prd-v[next].md`

### Stage 4: UX/Experience Design
Invoke the `designer` skill. Pass the approved PRD + Gandalf evaluation.
- Sequence: first principles → reality check → checklist
- Output: `design-spec-v1.md` — end-to-end experience design, layout rationale, alternatives considered
- Same scoring pattern as Gandalf (hybrid scoring, 3 rounds max) but focused on experience quality
- If interactive mode: pause for human review
- **Feedback (4→2):** After design spec is finalized, the Designer writes an "End-to-End Experience" section summarizing the designed user journey. The PRD Writer agent patches this into the PRD's experience section → `prd-v[next].md`. This runs in parallel with Stage 5 starting.

### Stage 5: Prototype
Invoke the `prototype-builder` skill. Pass the approved design spec.
- Output: `prototype-v1.html` — single-file Cloudscape HTML prototype
- Validate: render check, JS error check, interactivity check
- If interactive mode: pause for human review and iteration
- **Feedback (5→4 critique):** After prototype is validated, the Prototype Builder emits a "Fidelity Report" comparing what was built vs what the design spec specified, with a fidelity score (0-100%). If fidelity score < 90%, the Designer reviews the report and updates the design spec to reconcile gaps → `design-spec-v[next].md`. This runs as a side effect, not a blocker.
- **Feedback (5→2 final):** After prototype is finalized (including any fidelity-driven updates), the Prototype Builder patches the PRD's "End-to-End Experience" section with the canonical prototype experience (what was actually built and validated) → `prd-v[final].md`. This is the last PRD update in the pipeline.

### Stage 6: Launch Readiness
Invoke the `launch-readiness` skill. Pass all approved artifacts (using the latest versions, including feedback-patched PRD and design spec).
- Output: `launch-readiness-v1.md` — eng spec, acceptance criteria, phased rollout, success metrics, meeting deck outline

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
Stage 4 completes
  ├─ [parallel] Loop 1 fires (4→2): patch PRD with designed experience
  └─ [parallel] Stage 5 starts: build prototype from design spec

Stage 5 completes
  ├─ [side effect] Loop 2 fires (5→4): fidelity report, update design spec if < 90%
  └─ [after Loop 2] Loop 3 fires (5→2): patch PRD with canonical prototype experience → prd-v[final].md

Stage 6 starts after Loop 3 completes (needs final PRD)

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

- Stage 2 gets: research-v1.md (full)
- Stage 3 gets: latest prd version (full) + research-v1.md (summary only)
- Stage 4 gets: latest prd version (full) + gandalf-evaluation (full) + research (summary)
- Stage 5 gets: design-spec (full) + prd (executive summary only)
- Loop 1 (4→2): design-spec "End-to-End Experience" section → PRD Writer
- Loop 2 (5→4): fidelity report (full) → Designer + design-spec (full)
- Loop 3 (5→2): prototype canonical experience summary → PRD Writer + latest prd version
- Stage 6 gets: all artifacts (executive summaries) + design-spec latest version (full) + prd-v[final] (full) + prototype path
- Stage 7 gets: launch-readiness (Sections 5, 11, 13 only) + prd-v[final] (JTBD list + North Star only) + user-provided post-launch metrics + incident log (if available)
- Loop 4 (7→1, next cycle): iteration backlog + risk calibration + JTBD verdicts → next cycle's Researcher

## Error Handling

- If any stage fails, log the error in pipeline-state.md and continue to the next stage
- If a feedback loop fails, log it in pipeline-state.md with status "failed" and continue — loops are non-blocking
- Never block the pipeline. Flag issues for human review.
- In autonomous mode, collect all flags and present them at the end
