---
artifact: prd
version: v1
topic: AI Adoption Control Plane for AWS CloudWatch
timestamp: 2026-05-19T14:20:00Z
status: draft
---

# PRD: CloudWatch AI Control Plane

## Executive Summary

Enterprise AI adoption is outpacing governance: 72% of organizations run agentic AI in production, yet 60% lack governance (Agentic AI Institute, 2026). AWS customers building on Bedrock, SageMaker, and third-party models have no unified console to monitor AI health, enforce guardrails, track costs, or measure business impact. CloudWatch AI Control Plane fills this gap — a single console inside CloudWatch that unifies AI asset discovery, guardrail monitoring, cost optimization, and adoption maturity scoring. Unlike ServiceNow's AI Control Tower (which sits on top of cloud), this is cloud-native, IAM-integrated, and cross-account by default.

## 1. Customer Problem

### Target Persona

**Primary: Maya Chen, Sr. Cloud Operations Lead at a mid-size fintech (800 employees)**

Maya manages a team of 4 SREs responsible for all AWS infrastructure. Over the past 18 months, 6 different engineering teams have deployed AI-powered features — a fraud detection model on SageMaker, a customer support chatbot on Bedrock (Claude), a code review agent using OpenAI's API, and three internal tools using various LLMs. Maya knows about 4 of these 6 deployments. She has no unified view of what AI is running, what it costs, whether guardrails are in place, or if any model is behaving unexpectedly.

Her day looks like this: she checks CloudWatch dashboards for traditional infrastructure, then opens a separate Bedrock console tab for guardrail status, then asks engineering leads via Slack whether their AI features are working. She has no way to answer her VP's question: "Are we using AI responsibly, and is it worth what we're spending?"

**Secondary: Raj Patel, CISO at a healthcare SaaS company (2,000 employees)**

Raj is responsible for compliance across all systems, including AI. He needs to ensure no AI model is processing PHI without proper guardrails, that prompt injection defenses are active, and that the company can demonstrate AI governance to auditors. Today he relies on quarterly manual reviews — by the time he discovers an ungoverned AI deployment, it's been running for months.

### Jobs to Be Done

1. **When** I discover a new AI deployment I didn't know about, **I want to** immediately see its guardrail status, cost footprint, and usage patterns, **so I can** assess risk without a 2-week investigation.

2. **When** my VP asks "what's our AI spend and what are we getting for it," **I want to** pull up a single dashboard showing cost by team/model/use-case correlated with business metrics, **so I can** justify continued investment or flag waste in a 5-minute conversation.

3. **When** a Bedrock guardrail triggers on a production workload, **I want to** be alerted immediately with context (which model, what content, how often), **so I can** decide whether to tighten the guardrail or investigate the upstream application.

4. **When** we're preparing for a compliance audit, **I want to** generate a report showing all AI assets, their governance status, guardrail enforcement history, and data handling policies, **so I can** demonstrate responsible AI use without weeks of manual evidence gathering.

5. **When** we're evaluating whether to switch from GPT-4 to a cheaper model for a specific workflow, **I want to** see cost vs. quality tradeoffs with real data from our usage, **so I can** make the switch with confidence rather than guessing.

**Ranked by frequency and pain:**
1. JTBD #2 (cost justification) — happens weekly, high executive visibility
2. JTBD #1 (discovery/risk) — happens monthly, high compliance risk
3. JTBD #3 (guardrail alerts) — happens daily for ops teams
4. JTBD #5 (cost optimization) — happens quarterly, high dollar impact
5. JTBD #4 (audit prep) — happens semi-annually, extremely painful when it does

### Problem Depth

**Root cause:** AWS built AI services (Bedrock, SageMaker) and monitoring primitives (CloudWatch metrics, CloudTrail) independently. There's no experience layer that connects them into an AI-specific operations view. Customers must build this themselves — and most don't.

**Current workarounds:**
- Custom CloudWatch dashboards manually configured per AI workload (works for Bedrock only, misses non-Bedrock AI)
- Spreadsheets tracking AI deployments manually (stale within days)
- Slack threads asking "who deployed what" (undiscoverable, no audit trail)
- Third-party tools like Datadog LLM Observability bolted on (adds vendor, duplicates cost, doesn't integrate with IAM/Guardrails)

**Cost of status quo:**
- **Time:** Maya spends ~5 hours/week manually correlating AI data across consoles
- **Risk:** 62% of CIOs are compromising on governance because they lack tools (Logicalis 2026)
- **Money:** Without cost-per-workflow visibility, organizations overspend by an estimated 20-40% on AI compute (extrapolated from FinOps Foundation cloud waste data applied to AI workloads)
- **Compliance:** 54% of COOs cite regulatory uncertainty about AI (Writer 2026) — a single ungoverned AI deployment could trigger regulatory action

**Who else is affected:**
- Engineering leads: need to understand their team's AI usage and costs
- Finance: need AI cost attribution for budgeting
- Legal/Compliance: need audit-ready AI governance evidence
- VP/Director of Engineering: needs to answer "is AI worth it" for the org

## 2. Solution Proposal

**CloudWatch AI Control Plane** — a new experience within the CloudWatch console that provides:

1. **AI Asset Discovery:** Automatically discover all AI workloads across an AWS Organization — Bedrock models, SageMaker endpoints, Lambda functions calling AI APIs (via CloudTrail pattern detection), and ECS/EKS containers with AI SDK dependencies.

2. **Unified AI Dashboard:** Single-pane view of all AI workloads showing health (latency, errors, throughput), cost (tokens, compute, by team/model/workflow), and governance status (guardrail coverage, policy compliance).

3. **Guardrail Monitoring:** Real-time visibility into Bedrock Guardrails enforcement — what's being blocked, how often, which applications are triggering guardrails. Extend to non-Bedrock AI via custom guardrail policies.

4. **Cost Intelligence:** AI-specific cost breakdown by model, team, use case, and workflow. Cost optimization recommendations (e.g., "Workflow X uses GPT-4 for simple classification — switching to Haiku would save $2,400/month with comparable accuracy based on your guardrail pass rates").

5. **Adoption Maturity Score:** Prescriptive maturity model (Level 1-5) that scores the organization's AI governance posture and recommends next actions. Not just a dashboard — a guided path from "ungoverned" to "mature."

### Scope

**In scope (v1):**
- AI asset discovery for Bedrock + SageMaker workloads
- Unified dashboard with health, cost, and governance views
- Bedrock Guardrails monitoring and alerting
- Cost attribution by model, account, and team (via tags)
- Adoption maturity assessment (read-only, recommendation-driven)
- Cross-account support via AWS Organizations

**Out of scope (v1):**
- Non-AWS AI discovery (OpenAI API, Anthropic direct, self-hosted models) — v2
- Automated guardrail enforcement for non-Bedrock AI — v2
- Business outcome correlation (tying AI spend to conversion/CSAT) — v2
- Kill switches for AI workloads — v2 (requires deep service integration)
- Model A/B testing — v3

### Competitive Differentiation

Unlike ServiceNow AI Control Tower (30+ integrations but sits OUTSIDE the cloud):
- **Cloud-native:** IAM-integrated, no additional vendor credentials. If you can access CloudWatch, you can access AI Control Plane.
- **Cross-account by default:** Leverages AWS Organizations and cross-account CloudWatch — competitors require per-account setup.
- **Zero-instrumentation for Bedrock:** Existing CloudWatch metrics and CloudTrail events auto-populate the dashboard. No SDK changes required.
- **Cost of entry:** Included in CloudWatch pricing (usage-based), not a separate enterprise license.

Unlike Datadog LLM Observability (deep monitoring but no governance):
- **Governance built in:** Guardrail monitoring, policy compliance, maturity scoring — not just metrics.
- **Discovery, not just instrumentation:** Finds AI you didn't know about, doesn't just monitor what you explicitly configured.

## 3. Success Metrics

| Metric | Type | Target | Current Baseline |
|--------|------|--------|-----------------|
| % of AI workloads with guardrail coverage | North Star | 80% within 6 months of adoption | ~30% (estimated from Bedrock-only guardrail adoption) |
| Time to discover new AI deployment | Supporting | < 24 hours (automated) | Weeks to months (manual) |
| Time to generate compliance report | Supporting | < 5 minutes | 2-3 weeks manual effort |
| AI cost visibility (% of spend attributed) | Supporting | > 90% of AI spend attributed to team/workflow | < 20% (most AI spend is in undifferentiated compute buckets) |
| Console adoption (monthly active users) | Supporting | 500 MAU within 6 months of launch | 0 (new product) |
| Customer-reported AI governance confidence | Supporting | CSAT > 4.0/5.0 on governance capability | No baseline (new category) |
| Alert fatigue (false positive rate) | Anti-metric | < 10% false positive rate on guardrail alerts | N/A |
| Time to value (first useful insight) | Anti-metric | Should not exceed 30 minutes from enablement | N/A |

## 4. FAQs

### Category: Customer & Problem

**Q1: Who is the primary buyer for this product?**
The primary buyer is the Cloud Operations or Platform Engineering lead responsible for AI infrastructure at organizations with 3+ AI workloads in production. This is typically a Senior SRE, Cloud Operations Manager, or VP of Platform Engineering. The secondary buyer is the CISO or compliance officer who needs AI governance evidence for audits. According to the Logicalis CIO Report 2026, 76% of CIOs consider unchecked AI a serious concern, making this a board-level priority that creates top-down demand. (~100w)

**Q2: Why can't customers just build custom CloudWatch dashboards for AI monitoring?**
They can, and some do — but only for Bedrock workloads with known metric namespaces. Custom dashboards require manual configuration per workload, provide no AI asset discovery (you must know what to monitor first), cannot surface guardrail enforcement patterns, and offer no governance maturity assessment. A customer with 10 AI workloads across 5 accounts would need to manually create and maintain dashboards in each account, correlate costs via Cost Explorer separately, and check Bedrock Guardrails in yet another console. The AI Control Plane collapses all of this into a single cross-account experience that auto-discovers workloads and self-configures. (~120w)

**Q3: What evidence do we have that customers actually want this?**
Three data points: (1) 72% of enterprises have agentic AI in production but 60% lack governance (Agentic AI Institute 2026), creating a massive unmet need. (2) 62% of CIOs are compromising on governance due to lack of tools (Logicalis 2026) — the demand exists, the supply doesn't. (3) ServiceNow invested heavily enough to acquire two companies (Traceloop, Veza) and build a 5-pillar AI Control Tower — validating the market opportunity with hundreds of millions in M&A spend. Direct customer voice is needed for v2 of this research — the current evidence is market-level, not AWS-customer-specific. (~110w)

**Q4: Is the governance gap real or just analyst hype?**
The data is convergent across independent sources: Cisco's 2026 Privacy Benchmark found only 12% of organizations have mature AI governance. Writer's enterprise survey found 79% face AI adoption challenges. The Agentic AI Institute found a 60% governance gap. When three unrelated surveys from different methodologies converge on the same finding — governance lags adoption badly — the signal is robust. More concretely, only 1 in 5 companies has mature governance for autonomous AI agents specifically (Cisco 2026), and 54% of C-suite executives say AI adoption is "tearing the company apart" (Writer 2026). This is not speculative. (~120w)

### Category: Solution & Approach

**Q5: Why build this inside CloudWatch rather than as a standalone console?**
CloudWatch is where operations teams already live — 500,000+ active customers. Building inside CloudWatch means: (a) zero new console to learn, (b) automatic integration with existing alarms, dashboards, and cross-account setups, (c) IAM permissions already configured, (d) consolidated billing. A standalone console would fragment the operations experience and require customers to maintain two monitoring tools. ServiceNow made the opposite bet (standalone platform) — our advantage is being embedded where customers already work. (~100w)

**Q6: How does AI asset discovery work technically?**
Three data sources, correlated: (1) CloudTrail events — detect Bedrock InvokeModel, SageMaker InvokeEndpoint, and API Gateway calls to known AI provider endpoints (OpenAI, Anthropic). (2) Service Catalog / Resource Groups — tagged AI resources. (3) CloudWatch metrics — identify metric namespaces associated with AI workloads (aws/bedrock, aws/sagemaker). The discovery engine runs continuously, not on-demand, so new deployments surface within hours. In v1, discovery accuracy is highest for Bedrock and SageMaker workloads (direct service integration). Third-party AI API detection via CloudTrail pattern matching will have lower recall and is scoped for v2 hardening. (~130w)

**Q7: What does "prescriptive maturity model" mean concretely?**
A 5-level scoring framework assessed automatically based on observable signals. Level 1 (Ad Hoc): AI workloads exist but no guardrails, no cost tracking, no policy. Level 2 (Aware): Bedrock Guardrails enabled for some workloads. Level 3 (Managed): >50% of workloads have guardrails, cost attribution active, alerts configured. Level 4 (Optimized): Cross-account governance, automated compliance reports, cost optimization recommendations acted upon. Level 5 (Leading): Business outcome correlation active, governance-as-code, automated remediation. Each level comes with specific recommended actions to reach the next level. This is the "prescriptive > configurable" principle — we tell customers what to do, not just show them a dashboard. (~140w)

### Category: Scope & Boundaries

**Q8: Why is non-AWS AI discovery out of scope for v1?**
Detecting AI workloads that call external APIs (OpenAI, Anthropic direct) requires CloudTrail pattern matching on outbound API calls, which has high false-positive potential (any HTTPS call to api.openai.com could be AI or could be account management). We chose to launch with high-accuracy discovery (Bedrock, SageMaker — where we have native integration) and add third-party detection in v2 once we validate the discovery UX and establish accuracy baselines. Shipping a v1 with noisy discovery would undermine trust in the feature. (~100w)

**Q9: What's the phased plan beyond v1?**
V1 (launch): Bedrock + SageMaker discovery, unified dashboard, guardrail monitoring, cost attribution, maturity scoring. V2 (3 months post-launch): Third-party AI detection, custom guardrail policies for non-Bedrock AI, business outcome correlation, enhanced cost optimization recommendations. V3 (6 months): Kill switches for AI workloads, model A/B testing support, governance-as-code (CloudFormation templates for AI policies), automated remediation actions. Each phase is gated on adoption metrics from the previous phase — we don't build v2 features until v1 proves value. (~110w)

### Category: Competitive & Market

**Q10: How does ServiceNow AI Control Tower compare, and what's our differentiation?**
ServiceNow launched their 5-pillar AI Control Tower at Knowledge 2026 with 30+ enterprise integrations, cross-platform discovery, and enforcement (kill switches). They acquired Traceloop for observability and Veza for identity security. It's the most complete offering today. Our differentiation: (1) Cloud-native vs. overlay — we're inside the cloud, not on top of it. No additional vendor credentials needed. (2) Zero-instrumentation — Bedrock/SageMaker workloads auto-populate without SDK changes. (3) Cross-account by default via AWS Organizations. (4) Cost — usage-based CloudWatch pricing vs. enterprise ServiceNow license. ServiceNow wins for multi-cloud heterogeneous environments. We win for AWS-primary shops that want governance built into their cloud, not bolted on. (~150w)

**Q11: Is Datadog a threat here?**
Datadog LLM Observability is the strongest developer-focused offering — execution flow charts, per-branch cost attribution, auto-instrumentation for 4+ frameworks. But Datadog is pure observability with no governance layer (no guardrails, no policy enforcement, no maturity scoring, no compliance reports). They also require explicit SDK instrumentation — they monitor what you configure, not what exists. For customers who already use Datadog for APM, LLM Observability is a natural add-on. Our bet: the ops/governance buyer is different from the developer/observability buyer. Datadog serves developers. We serve operations and compliance teams. Both can coexist. (~120w)

### Category: Metrics & Success

**Q12: Why is "% of AI workloads with guardrail coverage" the North Star metric?**
Because it directly measures the governance gap that this product exists to close. It's actionable (teams can improve it by enabling guardrails), measurable (we can observe guardrail configuration state), and correlated with customer value (higher coverage = lower risk). Alternative candidates: MAU (vanity), cost savings (lagging), discovery accuracy (too technical). The governance coverage metric ties directly to the customer pain ("are we using AI responsibly?") and the compliance need ("can we prove governance to auditors?"). (~100w)

**Q13: How will we measure adoption without cannibalization?**
CloudWatch AI Control Plane is additive — it doesn't replace existing CloudWatch dashboards or Bedrock console views. We measure adoption via: (1) MAU on the AI Control Plane console page, (2) # of AI workloads auto-discovered and monitored, (3) # of guardrail alerts configured, (4) # of compliance reports generated. The anti-metric is Bedrock console traffic — if AI Control Plane causes a drop in direct Bedrock console usage, that's expected (consolidation) not cannibalization. We track both. (~100w)

### Category: Technical & Architecture

**Q14: What existing AWS services does this integrate with?**
Core integrations: Amazon Bedrock (guardrails, model invocation metrics), Amazon SageMaker (endpoint metrics, model monitor), CloudWatch (metrics, alarms, dashboards), CloudTrail (API event detection for discovery), AWS Organizations (cross-account governance), IAM (permission model), Cost Explorer API (cost attribution), Resource Groups / Tag Editor (AI asset classification). Each integration uses existing service APIs — no new service dependencies. The AI Control Plane is a CloudWatch console experience that aggregates data from these sources, not a new backend service. (~110w)

**Q15: How does cross-account governance work?**
Via CloudWatch cross-account observability, which already supports centralized monitoring across AWS Organizations. The AI Control Plane adds an AI-specific aggregation layer: a delegated administrator account sees all AI workloads, guardrail statuses, and costs across member accounts. This uses existing IAM roles and organization-level service-linked roles — no new permission model required. For guardrail enforcement, the central account can push recommended guardrail policies to member accounts via CloudFormation StackSets (existing mechanism). This is the AWS-native moat: no competitor can replicate cross-account governance without the underlying Organizations + IAM infrastructure. (~130w)

**Q16: What's the data architecture?**
No new data store. The AI Control Plane reads from existing data sources in real-time: CloudWatch Metrics (health/performance), CloudTrail events (discovery/audit), Bedrock Guardrails API (governance status), Cost Explorer API (cost data). The maturity score is computed on-read from these signals. The only new storage is a lightweight AI asset inventory (a DynamoDB table per Organization) that caches discovery results for fast rendering. All source-of-truth data remains in the existing services. This minimizes operational overhead and ensures the AI Control Plane always shows current state, not stale snapshots. (~110w)

### Category: Business & Strategy

**Q17: What's the TAM for this product?**
The AI observability market is $1.1B in 2025, growing to $3.29B by 2035 (Precedence Research). However, the directly addressable market for an AWS-native AI governance console is narrower: roughly 150,000 AWS accounts actively using Bedrock or SageMaker (estimated from public adoption data), with an average potential spend of $500-2,000/year on AI monitoring. This gives a serviceable addressable market of $75M-300M. Obtainable in 2 years: assuming 5-10% adoption among Bedrock/SageMaker users, approximately $4M-30M in incremental CloudWatch revenue. The strategic value exceeds direct revenue — AI Control Plane is a retention mechanism that makes CloudWatch stickier for AI-heavy customers. (~140w)

**Q18: How does this affect CloudWatch pricing?**
AI Control Plane features are included in existing CloudWatch pricing — usage-based charges for metrics, alarms, and dashboards. The AI asset discovery and maturity scoring are free features (hooks that drive deeper CloudWatch usage). Cost optimization recommendations generate value by reducing customer AI spend, which could reduce our revenue from AI service usage — but increases retention and NPS. The net effect is positive: customers who optimize AI spend within AWS (rather than leaving for competitors who promise cheaper AI ops) retain more total spend on AWS. (~110w)

### Category: Risks & Mitigation

**Q19: What if AI asset discovery has high false positives?**
The highest risk is false positives in non-Bedrock AI detection (CloudTrail pattern matching for third-party API calls). Mitigation: v1 limits discovery to Bedrock + SageMaker workloads where detection accuracy is near 100% (native service integration). Non-Bedrock detection ships in v2 with a confidence score per detected asset and a human-in-the-loop confirmation step. We also provide a manual "add asset" flow for workloads that automated discovery misses. Users always see the detection method and confidence level. (~100w)

**Q20: What if customers don't adopt the maturity model?**
The risk is that prescriptive scoring feels judgmental — "you're Level 1" could be received negatively. Mitigation: frame levels as progression stages, not grades. Use language like "Next recommended action" not "You're failing at." Benchmark against anonymized peer cohorts ("organizations your size are typically at Level 3"). Make each recommended action concrete and achievable ("Enable Bedrock Guardrails on your fraud-detection model — estimated effort: 15 minutes"). The maturity model is opt-in visible, not forced onto the dashboard. (~100w)

**Q21: What's the biggest technical risk?**
Cross-account data aggregation latency. When an Organization has 100+ accounts, aggregating AI asset inventory, guardrail status, and cost data in real-time could be slow. Mitigation: use an async aggregation pipeline with a cached view (15-minute refresh) for the dashboard, with a manual "refresh now" option. Accept that the dashboard shows near-real-time, not real-time data. This is acceptable for governance use cases where minute-level freshness is overkill. Guardrail alerts remain real-time via CloudWatch Alarms (already sub-minute). (~110w)

**Q22: What regulatory risks should we consider?**
The AI Control Plane monitors AI workloads but does not process the AI content itself. However, the discovery engine examines CloudTrail logs that may contain metadata about AI inputs/outputs. Ensure all CloudTrail data stays within the customer's account (no cross-account exfiltration of content). The maturity scoring must not create legal liability — frame it as "assessment" not "certification." Explicitly disclaim that maturity scoring does not constitute compliance with any specific regulation (EU AI Act, NIST AI RMF). (~100w)

### Category: Risks & Mitigation (continued)

**Q23: How do we handle the "yet another dashboard" objection?**
Valid concern — CloudWatch already has many dashboard types. Mitigation: AI Control Plane is not a dashboard you build, it's a console page you land on. Automatic, pre-configured, opinionated. Think "EC2 instances page" not "custom dashboard builder." Zero configuration to get value — enable it, see your AI workloads. This is the ServiceNow critique in reverse: they add another module to an already complex platform. We add a focused page to an existing console. (~100w)

**Q24: What if Bedrock Guardrails coverage is too narrow for customer needs?**
Bedrock Guardrails covers content moderation, prompt attacks, PII, hallucination detection, and contextual grounding. But customers using OpenAI or self-hosted models can't use Bedrock Guardrails. V1 mitigation: the maturity model acknowledges this gap explicitly ("guardrail coverage applies to Bedrock workloads only"). V2: introduce Custom AI Policies that allow customers to define guardrail-equivalent rules for non-Bedrock workloads, enforced via Lambda-based evaluation functions. This extends the governance boundary beyond Bedrock without requiring customers to migrate all AI to Bedrock. (~110w)

**Q25: What happens if ServiceNow makes their AI Control Tower free or significantly cheaper?**
ServiceNow's business model is enterprise licenses — making AI Control Tower free would undermine their revenue model. More likely scenario: they offer it as an included module for existing customers, widening adoption. Our response: emphasize the cloud-native advantage (no new vendor, no new credentials, no new security review). For AWS-primary customers, the switching cost to ServiceNow is the entire ITSM platform adoption, not just the AI governance module. Our real risk is Datadog adding governance features to their existing observability — monitor this via the competitive research cycle. (~120w)

## 5. Risks & Open Questions

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Discovery false positives erode trust | Medium | High | V1 limited to native services; confidence scores in v2 |
| Cross-account aggregation latency | Medium | Medium | 15-minute cached refresh with real-time alerts separate |
| "Yet another dashboard" fatigue | Medium | Medium | Auto-configured page, zero setup required |
| ServiceNow AI Control Tower gains AWS-native integrations | Low | High | Accelerate v1 launch; deepen Organizations integration |
| Maturity model perceived as judgmental | Medium | Low | Frame as progression, not grades; benchmark vs. peers |
| Bedrock Guardrails too narrow | High | Medium | Custom AI Policies in v2; acknowledge gap explicitly in v1 |

### Open Questions

1. **Pricing model:** Should AI Control Plane features incur additional CloudWatch charges, or be included to drive AI service adoption? — Owner: Product/Finance
2. **Bedrock team alignment:** Does the Bedrock team see this as complementary or competitive to their console? — Owner: PM (cross-team alignment needed)
3. **Customer validation:** We need 5-10 customer interviews specifically about AI governance pain. Current evidence is market-level, not AWS-specific. — Owner: PM/UXR
4. **SageMaker integration depth:** How deep should v1 SageMaker integration go? Model Monitor data in the dashboard? — Owner: PM/Eng
5. **EU AI Act implications:** Does the maturity model need to align with the EU AI Act risk classification? — Owner: Legal
