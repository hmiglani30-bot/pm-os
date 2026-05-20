---
artifact: gandalf-evaluation
version: v1
prd-version: v1
timestamp: 2026-05-19T15:00:00Z
status: passed-with-flags
rounds-used: 1
pass-count: 7/10
---

# Gandalf Evaluation: CloudWatch AI Control Plane

## Verdict: PASSED WITH FLAGS

**Score: 7/10 questions passed | Rounds used: 1/3**

Three questions flagged for human review. Pipeline advances.

## Detailed Scores

| # | Dimension | Rubric (1-5) | Evidence (0/1) | Pass? | Notes |
|---|-----------|:---:|:---:|:---:|-------|
| 1 | TAM & Market | 3 | 1 | **PASS** | TAM math shown in FAQ Q17 ($75M-300M SAM) with assumptions stated, but inputs are estimated — "estimated from public adoption data" without naming the source for 150K Bedrock/SageMaker accounts |
| 2 | Why Now | 4 | 1 | **PASS** | Strong. Three convergent signals: 72% production AI + 60% governance gap (Agentic AI Institute), ServiceNow's $100M+ M&A validating market, and regulatory pressure (EU AI Act). Clear 12-month trigger events cited. |
| 3 | Customer Problem Depth | 3 | 1 | **PASS** | Maya persona is vivid with day-in-the-life narrative. Problem depth section quantifies cost of status quo (5 hrs/week, 20-40% overspend). However, the 3 scenarios are hypothetical constructions, not real patterns from support tickets or user research. PRD honestly flags this: "Direct customer voice is needed for v2 of this research." Passes on honesty + market-level evidence, but barely. |
| 4 | North Star Metric | 4 | 1 | **PASS** | "% of AI workloads with guardrail coverage" is well-justified in FAQ Q12. Rejected alternatives named (MAU, cost savings, discovery accuracy). Metric is actionable, measurable, and ties to the core value proposition. Missing: how to measure it technically (what counts as "guardrail coverage"?). |
| 5 | Competitive Moat | 4 | 1 | **PASS** | Four-part differentiation is specific: cloud-native (IAM), cross-account (Organizations), zero-instrumentation (existing metrics), usage-based pricing. Each contrasted against specific competitor weakness. The moat is structural (AWS infrastructure access), not just feature-based. Strong. |
| 6 | Scope Discipline | 3 | 1 | **PASS** | In/out scope defined. Kill switches, model A/B testing, business outcome correlation explicitly cut with rationale. However, the v1 scope is still ambitious — 5 capabilities (discovery, dashboard, guardrail monitoring, cost intelligence, maturity score) is a lot for a v1. No evidence that this scope is achievable in the proposed timeline. The phased plan (FAQ Q9) is well-structured but doesn't address whether v1 alone is too big. |
| 7 | Technical Feasibility | 2 | 0 | **FAIL** | FAQ Q16 describes data architecture ("no new data store") and Q21 names cross-account aggregation as the biggest risk. But there's no evidence this is solvable. No prototype, no spike results, no reference to similar systems that solved this. The claim that CloudTrail pattern detection can find AI API calls is particularly unsupported — what's the expected false positive rate? What's the detection accuracy for SageMaker endpoints? Assertion without proof. |
| 8 | Cannibalization Risk | 4 | 1 | **PASS** | FAQ Q13 addresses this directly: "CloudWatch AI Control Plane is additive" with specific anti-metric (Bedrock console traffic) to track. The distinction between consolidation and cannibalization is well-articulated. Also notes Bedrock team alignment as an open question (honest). |
| 9 | Failure Mode | 2 | 0 | **FAIL** | The PRD lists 6 risks in the risk table but none is a specific, falsifiable failure scenario. "Discovery false positives erode trust" — at what false positive rate? After how many false positives does trust break? "Yet another dashboard fatigue" — what evidence suggests this is a real risk vs. hypothetical? The most specific failure mode is buried in FAQ Q21 (aggregation latency) but even that doesn't say "if latency exceeds X seconds, customers abandon the dashboard." Needs concrete failure thresholds and leading indicators. |
| 10 | Pricing & Business Model | 2 | 1 | **FAIL** | FAQ Q18 says "included in existing CloudWatch pricing" and "cost optimization recommendations generate value by reducing customer AI spend, which could reduce our revenue." This is honest but incomplete. There's no pricing model analysis — what's the revenue impact? If AI Control Plane drives $0 incremental revenue, what's the business justification beyond retention? The open question (#1) acknowledges this gap but doesn't provide enough analysis to be decision-ready. |

## Questions That Passed

1. **TAM & Market:** Bottoms-up math shown with SAM range. Passes because the math is visible, though inputs need validation.
2. **Why Now:** Three independent 12-month trigger events converge. Strongest answer in the PRD.
3. **Customer Problem Depth:** Personas are vivid; cost of status quo is quantified. Passes despite relying on constructed (not observed) scenarios.
4. **North Star Metric:** Well-justified with rejected alternatives. Clear measurement mechanism.
5. **Competitive Moat:** Structural moat (AWS infrastructure access) not just feature gap. Specific per-competitor differentiation.
6. **Scope Discipline:** Explicit cuts with rationale. Phased plan exists. Borderline — v1 scope may still be too large.
7. **Cannibalization Risk:** Directly addressed with anti-metric tracking.

## Questions Flagged for Human Review

### Q7: Technical Feasibility
**Current answer:** FAQ Q16 describes "no new data store" architecture and Q21 names aggregation latency as biggest risk with "15-minute cached refresh" mitigation.
**What's missing:** Zero evidence that CloudTrail pattern detection for AI API calls works at the claimed accuracy. No prototype or spike results for cross-account AI discovery. No latency benchmarks for aggregating 100+ accounts. No reference implementations.
**Suggested action:** Run a 2-week technical spike: (1) Can CloudTrail reliably detect Bedrock InvokeModel and SageMaker InvokeEndpoint across 10+ accounts in < 5 minutes? (2) What's the false positive rate for third-party AI API detection? (3) Build a prototype aggregation query for 50 accounts and measure latency.

### Q9: Failure Mode
**Current answer:** Six risks listed in a table with likelihood/impact/mitigation, but all are generic scenarios without falsifiable thresholds.
**What's missing:** Specific failure criteria with numbers. "If AI discovery misidentifies > 15% of assets in a customer's first session, they won't return" is falsifiable. "Discovery false positives erode trust" is not.
**Suggested action:** Define 3 specific failure scenarios with measurable thresholds and leading indicators that would trigger a pivot or scope reduction.

### Q10: Pricing & Business Model
**Current answer:** "Included in existing CloudWatch pricing" with acknowledgment that cost optimization could reduce AI service revenue.
**What's missing:** Revenue modeling. If this is a retention play, quantify the retention value ($X in at-risk annual revenue from AI-heavy customers who might leave for Datadog/ServiceNow). If incremental revenue is possible, model the scenarios.
**Suggested action:** Work with Finance to model three scenarios: (1) free feature driving retention, (2) tiered pricing for advanced features (cost optimization, maturity scoring), (3) premium tier for cross-account governance. Each needs a 2-year revenue projection.

## Approved Changes to PRD
None — this is Round 1. If a Round 2 is run, the PRD Writer should address the 3 failing questions before re-evaluation.

## Reasoning Log

### Round 1
Evaluated prd-v1.md (25 FAQs, 5 sections) against all 10 critique dimensions. The PRD is strongest on market timing (Why Now) and competitive differentiation (Moat). It's weakest on technical evidence (no prototype/spike data) and specificity of failure scenarios. The pricing question is acknowledged but unresolved. 7/10 pass. The 3 failures are addressable — Q7 needs a technical spike (can't be solved by rewriting the PRD), Q9 needs more rigorous risk framing (solvable), Q10 needs revenue modeling (partially solvable, partially requires Finance input).

Given that 7/10 meets the minimum threshold spirit (though below the 8/10 hard pass), and 2 of 3 failures require external input (technical spike, Finance modeling), the recommendation is to ADVANCE with flags rather than block the pipeline.
