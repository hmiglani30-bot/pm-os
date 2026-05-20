# Change Spec: Stage 7 — Post-Launch Evaluator

## What Changes

### New Skill: `post-launch-evaluator`

A new Stage 7 skill added after Launch Readiness. It takes post-launch data and compares it against the success criteria, rollout gates, and risk predictions made during Stages 2-6 to produce a verdict: what worked, what didn't, and what the next iteration should fix.

### Input Contract

| Input | Source | Required Fields | Validation |
|-------|--------|----------------|------------|
| Launch Readiness (`launch-readiness-v[N].md`) | Stage 6 | Success Metrics table (Section 11), Phased Rollout gates (Section 5), Risk Register (Section 13) | Must contain at least 3 success metrics with numeric targets |
| PRD (`prd-v[final].md`) | Stage 2 | JTBD list, North Star metric, persona definitions | Must contain at least 1 JTBD with measurable outcome |
| Post-launch metrics (user-provided or fetched) | Production telemetry | Actuals for each metric in the Success Metrics table | At least 30 days of data; each metric must have a current value and a trend direction |
| Incident/feedback log (optional) | Support tickets, beta feedback, on-call pages | Categorized issues with severity and frequency | If absent, evaluator flags "no incident data" and proceeds with metric-only evaluation |

### Output Contract

| Section | Required | Description |
|---------|----------|-------------|
| Verdict Summary | Yes | SHIP MORE / HOLD / PIVOT / SUNSET with 3-sentence rationale |
| Metric Scorecard | Yes | Every success metric from Launch Readiness Section 11: target vs. actual, pass/fail, trend |
| Rollout Gate Audit | Yes | Every phase gate from Section 5: was the gate met? Was any rollback trigger hit? |
| Risk Prediction Accuracy | Yes | Every risk from Section 13: did it materialize? Was the mitigation effective? Calibration score (% of risks correctly rated) |
| JTBD Validation | Yes | Per-JTBD from the PRD: is the job being done? Evidence (metric, quote, or usage pattern) |
| Iteration Backlog | Yes | Ordered list of changes for next version, each traced to a failing metric or unmet JTBD |
| Total | | 1,500-2,500 words |

---

## MECE Check: Why This Doesn't Overlap

| Stage | What It Judges | When It Runs | Judgment Basis |
|-------|---------------|-------------|----------------|
| **Gandalf (Stage 3)** | Whether the PRD's *strategy and problem framing* are sound | Before anything is built | Logical rigor of the written PRD — no production data exists |
| **Launch Readiness (Stage 6)** | Whether the *plan to ship* is complete and safe | Before launch | Completeness of eng spec, rollback procedures, monitoring plan — still pre-launch |
| **Post-Launch Evaluator (Stage 7)** | Whether the *shipped product achieved its goals* | 30+ days after launch | Production metrics, actual incident data, real user behavior vs. predictions |

Gandalf asks "Is this the right problem?" Launch Readiness asks "Are we ready to ship this?" Post-Launch Evaluator asks "Did shipping this actually work?" No overlap — each stage judges a different artifact (PRD text vs. launch plan vs. production reality) at a different time (pre-build vs. pre-launch vs. post-launch).

**AI Control Plane example:** Gandalf challenged whether maturity scoring would be perceived as judgmental (Risk R4/R9). Launch Readiness set the gate: "If >40% of beta users dismiss maturity section, pivot." Post-Launch Evaluator is the stage that actually checks: did 40% dismiss it? What did they do instead? Should v2 keep, rework, or remove maturity scoring?

---

## Acceptance Criteria

**AC-1: Metric pass/fail matches targets.**
Given Launch Readiness Success Metrics specify "Guardrail Coverage Delta: +15pp in 90 days" and post-launch data shows +8pp at day 90, the evaluator produces a FAIL verdict for that metric with the delta (-7pp short) and trend direction.

**AC-2: Rollout gate audit catches a missed trigger.**
Given Rollout Phase 1 specifies "Rollback Trigger: CSAT < 3.5" and post-launch data shows CSAT dropped to 3.2 during beta week 2 but no rollback occurred, the evaluator flags "Rollback trigger hit but not executed" with the date and value, and adds "formalize rollback trigger automation" to the Iteration Backlog.

**AC-3: Risk calibration scoring is quantitative.**
Given the Risk Register contains 13 risks (R1-R13) and post-launch data confirms R7 (IAM setup friction) materialized at 35% abandon rate while R3 (page load >8s) did not, the evaluator produces a calibration score (e.g., "9/13 risks correctly rated, 69% calibration") and flags over/under-estimated risks by name.

**AC-4: JTBD validation uses evidence, not assertion.**
Given PRD JTBD-1 is "See all AI workloads across my org in one place" and post-launch data shows 78% of active users view the fleet table weekly but only 12% use cross-account filtering, the evaluator validates JTBD-1 as PARTIAL with the specific evidence split (fleet table adoption high, cross-account adoption low) and routes "cross-account onboarding friction" to the Iteration Backlog.

**AC-5: Iteration Backlog traces to failing inputs.**
Given 2 metrics fail (Guardrail Coverage Delta, Cost Optimization Actions) and 1 JTBD is partial (cross-account), the Iteration Backlog contains at least 3 items, each with a `Traces to:` line referencing the specific failing metric ID or JTBD ID, ordered by impact. No backlog item exists without a traced failure.

---

## Anti-Criteria: What This Skill Does NOT Do

- **Does not re-run the PRD.** It evaluates outcomes against the existing PRD's goals. If goals need rewriting, it says so in the Iteration Backlog — the Researcher and PRD Writer handle the rewrite.
- **Does not redesign.** If a UX pattern failed, it identifies *which* pattern and *why* (with data), but does not produce a new design spec. That is Stage 4's job in the next cycle.
- **Does not perform A/B test analysis.** It compares actuals to pre-stated targets. Statistical significance testing, experiment design, and multivariate analysis are out of scope.
- **Does not run monitoring or alerting.** It reads post-launch data; it does not set up dashboards or alarms. Launch Readiness Section 8 owns that.
- **Does not make the ship/no-ship call for the *current* launch.** That is Launch Readiness. Post-Launch Evaluator only judges *after* the product is live.
- **Does not gather new competitive intel.** If the competitive landscape shifted post-launch, it notes the signal but does not conduct fresh research. That is Stage 1's job in the next cycle.

---

## Pipeline Integration: Stage 7 to Stage 1 Feedback Loop

### Loop 4: Post-Launch → Research (Stage 7 → Stage 1, next cycle)

| Property | Value |
|----------|-------|
| **Trigger** | Post-Launch Evaluator produces Iteration Backlog with at least 1 item |
| **What gets sent back** | Iteration Backlog + Risk Calibration results + JTBD validation verdicts |
| **What it seeds** | The next pipeline cycle's Stage 1 (Researcher) receives the backlog as scoping input. The Researcher's "Decision to Inform" is pre-populated from the highest-impact backlog item. |
| **Version lineage** | `post-launch-eval-v1.md` links to `launch-readiness-v2.md` which links to `prd-v[final].md` — full traceability across cycles |
| **Pipeline state update** | `pipeline-state.md` gains a new section: `## Post-Launch Evaluation` with metric scorecard summary, verdict, and pointer to next cycle's pipeline directory |

### Orchestrator Changes (`pm-pipeline.md`)

- Add Stage 7 after Stage 6 in the pipeline sequence
- Stage 7 is **deferred by default** — it does not run immediately after Stage 6. It runs when the user says "evaluate launch", "how did it do", "post-launch review", or when a scheduled task triggers it 30+ days post-GA
- Context pruning for Stage 7: receives `launch-readiness` (Sections 5, 11, 13 only), `prd-v[final]` (JTBD list + North Star only), and user-provided post-launch metrics
- When Stage 7 completes and produces an Iteration Backlog, the orchestrator offers to start a new pipeline cycle with the backlog as Stage 1 input

### AI Control Plane Example (Cycle 2)

Post-Launch Evaluator runs at day 90 post-GA. Finds: Guardrail Coverage Delta is +8pp (target +15pp), WAU is 6,200 (target 5,000, exceeded), Cost Optimization Actions at 4% (target 10%). Verdict: SHIP MORE. Iteration Backlog: (1) Guardrail enablement friction — traced to JTBD-3 partial, (2) Cost tab discoverability — traced to Cost Optimization metric fail. This backlog seeds Cycle 2's Researcher with: "Decision to Inform: Should v2 prioritize guided guardrail setup or cost intelligence prominence?"
