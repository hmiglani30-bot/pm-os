---
artifact: gandalf-evaluation
version: v2
prd-version: v2
timestamp: 2026-05-19T21:00:00Z
status: passed
rounds-used: 1
pass-count: 10/11
---

# Gandalf Evaluation: CloudWatch AI Control Plane

## Verdict: PASSED

**Score: 10/11 questions passed | Rounds used: 1/3**

One question flagged for human review. Pipeline advances.

## Detailed Scores

| # | Dimension | Rubric (1-5) | Evidence (0/1) | Pass? | Notes |
|---|-----------|:---:|:---:|:---:|-------|
| 1 | TAM & Market | 4 | 1 | **PASS** | Improved from v1. FAQ Q18 now shows full bottoms-up math: $492M Gartner TAM (Tier 3), SAM of ~$148M derived from 150K-200K AWS AI customers, SOM of ~$43M/year (30K Bedrock customers x 60% governance gap x $200/mo). Assumptions are explicit and traceable. The 150K-200K estimate still lacks a primary source but is grounded in AWS's ~1M active customers at 15-20% AI usage. |
| 2 | Why Now | 4 | 1 | **PASS** | Unchanged from v1 and still strong. Three convergent 12-month signals: 72% production AI with 60% governance gap (Agentic AI Institute 2026), ServiceNow's multi-hundred-million M&A (Traceloop + Veza acquisitions), Gartner sizing the market at $492M with 45% CAGR. Executive Summary also cites Logicalis 76% CIO concern and Cisco 12% maturity. Clear urgency. |
| 3 | Customer Problem Depth | 4 | 1 | **PASS** | Improved from v1. Section 1 now has two detailed personas (Maya Chen, Raj Patel) with specific company profiles, tools used, and day-in-the-life narratives. Five enumerated workarounds with specifics (custom dashboards, spreadsheets, Slack threads, third-party tools, quarterly audits). Quantified cost: 260 hours/year per ops lead, 20-40% AI overspend estimate, HIPAA fines up to $1.5M. Five ranked JTBDs with frequency and pain scores. Still constructed scenarios rather than verbatim support tickets, but depth and specificity are substantially better. PRD honestly flags need for 5-10 customer interviews (Open Question #3). |
| 4 | North Star Metric | 5 | 1 | **PASS** | Improved from v1. Section 3 names "% of AI Workloads with Guardrail Coverage" with full justification: actionable (teams enable guardrails), measurable (Bedrock API), correlated with customer value. Three rejected alternatives named with specific rejection reasons (MAU = vanity, cost savings = lagging, discovery accuracy = too narrow). Now includes phase gates ("if <50% after 6 months AND MAU <200, re-evaluate"), anti-metrics (false positive rate <10%, time-to-value <30 min), and a kill switch for the maturity model (>40% disable in 30 days). Exceptional — addresses counterarguments and includes guard rails on the metric itself. |
| 5 | Competitive Moat | 4 | 1 | **PASS** | Unchanged in substance from v1. Four structural differentiators vs. ServiceNow: cloud-native (IAM-integrated, no new credentials), cross-account (Organizations), zero-instrumentation (existing metrics), usage-based pricing. Per-competitor contrast with Datadog (governance gap) and Dynatrace (self-sufficient enforcement vs. partnership dependency). FAQ Q25 addresses the "what if ServiceNow goes free" scenario. Moat is structural (AWS infrastructure access), not feature-based. |
| 6 | Scope Discipline | 4 | 1 | **PASS** | Improved from v1. Section 2 Scope Boundary table is now explicit: 6 items in v1, 5 in v2, 3 in v3 with rationale for each phasing decision. Kill switches cut to v3 ("safety-critical feature needs extensive testing"), model A/B testing cut ("adjacent capability, not core governance"), business outcome correlation deferred ("requires base console to exist first"). Each cut has a specific reason, not just priority ranking. The v1 scope is still 5 capabilities which is ambitious, but now each capability's technical feasibility is better grounded (see Q7). |
| 7 | Technical Feasibility | 3 | 1 | **PASS** | Previously FAIL in v1. The v2 PRD materially addresses the gap. Each capability section now includes a "How it works" subsection with specific technical details. Key improvements: (a) Discovery explicitly names three data sources (CloudTrail events with specific event types like `InvokeModel`, `InvokeModelWithResponseStream`; Service Catalog/Resource Groups; CloudWatch metric namespaces `aws/bedrock`, `aws/sagemaker`). (b) Detection is scoped to explicit, typed API calls with "near-100% detection accuracy" for Bedrock/SageMaker — not pattern matching. Third-party detection honestly stated at "60-75% recall" and pushed to v2. (c) Cross-account aggregation cites Security Hub precedent: "100 accounts aggregated in <5 minutes cached, <15 minutes cold" (FAQ Q22). (d) Dashboard reads from existing data sources with "15-minute cached refresh" and real-time alerts via CloudWatch Alarms. (e) FAQ Q22 recommends a specific technical spike: "2 weeks, 1 engineer — build CloudTrail query across 10 sandbox accounts, measure latency, build aggregation view at 50-account scale." The Security Hub precedent is genuine evidence (same delegated admin pattern at scale). However, the spike has not been run yet — the PRD cites the precedent and proposes validation rather than presenting results. This is a reasonable state for a PRD (pre-spike), but the question passes because: the precedent is real, the approach is grounded in existing AWS mechanisms, the scope is limited to known-high-accuracy sources, and the validation plan is specific. Score 3, not 4, because proof is by analogy, not by prototype. |
| 8 | Cannibalization Risk | 4 | 1 | **PASS** | FAQ Q14 addresses directly: "AI Control Plane is additive — it does not replace existing CloudWatch dashboards or Bedrock console views." Defines specific anti-metric: Bedrock console traffic decline = consolidation (intended), not cannibalization. Open Question #2 flags Bedrock team alignment as a risk needing resolution in 2 weeks. Honest and well-tracked. |
| 9 | Failure Mode | 4 | 1 | **PASS** | Previously FAIL in v1. Major improvement. Section 3 now includes three specific, falsifiable failure scenarios: (1) "If AI asset discovery misidentifies >10% of assets in a customer's first 7 days, the customer will not return within 30 days. Pivot trigger: accuracy <90% after 2 weeks of beta with 20+ customers -> scope to Bedrock-only." (2) "If main dashboard takes >8 seconds to render for 50-account Organization -> switch to daily batch aggregation." (3) "If >40% of beta users disable maturity score within 30 days -> demote to optional, replace with coverage bar." Each has a measurable threshold, a timeframe, a sample size, and a specific pivot action. This is exactly what v1 was missing. The failure scenarios are now falsifiable, time-bound, and actionable. |
| 10 | Pricing & Business Model | 3 | 1 | **PASS** | Previously FAIL in v1. FAQ Q19 now provides a clear pricing strategy: "V1 recommendation: free — AI Control Plane features included in existing CloudWatch pricing." Revenue mechanism articulated: retention of AI-heavy customers, plus increased usage of paid CloudWatch features (alarms, Logs Insights). Quantified retention estimate: "$100M-$150M in protected annual revenue (based on ~5,000 at-risk accounts with >$50K annual AI spend, 10-15% retention lift)." V2 pricing gate defined: "If adoption exceeds 50,000 monitored workloads, introduce usage-based pricing ($0.50-2.00 per AI workload/month)." Honest caveat: "Finance alignment needed to validate retention estimate." Open Question #1 tracks this with a deadline (4 weeks pre-launch). Passes because: the strategy is stated (free retention play), the business justification is quantified (even if estimated), the escalation path to paid is defined (v2 gate), and the gap is honestly flagged. Score 3 not 4 because the $100M-$150M retention figure is an estimate without Finance validation — the PRD acknowledges this. |
| 11 | Solution Direction Deliberation | 4 | 1 | **PASS** | New question in v0.2.0. The PRD v2 includes a Solution Lineage table (Section 2) that maps each selected capability to its source opportunity in research-v2's Opportunity-Solution Tree. Seven rows trace: AI Asset Discovery, Unified Dashboard, Guardrail Monitoring, Cost Intelligence, Adoption Maturity Score, Non-Bedrock AI support (v2), and Business outcome correlation (v2). For each, the table shows: the chosen direction, rejected alternatives, and specific rejection rationale. Key evidence of deliberate selection: (a) Direction B (standalone service) rejected for AI Asset Discovery with concrete reason — "requires new IAM actions, new pricing model, and new service team formation — 6-9 month build vs. 2-3 months for CloudWatch embedding." (b) Direction C (Bedrock console expansion) rejected because it "limits scope to Bedrock-only customers, reducing TAM." (c) Cost Intelligence Direction B (anomaly detection only) rejected as "undifferentiated — Datadog and ServiceNow already track cost spikes." (d) Maturity Score Direction A (Config rules) rejected because "Config rules check configuration state only, not runtime behavior or organizational maturity." (e) Direction C (compliance reports) rejected as "an output of governance, not a driver" — this shows strategic thinking about means vs. ends. The lineage table demonstrates that the PRD Writer evaluated 13 directions across 5 opportunities from the research and selected 5 for v1 with 2 deferred to v2. Rejection rationales reference specific constraints (time-to-market, TAM impact, differentiation) rather than just preference. This is deliberate selection, not defaulting to the obvious. |

## Questions That Passed

1. **TAM & Market (Q1):** Full bottoms-up math with three layers (TAM, SAM, SOM). Assumptions stated explicitly. Gartner $492M market sizing cited.
2. **Why Now (Q2):** Three independent 12-month triggers converge — governance gap data, ServiceNow M&A validation, and Gartner market sizing.
3. **Customer Problem Depth (Q3):** Two detailed personas with day-in-the-life narratives, five enumerated workarounds, quantified cost of status quo across four dimensions (time, risk, money, compliance).
4. **North Star Metric (Q4):** Strongest answer in the PRD. Metric justified with rejected alternatives, phase gates, anti-metrics, and a kill switch for the maturity model feature.
5. **Competitive Moat (Q5):** Structural differentiation (IAM, Organizations, zero-instrumentation) against three named competitors. Moat is infrastructure-level, not feature-level.
6. **Scope Discipline (Q6):** Explicit v1/v2/v3 phasing table with rationale per capability. Hard cuts named (kill switches, A/B testing, governance-as-code).
7. **Technical Feasibility (Q7):** Upgraded from FAIL. Now grounded in specific AWS mechanisms (CloudTrail event sources, Security Hub precedent), with honest accuracy ranges and a defined validation spike.
8. **Cannibalization Risk (Q8):** Directly addressed with anti-metric tracking and Bedrock team alignment flagged as open question.
9. **Failure Mode (Q9):** Upgraded from FAIL. Three falsifiable scenarios with measurable thresholds, timeframes, and pivot actions.
10. **Pricing & Business Model (Q10):** Upgraded from FAIL. Free-tier strategy with quantified retention justification and a defined v2 pricing gate.

## Questions Flagged for Human Review

### Q10: Pricing & Business Model
**Current answer:** Free v1 as retention play, $100M-$150M protected annual revenue estimate, usage-based pricing gate at 50K workloads for v2.
**What's remaining:** The $100M-$150M retention figure is an estimate based on ~5,000 at-risk accounts with >$50K annual AI spend and 10-15% retention lift. This has not been validated by Finance. The PRD honestly flags this (Open Question #1, deadline 4 weeks pre-launch).
**Suggested action:** Complete the Finance alignment described in Open Question #1. Model three scenarios: (1) free-only with retention value, (2) freemium with premium cross-account features, (3) usage-based from launch. Each needs a 2-year revenue projection validated by Finance.
**Why it still passes:** The strategy is stated, the business case is framed with quantified estimates, and the validation path is defined with a deadline. The gap is execution (Finance meeting), not analysis quality. Blocking the pipeline for a Finance meeting that is already scheduled is not productive.

## Comparison: v1 vs. v2

| # | Dimension | v1 Score | v2 Score | Change | What Changed |
|---|-----------|:---:|:---:|:---:|------|
| 1 | TAM & Market | 3 / PASS | 4 / PASS | +1 | Full bottoms-up math with TAM/SAM/SOM layers |
| 2 | Why Now | 4 / PASS | 4 / PASS | = | Already strong in v1 |
| 3 | Customer Problem Depth | 3 / PASS | 4 / PASS | +1 | Second persona (Raj), five workarounds, ranked JTBDs with rationale |
| 4 | North Star Metric | 4 / PASS | 5 / PASS | +1 | Phase gates, anti-metrics, kill switch for maturity model |
| 5 | Competitive Moat | 4 / PASS | 4 / PASS | = | Already strong in v1 |
| 6 | Scope Discipline | 3 / PASS | 4 / PASS | +1 | Explicit v1/v2/v3 table with per-item rationale |
| 7 | Technical Feasibility | 2 / FAIL | 3 / PASS | +1, FAIL->PASS | Per-capability technical details, Security Hub precedent, defined spike |
| 8 | Cannibalization Risk | 4 / PASS | 4 / PASS | = | Already strong in v1 |
| 9 | Failure Mode | 2 / FAIL | 4 / PASS | +2, FAIL->PASS | Three falsifiable scenarios with thresholds and pivot actions |
| 10 | Pricing & Business Model | 2 / FAIL | 3 / PASS | +1, FAIL->PASS | Free-tier strategy quantified, v2 pricing gate defined |
| 11 | Solution Direction Deliberation | N/A | 4 / PASS | NEW | Solution Lineage table with 7 rows tracing selections to opportunity tree |

## Approved Changes to PRD

The following changes from v1 to v2 are validated as improvements:

1. **Technical feasibility sections added per capability** — each of the five capabilities now has a "How it works" subsection grounding the approach in specific AWS services and APIs.
2. **Failure scenarios with falsifiable thresholds** — three specific scenarios with measurable criteria and pivot actions replace the generic risk table from v1.
3. **Pricing strategy with retention quantification** — free v1 with $100M-$150M retention estimate and v2 pricing gate at 50K workloads replaces the vague "included in CloudWatch pricing" from v1.
4. **Solution Lineage table** — new addition documenting deliberate selection from the opportunity-solution tree with rejection rationale for 13 directions across 5 opportunities.
5. **Enhanced persona depth** — second persona (Raj, CISO) added, JTBDs ranked with explicit rationale, cost of status quo quantified across four dimensions.
6. **Phase gates added to metrics** — v2 gate, pricing gate, and maturity model kill switch provide measurable decision criteria for future scope changes.

## Reasoning Log

### Round 1

Evaluated prd-v2.md against all 11 critique dimensions from Gandalf v0.2.0. The PRD v2 is a substantial improvement over v1, addressing all three previously failing questions (Q7, Q9, Q10) with specific, evidence-backed content.

**Q7 (Technical Feasibility) — Previously FAIL, now PASS (3/5, Evidence 1):** The v1 evaluation flagged zero evidence for CloudTrail-based AI detection and no cross-account aggregation benchmarks. V2 addresses this by: (a) scoping v1 discovery to Bedrock + SageMaker only, where detection uses explicit CloudTrail event sources with near-100% accuracy — no pattern matching, (b) citing Security Hub as a precedent for cross-account aggregation at scale (100+ accounts, <15 minute latency, same delegated admin pattern), (c) honestly stating third-party AI detection at 60-75% recall and deferring to v2, (d) recommending a specific 2-week spike with 1 engineer for validation. I did not auto-pass — the Security Hub precedent is real but not identical (security findings vs. AI workload aggregation). The spike has not been run. Score 3 reflects "adequate with some evidence" — the evidence is by analogy, not by prototype. This is a reasonable state for a PRD that is pre-spike.

**Q9 (Failure Mode) — Previously FAIL, now PASS (4/5, Evidence 1):** The v1 evaluation demanded "specific, falsifiable failure scenarios with measurable thresholds." V2 delivers exactly that: >10% asset misidentification in first 7 days triggers Bedrock-only pivot after 2 weeks of beta; >8s P95 dashboard latency triggers batch aggregation switch; >40% maturity model opt-out in 30 days triggers demotion to optional. Each has a number, a timeframe, a sample condition, and a specific action. This is a strong improvement.

**Q10 (Pricing & Business Model) — Previously FAIL, now PASS (3/5, Evidence 1):** The v1 evaluation demanded revenue modeling beyond "included in CloudWatch pricing." V2 provides: free v1 strategy with retention rationale, $100M-$150M quantified retention estimate (with stated assumptions: 5K at-risk accounts, $50K+ annual AI spend, 10-15% retention lift), and a v2 pricing gate (usage-based at 50K workloads). The estimate needs Finance validation (flagged as Open Question #1 with deadline). Score 3 because the retention figure is still an estimate — but the analysis framework is sound and the validation path is defined.

**Q11 (Solution Direction Deliberation) — New in v0.2.0, PASS (4/5, Evidence 1):** The Solution Lineage table demonstrates deliberate selection from the research-v2 opportunity tree. Seven capability rows trace to specific opportunities, name rejected alternatives, and provide concrete rejection rationale (time-to-market, TAM impact, differentiation, dependency risk). This is not a checkbox exercise — the rationale shows strategic reasoning. Example: choosing maturity model (Opp 5, Direction B) over Config rules (Direction A) because "Config rules check configuration state only, not runtime behavior or organizational maturity" demonstrates understanding of means vs. ends. Deferred capabilities (non-Bedrock AI, business outcome correlation) also show lineage with rationale for deferral. Score 4 because the deliberation is thorough and evidence-based. Not 5 because some rows share rationale (AI Asset Discovery and Unified Dashboard both cite the same Direction A vs. B vs. C reasoning, which is accurate but slightly reduces the sense of independent evaluation per capability).

**Overall assessment:** 10/11 pass. The only question flagged (Q10) passes on rubric but has a remaining action item (Finance validation). The PRD v2 is decision-ready for engineering alignment with one tracked open item. This is a clean PASS — the threshold is 9/11 and the PRD achieves 10/11.
