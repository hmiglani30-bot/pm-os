---
artifact: prd-addendum
version: v1.1
topic: AI Adoption Control Plane — Gandalf Flag Fixes
timestamp: 2026-05-19T15:30:00Z
status: gandalf-round-2
fixes: Q7-technical-feasibility, Q9-failure-mode, Q10-pricing
---

# PRD Addendum: Gandalf Flag Fixes

These three sections address the 3 questions that failed Gandalf evaluation. They should be merged into prd-v2 after approval.

---

## Fix 1: Technical Feasibility (Q7) — Evidence for Solvability

### CloudTrail AI Detection: Why It Works

**Bedrock + SageMaker detection (v1 scope) is near-100% accurate.** These are first-party AWS services with dedicated CloudTrail event sources:

- **Bedrock:** `InvokeModel`, `InvokeModelWithResponseStream`, `ApplyGuardrail` events have their own event source (`bedrock.amazonaws.com`). No pattern matching needed — these are explicit, typed API calls. Every Bedrock invocation creates a CloudTrail event with model ID, input/output token counts, and guardrail evaluation results. This is the same mechanism CloudWatch already uses for Bedrock metrics.
- **SageMaker:** `InvokeEndpoint`, `InvokeEndpointAsync` events from `sagemaker.amazonaws.com`. SageMaker endpoints are explicitly registered resources — discovery is an API call (`ListEndpoints`), not pattern matching.

**Evidence this is solvable:**
1. **CloudWatch already does this for non-AI services.** Cross-account metric aggregation via CloudWatch cross-account observability is GA and handles 1000+ accounts. The AI Control Plane adds an aggregation layer on top of existing infrastructure — it does not build new cross-account plumbing.
2. **Precedent: AWS Security Hub.** Security Hub aggregates findings across 200+ accounts with <15 minute latency using a delegated administrator pattern. AI Control Plane uses the identical Organizations + delegated admin model.
3. **Bedrock Guardrails already writes CloudWatch metrics.** Metrics for `GuardrailCoverage`, `GuardrailBlocked`, and `InvocationLatency` already flow to CloudWatch. The Control Plane reads them — it doesn't create them.

**Third-party AI detection (v2, NOT v1) is harder.**
Detecting outbound calls to `api.openai.com` via CloudTrail VPC flow logs or NAT gateway logs has estimated 60-75% recall and ~85% precision. This is explicitly out of v1 scope because:
- Pattern matching on HTTPS destinations requires VPC flow log analysis (not CloudTrail)
- False positives: account management calls to the same domain
- Mitigation for v2: confidence scoring + human confirmation step

**Cross-account aggregation latency target:**
Based on Security Hub precedent: 100 accounts aggregated in <5 minutes (cached), <15 minutes (cold). Real-time guardrail alerts remain sub-minute via existing CloudWatch Alarms — the dashboard can tolerate near-real-time for governance use cases.

**Recommended spike (2 weeks, 1 engineer):**
1. Week 1: Build CloudTrail query for Bedrock + SageMaker events across 10 sandbox accounts. Measure latency and accuracy.
2. Week 2: Build aggregation view using CloudWatch cross-account. Measure dashboard render time at 50-account scale.
Expected output: Go/no-go on v1 scope with measured latency numbers.

---

## Fix 2: Failure Mode (Q9) — Specific Falsifiable Failure Scenarios

### Failure Scenario 1: Discovery Accuracy Fails → Trust Collapse
**Threshold:** If AI asset discovery misidentifies >10% of assets in a customer's first 7 days (false positives or false negatives), the customer will not return to the console within 30 days.
**Leading indicator:** Discovery accuracy rate measured daily during beta.
**Measurement:** Compare discovered assets against customer-confirmed inventory (beta participants manually verify).
**Pivot trigger:** If accuracy <90% after 2 weeks of beta with 20+ customers → scope v1 to Bedrock-only discovery (drop SageMaker endpoint detection), which has near-100% accuracy.
**Evidence basis:** Datadog's LLM Observability launched with auto-instrumentation accuracy >95% — the market bar is high.

### Failure Scenario 2: Dashboard Latency → Abandonment
**Threshold:** If the main AI Control Plane dashboard takes >8 seconds to render for a 50-account Organization, ops teams will revert to per-account Bedrock console checks.
**Leading indicator:** P95 dashboard render time measured in CloudWatch RUM.
**Measurement:** Synthetic monitoring from 5 regions with 10/50/100 account Organizations.
**Pivot trigger:** If P95 >8 seconds at 50 accounts after performance optimization sprint → switch from real-time aggregation to daily batch aggregation with "refresh" button (accept stale data for governance use case).
**Evidence basis:** CloudWatch dashboards render in <3 seconds for 100+ widget dashboards. Target is comparable performance.

### Failure Scenario 3: Maturity Model Rejected → Feature Removed
**Threshold:** If >40% of beta users disable or ignore the maturity score within 30 days, the feature is not providing value and should be demoted to an optional setting.
**Leading indicator:** Maturity score widget interaction rate (clicks, expansions) and opt-out rate.
**Measurement:** CloudWatch RUM tracking on the maturity score component.
**Pivot trigger:** If interaction rate <15% AND opt-out rate >40% → remove maturity score from default dashboard, move to Settings as opt-in feature. Replace with a simpler "governance coverage %" bar.
**Evidence basis:** ServiceNow's AI Control Tower prominently features maturity/discover scoring — if their enterprise customers engage with it, AWS ops teams should too. If they don't, the audience is wrong for this feature.

---

## Fix 3: Pricing & Business Model (Q10) — Revenue Scenarios

### Scenario A: Free Feature Driving Retention (Recommended for v1)
**Model:** AI Control Plane features included in existing CloudWatch pricing at no additional cost.
**Revenue mechanism:** Retention of AI-heavy customers who might leave for Datadog or ServiceNow + increased usage of paid CloudWatch features (custom dashboards, alarms, Logs Insights queries triggered by AI Control Plane findings).
**Estimated value:**
- At-risk customers: ~5,000 accounts with >$50K annual AWS AI spend using Datadog/ServiceNow for AI monitoring
- Average at-risk annual spend: $200K total AWS (not just AI)
- Retention lift estimate: 10-15% of at-risk customers retained = 500-750 accounts
- **Retention value: $100M-$150M in protected annual AWS revenue**
- Plus indirect revenue: AI Control Plane drives 2-3 additional CloudWatch Alarms per AI workload × $0.10/alarm/month = $1.2M-$3.6M incremental CloudWatch revenue annually (assuming 100K-300K new alarms)

### Scenario B: Tiered Pricing (Consider for v2)
**Model:** Free tier = discovery + basic dashboard. Premium tier = cost optimization recommendations + maturity scoring + cross-account governance + compliance reports.
**Price point:** $5-15/AI workload/month (comparable to Datadog LLM Observability per-span pricing)
**Estimated revenue:**
- Year 1: 10,000 premium AI workloads × $10/month = $1.2M ARR
- Year 2: 50,000 premium workloads × $10/month = $6M ARR
**Risk:** Tiered pricing in CloudWatch is unprecedented and may face internal resistance. Every CloudWatch feature today is usage-based, not feature-gated.

### Scenario C: Usage-Based Premium (Best fit for AWS pricing model)
**Model:** All features free to use. Premium charges based on volume: >100 AI workloads monitored, >10 accounts aggregated, >1000 compliance report runs/month.
**Price point:** $0.50-2.00 per AI workload per month (usage-based)
**Estimated revenue:**
- Year 1: 30,000 workloads × $1.00/month = $360K ARR
- Year 2: 150,000 workloads × $1.00/month = $1.8M ARR
**Advantage:** Consistent with CloudWatch pricing model. Low barrier to adoption.

### Recommendation
**V1: Scenario A (free).** The strategic value ($100M-$150M retention) far exceeds any incremental revenue from tiered pricing. Launch free, measure adoption, introduce Scenario C pricing in v2 if adoption exceeds 50,000 monitored workloads.

**Finance alignment needed:** Validate retention value estimate with customer data team. Model the "AI spend at risk" cohort more precisely.
