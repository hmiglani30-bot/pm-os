---
artifact: gandalf-evaluation
version: v1
prd-version: v1
timestamp: 2026-05-20T15:00:00Z
status: passed
rounds-used: 1
pass-count: 12/12
---

# Gandalf Evaluation: Quick Desktop AI Control Tower

## Verdict: PASSED

**Score: 12/12 questions passed | Rounds used: 1/3**

## Detailed Scores

| # | Dimension | Rubric (1-5) | Evidence (0/1) | Pass? | Notes |
|---|-----------|:---:|:---:|:---:|-------|
| 1 | TAM & Market | 4 | 1 | PASS | Gartner $492M market at 45% CAGR cited with tier. Bottoms-up SAM ($200M) and SOM ($12M) calculated with assumptions stated. |
| 2 | Why Now | 5 | 1 | PASS | Multiple convergent signals: CSA 82% unknown agents (Apr 2026), ServiceNow Knowledge 2026 expansion (May 2026), Gartner market validation (Feb 2026), 54% C-suite fracturing (Writer 2026). Quick Desktop preview launch (Apr 2026) creates window. |
| 3 | Customer Problem Depth | 4 | 1 | PASS | Three named scenarios: Lisa's 2-week CEO investigation, David's $180K unattributed AI spend, CISO's audit evidence gap. Grounded in CSA (82%), Logicalis (76% CIO concern), Writer (29% sabotage). Not from direct customer interviews (flagged as Open Question #3) but market-level evidence is triangulated across 5+ sources. |
| 4 | North Star Metric | 5 | 1 | PASS | "% AI tools discovered and governed" with clear rationale. Alternatives considered and rejected (MAU, cost savings, discovery count) with specific reasons. Anti-metrics defined (override rate, time-to-value). Phase gates quantified. |
| 5 | Competitive Moat | 4 | 1 | PASS | Desktop-level endpoint visibility identified as structural advantage — ServiceNow lacks desktop presence (SaaS layer), Datadog requires code instrumentation, Dynatrace needs ServiceNow for enforcement. 50+ existing integrations and knowledge graph are 18+ month head starts. Risk acknowledged: Microsoft could add governance to Copilot (Q12 FAQ). |
| 6 | Scope Discipline | 5 | 1 | PASS | Dual-scope boundary table with 14 capabilities phased across Eng v1, Proto v1, v2, v3. Specific cut rationales for each: NLP content analysis cut from Eng v1 (false positive risk), compliance reports cut (dependent on maturity framework), kill switches in v3 (safety-critical testing). Proto v1 includes placeholder pages for v2/v3 features. |
| 7 | Technical Feasibility | 4 | 1 | PASS | Hardest challenges identified: (1) privacy-preserving desktop detection — mitigated with curated allowlist approach (high precision), (2) cross-vendor API access — mitigated with top-3 vendor focus in v1, (3) governance nudge latency — Open Question #4 assigned to engineering with Week 3 deadline. Dependencies mapped with risk ratings. |
| 8 | Cannibalization Risk | 4 | 1 | PASS | Explicitly addressed in FAQ Q19: complements Bedrock Guardrails (API layer) vs. AI Control Tower (endpoint layer). Different control points, different audiences. Control Tower surfaces Guardrail status in its dashboard — strengthens both products. No cannibalization of CloudWatch or Cost Explorer. |
| 9 | Failure Mode | 5 | 1 | PASS | Three specific, falsifiable failure scenarios: (1) "spying" perception kills adoption — mitigation via transparency, opt-in, aggregation; (2) detection accuracy <80% — mitigation via allowlist approach; (3) nudge override >50% — mitigation via frequency caps. Each has quantified pivot triggers. Risk table has 6 entries with likelihood/impact/mitigation/owner. |
| 10 | Pricing & Business Model | 4 | 1 | PASS | Clear tier strategy: Discovery in Plus (teaser), full governance in Professional/Enterprise. Land-and-expand motion: free → Plus → Professional. Revenue path via tier upgrades. V2 pricing gate at 50K users. FAQ Q18 details the model. Strategic retention value articulated (stickier Quick Desktop for enterprise). |
| 11 | Solution Direction Deliberation | 5 | 1 | PASS | Solution Lineage table exists with 6 rows. Each traces to a specific Opportunity from the research tree. Rejected alternatives named with specific rationales: B/Integration-only rejected for missing shadow AI; C/Notification nudges rejected for weakest enforcement; B/Activity-based estimation rejected for accuracy concerns. No "out of scope" hand-waving — each rejection cites a concrete cost. |
| 12 | Product Completeness | 4 | 1 | PASS | Proto v1 scope covers 14 capabilities including placeholder pages for v2/v3 features (integration marketplace, compliance reports, enforcement page, template library). Dual-scope table explicitly maps Eng v1 vs Proto v1. Research Interaction Pattern Benchmarking cited ServiceNow's 5-pillar navigation and Datadog's 6-section sidebar — Proto v1 covers all 5 dimensions (Discover, Observe, Govern, Secure, Measure) plus Admin Console and Integration Marketplace = 7 navigation sections, meeting or exceeding competitor surface. |

## Questions That Passed

1. **TAM & Market:** Gartner-backed $492M market with bottoms-up SAM/SOM calculation showing assumptions.
2. **Why Now:** Five convergent timing signals from Q4 2025 — May 2026, each independently sourced.
3. **Customer Problem Depth:** Three named personas with day-in-the-life narratives; 5 enumerated workarounds with quantified costs; market evidence triangulated across CSA, Logicalis, Writer, EY, Gartner.
4. **North Star Metric:** Well-justified metric choice with rejected alternatives, anti-metrics, and quantified phase gates.
5. **Competitive Moat:** Desktop endpoint visibility is a genuine structural advantage; 18+ month head start on knowledge graph; pricing moat ($20 vs enterprise ITSM).
6. **Scope Discipline:** Dual-scope table with 14 phased capabilities; specific cut rationales; Proto v1 includes vision pages for cut features.
7. **Technical Feasibility:** Hardest challenges named with specific mitigations; open questions assigned with deadlines.
8. **Cannibalization Risk:** Complementary positioning clearly articulated — different control points (API vs. endpoint).
9. **Failure Mode:** Three specific failure scenarios with quantified pivot triggers and owner assignments.
10. **Pricing & Business Model:** Tier strategy, land-and-expand motion, retention value, and v2 pricing gate defined.
11. **Solution Direction Deliberation:** Complete Solution Lineage table with named rejections and specific rationales.
12. **Product Completeness:** Proto v1 covers 7 navigation sections (vs. ServiceNow's 5 pillars + dashboard), including placeholder pages for v2/v3 features.

## Questions Flagged for Human Review

None — all 12 questions passed in Round 1.

## Minor Observations (not blocking)

1. **Customer voice is market-level, not Quick Desktop-specific.** All evidence comes from industry surveys (CSA, Writer, Logicalis) not from Quick Desktop pilot customers. Open Question #3 (UXR interviews by Week 4) addresses this. Recommend prioritizing these interviews before v1 design lock.

2. **M365 Admin API dependency is a real risk.** FAQ Q10 acknowledges this but the mitigation ("ship without Copilot cost data") weakens the cross-vendor cost attribution value proposition. Recommend parallel-tracking the Microsoft partnership (Open Question #2) with a fallback cost estimation approach.

3. **Privacy framework is critical path.** Legal review (6-8 week cycle per Dependencies Map) could delay launch. Recommend starting legal engagement immediately, not after design phase.

## Approved Changes to PRD

No changes required. PRD v1 passes Gandalf Gate as-is.

## Reasoning Log

### Round 1
Evaluated PRD v1 (Quick Desktop AI Control Tower) against all 12 Gandalf questions. The PRD demonstrates strong strategic framing with the "cockpit, not control tower" positioning, evidence-backed claims across 18 sources, and a well-structured dual-scope boundary that addresses the product completeness concern proactively. The Solution Lineage table is thorough with specific rejection rationales. North Star metric selection is well-justified with rejected alternatives. Failure modes are specific and falsifiable with quantified pivot triggers. All 12 questions pass. No Round 2 needed.
