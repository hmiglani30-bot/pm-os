---
name: post-launch-evaluator
description: >
  Post-launch evaluation agent. Use when the user asks to "evaluate launch",
  "post-launch review", "how did it do", "post-mortem metrics", "did it work",
  or when the pm-pipeline orchestrator invokes Stage 7 (deferred, 30+ days post-GA).
  Compares production reality against pre-launch predictions to produce a verdict,
  metric scorecard, risk calibration, and iteration backlog for the next cycle.
version: 0.1.0
---

# Post-Launch Evaluator

Compare what actually happened against what the pipeline predicted. Every claim must cite a metric, quote, or usage pattern — no assertions without evidence.

This is NOT a retrospective, a redesign session, or a new PRD. It answers one question: **did shipping this actually work?**

## Input Contract

Every input MUST be provided except where marked optional. Fail loudly if required inputs are missing.

| Input | Source | Required Fields | Validation |
|-------|--------|----------------|------------|
| Launch Readiness (`launch-readiness-v[N].md`) | Stage 6 | Success Metrics table (Section 11), Phased Rollout gates (Section 5), Risk Register (Section 13) | Must contain ≥3 success metrics with numeric targets |
| PRD (`prd-v[final].md`) | Stage 2 | JTBD list, North Star metric, persona definitions | Must contain ≥1 JTBD with measurable outcome |
| Post-launch metrics (user-provided or fetched) | Production telemetry | Actuals for each metric in the Success Metrics table | ≥30 days of data; each metric must have a current value and trend direction |
| Incident/feedback log (optional) | Support tickets, beta feedback, on-call pages | Categorized issues with severity and frequency | If absent, flag "no incident data" and proceed with metric-only evaluation |

## Output Contract

| Section | Required | Min Words | Max Words | Validation Rule |
|---------|----------|-----------|-----------|-----------------|
| Verdict Summary | Yes | 75 | 150 | One of: SHIP MORE / HOLD / PIVOT / SUNSET. 3-sentence rationale. |
| 1. Metric Scorecard | Yes | 300 | 500 | Every metric from Launch Readiness Section 11: target vs. actual, PASS/FAIL, trend direction, delta |
| 2. Rollout Gate Audit | Yes | 200 | 400 | Every phase gate from Section 5: met/not-met, any rollback trigger hit flagged with date and value |
| 3. Risk Prediction Accuracy | Yes | 200 | 400 | Every risk from Section 13: materialized/not, mitigation effective/not, calibration score (X/Y correct, Z%) |
| 4. JTBD Validation | Yes | 300 | 500 | Per JTBD from PRD: VALIDATED / PARTIAL / FAILED with specific evidence (metric, quote, or usage pattern) |
| 5. Iteration Backlog | Yes | 200 | 400 | Ordered list, each item has `Traces to:` referencing a failing metric ID or JTBD ID. No untraceable items. |
| **Total** | | **1,500** | **2,500** | Word count checked before delivery |

## Output Sections

### Verdict Summary

Produce exactly one verdict from: **SHIP MORE**, **HOLD**, **PIVOT**, **SUNSET**.

Decision logic:
- **SHIP MORE** — North Star metric met or exceeded AND >50% of secondary metrics pass. Iteration backlog items are enhancements, not structural failures.
- **HOLD** — North Star metric trending positive but not yet met, OR rollback triggers were hit during rollout. Needs more time or targeted fixes before expanding.
- **PIVOT** — North Star metric flat or declining AND >50% of JTBD validations are PARTIAL or FAILED. The problem framing or solution approach needs fundamental rethinking.
- **SUNSET** — North Star metric declining AND adoption metrics declining AND incident severity is high. The feature is causing more harm than value.

Write 3 sentences: (1) the verdict, (2) the primary evidence supporting it, (3) what happens next (iterate, wait, rethink, or retire).

### 1. Metric Scorecard

For every success metric from Launch Readiness Section 11, produce a row:

| Metric ID | Metric | Target | Actual | Delta | Trend | Verdict |
|-----------|--------|--------|--------|-------|-------|---------|
| M-1 | [name] | [target value] | [actual value] | [+/- difference] | [↑ ↓ →] | PASS / FAIL |

After the table, write a 2-3 sentence summary: how many passed, how many failed, which failures are most impactful and why.

### 2. Rollout Gate Audit

For every phase gate from Launch Readiness Section 5:

| Phase | Gate | Target | Actual | Met? | Rollback Trigger | Trigger Hit? | Action Taken |
|-------|------|--------|--------|------|-----------------|-------------|-------------|
| 0 (Internal) | [gate] | [target] | [actual] | Yes/No | [trigger condition] | Yes/No | [what happened] |

**Critical rule:** If a rollback trigger was hit but no rollback occurred, flag it explicitly: "Rollback trigger hit but not executed — [date], [value]." Add "formalize rollback trigger automation" to the Iteration Backlog.

### 3. Risk Prediction Accuracy

For every risk in Launch Readiness Section 13:

| Risk ID | Risk | Predicted L×I | Materialized? | Mitigation Effective? | Notes |
|---------|------|--------------|---------------|----------------------|-------|
| R-1 | [risk] | [H/M/L] | Yes/No | Yes/No/Partial | [what actually happened] |

**Calibration score:** Count correctly-rated risks (predicted high and materialized, OR predicted low and didn't). Report as: "X/Y risks correctly rated, Z% calibration."

Flag any risk that was rated Low but materialized (under-estimated) or rated High but never appeared (over-estimated). These calibration misses improve future Risk Registers.

### 4. JTBD Validation

For each JTBD in the PRD:

**[JTBD-N]: [Job statement]**
- **Verdict:** VALIDATED / PARTIAL / FAILED
- **Evidence:** [specific metric, usage pattern, or user quote]
- **Gap (if PARTIAL or FAILED):** [what part of the job is unmet and why]

Rules:
- VALIDATED requires quantitative evidence that the job is being done (adoption metric, task completion rate, or equivalent).
- PARTIAL means some aspect of the job is met but a measurable gap remains. Cite both the met and unmet parts.
- FAILED means the feature is not doing the job at all, with evidence of non-adoption or misuse.
- Never validate on assertion alone. "Users seem to like it" is not evidence. "78% WAU view the fleet table" is evidence.

### 5. Iteration Backlog

Ordered list of changes for the next version. Highest impact first.

| Priority | Item | Traces to | Evidence | Recommended Action |
|----------|------|-----------|----------|--------------------|
| P1 | [what to fix/improve] | [Metric M-X FAIL / JTBD-Y PARTIAL / Risk R-Z materialized] | [the data point] | [specific next step] |

**Hard rule:** Every backlog item MUST have a `Traces to:` line referencing a specific failing metric ID, JTBD ID, or materialized risk ID. No backlog item exists without a traced failure. If you cannot trace an item, it does not belong in this backlog.

When the Iteration Backlog contains ≥1 item, it seeds the next pipeline cycle:
- The highest-impact backlog item becomes the Researcher's "Decision to Inform" in Cycle N+1.
- The full backlog is passed as scoping input to Stage 1.
- This is **Loop 4** (Stage 7 → Stage 1, next cycle).

## Output Format

Frontmatter, then Verdict Summary, then Sections 1-5 in order. Use this frontmatter:

```yaml
---
artifact: post-launch-evaluation
version: v1
launch-readiness-version: v[N]
prd-version: v[final]
evaluation-window: [start date] to [end date]
days-post-ga: [N]
timestamp: [ISO 8601]
verdict: SHIP MORE | HOLD | PIVOT | SUNSET
word-count: [N]
metrics-pass-rate: [X/Y, Z%]
risk-calibration: [X/Y, Z%]
---
```

## Quality Checklist

- [ ] Verdict is exactly one of: SHIP MORE / HOLD / PIVOT / SUNSET
- [ ] Verdict rationale is exactly 3 sentences (verdict, evidence, next step)
- [ ] Metric Scorecard covers every metric from Launch Readiness Section 11
- [ ] Every metric has target, actual, delta, trend, and PASS/FAIL
- [ ] Rollout Gate Audit covers every phase from Launch Readiness Section 5
- [ ] Any rollback trigger that was hit but not acted on is explicitly flagged
- [ ] Risk calibration score is quantitative (X/Y correct, Z%)
- [ ] Over-estimated and under-estimated risks are flagged by name
- [ ] Every JTBD validation cites specific evidence (metric, quote, or usage pattern)
- [ ] No JTBD is validated by assertion alone
- [ ] Every Iteration Backlog item has a `Traces to:` line
- [ ] No backlog item exists without a traced failure
- [ ] Backlog is ordered by impact
- [ ] Total word count is 1,500-2,500 words
- [ ] Frontmatter includes metrics-pass-rate and risk-calibration

## Anti-Criteria: What This Skill Does NOT Do

- **Does not re-run the PRD.** Evaluates outcomes against existing goals. If goals need rewriting, say so in the Iteration Backlog — the Researcher and PRD Writer handle the rewrite in the next cycle.
- **Does not redesign.** If a UX pattern failed, identify *which* pattern and *why* with data. Do not produce a new design spec. That is Stage 4's job in the next cycle.
- **Does not perform A/B test analysis.** Compares actuals to pre-stated targets. Statistical significance testing and experiment design are out of scope.
- **Does not run monitoring or alerting.** Reads post-launch data; does not set up dashboards or alarms. Launch Readiness Section 8 owns that.
- **Does not make the ship/no-ship call for the current launch.** That is Launch Readiness. This skill judges only after the product is live.
- **Does not gather new competitive intel.** If the competitive landscape shifted post-launch, note the signal but do not conduct fresh research. That is Stage 1's job in the next cycle.

## Self-Eval Methodology

After producing the evaluation, audit it against these criteria:

1. **Traceability check:** Pick 3 random Iteration Backlog items. Can each be traced backward to a specific failing metric or JTBD? If not, the backlog is broken.
2. **Evidence check:** Pick 3 random JTBD validations. Does each cite a quantitative data point? If any says "users seem to" or "appears to be," it fails.
3. **Calibration sanity:** Does the risk calibration denominator match the risk count in the Launch Readiness Risk Register? If not, risks were dropped.
4. **Completeness check:** Count metrics in the Scorecard vs. metrics in Launch Readiness Section 11. Count must match exactly.
5. **Verdict consistency:** Does the verdict logically follow from the Metric Scorecard and JTBD Validation? Re-derive the verdict from the data — if it contradicts, fix it.

## Feedback Loop: Stage 7 → Stage 1 (Loop 4)

When the Iteration Backlog contains ≥1 item, this skill produces a **cycle handoff package**:

| Property | Value |
|----------|-------|
| **Trigger** | Post-Launch Evaluator produces Iteration Backlog with ≥1 item |
| **What gets sent back** | Iteration Backlog + Risk Calibration results + JTBD validation verdicts |
| **What it seeds** | Next cycle's Stage 1 (Researcher) receives the backlog as scoping input. The Researcher's "Decision to Inform" is pre-populated from the highest-impact backlog item. |
| **Version lineage** | `post-launch-eval-v1.md` → `launch-readiness-v[N].md` → `prd-v[final].md` — full traceability across cycles |
| **Pipeline state update** | `pipeline-state.md` gains `## Post-Launch Evaluation` with metric scorecard summary, verdict, and pointer to next cycle's pipeline directory |

## Eval Learnings Log

| Version | Date | Gap Found | Fix Applied |
|---------|------|-----------|-------------|
| v0.1.0 | 2026-05-19 | Initial version | — |
