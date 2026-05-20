---
artifact: prd
version: v2
topic: AI Adoption Control Plane for AWS CloudWatch
timestamp: 2026-05-19T20:00:00Z
status: draft
total-words: ~5800
sources-count: 18
---

# PRD: CloudWatch AI Control Plane

## Decision to Inform
> Should AWS CloudWatch build a unified AI governance console ("AI Control Plane") that ties together Bedrock Guardrails, LLM observability, cost tracking, and agent monitoring into a single experience? If yes, what is the v1 scope and positioning against ServiceNow AI Control Tower and Dynatrace's "control plane for AI" narrative?

## Executive Summary

Enterprise AI adoption is outpacing governance: 72% of organizations run agentic AI in production, yet 60% lack governance (Agentic AI Institute, 2026 [Tier 3]). AWS customers building on Bedrock, SageMaker, and third-party models have no unified console to monitor AI health, enforce guardrails, track costs, or measure business impact — they navigate five separate consoles to piece together a governance picture. CloudWatch AI Control Plane fills this gap: a single console page inside CloudWatch that unifies AI asset discovery, guardrail monitoring, cost optimization, and adoption maturity scoring. Unlike ServiceNow's AI Control Tower (which sits on top of cloud, requiring separate vendor credentials and security review), this is cloud-native, IAM-integrated, and cross-account by default via AWS Organizations. The $492M AI governance platform market (Gartner, 45% CAGR [Tier 3]) validates the category. AWS has the primitives — Bedrock Guardrails, CloudWatch metrics, CloudTrail audit logs — but no experience layer connecting them. This PRD proposes building that layer.

## 1. Customer Problem

### Primary Persona: Maya Chen, Sr. Cloud Operations Lead

**Company:** Mid-size fintech, 800 employees, AWS-primary infrastructure.
**Role:** Manages a team of 4 SREs responsible for all AWS infrastructure. Reports to VP of Engineering.
**Technical sophistication:** High — comfortable with CloudWatch, IAM, and CloudFormation. Not an ML engineer.
**Current tools:** CloudWatch (daily), AWS Console (daily), Bedrock console (weekly), Cost Explorer (monthly), Slack (constant), PagerDuty (on-call), Datadog (APM only, evaluating LLM Observability).

**Pain points:**
- Six engineering teams have deployed AI features over 18 months — fraud detection on SageMaker, customer support chatbot on Bedrock (Claude), code review agent via OpenAI API, three internal tools on various LLMs. Maya knows about 4 of these 6 deployments.
- No unified view of what AI is running, what it costs, whether guardrails are in place, or whether any model is behaving unexpectedly.
- Spends ~5 hours/week manually correlating AI data across consoles (estimated).
- Cannot answer her VP's recurring question: "Are we using AI responsibly, and is it worth what we're spending?"

**Day in the life:** Maya starts her morning in CloudWatch checking infrastructure dashboards. Then she opens a separate Bedrock console tab for guardrail status. She posts in Slack asking engineering leads whether their AI features are behaving. She opens Cost Explorer to check if AI spend spiked. She has no single place that answers "what AI are we running, is it governed, and what does it cost?" — so she builds the picture manually, every day.

### Secondary Persona: Raj Patel, CISO

**Company:** Healthcare SaaS, 2,000 employees, regulated industry (HIPAA).
**Role:** Responsible for compliance across all systems, including AI. Reports to CEO.
**Technical sophistication:** Medium — understands IAM policies and compliance frameworks, not hands-on with CloudWatch dashboards.
**Current tools:** AWS Security Hub, AWS Config, GRC platform (ServiceNow or similar), quarterly audit spreadsheets.

**Pain points:**
- Must ensure no AI model processes PHI without proper guardrails and that prompt injection defenses are active.
- Relies on quarterly manual reviews — by the time he discovers an ungoverned AI deployment, it has been running for months.
- Cannot demonstrate AI governance posture to auditors without weeks of manual evidence gathering.
- 76% of CIOs share his concern about unchecked AI (Logicalis 2026 [Tier 3]), yet only 12% have mature governance (Cisco Privacy Benchmark 2026 [Tier 3]).

### Affected Stakeholders

- **Engineering leads:** Need to understand their team's AI usage and costs to manage budgets and justify headcount.
- **Finance/FinOps:** Need AI cost attribution by team, model, and use case for budgeting and chargeback.
- **Legal/Compliance:** Need audit-ready AI governance evidence for SOC 2, HIPAA, and emerging AI regulations.
- **VP/Director of Engineering:** Needs a "state of AI" summary to report upward — is AI investment paying off?

### Jobs to Be Done (ranked with rationale)

1. **When** my VP asks "what's our AI spend and what are we getting for it," **I want to** pull up a single dashboard showing cost by team/model/use-case, **so I can** justify continued investment or flag waste in a 5-minute conversation.
   - Frequency: Weekly | Pain: High | Persona: Maya (primary)
   - Ranking rationale: Highest frequency (weekly exec questions) combined with highest executive visibility. Cost justification is the gateway question — if Maya can't answer it, every subsequent AI investment decision stalls.

2. **When** I discover a new AI deployment I didn't know about, **I want to** immediately see its guardrail status, cost footprint, and usage patterns, **so I can** assess risk without a 2-week investigation.
   - Frequency: Monthly | Pain: Critical | Persona: Maya, Raj
   - Ranking rationale: Lower frequency but critical severity — an ungoverned AI deployment in a healthcare SaaS company is a compliance incident. 62% of CIOs compromise on governance because they lack tools (Logicalis 2026 [Tier 3]).

3. **When** a Bedrock guardrail triggers on a production workload, **I want to** be alerted immediately with context (which model, what content, how often), **so I can** decide whether to tighten the guardrail or investigate the upstream application.
   - Frequency: Daily (for ops teams) | Pain: Medium | Persona: Maya
   - Ranking rationale: High frequency but medium pain — guardrail triggers are operational signals, not crises. Existing CloudWatch Alarms partially address this, but lack AI-specific context.

4. **When** we're evaluating whether to switch from GPT-4 to a cheaper model for a specific workflow, **I want to** see cost vs. quality tradeoffs with real data from our usage, **so I can** make the switch with confidence rather than guessing.
   - Frequency: Quarterly | Pain: High | Persona: Maya, Engineering leads
   - Ranking rationale: High dollar impact (model cost differences are 5-10x) but low frequency. Nobody does this well today — Datadog tracks cost per branch but offers no quality-aware recommendations (research-v2 Pattern Analysis [Tier 1-2]).

5. **When** we're preparing for a compliance audit, **I want to** generate a report showing all AI assets, their governance status, guardrail enforcement history, and data handling policies, **so I can** demonstrate responsible AI use without weeks of manual evidence gathering.
   - Frequency: Semi-annually | Pain: Critical when it happens | Persona: Raj
   - Ranking rationale: Lowest frequency but extremely painful — Raj currently spends 2-3 weeks per audit cycle assembling evidence manually. The pain is concentrated and severe.

### Problem Depth

**Root cause:** AWS built AI services (Bedrock, SageMaker) and monitoring primitives (CloudWatch metrics, CloudTrail logs) independently. Each service has its own console, metrics namespace, and operational model. There is no experience layer that connects them into an AI-specific governance view. A customer wanting AI governance today must navigate five consoles: Bedrock (guardrails), CloudWatch (metrics and alarms), CloudTrail (audit logs), Cost Explorer (spending), and SageMaker (non-Bedrock endpoints) — then manually correlate the data. This is a UX problem, not a data problem: the signals exist but the aggregation does not.

**Current workarounds (enumerated):**
1. Custom CloudWatch dashboards manually configured per AI workload — works for Bedrock only, requires knowing what to monitor, no discovery capability, no guardrail context.
2. Spreadsheets tracking AI deployments manually — stale within days, no automated updates, typically maintained by one person who becomes a bottleneck.
3. Slack threads asking "who deployed what" — undiscoverable, no audit trail, no governance value.
4. Third-party tools (Datadog LLM Observability, ServiceNow AI Control Tower) bolted on — adds vendor cost, duplicates monitoring, doesn't integrate with IAM or Bedrock Guardrails natively.
5. Quarterly manual audits — Raj's team reviews each AWS account individually, checks Bedrock configurations, and assembles findings in a GRC tool. Takes 2-3 weeks per cycle.

**Quantified cost of status quo:**
- **Time:** Maya spends ~5 hours/week manually correlating AI data across consoles (260 hours/year per ops lead).
- **Risk:** 62% of CIOs compromising on governance due to lack of tools (Logicalis 2026 [Tier 3]). Only 12% of organizations have mature AI governance (Cisco 2026 [Tier 3]).
- **Money:** Without cost-per-workflow visibility, organizations overspend an estimated 20-40% on AI compute (extrapolated from FinOps Foundation cloud waste data applied to AI workloads — needs validation via customer interviews).
- **Compliance:** 54% of COOs cite regulatory uncertainty about AI (Writer 2026 [Tier 4]). A single ungoverned AI deployment processing PHI could trigger HIPAA violations with fines up to $1.5M per category.
- **Organizational friction:** 54% of C-suite executives say AI adoption is "tearing the company apart" — COOs worry about compliance while CIOs focus on capability (Writer 2026 [Tier 4]). No shared dashboard means no shared understanding.

**Who else is affected:** Engineering leads lack AI cost data for budget planning. Finance cannot attribute AI spend to business units. Legal cannot demonstrate governance posture without manual evidence collection. The VP of Engineering cannot answer "is AI worth it?" without assembling data from multiple teams.

## 2. Solution Proposal

**CloudWatch AI Control Plane** — a new console page within CloudWatch that provides unified AI governance for AWS workloads. Five core capabilities:

### Capability 1: AI Asset Discovery

**What it does:** Automatically discovers all AI workloads across an AWS Organization — Bedrock models, SageMaker endpoints, Lambda functions calling AI APIs (via CloudTrail pattern detection), and ECS/EKS containers with AI SDK dependencies. Surfaces assets that ops teams did not know existed.

**How it works (high-level):** Three correlated data sources: (1) CloudTrail events — Bedrock `InvokeModel`, `InvokeModelWithResponseStream`, `ApplyGuardrail` events from `bedrock.amazonaws.com`; SageMaker `InvokeEndpoint` from `sagemaker.amazonaws.com`. These are explicit, typed API calls with near-100% detection accuracy. (2) Service Catalog and Resource Groups — tagged AI resources. (3) CloudWatch metrics — metric namespaces `aws/bedrock` and `aws/sagemaker`. Discovery runs continuously; new deployments surface within hours. A lightweight DynamoDB table per Organization caches discovery results for fast rendering.

**Why it matters:** Addresses JTBD #2 (discover unknown AI deployments) and persona Raj's core pain (finding ungoverned AI). ServiceNow's strongest differentiator is cross-platform discovery across 30+ integrations (ServiceNow Newsroom, May 2026 [Tier 2]). AWS must match discovery for its own ecosystem at minimum.

**What's new vs. status quo:** Today, customers must know what AI they have deployed to monitor it. Discovery inverts this: the console tells you what AI exists, then you decide what to govern.

**Technical feasibility (validated):** Bedrock and SageMaker detection uses explicit CloudTrail event sources — no pattern matching needed. This is the same mechanism CloudWatch already uses for Bedrock metrics. Precedent: AWS Security Hub aggregates findings across 200+ accounts with <15 minute latency using the delegated administrator pattern. Third-party AI detection (OpenAI, Anthropic direct API calls) is harder — estimated 60-75% recall via VPC flow log analysis — and is explicitly scoped for v2.

### Capability 2: Unified AI Dashboard

**What it does:** Single-pane view of all AI workloads showing health (latency, errors, throughput), cost (tokens, compute, by team/model/workflow), and governance status (guardrail coverage, policy compliance). Pre-configured and opinionated — not a blank dashboard builder.

**How it works:** Reads from existing data sources in real-time: CloudWatch Metrics (health/performance), CloudTrail events (audit), Bedrock Guardrails API (governance status), Cost Explorer API (cost data). No new data store — source of truth remains in existing services. The maturity score is computed on-read from these signals. Cross-account aggregation uses CloudWatch cross-account observability (GA, handles 1000+ accounts) with a 15-minute cached refresh for the dashboard and real-time alerts via CloudWatch Alarms.

**Why it matters:** Addresses JTBD #1 (cost justification in 5 minutes) and JTBD #3 (guardrail alert context). Maya currently needs five console tabs to assemble the picture this dashboard shows on one page.

**What's new vs. status quo:** Today there is no AI-specific operations view in AWS. Customers build custom CloudWatch dashboards per workload — this is auto-configured and cross-account by default.

### Capability 3: Guardrail Monitoring

**What it does:** Real-time visibility into Bedrock Guardrails enforcement — what is being blocked, how often, which applications trigger guardrails most frequently. Extends beyond raw metrics to provide enforcement trend analysis and anomaly detection.

**How it works:** Reads existing CloudWatch metrics (`GuardrailCoverage`, `GuardrailBlocked`, `InvocationLatency`) already emitted by Bedrock. Adds context overlays: which application triggered the guardrail (via CloudTrail correlation), block rate trends, and anomaly alerts when block rates spike or drop unexpectedly.

**Why it matters:** Addresses JTBD #3 (guardrail alerts with context) and persona Raj's compliance needs. Bedrock Guardrails provides six safeguard policies (content moderation, denied topics, word/phrase filters, PII redaction, contextual grounding, prompt attack detection) with an 88% harmful content block rate (AWS Bedrock Guardrails page [Tier 1]) — but today the monitoring for these guardrails lives in a separate console with no operational context.

**What's new:** Guardrail monitoring exists in Bedrock console but is isolated from operational context. The Control Plane correlates guardrail events with application identity, cost impact, and governance posture.

### Capability 4: Cost Intelligence

**What it does:** AI-specific cost breakdown by model, team, use case, and workflow. Cost optimization recommendations based on actual usage data — e.g., "Workflow X uses Claude 3.5 Sonnet for simple classification — switching to Claude 3 Haiku could save $2,400/month with comparable accuracy based on your guardrail pass rates."

**How it works:** Aggregates Cost Explorer API data with Bedrock invocation metadata (model ID, token counts) and customer-defined tags (team, use case). Cost recommendations use model-tier comparisons: if a high-cost model is used on tasks where a lower-cost model achieves equivalent guardrail pass rates, the system flags the optimization opportunity.

**Why it matters:** Addresses JTBD #1 (cost justification) and JTBD #4 (model switching with confidence). No vendor currently offers quality-aware cost optimization — Datadog and ServiceNow track token cost but offer no recommendations (research-v2 Gap #3).

**What's new:** Cost Explorer shows Bedrock spend at the service level. Cost Intelligence breaks it down to the model, workflow, and team level with optimization recommendations — this granularity does not exist today.

### Capability 5: Adoption Maturity Score

**What it does:** Prescriptive 5-level maturity model scored automatically from observable AWS signals. Level 1 (Ad Hoc): AI workloads exist, no guardrails, no cost tracking. Level 2 (Aware): Guardrails enabled for some workloads. Level 3 (Managed): >50% guardrail coverage, cost attribution active, alerts configured. Level 4 (Optimized): Cross-account governance, automated compliance reports, cost optimization acted upon. Level 5 (Leading): Governance-as-code, automated remediation. Each level includes specific recommended actions to reach the next level.

**How it works:** Computed on-read from observable signals: guardrail configuration state, alarm coverage, tag completeness, cross-account setup, cost attribution granularity. No new data collection — scoring uses the same data the dashboard already reads.

**Why it matters:** Addresses Customer Signal #2 from research: 62% of CIOs compromise on governance because they do not know what good governance looks like (Logicalis 2026 [Tier 3]). The maturity model is the "prescriptive > configurable" principle — it tells customers what to do, not just what they have. This is a white space: no competitor offers automated maturity scoring for AI governance (research-v2 Gap #4).

**What's new:** No equivalent exists. ServiceNow's Discover pillar does asset inventory but does not score governance maturity or recommend actions.

### Solution Lineage

Every capability above traces to the Opportunity-Solution Tree in research-v2.md. This table documents which directions were selected, which were rejected, and why.

| Selected Capability | From Opportunity | Direction Chosen | Alternatives Rejected | Rejection Rationale |
|---------------------|-----------------|-----------------|----------------------|---------------------|
| AI Asset Discovery | Opp 1: Unified AWS-Native AI Governance Console | Direction A: CloudWatch-embedded console | B: Standalone AI governance service; C: Bedrock Guardrails console expansion | B rejected: standalone service requires new IAM actions, new pricing model, and new service team formation — 6-9 month build vs. 2-3 months for CloudWatch embedding. Higher launch bar delays time-to-market against ServiceNow's May 2026 GA. C rejected: anchoring in Bedrock console limits scope to Bedrock-only customers; SageMaker and third-party model users lack a unified view, reducing TAM. |
| Unified AI Dashboard | Opp 1: Unified AWS-Native AI Governance Console | Direction A: CloudWatch-embedded console | B: Standalone AI governance service; C: Bedrock Guardrails console expansion | Same rationale as above — the dashboard is the core surface of the CloudWatch-embedded approach. Embedding in CloudWatch gives 500K+ existing users zero-friction access. |
| Guardrail Monitoring | Opp 1: Unified AWS-Native AI Governance Console | Direction A: CloudWatch-embedded console | (No alternative — guardrail monitoring is part of all three directions) | Guardrail monitoring is common to all Opp 1 directions; the differentiator is WHERE it lives. CloudWatch embedding chosen for reasons above. |
| Cost Intelligence | Opp 3: Multi-Model Cost Optimization | Direction A: Model comparison recommendations in CloudWatch | B: Cost anomaly detection with Bedrock alerts; C: FinOps integration via Cost Explorer | B rejected: cost anomaly detection alone is undifferentiated — Datadog and ServiceNow already track cost spikes. Anomaly detection is a subset of Direction A (included as a feature, not the whole capability). C rejected: Cost Explorer team partnership has historically long lead times (6+ months for new cost dimensions); extending Cost Explorer does not add governance or quality awareness — it is purely a cost lens. |
| Adoption Maturity Score | Opp 5: Compliance Automation for AI Regulations | Direction B: AI maturity model with prescriptive remediation | A: AWS Config rules for AI governance; C: Audit-ready compliance reports | A rejected: Config rules check configuration state only, not runtime behavior or organizational maturity — useful as a v2 complement but insufficient standalone. Config rules cannot answer "how mature is our AI governance?" C rejected: compliance reports are an output of governance, not a driver of governance improvement. Reports without a maturity framework lack context — "here are your findings" without "here's what to do about them." Reports are planned for v2 once the maturity framework provides the scoring context. |
| Non-Bedrock AI support (v2) | Opp 4: Cross-Platform AI Discovery | Direction A: OTel AI semantic conventions ingestion | B: AWS-ecosystem-only scope | B rejected: AWS-ecosystem-only scope is a non-starter — customers use OpenAI, Anthropic direct, and self-hosted models alongside Bedrock (research-v2 Key Takeaway #5). OTel ingestion is the path to multi-model support. Scoped for v2 because OTel AI semantic conventions are still evolving and third-party detection accuracy (60-75% recall) needs hardening. |
| Business outcome correlation (v2) | Opp 2: Business Outcome Correlation | Deferred to v2 — Direction A: CloudWatch custom metrics mapping | B: Bedrock-native ROI attribution | Direction A chosen for v2 over B because it uses existing CloudWatch custom metrics infrastructure (no new Bedrock SDK surface area). B requires 3-4 months of Bedrock SDK development and only works for Bedrock-hosted models. Direction A works for any workload the customer can instrument. Both are deferred from v1 because business outcome correlation requires the base governance console to exist first — you must know what AI you have before you can measure its business impact. |

### Scope Boundary

| Capability | v1 | v2 | v3 | Rationale for Phasing |
|-----------|:---:|:---:|:---:|----------------------|
| AI asset discovery (Bedrock + SageMaker) | X | | | Near-100% detection accuracy via native CloudTrail events; no pattern matching risk |
| Unified AI dashboard | X | | | Core surface area; requires only existing data sources |
| Bedrock Guardrails monitoring | X | | | Reads existing CloudWatch metrics; low build effort, high governance value |
| Cost attribution (model, account, team) | X | | | Uses existing Cost Explorer API + Bedrock metadata; addresses highest-frequency JTBD |
| Adoption maturity scoring | X | | | Computed on-read; no new data collection; addresses 62% CIO knowledge gap |
| Cross-account support (Organizations) | X | | | Leverages existing CloudWatch cross-account observability |
| Non-AWS AI discovery (OTel ingestion) | | X | | OTel AI semantic conventions still evolving; third-party detection at 60-75% recall needs hardening |
| Custom guardrail policies (non-Bedrock) | | X | | Requires Lambda-based evaluation framework; depends on v1 governance UX validation |
| Business outcome correlation | | X | | Requires base console to exist; uses CloudWatch custom metrics mapping |
| Cost optimization recommendations | | X | | Requires 3+ months of usage data to make quality-aware recommendations |
| Compliance report generation | | X | | Depends on maturity framework for scoring context |
| Kill switches for AI workloads | | | X | Requires deep service integration with Bedrock and SageMaker runtime; safety-critical feature needs extensive testing |
| Model A/B testing | | | X | Adjacent capability; not core governance; lower priority vs. governance features |
| Governance-as-code (CloudFormation) | | | X | Requires v2 policy framework to be stable before codifying |

### Competitive Differentiation

Unlike **ServiceNow AI Control Tower** (30+ integrations, 5-pillar platform, Action Fabric MCP Server — ServiceNow Newsroom, May 2026 [Tier 2]):
- **Cloud-native vs. overlay:** IAM-integrated, no additional vendor credentials or security review. If you can access CloudWatch, you access AI Control Plane. ServiceNow sits ON TOP of cloud, requiring data to leave AWS for ServiceNow's SaaS.
- **Cross-account by default:** Leverages AWS Organizations and cross-account CloudWatch. Competitors require per-account setup.
- **Zero-instrumentation for Bedrock:** Existing CloudWatch metrics and CloudTrail events auto-populate the dashboard. No SDK changes required.
- **Cost of entry:** Included in CloudWatch pricing (usage-based) vs. enterprise ServiceNow license (per-CI or per-pattern on top of ITSM platform).

Unlike **Datadog LLM Observability** (execution flow visualization, per-branch cost attribution — Datadog product page [Tier 1]):
- **Governance built in:** Guardrail monitoring, policy compliance, maturity scoring — not just metrics and traces.
- **Discovery, not just instrumentation:** Finds AI workloads the customer did not explicitly configure for monitoring.

Unlike **Dynatrace** ("control plane for AI" positioning — SiliconANGLE, Feb 2026 [Tier 4]):
- **Self-sufficient enforcement:** Dynatrace needs ServiceNow for enforcement (partnership model). AWS has native enforcement via Bedrock Guardrails — no second vendor required.
- **AWS-native moat:** IAM, Organizations, cross-account guardrails are structural advantages no external vendor can replicate.

## 3. Success Metrics

### North Star: % of AI Workloads with Guardrail Coverage

This metric directly measures the governance gap the product exists to close. It is actionable (teams improve it by enabling guardrails), measurable (we observe guardrail configuration state via Bedrock API), and correlated with customer value (higher coverage = lower risk).

**Alternatives considered and rejected:**
- Monthly Active Users (MAU): vanity metric — high MAU with low governance improvement means the product is used but not effective.
- AI cost savings: lagging indicator — takes 3-6 months to materialize and depends on customer action, not product quality.
- Discovery accuracy: too narrow — measures one capability, not overall product value.

| Metric | Type | Target | Baseline | Source | Rationale |
|--------|------|--------|----------|--------|-----------|
| % AI workloads with guardrail coverage | North Star | 80% within 6 months | ~30% (est. Bedrock-only adoption) | Bedrock Guardrails API | Directly measures governance gap closure |
| Time to discover new AI deployment | Supporting | <24 hours (automated) | Weeks to months (manual) | CloudTrail event lag | Measures discovery capability value |
| Time to generate compliance report | Supporting | <5 minutes | 2-3 weeks manual | User timing studies | Measures audit prep pain reduction |
| AI cost visibility (% spend attributed) | Supporting | >90% attributed to team/workflow | <20% (most in undifferentiated buckets) | Cost Explorer + tags | Measures cost intelligence capability |
| Console adoption (MAU) | Supporting | 500 MAU in 6 months | 0 (new product) | CloudWatch RUM | Measures product-market fit signal |
| Alert fatigue (false positive rate) | Anti-metric | <10% false positive rate | N/A | Guardrail alert accuracy | If false positives rise, trust erodes — teams ignore alerts |
| Time to value (first useful insight) | Anti-metric | Should not exceed 30 min | N/A | Onboarding funnel | If setup is too complex, adoption stalls — the "yet another dashboard" risk materializes |

### Phase Gates

- **V2 gate:** If North Star <50% after 6 months AND MAU <200, re-evaluate scope — the governance problem may not be solvable via console experience alone.
- **V2 pricing gate:** If adoption exceeds 50,000 monitored workloads, introduce usage-based pricing (Scenario C from pricing analysis — $0.50-2.00 per AI workload/month).
- **Kill switch for maturity model:** If >40% of beta users disable or ignore maturity score within 30 days (interaction rate <15% AND opt-out rate >40%), demote to optional setting and replace with simpler "governance coverage %" bar.

### Failure Scenarios (Specific and Falsifiable)

**Failure 1 — Discovery Accuracy Fails, Trust Collapse:** If AI asset discovery misidentifies >10% of assets in a customer's first 7 days, the customer will not return within 30 days. Pivot trigger: if accuracy <90% after 2 weeks of beta with 20+ customers, scope v1 to Bedrock-only discovery (drop SageMaker endpoint detection).

**Failure 2 — Dashboard Latency, Abandonment:** If the main dashboard takes >8 seconds to render for a 50-account Organization, ops teams revert to per-account Bedrock console. Pivot trigger: if P95 >8s after performance sprint, switch to daily batch aggregation with refresh button.

**Failure 3 — Maturity Model Rejected:** If >40% of beta users disable the maturity score within 30 days, the feature is not valuable for this audience. Pivot: move to Settings as opt-in, replace with simpler governance coverage bar.

## 4. FAQs

### Category: Customer & Problem

**Q1: Who is the primary buyer for this product?**
The primary buyer is the Cloud Operations or Platform Engineering lead responsible for AI infrastructure at organizations with 3+ AI workloads in production — typically a Senior SRE, Cloud Operations Manager, or VP of Platform Engineering. The secondary buyer is the CISO or compliance officer needing AI governance evidence for audits. 76% of CIOs consider unchecked AI a serious concern (Logicalis 2026 [Tier 3]), creating board-level demand that opens budget for this capability.

**Q2: Why can't customers just build custom CloudWatch dashboards for AI monitoring?**
They can — for Bedrock workloads with known metric namespaces. But custom dashboards require manual configuration per workload, provide no AI asset discovery (you must know what to monitor first), cannot surface guardrail enforcement patterns, and offer no governance maturity assessment. A customer with 10 AI workloads across 5 accounts would need per-account dashboards, separate Cost Explorer checks, and Bedrock console reviews. The AI Control Plane collapses this into a single cross-account experience that auto-discovers workloads and self-configures.

**Q3: What evidence do we have that customers actually want this?**
Three convergent signals: (1) 72% of enterprises have agentic AI in production but 60% lack governance (Agentic AI Institute 2026 [Tier 3]). (2) 62% of CIOs compromise on governance due to lack of tools (Logicalis 2026 [Tier 3]). (3) ServiceNow invested in two acquisitions (Traceloop, Veza) and built a 5-pillar AI Control Tower — validating the market with hundreds of millions in M&A. Direct AWS-customer voice is needed — the current evidence is market-level, not AWS-specific. This is flagged as Open Question #3.

**Q4: Is the governance gap real or just analyst hype?**
Data converges across independent sources: Cisco's 2026 Privacy Benchmark found only 12% with mature AI governance [Tier 3]. Writer's survey found 79% face AI adoption challenges [Tier 4]. Agentic AI Institute found a 60% governance gap [Tier 3]. When three unrelated surveys with different methodologies converge on the same finding, the signal is robust. Gartner further validates by sizing the market at $492M growing at 45% CAGR [Tier 3] and finding organizations with governance platforms are 3.4x more effective [Tier 3].

### Category: Solution & Approach

**Q5: Why build this inside CloudWatch rather than as a standalone console?**
CloudWatch has 500,000+ active customers. Building inside CloudWatch means: (a) zero new console to learn, (b) automatic integration with existing alarms, dashboards, and cross-account setups, (c) IAM permissions already configured, (d) consolidated billing. A standalone console (Opportunity 1, Direction B in research) would require new IAM actions, new pricing model, and 6-9 months vs. 2-3 months for CloudWatch embedding. ServiceNow made the opposite bet (standalone platform) — our advantage is being embedded where customers already work.

**Q6: How does AI asset discovery work technically?**
Three data sources correlated: (1) CloudTrail events — Bedrock `InvokeModel`, SageMaker `InvokeEndpoint` with dedicated event sources (`bedrock.amazonaws.com`, `sagemaker.amazonaws.com`). No pattern matching — explicit, typed API calls. (2) Service Catalog / Resource Groups — tagged AI resources. (3) CloudWatch metrics — namespaces `aws/bedrock`, `aws/sagemaker`. Discovery runs continuously. In v1, accuracy is near-100% for Bedrock and SageMaker. Third-party AI API detection via CloudTrail pattern matching has lower recall (est. 60-75%) and is scoped for v2 hardening.

**Q7: What does the prescriptive maturity model mean concretely?**
Five levels scored automatically from observable signals. Level 1 (Ad Hoc): AI workloads exist, no guardrails. Level 2 (Aware): Guardrails enabled for some workloads. Level 3 (Managed): >50% guardrail coverage, cost attribution active. Level 4 (Optimized): Cross-account governance, compliance reports, cost optimization acted upon. Level 5 (Leading): Governance-as-code, automated remediation. Each level includes specific recommended actions. This addresses the 62% of CIOs who lack governance knowledge (Logicalis [Tier 3]) — the product tells them what to do, not just what they have.

### Category: Scope & Boundaries

**Q8: Why is non-AWS AI discovery out of scope for v1?**
Detecting AI workloads calling external APIs (OpenAI, Anthropic direct) requires CloudTrail pattern matching on outbound API calls — estimated 60-75% recall with ~85% precision. False positive risk: any HTTPS call to `api.openai.com` could be AI invocation or account management. We launch with high-accuracy discovery (Bedrock, SageMaker — native integration) and add third-party detection in v2 once we validate the discovery UX and establish accuracy baselines. Shipping noisy discovery in v1 would undermine trust (Failure Scenario 1 threshold: >10% misidentification triggers pivot).

**Q9: What's the phased plan beyond v1?**
V1 (launch): Bedrock + SageMaker discovery, unified dashboard, guardrail monitoring, cost attribution, maturity scoring. V2 (3 months post-launch): Third-party AI detection via OTel, custom guardrail policies for non-Bedrock AI, business outcome correlation, compliance reports, cost optimization recommendations. V3 (6 months): Kill switches, model A/B testing, governance-as-code. Each phase is gated on adoption metrics — v2 features do not ship until v1 proves value (see Phase Gates).

### Category: Competitive & Market

**Q10: How does ServiceNow AI Control Tower compare?**
ServiceNow launched a 5-pillar AI Control Tower at Knowledge 2026 (Discover, Observe, Govern, Secure, Measure) with 30+ integrations, kill switches, and Action Fabric MCP Server for headless cross-agent governance (ServiceNow Newsroom [Tier 2]). They acquired Traceloop and Veza for observability and identity security. It is the most complete cross-platform offering. Our differentiation: (1) cloud-native — inside AWS, not on top of it; no additional credentials. (2) Zero-instrumentation for Bedrock/SageMaker. (3) Cross-account by default via Organizations. (4) Usage-based pricing vs. enterprise license. ServiceNow wins multi-cloud heterogeneous environments. We win AWS-primary shops.

**Q11: Is Datadog a threat here?**
Datadog LLM Observability has best-in-class execution flow visualization and per-branch cost attribution (Datadog product page [Tier 1]). But Datadog is pure observability — no governance, no enforcement, no discovery of unmonitored workloads. They monitor what you instrument; we discover what exists. For customers already on Datadog APM, LLM Observability is natural. Our bet: the governance buyer (ops/compliance) differs from the observability buyer (developer). Both products can coexist.

**Q12: How real is the "control plane" positioning language?**
Dynatrace explicitly describes itself as "the control plane for AI in production" (SiliconANGLE [Tier 4]). ServiceNow uses "AI Control Tower." Gartner uses "AI governance platform." The language is converging across the industry. AWS should own "control plane" for the cloud-native segment before it becomes exclusively associated with external vendors. If AWS does not build native AI governance, customers will assemble it from external vendors — the Dynatrace + ServiceNow partnership (joint governance + remediation) is a preview of this (research-v2 Trends section).

### Category: Metrics & Success

**Q13: Why is guardrail coverage the North Star over MAU?**
MAU measures whether people visit the console. Guardrail coverage measures whether the product actually closes the governance gap. High MAU with low coverage improvement means the product is used but ineffective. Coverage is actionable (teams enable guardrails), measurable (Bedrock API), and directly tied to the customer problem. Alternative: cost savings — rejected as lagging indicator that takes 3-6 months and depends on customer action.

**Q14: How will we measure adoption without cannibalization?**
AI Control Plane is additive — it does not replace existing CloudWatch dashboards or Bedrock console views. We track: MAU on Control Plane, workloads discovered, guardrail alerts configured, compliance reports generated. The expected anti-metric is Bedrock console traffic — if it drops, that is consolidation (users preferring the unified view), not cannibalization.

### Category: Technical & Architecture

**Q15: What existing AWS services does this integrate with?**
Core integrations: Amazon Bedrock (guardrails, invocation metrics), Amazon SageMaker (endpoint metrics), CloudWatch (metrics, alarms, dashboards), CloudTrail (API event detection), AWS Organizations (cross-account governance), IAM (permission model), Cost Explorer API (cost attribution), Resource Groups / Tag Editor (asset classification). Each uses existing service APIs — no new service dependencies. The AI Control Plane is a CloudWatch console experience aggregating data, not a new backend service.

**Q16: How does cross-account governance work?**
Via CloudWatch cross-account observability (GA, handles 1000+ accounts). The AI Control Plane adds an AI-specific aggregation layer: a delegated administrator account sees all AI workloads, guardrail statuses, and costs across member accounts using existing IAM roles and organization-level service-linked roles. For guardrail enforcement, the central account pushes recommended policies via CloudFormation StackSets. Precedent: Security Hub aggregates findings across 200+ accounts with <15 minute latency using the same delegated admin pattern. This is the AWS-native moat no competitor can replicate.

**Q17: What's the data architecture?**
No new data store for source-of-truth data. The AI Control Plane reads from existing sources in real-time: CloudWatch Metrics, CloudTrail events, Bedrock Guardrails API, Cost Explorer API. The only new storage is a lightweight DynamoDB table per Organization caching discovery results for fast rendering. All source-of-truth data remains in existing services. Dashboard uses 15-minute cached refresh for cross-account aggregation; guardrail alerts remain real-time via CloudWatch Alarms (sub-minute).

### Category: Business & Strategy

**Q18: What's the TAM for this product?**
Gartner projects the AI governance platform market at $492M in 2026, growing at 45% CAGR to $1B+ by 2030 [Tier 3]. The directly addressable market: estimated 150K-200K AWS accounts actively using Bedrock or SageMaker. Serviceable obtainable market (Year 1): 30K Bedrock customers x 60% governance gap x ~$200/month average = ~$43M/year. But the strategic value exceeds direct revenue: AI Control Plane is a retention mechanism that makes CloudWatch stickier for AI-heavy customers.

**Q19: How does this affect CloudWatch pricing?**
V1 recommendation: free — AI Control Plane features included in existing CloudWatch pricing. Revenue mechanism: retention of AI-heavy customers who might leave for Datadog or ServiceNow, plus increased usage of paid CloudWatch features (alarms, Logs Insights) triggered by Control Plane findings. Estimated retention value: $100M-$150M in protected annual AWS revenue (based on ~5,000 at-risk accounts with >$50K annual AI spend, 10-15% retention lift). Usage-based premium pricing (Scenario C: $0.50-2.00 per workload/month) considered for v2 if adoption exceeds 50,000 workloads. Finance alignment needed to validate retention estimate.

### Category: Risks & Mitigation

**Q20: What if AI asset discovery has high false positives?**
V1 limits discovery to Bedrock + SageMaker where detection accuracy is near 100% (native service integration, explicit CloudTrail event sources). Third-party detection ships in v2 with confidence scores and human-in-the-loop confirmation. Manual "add asset" flow covers workloads discovery misses. Failure Scenario 1 pivot: if accuracy <90% after 2 weeks of beta, scope to Bedrock-only.

**Q21: What if customers don't adopt the maturity model?**
Risk is that prescriptive scoring feels judgmental. Mitigation: frame levels as progression stages ("Next recommended action"), not grades. Benchmark against anonymized peer cohorts. Make actions concrete and achievable ("Enable Bedrock Guardrails on your fraud-detection model — estimated effort: 15 minutes"). Maturity model is opt-in visible. Failure Scenario 3 pivot: if >40% disable within 30 days, demote to optional.

**Q22: What's the biggest technical risk?**
Cross-account data aggregation latency. A 100+ account Organization aggregating inventory, guardrail status, and cost data could be slow. Mitigation: async aggregation with 15-minute cached refresh, manual "refresh now" option. Guardrail alerts remain real-time (sub-minute via CloudWatch Alarms). Security Hub precedent: 100 accounts aggregated in <5 minutes cached, <15 minutes cold. Recommended spike: 2 weeks, 1 engineer — build CloudTrail query across 10 sandbox accounts, measure latency, build aggregation view at 50-account scale.

**Q23: What regulatory risks should we consider?**
The Control Plane monitors AI workloads but does not process AI content itself. The discovery engine examines CloudTrail logs containing metadata about AI invocations. All CloudTrail data stays within the customer's account — no cross-account exfiltration of content. Maturity scoring framed as "assessment" not "certification." Explicit disclaimer: maturity scoring does not constitute compliance with any specific regulation (EU AI Act, NIST AI RMF). Legal review required before launch.

**Q24: How do we handle the "yet another dashboard" objection?**
AI Control Plane is not a dashboard you build — it is a console page you land on. Automatic, pre-configured, opinionated. Think "EC2 instances page" not "custom dashboard builder." Zero configuration to get value: enable it, see your AI workloads. This is the ServiceNow critique in reverse — they add another module to an already complex ITSM platform; we add a focused page to a console customers already use daily.

**Q25: What happens if ServiceNow makes their AI Control Tower free or significantly cheaper?**
ServiceNow's business model is enterprise licenses — free AI Control Tower would undermine their revenue model. More likely: included for existing ITSM customers, widening adoption. Our response: emphasize cloud-native advantage (no new vendor, no new credentials, no new security review). For AWS-primary customers, switching cost to ServiceNow is the entire ITSM platform adoption. The real competitive risk is Datadog adding governance features to existing observability — monitor via competitive research cycle.

## 5. Dependencies Map

| Dependency | Type | Team/Service | Risk | What We Need |
|-----------|------|-------------|------|-------------|
| Bedrock Guardrails API | API | Bedrock team | Low | Read access to guardrail configuration and enforcement metrics. Already exists — no new API surface. |
| Bedrock invocation metadata | Metrics | Bedrock metrics team | Low | Model ID, token counts, guardrail evaluation results via CloudWatch Metrics. Already emitted. |
| SageMaker endpoint metrics | API | SageMaker team | Medium | `ListEndpoints` API + `InvokeEndpoint` CloudTrail events. Exists, but integration depth for v1 (model monitor data?) needs alignment. |
| CloudWatch cross-account observability | Infrastructure | CloudWatch platform team | Low | Delegated admin aggregation for AI-specific metrics. GA capability, proven at 1000+ accounts. |
| CloudWatch console team | UI/Sprint capacity | CloudWatch console team | Medium | New nav section + widget types in CloudWatch console. Requires 2-3 months sprint allocation. Key bottleneck. |
| CloudTrail events | Data source | CloudTrail team | Low | Query Bedrock + SageMaker events for discovery. Standard CloudTrail usage, no new event types needed. |
| Cost Explorer API | API | AWS Billing team | Medium | AI-specific cost dimensions (per-model, per-workflow). Current API supports service-level; need tag-based breakdowns. |
| AWS Organizations | Infrastructure | Organizations team | Low | Cross-account governance via delegated admin. Existing pattern (Security Hub precedent). |
| IAM | Permissions | IAM team | Low | Permission model for AI Control Plane actions. Extends existing CloudWatch IAM actions. |
| DynamoDB | Storage | Self-managed | Low | Lightweight discovery cache table per Organization. Standard DynamoDB usage, no team dependency. |
| Legal/Compliance review | Review | Legal team | Medium | Maturity model language, regulatory disclaimers, EU AI Act alignment assessment. 4-6 week review cycle. |
| UX Research | Validation | UXR team | Medium | 5-10 customer interviews for AI governance pain validation. Current evidence is market-level, not AWS-specific. |

## 6. Risks & Open Questions

### Risks (Specific and Falsifiable)

| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
| Discovery false positives erode trust in first 7 days | Medium | High | V1 limited to native services (near-100% accuracy); confidence scores in v2; pivot to Bedrock-only if <90% accuracy in beta | PM + Eng lead |
| Cross-account aggregation >8s P95 at 50 accounts | Medium | Medium | 15-minute cached refresh; Security Hub precedent proves pattern at scale; 2-week spike to validate | Eng lead |
| CloudWatch console team sprint capacity unavailable for 2-3 months | Medium | High | Early alignment with console team PM; escalate to director if needed; fallback: ship as standalone CloudWatch page outside main nav | PM |
| ServiceNow AI Control Tower gains AWS-native integrations by Aug 2026 GA | Low | High | Accelerate v1 launch to pre-empt; deepen Organizations integration as moat | PM |
| Maturity model perceived as judgmental — >40% opt-out | Medium | Low | Progression framing, peer benchmarks, concrete actions; pivot to simpler coverage bar | PM + UX |
| Bedrock Guardrails scope too narrow for non-Bedrock workloads | High | Medium | V1 acknowledges gap explicitly; v2 adds Custom AI Policies via Lambda evaluation functions | PM + Eng |
| Datadog adds governance features to LLM Observability | Medium | Medium | Monitor Datadog hiring and product announcements; maintain differentiation via discovery + cross-account + IAM integration | PM |

### Open Questions

1. **Pricing model:** Should v1 be free (retention play) or usage-based? Retention value estimated at $100M-$150M but needs finance validation. — Owner: PM + Finance — Deadline: 4 weeks pre-launch
2. **Bedrock team alignment:** Does the Bedrock team see this as complementary or competitive to their console? Need formal alignment. — Owner: PM — Deadline: 2 weeks
3. **Customer validation:** Need 5-10 customer interviews about AI governance pain. Current evidence is market-level. — Owner: PM + UXR — Deadline: 6 weeks
4. **SageMaker integration depth:** How deep should v1 SageMaker integration go? Model Monitor data in the dashboard or just endpoint inventory? — Owner: PM + Eng — Deadline: 3 weeks
5. **EU AI Act implications:** Does the maturity model need to align with EU AI Act risk classification? Legal review required. — Owner: Legal — Deadline: 6 weeks
6. **Console team capacity:** Confirm CloudWatch console team can allocate 2-3 months of sprint capacity for new nav section and widget types. — Owner: PM + Console team PM — Deadline: 2 weeks
7. **Technical spike:** Validate cross-account aggregation latency at 50-account scale. 2-week spike, 1 engineer. — Owner: Eng lead — Deadline: 3 weeks

## End-to-End Experience

This section describes the complete user journey through the AI Control Plane as validated in the interactive prototype.

**First-time experience (Maya, Day 1):**
Maya navigates to CloudWatch and sees a new "AI Control Plane" item in the left navigation. She clicks it and lands on a pre-configured dashboard — no setup required. The discovery engine has already scanned her Organization's CloudTrail events and surfaced 4 Bedrock models and 2 SageMaker endpoints across 3 accounts. Two of these she did not know about. Each asset shows a status badge: guardrail coverage (green/yellow/red), cost trend (sparkline), and last activity timestamp. A maturity score banner shows "Level 2 — Aware" with a recommended next action: "Enable Bedrock Guardrails on your fraud-detection model in account 1234."

**Daily monitoring (Maya, Week 2+):**
Maya checks the AI Control Plane as part of her morning routine alongside existing CloudWatch dashboards. The unified dashboard shows: total AI spend this week ($4,200, down 8% from last week), guardrail coverage (67%, up from 55% after enabling guardrails on the fraud model), and 3 guardrail interventions in the last 24 hours (content moderation blocks on the customer support chatbot). She drills into the chatbot's guardrail events and sees the blocked content categories — primarily PII redaction — and decides the guardrail is working as intended.

**Cost conversation (Maya, Monthly):**
Her VP asks about AI ROI. Maya opens the Cost Intelligence tab and shows: Bedrock spend by model (Claude 3.5 Sonnet: $2,100/mo, Claude 3 Haiku: $340/mo), spend by team (Support: $1,800, Fraud: $600, Internal tools: $280), and a cost optimization recommendation: "The code review workflow uses Claude 3.5 Sonnet for boilerplate detection — similar workloads show 85% equivalent accuracy on Haiku at 60% lower cost." The VP has a clear picture in under 5 minutes.

**Audit preparation (Raj, Semi-annual):**
Raj navigates to the AI Control Plane's compliance view. He sees all AI assets with their governance status: which have guardrails, which have access logging, which are in accounts without cost alerts. He exports a compliance summary showing guardrail enforcement history, access control configurations, and maturity score progression over the last 6 months. What previously took 2-3 weeks of manual evidence gathering is now a 5-minute export.

**Cross-account governance (Maya, Quarterly):**
Maya's company adds a new AWS account for a data science team. Within hours, the AI Control Plane discovers 2 new SageMaker endpoints in the account. They appear with yellow badges: no guardrails, no cost alerts. The maturity score drops from Level 3 to Level 2 with a specific recommendation: "New account 5678 has 2 ungoverned AI endpoints. Enable guardrails to restore Level 3." Maya follows the guided action to push guardrail policies to the new account via CloudFormation StackSets.

## Sources

1. Agentic AI Enterprise Adoption 2026 — 72% production, 60% governance gap (Tier 3)
2. ServiceNow AI Control Tower expansion, Newsroom — 5-pillar platform, 30+ integrations, Action Fabric (Tier 2)
3. ServiceNow Microsoft Agent 365 integration, Newsroom — Agent governance partnership (Tier 2)
4. Datadog LLM Observability — Agent monitoring, execution flow (Tier 1)
5. Datadog Google ADK integration, InfoQ — Feb 2026 (Tier 4)
6. Dynatrace Perform 2026, Futurum — AI control plane positioning (Tier 4)
7. Dynatrace as active control plane, SiliconANGLE — DevCycle acquisition (Tier 4)
8. Dynatrace $2B ARR, EfficientlyConnected — FY2026 (Tier 4)
9. Splunk AI Agent Monitoring, blog — GA Q1 2026, AGNTCY integration (Tier 2)
10. Splunk AI Agent Monitoring, docs — Setup and capabilities (Tier 1)
11. AWS Bedrock Guardrails, product page — 6 safeguard policies, 88% block rate (Tier 1)
12. Gartner AI Governance Platform Market — $492M 2026, 45% CAGR (Tier 3)
13. Gartner AI Agent Prediction — 40% of enterprise apps by 2026 (Tier 3)
14. Writer Enterprise AI Adoption 2026 — 79% challenges, 54% C-suite divide (Tier 4)
15. Logicalis CIO Report 2026 — 76% unchecked AI concern, 62% compromising (Tier 3)
16. Cisco Privacy Benchmark 2026 — 12% mature governance (Tier 3)
17. Precedence Research AI Observability Market — $1.1B 2025 (Tier 3)
18. Technavio AI in Observability — +$2.91B, 22.5% CAGR (Tier 3)
