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

6 stages, executed sequentially. Each stage produces a versioned artifact in the working directory.

### Stage 0: Setup
1. Create a working directory: `pipeline-[topic-slug]/`
2. Create `pipeline-state.md` with: topic, mode, timestamp, status per stage
3. Read any existing artifacts if resuming

### Stage 1: Research
Invoke the `researcher` skill. Pass the topic.
- Output: `research-v1.md` — competitor landscape, capability evolution, quantitative data, market context
- The researcher uses the `research-librarian` skill for web lookups

### Stage 2: Strategy & PRD
Invoke the `prd-writer` skill. Pass `research-v1.md` as input.
- Output: `prd-v1.md` — customer-first PRD with persona, JTBD, problem depth, solution, 25 MECE FAQs
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

### Stage 5: Prototype
Invoke the `prototype-builder` skill. Pass the approved design spec.
- Output: `prototype-v1.html` — single-file Cloudscape HTML prototype
- Validate: render check, JS error check, interactivity check
- If interactive mode: pause for human review and iteration

### Stage 6: Launch Readiness
Invoke the `launch-readiness` skill. Pass all approved artifacts.
- Output: `launch-readiness-v1.md` — eng spec, acceptance criteria, phased rollout, success metrics, meeting deck outline

## State Management

After each stage completes:
1. Update `pipeline-state.md` with: stage completed, artifact version, scores (if applicable), timestamp
2. Version all artifacts (v1, v2, v3...) — never overwrite, always increment
3. If interactive mode: present the artifact to the user with a summary of what was produced

## Context Pruning (borrowed from agentic-pm)

When handing off between stages, pass ONLY what the next stage needs:
- Stage 2 gets: research-v1.md (full)
- Stage 3 gets: latest prd version (full) + research-v1.md (summary only)
- Stage 4 gets: latest prd version (full) + gandalf-evaluation (full) + research (summary)
- Stage 5 gets: design-spec (full) + prd (executive summary only)
- Stage 6 gets: all artifacts (executive summaries) + design-spec (full) + prototype path

## Error Handling

- If any stage fails, log the error in pipeline-state.md and continue to the next stage
- Never block the pipeline. Flag issues for human review.
- In autonomous mode, collect all flags and present them at the end
