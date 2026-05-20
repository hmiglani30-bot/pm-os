---
artifact: prd
version: v3
topic: AI Control Tower Capability for Amazon Quick Desktop
timestamp: 2026-05-20T14:00:00Z
status: draft
total-words: ~8,600
sources-count: 18
---

# PRD: Quick Desktop AI Control Tower

## Decision to Inform
> Should Amazon Quick Desktop build an integrated AI Control Tower — a capability for discovering, observing, governing, securing, and measuring enterprise AI adoption from the desktop — positioned as the cross-vendor governance layer that only a desktop AI agent can deliver? If yes, what is the v1 scope and how should it be positioned against ServiceNow AI Control Tower?

## Executive Summary (190 words)

Enterprise AI adoption is outpacing governance: 82% of enterprises have unknown AI agents in their infrastructure (CSA 2026), yet only 12% have mature governance (Cisco 2026). Gartner sizes the AI governance platform market at $492M, growing 45% CAGR to $1B+ by 2030. Amazon Quick Desktop has a unique structural advantage: it already runs on employee desktops, integrates with 50+ enterprise applications, and maintains a personal knowledge graph of how users work. No other tool — not ServiceNow, not Datadog, not Dynatrace — has endpoint-level visibility into which AI tools employees actually use day to day.

Quick Desktop AI Control Tower embeds governance where employees work: discovering shadow AI from the desktop, guiding users toward compliant AI usage through assistant-style nudges, attributing AI costs across vendors, measuring adoption health, and automating compliance evidence. The positioning is "cockpit, not control tower" — governance embedded in the daily workflow, not layered on top of it in an IT dashboard. V1 anchors on AI discovery (the "show me my shadow AI" moment) plus an adoption dashboard, with governance enforcement and compliance automation in v2.

## 1. Customer Problem

### Primary Persona: Lisa Nakamura, Director of Digital Workplace

**Company:** Mid-market manufacturing firm, 3,500 employees, AWS + Microsoft hybrid environment.
**Role:** Oversees all end-user technology — productivity tools, collaboration platforms, AI adoption. Reports to CIO. Team of 8 IT operations staff.
**Technical sophistication:** Medium-high. Comfortable evaluating SaaS tools, managing vendor relationships, reading dashboards. Not writing CloudWatch queries.
**Current tools:** Microsoft 365 Admin Center (daily), ServiceNow ITSM (daily for tickets), Slack (constant), Quick Desktop Plus (new, piloting with 200 users), Salesforce (weekly), AWS Console (monthly, for cost reviews).

**Pain points:**
- Three months ago, the CEO asked "how many AI tools are our people using and what are they costing us?" Lisa couldn't answer. She found ChatGPT Plus subscriptions on 47 expense reports, Copilot licenses on 600 seats, Claude Team on the engineering Slack, Jasper on the marketing team, and Quick Desktop on her pilot group — all discovered manually over two weeks.
- No ongoing visibility into AI adoption. New tools appear without IT approval. 52% of department-level AI initiatives operate without formal oversight (EY 2026).
- Cannot enforce AI policies at the point of use. The company's AI acceptable-use policy exists as a PDF on the intranet. 29% of employees admit to sabotaging AI strategy (Writer 2026) — they'll use whatever tool works, policy or not.
- Budget pressure: the CFO wants AI spend consolidated and attributed to business units. Currently impossible across 5+ AI vendors with separate billing.

**Day in the life:** Lisa opens her morning with 3 ServiceNow tickets about AI tools: an employee asking for Claude access, a manager complaining about a ChatGPT data leak concern, and a finance request for AI spend reports. She has no single system that tells her what AI is being used, by whom, whether it's compliant, or what it costs. She opens Quick Desktop to handle her own work — and wonders why this tool can't also tell her what's happening with AI across the organization.

### Secondary Persona: David Park, VP of Engineering

**Company:** Same manufacturing firm, leads a 120-person engineering org.
**Role:** Owns engineering productivity, including AI tool adoption. Reports to CTO.
**Technical sophistication:** High. Former SRE. Manages AWS infrastructure budget.
**Current tools:** Quick Desktop Enterprise (power user), Jira, GitHub, Datadog (for APM), AWS Console, Slack.

**Pain points:**
- His engineers use Quick Desktop, Copilot, Claude, and ChatGPT interchangeably. He wants to know which tools drive the most productivity — and whether the $180K/year combined AI spend is worth it.
- Bedrock Guardrails protect the company's customer service chatbot but nothing governs the AI tools engineers use daily on their laptops.
- Cannot prove AI ROI to the CTO's quarterly review — anecdotally "we're more productive" but no data.

### Affected Stakeholders

- **CISO:** Needs visibility into AI data handling across vendors, especially for regulated data. 76% of CIOs say unchecked AI is a serious concern (Logicalis 2026).
- **CFO / Finance:** Needs cross-vendor AI cost attribution by business unit for budgeting and chargeback. Currently gets separate invoices from AWS, Microsoft, OpenAI, Anthropic.
- **Legal/Compliance:** Needs audit-ready evidence of AI governance posture for SOC 2 and emerging AI regulations (EU AI Act, NIST AI RMF).
- **Department managers:** Need to understand their team's AI usage to make tool selection and training decisions.

### Jobs to Be Done (ranked with rationale)

1. **When** the CEO asks "what AI are our people using and what does it cost," **I want to** pull up a single view showing every AI tool in use across the organization with cost per vendor/team, **so I can** answer in a 5-minute conversation instead of a 2-week investigation.
   - Frequency: Monthly | Pain: Critical | Persona: Lisa (primary)
   - Ranking rationale: Highest executive visibility combined with highest pain (2-week manual effort today). This is the gateway question — answering it unlocks every subsequent governance decision. 82% of enterprises have unknown AI agents (CSA 2026), making this the universal entry point.

2. **When** an employee uses an unapproved AI tool with sensitive data, **I want to** be notified immediately and have the employee guided toward a compliant alternative, **so I can** prevent data leaks without policing every desktop manually.
   - Frequency: Weekly | Pain: Critical | Persona: Lisa, CISO
   - Ranking rationale: High frequency (67% of executives believe their company has already suffered an AI-related data breach — Writer 2026) and critical severity (regulatory + reputational risk). But ranked #2 because enforcement requires discovery first — you can't govern what you can't see.

3. **When** I'm preparing the quarterly AI ROI report, **I want to** see adoption metrics, productivity correlation, and cost data across all AI tools, **so I can** justify continued investment or reallocate budget.
   - Frequency: Quarterly | Pain: High | Persona: Lisa, David
   - Ranking rationale: High dollar impact (AI spend often $500K+/year for mid-market) but lower frequency. Nobody does business outcome correlation well today — ServiceNow's Measure pillar just launched (research-v1 Competitor Analysis).

4. **When** we're evaluating a new AI tool for the sales team, **I want to** see how similar tools perform in our organization (adoption rate, usage patterns, user satisfaction), **so I can** make evidence-based procurement decisions instead of vendor demos.
   - Frequency: Quarterly | Pain: Medium | Persona: Lisa, department managers
   - Ranking rationale: Medium frequency and pain but high strategic value. Currently, tool selection is based on vendor marketing; organizational usage data doesn't exist.

5. **When** we're preparing for a compliance audit, **I want to** generate a report showing all AI tools, their data handling policies, governance controls, and usage history, **so I can** demonstrate responsible AI use without weeks of manual evidence gathering.
   - Frequency: Semi-annually | Pain: Critical when it happens | Persona: CISO, Legal
   - Ranking rationale: Lowest frequency but extremely painful when triggered. Gartner predicts 50% of AI agent deployment failures by 2030 due to insufficient governance (Gartner 2026). Regulations extending to 75% of economies by 2030.

### Problem Depth (550 words)

**Root cause:** AI adoption happened bottom-up. Employees adopted ChatGPT, Copilot, Claude, Jasper, and dozens of other AI tools individually — through browser tabs, desktop apps, browser extensions, and Slack integrations. No central system tracks this because: (1) cloud consoles only see cloud-side AI workloads (Bedrock, SageMaker) not desktop AI tools, (2) ITSM platforms like ServiceNow discover AI through API integrations and CMDB entries but can't see what runs on employee machines, (3) no endpoint-level AI visibility tool exists. The governance problem is architectural — the control point for AI governance must be where AI is used (the desktop), not where AI infrastructure runs (the cloud) or where IT workflows live (ITSM).

**Current workarounds (enumerated):**
1. Manual expense report auditing — finance searches credit card statements for AI vendor charges (ChatGPT Plus, Claude Pro, etc.). Misses team/enterprise licenses. Stale by the time it's compiled.
2. IT asset management queries — ServiceNow or similar CMDB checks for approved AI tools. Misses unapproved/shadow AI. Only discovers what's in the asset database.
3. Network traffic monitoring — some security teams inspect DNS/traffic for AI API endpoints (api.openai.com, api.anthropic.com). High false positive rate, encrypted traffic limits visibility, doesn't show what data was sent.
4. Policy-and-prayer — acceptable use policy published on intranet, annual training, hope for compliance. 29% employee sabotage rate (Writer 2026) shows this approach fails.
5. Vendor-by-vendor admin consoles — check M365 admin for Copilot usage, OpenAI admin for ChatGPT, AWS Console for Bedrock. No single view. Different metrics, different granularity, different reporting periods.

**Quantified cost of status quo:**
- **Time:** Lisa spent 2 weeks (80 hours) answering the CEO's AI inventory question. This repeats quarterly. ~320 hours/year for one person.
- **Risk:** 82% of enterprises have unknown AI agents (CSA 2026). 65% have experienced AI agent-related incidents (CSA 2026). A single data leak through an unapproved AI tool could cost $4.45M (IBM Cost of Data Breach 2025 average).
- **Money:** Without cross-vendor cost visibility, organizations overspend on duplicated AI tools (e.g., paying for both Copilot and ChatGPT Plus for the same users). Estimated 15-25% waste on redundant AI subscriptions — needs validation via customer interviews.
- **Compliance:** Gartner predicts 50% of AI agent deployment failures by 2030 due to insufficient governance platform enforcement. EU AI Act fines up to 7% of global turnover for non-compliance.
- **Organizational friction:** 54% of C-suite say AI adoption is "tearing the company apart" (Writer 2026). COOs worry about compliance while CIOs focus on capability. No shared visibility means no shared strategy.

**Who else is affected:** CFO cannot attribute AI costs to business units. Department managers cannot compare tool effectiveness. CISO cannot assess data handling risk across AI vendors. HR cannot target AI training to the teams that need it. The board cannot assess AI adoption maturity.

## 2. Solution Proposal

**Quick Desktop AI Control Tower** — a new capability section within Amazon Quick Desktop that provides cross-vendor AI governance from the desktop. Six core capabilities spanning five dimensions (Discover, Observe, Govern, Secure, Measure):

### Capability 1: AI Discovery Engine

**What it does:** Automatically detects AI tools in use across the organization by leveraging Quick Desktop's endpoint presence and integration layer. Discovers both sanctioned AI (Copilot, Bedrock, corporate ChatGPT) and shadow AI (personal ChatGPT accounts, browser-based AI tools, AI browser extensions) — building a living organizational AI inventory.

**How it works (high-level):** Hybrid approach combining (1) desktop signals — Quick Desktop's knowledge graph and app integration layer detect AI tool interactions (app launches, browser tabs, API calls) in a privacy-preserving way (aggregated, anonymized, opt-in per org policy), and (2) integration APIs — vendor admin APIs (M365 for Copilot, OpenAI org API, Anthropic admin, AWS for Bedrock) provide usage data for sanctioned tools. Desktop signals catch shadow AI; integrations provide depth for approved AI.

**Why it matters:** Addresses JTBD #1 (CEO's AI inventory question) and the universal entry point. 82% of enterprises have unknown AI agents (CSA 2026). Quick Desktop's endpoint visibility is the structural advantage: no other tool can detect what runs on employee desktops.

**What's new vs. status quo:** Today, AI discovery requires 2-week manual investigations or network traffic analysis. Quick Desktop inverts this: the tool employees use daily passively builds the AI inventory. The IT team sees it without asking.

### Capability 2: AI Adoption Dashboard (Command Center)

**What it does:** Single-pane view summarizing all five governance dimensions: what AI exists (Discover), how it's behaving (Observe), what policies apply (Govern), what risks are detected (Secure), and what value it's delivering (Measure). Pre-configured and opinionated — not a blank dashboard builder.

**How it works:** Aggregates data from the Discovery Engine, vendor integrations, and Quick Desktop's knowledge graph activity signals. Renders as a dedicated section within the Quick Desktop interface — accessible to IT admins and managers. Organization-level rollup with drill-down to team and tool level.

**Why it matters:** Addresses JTBD #1 and #3 — the single view that replaces 5+ vendor admin consoles and 2-week manual audits. The command-center pattern is table stakes — ServiceNow and Datadog both have hub dashboards.

### Capability 3: Governance Policy Engine

**What it does:** Allows IT admins to define AI acceptable-use policies (approved tools, data handling rules, usage limits by role) and Quick Desktop enforces them at the desktop level through assistant-model nudges rather than hard blocks.

**How it works:** Admin console for policy definition (approved tool list, data sensitivity rules, role-based access). When Quick Desktop detects a user interacting with a non-compliant AI tool or pasting sensitive data into an unapproved tool, it surfaces a contextual nudge: "I notice you're using [tool] with what looks like customer data. Want me to handle this through [approved alternative] instead?" Enforcement is guide-first, block-last — respecting the finding that 29% of employees sabotage AI strategy when governance is purely restrictive (Writer 2026).

**Why it matters:** Addresses JTBD #2 (prevent data leaks through compliant alternatives). This is the key differentiator: assistant-model governance (guide, don't just block) is a gap no competitor fills. ServiceNow governs through IT dashboards; Quick Desktop governs at the point of use.

### Capability 4: Security & Risk Detection

**What it does:** Monitors AI interactions for security risks — sensitive data exposure to unapproved AI tools, prompt injection patterns, policy violations — and alerts the security team with actionable context.

**How it works:** Leverages Quick Desktop's content awareness to detect when sensitive data patterns (PII, financial data, proprietary information) are being sent to AI tools. Integrates with Bedrock Guardrails for AWS-side enforcement. Provides security dashboards showing risk hotspots by team, tool, and data type.

**Why it matters:** Addresses JTBD #2 and CISO stakeholder needs. 67% of executives believe their company has suffered AI-related data breaches (Writer 2026). Desktop-level security detection is unique — cloud-side guardrails only protect cloud-hosted AI; Quick Desktop protects the endpoint.

### Capability 5: AI Cost Attribution

**What it does:** Cross-vendor AI cost tracking attributed to teams, tools, and use cases. Aggregates billing data from AWS (Bedrock), Microsoft (Copilot), OpenAI, Anthropic, and other vendors into a single cost view per business unit.

**How it works:** Pulls cost data from vendor admin APIs where available; estimates costs from usage patterns (via Quick Desktop activity data) where vendor APIs lack cost endpoints. Attributes spend to teams based on user-to-team mapping from the organization's identity provider (SSO integration).

**Why it matters:** Addresses JTBD #1 and #3 (CFO's cost justification question). No vendor currently offers cross-vendor, user-level AI cost attribution — this is a white space.

### Capability 6: Adoption Health & Maturity Scoring

**What it does:** Prescriptive 5-level maturity model scored per team/department: (1) Unaware — no AI tools detected, (2) Experimenting — ad hoc AI tool usage, no governance, (3) Adopting — approved tools in use, basic policies, (4) Optimizing — cost-tracked, ROI-measured, policy-enforced, (5) Governing — compliance-automated, maturity-managed. Each level includes specific recommended actions.

**How it works:** Computed from Discovery Engine signals, policy compliance data, cost attribution coverage, and governance configuration state. Scored per team, aggregated to organization level.

**Why it matters:** Addresses the 62% of CIOs who don't know what good governance looks like (Logicalis 2026). The maturity model tells organizations what to do next, not just what they have. No competitor offers automated AI adoption maturity scoring with prescriptive remediation.

### Solution Lineage

| Selected Capability | From Opportunity | Direction Chosen | Alternatives Rejected | Rejection Rationale |
|---------------------|-----------------|-----------------|----------------------|---------------------|
| AI Discovery Engine | Opp 1: Desktop-Level AI Discovery | Direction C: Hybrid discovery (desktop + integration) | A: Passive desktop-only; B: Integration-only | A rejected: misses sanctioned tool deep data (usage metrics, cost). B rejected: misses shadow AI entirely — defeats the core value proposition (82% unknown agents). Hybrid requires most effort (4-5 months) but delivers the unique value. |
| AI Adoption Dashboard | Opp 4: AI Adoption Measurement | Direction B: Adoption health scorecard | A: Productivity correlation engine | A rejected for v1: requires robust productivity baselines, correlation != causation risk, and privacy-sensitive productivity tracking. Scorecard is achievable from Discovery Engine signals without new data collection. Productivity correlation planned for v2. |
| Governance Policy Engine | Opp 2: Assistant-Model Governance | Direction A: Proactive policy assistant | B: Dashboard-only governance; C: Notification nudges | B rejected: replicates ServiceNow's dashboard approach at smaller scale — doesn't leverage Quick Desktop's assistant model. C rejected: weakest enforcement — notifications ignored. Direction A is highest-value but hardest; scoped as Eng v1 with simplified rule engine, full NLP content analysis in v2. |
| Security & Risk Detection | Opp 2: Assistant-Model Governance | Direction A: Proactive policy assistant (security subset) | N/A — security is a cross-cutting dimension | Security is integral to the governance policy engine, not a separate opportunity direction. Separated as a capability for clarity but technically part of the same system. |
| AI Cost Attribution | Opp 3: Cross-Vendor Cost Attribution | Direction A: User-level AI spend tracking | B: Activity-based cost estimation | B rejected for primary approach: estimates are unreliable and erode CFO trust. Direction A (vendor API cost data) provides accurate numbers. Direction B retained as fallback for vendors without cost APIs. |
| Adoption Health & Maturity | Opp 4: AI Adoption Measurement | Direction B: Adoption health scorecard | A: Productivity correlation engine | Same rationale as Dashboard row. Maturity scoring is achievable from governance signals; productivity correlation requires new data infrastructure. |

### Scope Boundary (Dual-Scope)

| Capability | Eng v1 | Proto v1 | v2 | v3 | Rationale |
|-----------|:------:|:--------:|:---:|:---:|-----------|
| AI Discovery (desktop + integration hybrid) | X | X | | | Core anchor feature — the "show me my shadow AI" moment. Desktop detection for shadow AI + top 3 vendor integrations (M365/Copilot, OpenAI, AWS/Bedrock). |
| AI Adoption Dashboard (command center) | X | X | | | Core surface area — the five-dimension hub with KPI hero bar. |
| Governance Policy Engine (simplified rules) | X | X | | | Simplified rule engine: approved/blocked tool list + basic data sensitivity nudges. Full NLP content analysis in v2. |
| Security Risk Alerts (basic) | X | X | | | Basic pattern matching for sensitive data + unapproved tool usage alerts. Deep content analysis in v2. |
| AI Cost Attribution (top 3 vendors) | X | X | | | AWS Bedrock + M365 Copilot + OpenAI cost APIs. Additional vendors in v2. |
| Maturity Scoring (5-level model) | X | X | | | Computed from Discovery + Policy signals. No new data collection needed. |
| Admin Console (policy management) | X | X | | | IT admin interface for setting approved tools, data policies, and team configurations. |
| Full NLP content analysis for governance | | X (simplified demo) | X | | Proto v1 shows the interaction; Eng v1 uses pattern matching; v2 adds ML-powered content classification. |
| Compliance report generation | | X (mock export) | X | | Proto v1 shows report preview; v2 generates real audit-ready exports. |
| Additional vendor integrations (10+) | | X (marketplace page) | X | | Proto v1 shows the integration marketplace page with "coming soon" connectors. V2 ships next 7+ integrations. |
| Productivity correlation engine | | X (mock insights) | X | | Proto v1 shows "AI ROI insights" with sample data. V2 builds real correlation from knowledge graph data. |
| Kill switches / hard blocking | | X (enforcement page) | | X | Proto v1 shows the enforcement UI with toggle. V3 implements real-time agent termination. Safety-critical requires extensive testing. |
| Governance-as-code (policy templates) | | X (template library page) | | X | Proto v1 shows template library. V3 implements importable/exportable policy-as-code. |
| Cross-org benchmarking | | | | X | Requires aggregated anonymized data from multiple organizations. Long-term network effect feature. |

### Competitive Differentiation

Unlike **ServiceNow AI Control Tower** (5-pillar platform, 30+ integrations, kill switches, Action Fabric — ServiceNow Newsroom, May 2026 [Tier 2]):
- **Cockpit vs. control tower:** Quick Desktop governance lives where employees work — not in an IT dashboard nobody outside IT visits. ServiceNow governs from above; Quick Desktop governs from within.
- **Desktop-level discovery:** Quick Desktop detects shadow AI at the endpoint. ServiceNow discovers through API integrations and CMDB — misses what runs on employee desktops.
- **Assistant-model enforcement:** Quick Desktop guides users toward compliant alternatives in real time. ServiceNow enforces through IT workflows — after the fact.
- **Pricing:** $20/user/month with free tier vs. enterprise ITSM contract. Zero-procurement pilots possible.

Unlike **Datadog LLM Observability** (execution flow visualization, agent monitoring — Datadog product page [Tier 1]):
- **Governance, not just observability:** Quick Desktop adds policy enforcement, compliance automation, and adoption measurement. Datadog monitors; Quick Desktop governs.
- **Discovery, not instrumentation:** Quick Desktop finds AI tools employees use. Datadog monitors what developers instrument.
- **End-user-facing:** Quick Desktop serves business operations leaders. Datadog serves developers.

Unlike **Dynatrace** ("control plane for AI" positioning — SiliconANGLE [Tier 4]):
- **Self-sufficient:** Dynatrace needs ServiceNow for enforcement (partnership model). Quick Desktop handles observation AND enforcement in one product.
- **Desktop-native:** No agent installation beyond Quick Desktop itself. Dynatrace requires separate infrastructure agents.

## 3. Success Metrics (380 words)

### North Star: % of Organization's AI Tools Discovered and Governed

This metric directly measures the governance gap the product exists to close. "Discovered" = AI tool detected by the Discovery Engine. "Governed" = policy applied (approved, blocked, or monitored). This is actionable (IT teams improve it by setting policies), measurable (Discovery Engine + Policy Engine data), and tied to customer value (higher coverage = lower shadow AI risk).

**Alternatives considered and rejected:**
- Monthly Active Users (MAU): vanity metric — high MAU with zero discovery coverage means the product is used but governance gap persists.
- Cost savings: lagging indicator — takes 6+ months to materialize and depends on customer budget actions, not product quality.
- Discovery count: too narrow — counts assets found but not whether they're governed.

| Metric | Type | Target | Baseline | Source | Rationale |
|--------|------|--------|----------|--------|-----------|
| % AI tools discovered & governed | North Star | 70% within 6 months | ~15% (est. — only IT-approved tools are "governed" today) | Discovery Engine + Policy Engine | Directly measures governance gap closure |
| Time to complete AI inventory | Supporting | <1 hour (automated) | 2 weeks manual | User timing studies | Measures discovery value — the "CEO question" test |
| Shadow AI tools detected per org | Supporting | 5+ in first 30 days | 0 (currently invisible) | Discovery Engine | Measures the "aha" moment that drives adoption |
| Cross-vendor cost visibility (% spend attributed) | Supporting | >80% of AI spend attributed | <20% (most unknown) | Cost Attribution Engine | Measures CFO value |
| Governance policy compliance rate | Supporting | >60% within 6 months | ~0% (no policies enforced today) | Policy Engine | Measures enforcement effectiveness |
| User override rate on governance nudges | Anti-metric | <40% override rate | N/A | Policy Engine | If users override >40% of nudges, policies are too restrictive or nudges are poorly timed — trust erodes |
| Time-to-value (first discovery insight) | Anti-metric | <30 minutes | N/A | Onboarding funnel | If setup takes >30 min, adoption stalls |

### Phase Gates
- **V2 gate:** If North Star <30% after 6 months AND shadow AI detection <3 tools per org, re-evaluate discovery approach — desktop detection may be less effective than expected.
- **V2 pricing gate:** If governance feature adoption exceeds 50,000 users, evaluate governance-tier pricing ($5-10/user/month add-on to Quick Desktop Plus).
- **Maturity model kill switch:** If >40% of admins disable maturity scoring within 30 days, demote to optional and replace with simpler governance coverage bar.

## 4. FAQs (25 total)

### Category: Customer & Problem

**Q1: Who is the primary buyer for AI Control Tower?**
The primary buyer is the Director of Digital Workplace, IT Operations, or equivalent role responsible for end-user technology and AI adoption. In mid-market companies (1,000-10,000 employees), this person manages the tools employees use daily and fields the CEO's AI questions. The secondary buyer is the CISO needing AI governance evidence. The economic buyer is the CIO responding to board pressure — 76% of CIOs say unchecked AI is a serious concern (Logicalis 2026 [Tier 3]).

**Q2: Why can't customers just use ServiceNow AI Control Tower?**
They can — and for large enterprises with existing ServiceNow ITSM contracts, it's a strong option. But ServiceNow is an IT operations platform that sits on top of enterprise applications; employees never interact with it during their daily workflow. ServiceNow discovers AI through API integrations and CMDB entries — it cannot detect shadow AI running on employee desktops. Quick Desktop's structural advantage is endpoint visibility: it's already running where AI is being used. For mid-market organizations without a ServiceNow contract ($100K+ annual ITSM license), Quick Desktop at $20/user with a free tier is a fundamentally different adoption path.

**Q3: Is shadow AI really that big of a problem?**
Yes. The Cloud Security Alliance (April 2026) found 82% of enterprises have unknown AI agents in their infrastructure, and 65% have experienced AI agent-related incidents. Writer's 2026 survey found 67% of executives believe their company has already suffered data leaks from unapproved AI tools. The 29% employee sabotage rate (Writer 2026) means governance-by-policy alone fails. The problem is structural: AI adoption happened bottom-up, and existing governance tools operate top-down from cloud consoles and ITSM platforms that lack endpoint visibility.

### Category: Solution & Approach

**Q4: Why build this inside Quick Desktop rather than as a standalone product?**
Quick Desktop has 50+ enterprise integrations, runs on employee machines, and maintains a personal knowledge graph — this is the infrastructure needed for desktop-level AI discovery. Building standalone would require recreating this endpoint presence from scratch. Additionally, Quick Desktop's assistant model enables guide-don't-block governance that a standalone dashboard cannot deliver. The "yet another dashboard" objection kills standalone governance tools; embedding in Quick Desktop means zero new tools for employees and IT teams already using Quick.

**Q5: How does desktop-level AI discovery work without violating employee privacy?**
Three safeguards: (1) Opt-in at the organization level — IT admins enable discovery through the admin console; it's not on by default. (2) Aggregation, not surveillance — the Discovery Engine reports "Marketing team uses 4 AI tools: Copilot, ChatGPT, Jasper, Claude" not "Jane pasted customer PII into ChatGPT at 2:47 PM." Individual-level data is available only with explicit employee consent or as anonymized patterns. (3) Data stays local — discovery signals are processed on-device and only aggregated summaries are transmitted. Quick Desktop's existing privacy architecture (data not used to train external models) extends to governance signals.

**Q6: What does "assistant-model governance" mean in practice?**
When Quick Desktop detects a user interacting with a non-compliant AI tool or sending sensitive data to an unapproved service, it surfaces a contextual suggestion — not a block screen. Example: "I notice you're drafting a customer proposal in ChatGPT. Would you like me to handle this in Quick Desktop instead? Our company's AI policy recommends using approved tools for customer data." The user can accept the suggestion, dismiss it, or snooze it. Override rates are tracked and surfaced to IT admins as policy compliance signals. This is fundamentally different from ServiceNow's enforcement (kill switches, workflow blocks) — it respects employee autonomy while nudging toward compliance.

**Q7: How does this integrate with existing AWS governance tools?**
The AI Control Tower complements Bedrock Guardrails and CloudWatch, not replaces them. Bedrock Guardrails continue to enforce content safety for Bedrock-hosted models at the API layer. CloudWatch continues to provide infrastructure metrics. The AI Control Tower adds the cross-vendor, desktop-level layer: it discovers non-AWS AI tools, governs usage at the endpoint, and provides the unified view that connects AWS-side metrics with third-party AI usage data. For AWS-heavy organizations, the Control Tower also surfaces Bedrock Guardrail status and CloudWatch metrics in the unified dashboard.

### Category: Scope & Boundaries

**Q8: What's in v1 vs. v2?**
V1: AI Discovery (hybrid desktop + top 3 vendor integrations), Adoption Dashboard, simplified Governance Policy Engine (approved/blocked lists + basic sensitivity nudges), basic Security Risk Alerts, Cost Attribution (AWS + M365 + OpenAI), Maturity Scoring. V2 (3-6 months): full NLP content analysis, compliance report generation, 10+ vendor integrations, productivity correlation engine. V3 (6-12 months): kill switches, governance-as-code, cross-org benchmarking. Each phase is gated on adoption metrics.

**Q9: Why is full NLP content analysis out of v1?**
Real-time content classification (determining whether text contains PII, financial data, or proprietary information) requires ML model deployment and tuning with low false-positive rates. V1 uses pattern matching (regex for SSN formats, credit card numbers, email patterns) which covers 60-70% of sensitive data detection with near-zero false positives. V2 adds ML-powered classification for nuanced content types. Shipping noisy content analysis in v1 would undermine user trust in the governance nudges — false positives erode compliance willingness.

**Q10: Why only 3 vendor integrations in v1?**
The top 3 vendors (AWS/Bedrock, Microsoft/Copilot, OpenAI/ChatGPT) cover an estimated 70-80% of enterprise AI usage. Each integration requires API partnership, authentication flow, data mapping, and testing — 4-6 weeks per vendor. V1 ships the 3 highest-coverage integrations; v2 adds Anthropic/Claude, Google/Gemini, Jasper, and others. The prototype shows the full integration marketplace to demonstrate vision.

### Category: Competitive & Market

**Q11: How does the $492M market size apply to Quick Desktop?**
Gartner's $492M (2026) covers the entire AI governance platform market [Tier 3]. Quick Desktop's serviceable addressable market is the desktop-delivered, cross-vendor segment — estimated at ~$200M (40% of total market addressable via desktop agent approach). Year 1 SOM: ~$12M (500K Quick Desktop users x 10% governance adoption x $20/month tier upgrade). The strategic value exceeds direct revenue: AI Control Tower is a retention and upgrade mechanism that makes Quick Desktop stickier for enterprise customers.

**Q12: What if Microsoft adds AI governance to Copilot?**
Likely — Microsoft has the desktop presence (Windows + M365) and the AI governance need. But Microsoft's governance would be M365-centric, not cross-vendor. Copilot governance would cover Copilot usage but not ChatGPT, Claude, Bedrock, or Jasper. Quick Desktop's cross-vendor positioning (50+ integrations including non-Microsoft tools) is the defensive moat. The risk: if Microsoft ships cross-vendor governance first, Quick Desktop loses the window. Monitor Microsoft Ignite 2026 for signals.

### Category: Metrics & Success

**Q13: Why is "% discovered and governed" the North Star over MAU?**
MAU measures visits. Discovery + governance rate measures whether the product actually closes the governance gap. High MAU with 10% governance coverage means the dashboard is interesting but useless. The North Star ties directly to the customer problem (82% unknown agents) and is actionable by IT teams (enable policies, approve tools, configure alerts).

**Q14: How do we handle the cold-start problem?**
Discovery provides instant value — within 30 minutes of enabling, the Discovery Engine surfaces AI tools detected from Quick Desktop's knowledge graph and connected integrations. The "aha" moment (discovering shadow AI tools IT didn't know about) drives admin engagement. Target: 5+ shadow AI tools discovered per organization in the first 30 days. If cold-start time-to-value exceeds 30 minutes, the onboarding needs redesign.

### Category: Technical & Architecture

**Q15: What data does the Discovery Engine actually collect?**
Application-level metadata, not content. "User launched ChatGPT at 9 AM" and "User interacted with Claude Slack bot" — not "User typed this prompt." Detection signals: app process names, browser tab domains (ai.com, chat.openai.com, claude.ai, copilot.microsoft.com), API endpoint patterns from Quick Desktop's integration layer. Content of AI interactions is never collected for discovery — only for real-time governance nudges (processed on-device, not stored).

**Q16: How does cross-vendor cost attribution work technically?**
Three data sources: (1) Vendor admin APIs (M365 Admin Center for Copilot seat costs, OpenAI Organization API for usage/spend, AWS Cost Explorer for Bedrock) providing exact costs. (2) License management data — Quick Desktop integration with SSO/IdP maps users to teams, enabling per-team attribution. (3) Usage-based estimation for vendors without cost APIs — Quick Desktop activity signals (interaction count, estimated tokens) multiplied by published per-token pricing.

**Q17: What's the deployment model?**
Quick Desktop AI Control Tower ships as a capability update to Quick Desktop Enterprise/Professional tiers — no additional agent installation. Admin console is a web-based dashboard accessible through Quick Desktop's management portal. Discovery Engine runs within the existing Quick Desktop process on each endpoint. Governance policies sync from the admin console to each Quick Desktop instance.

### Category: Business & Strategy

**Q18: How does this affect Quick Desktop pricing?**
V1 recommendation: AI Control Tower capabilities included in Professional and Enterprise tiers (drives tier upgrades from Plus). Discovery-only included in Plus tier as a teaser — see your AI tools, upgrade to govern them. Free tier shows the AI Control Tower section with a value proposition and upgrade CTA. This creates a natural land-and-expand motion: free Quick Desktop → Plus for basic AI visibility → Professional/Enterprise for governance.

**Q19: Does this compete with or complement Bedrock Guardrails?**
Complements. Bedrock Guardrails enforce content safety at the API layer for Bedrock-hosted models. AI Control Tower provides the desktop-level, cross-vendor governance layer. They serve different control points: Guardrails = cloud-side API enforcement; Control Tower = endpoint-side user governance. Organizations need both. The Control Tower surfaces Bedrock Guardrail status in its dashboard, creating a unified governance view that strengthens both products.

**Q20: What's the go-to-market strategy?**
Phase 1 (launch): "Discover your shadow AI" campaign — free discovery scan for any Quick Desktop user. Show enterprises what AI tools they don't know about. This is the hook that drives adoption. Phase 2 (1 month post-launch): governance tier promotion — "Now that you see the problem, here's how to govern it." Phase 3 (3 months): enterprise case studies, compliance-focused marketing for regulated industries.

### Category: Risks & Mitigation

**Q21: What if desktop AI detection has high false positives?**
Risk: detecting non-AI applications as AI tools (e.g., a website with "AI" in the domain). Mitigation: v1 detection uses a curated allowlist of known AI tool domains and process names — not heuristic-based detection. Allowlist approach has near-100% precision but lower recall (misses new/niche AI tools). V2 adds ML-based detection for emerging tools. Fallback: manual "add tool" flow for IT admins to register AI tools the Discovery Engine misses.

**Q22: What if employees reject governance nudges?**
Risk: 40%+ override rate means governance is perceived as obstructive. Mitigation: (a) nudges are suggestions, not blocks — respects autonomy; (b) nudge frequency is capped per user per day; (c) IT admins can tune sensitivity; (d) override data becomes a signal (high override = policy too restrictive, not employee non-compliance). Failure scenario: if override rate >50% after 60 days, redesign nudge UX — likely too intrusive or poorly timed.

**Q23: What's the biggest privacy risk?**
Employee perception that Quick Desktop is "spying" on their AI usage. This is the existential risk for the product. Mitigation: (a) discovery is opt-in at org level with transparent employee notification; (b) individual-level data requires explicit consent; (c) default reports show team-level aggregates, not individual usage; (d) "What we see" transparency page in Quick Desktop shows employees exactly what data is collected; (e) data processed on-device by default. Launch requires employee communications template and FAQ.

**Q24: What if ServiceNow makes AI Control Tower free for existing ITSM customers?**
ServiceNow's business model is enterprise licenses — free governance would undermine ITSM revenue. More likely: bundled for existing customers, widening adoption. Our response: emphasize desktop-level discovery (ServiceNow can't match), assistant-model governance (ServiceNow doesn't have a desktop agent), and the $20 vs. $100K+ pricing gap for organizations without ServiceNow. The real threat is Microsoft adding governance to Copilot — monitor Ignite 2026.

**Q25: How do we handle regulatory uncertainty?**
AI governance regulations are evolving rapidly. Risk: building compliance features aligned to today's regulations that become obsolete. Mitigation: (a) compliance templates are updatable (not hardcoded); (b) v1 focuses on universally applicable governance (discovery, policy enforcement, audit trail) rather than regulation-specific compliance; (c) compliance report generation scoped for v2 to allow regulatory landscape to stabilize. Legal review required before any compliance-related claims in marketing or product UI.

## 5. Dependencies Map

| Dependency | Type | Team/Service | Risk | What We Need |
|-----------|------|-------------|------|-------------|
| Quick Desktop knowledge graph | Data | QD Core team | Medium | Access to app interaction signals for AI tool detection. Knowledge graph architecture may need extensions for governance aggregation. |
| Quick Desktop integration framework | API | QD Integrations team | Low | Existing 50+ integrations provide the foundation. Need API access patterns for vendor admin endpoints (M365, OpenAI). |
| Quick Desktop notification system | UI | QD Core team | Low | Existing proactive notification system for governance nudges. May need new notification types. |
| Quick Desktop admin console | UI/New | QD Enterprise team | High | New admin interface for policy management, team configuration, and organizational dashboards. This is the biggest new surface area. |
| M365 Admin Center API | External API | Microsoft partnership | Medium | Copilot usage and cost data. Requires API partnership agreement. Data access may be limited. |
| OpenAI Organization API | External API | OpenAI partnership | Medium | ChatGPT usage and cost data for enterprise customers. API exists but access terms need negotiation. |
| AWS Bedrock / Cost Explorer APIs | API | AWS internal teams | Low | Existing APIs for Bedrock metrics and cost data. Standard AWS service integration. |
| SSO/IdP integration | Data | QD Enterprise team | Low | User-to-team mapping for cost attribution and team-level reporting. Likely exists for enterprise tier. |
| Legal/Privacy review | Review | Legal team | High | Privacy framework for desktop AI detection, employee notification templates, regulatory disclaimers. 6-8 week review cycle. Critical path. |
| UX Research | Validation | UXR team | Medium | 8-10 customer interviews for AI governance pain validation and nudge UX testing. Current evidence is market-level surveys, not Quick Desktop-specific. |

## 6. Risks & Open Questions

### Risks (specific and falsifiable)

| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
| Employee "spying" perception kills adoption | Medium | Critical | Transparency page, opt-in, team-level aggregation defaults, employee FAQ | PM + Legal |
| Desktop AI detection accuracy <80% in first 30 days | Low | High | Curated allowlist approach (high precision); manual "add tool" fallback | Engineering |
| M365 Admin API access denied or delayed by Microsoft | Medium | Medium | V1 ships without Copilot cost data; desktop detection still catches Copilot usage | Partnerships |
| ServiceNow ships desktop agent for AI governance | Low | High | Accelerate v1 launch; desktop-native knowledge graph is 18+ month head start | PM |
| Governance nudge UX annoys users, >50% override rate | Medium | Medium | Frequency caps, tunability, A/B test nudge formats in beta | Design |
| Privacy regulations restrict desktop AI detection in EU | Medium | High | Legal review before EU launch; may need EU-specific detection scope | Legal |

### Open Questions
1. **Does Quick Desktop's knowledge graph currently capture AI tool interaction signals?** — Owner: QD Core Engineering — Deadline: Week 2
2. **What M365 Admin API data is available for Copilot usage/cost?** — Owner: Partnerships — Deadline: Week 3
3. **What is the actual shadow AI prevalence among Quick Desktop pilot organizations?** — Owner: UXR — Deadline: Week 4 (via customer interviews)
4. **Can governance nudges be surfaced without impacting Quick Desktop's core assistant latency?** — Owner: QD Performance Engineering — Deadline: Week 3
5. **What employee notification is legally required for desktop-level AI detection in US/EU/UK?** — Owner: Legal — Deadline: Week 4

## Sources

1. Cloud Security Alliance — 82% unknown AI agents, 65% AI incidents survey, Apr 2026 (Tier 3)
2. Cisco Privacy Benchmark 2026 — 12% mature governance (Tier 3)
3. Gartner — AI governance platform market $492M, 45% CAGR, Feb 2026 (Tier 3)
4. Gartner — 50% AI agent failures from insufficient governance by 2030 (Tier 3)
5. Gartner — 3.4x effectiveness with governance platforms, Q2 2025 (Tier 3)
6. ServiceNow Newsroom — AI Control Tower Knowledge 2026, 5-pillar platform (Tier 2)
7. Datadog product page — LLM Observability features (Tier 1)
8. Dynatrace — "control plane for AI" positioning, SiliconANGLE (Tier 4)
9. Writer Enterprise AI Adoption 2026 — 79% challenges, 54% tearing apart, 29% sabotage (Tier 4)
10. EY survey — 52% department AI without oversight, Mar 2026 (Tier 3)
11. Logicalis CIO Report 2026 — 76% unchecked AI concern, 62% compromising on governance (Tier 3)
12. AWS product page — Amazon Quick features and pricing (Tier 1)
13. AWS About Amazon — Quick Desktop launch, Apr 2026 (Tier 1)
14. Splunk docs — AI Agent Monitoring GA (Tier 1)
15. Dynatrace press — Bindplane and DevCycle acquisitions (Tier 2)
16. Deloitte State of AI 2026 — governance readiness data (Tier 3)
17. SiliconANGLE — Quick Desktop proactive desktop coverage (Tier 4)
18. InfoQ — Datadog Google ADK integration (Tier 4)

---

## End-to-End Experience (Design Feedback — v2 patch from Stage 4)

*Added by Designer stage (design-spec-v1). This section captures design decisions, assumptions, and scope adjustments discovered during UX design.*

### Canonical User Flow (as designed)

1. **Entry:** User navigates to AI Control Tower via Quick Desktop sidebar. Lands on Command Center.
2. **Orientation (0 clicks):** Hero KPI bar shows 5 governance dimensions at a glance — tools discovered, spend, governed %, active risks, maturity level. Answers the CEO's AI question in 5 seconds.
3. **Alert triage (1 click):** Shadow AI alert zone highlights newly discovered unapproved tools. Click any alert to open AI Inventory with pre-applied filter.
4. **Investigation (2 clicks):** AI Inventory table with sort/filter/pagination. Click any tool row to open split-panel detail: usage data, cost, compliance status, risk assessment, user list.
5. **Action (3 clicks):** "Apply Policy" button in split panel → modal with Approve/Monitor/Block options + conditions → confirm. Policy propagates to affected users within 24 hours.
6. **Reporting:** Cost Attribution page for CFO questions. Adoption & Maturity page for quarterly reviews. Governance page for compliance posture.
7. **Configuration:** Admin Console for integration management, notification tuning, team setup. Audit Log for compliance evidence.

### Navigation Architecture (13 pages)

| # | Page | Eng v1 | Proto v1 |
|---|------|:------:|:--------:|
| 1 | Command Center | Full | Full |
| 2 | AI Inventory | Full | Full |
| 3 | Governance | Full | Full |
| 4 | Security & Risk | Full | Full |
| 5 | Cost Attribution | Full | Full |
| 6 | Adoption & Maturity | Full | Full |
| 7 | Admin Console | Full | Full |
| 8 | Activity Audit Log | Full | Full |
| 9 | Integration Marketplace | Top 3 only | Placeholder (10+ coming soon) |
| 10 | Compliance Reports | — | Placeholder (mock export) |
| 11 | Enforcement Rules | Simplified | Placeholder (full rule builder) |
| 12 | AI ROI Insights | — | Placeholder (mock data) |
| 13 | Policy Templates | — | Placeholder (template library) |

### Design-Driven Scope Additions

1. **Activity Audit Log (new Eng v1 requirement):** Enterprise governance buyers require a filterable audit trail of all governance actions (policy changes, tool approvals, nudge overrides). Design adds this as a primary page under Admin Console. Engineering effort: ~1 sprint (table with filter, timestamp, user, action fields backed by existing event logging).

2. **Deep-link URL state management (new Eng v1 requirement):** Every meaningful UI state (filters, selected tool, active tab, time range) must be representable as a URL for Slack sharing, runbook embedding, and browser bookmarking. Engineering effort: frontend routing framework with query parameter serialization.

3. **Saved views / user preferences API (new dependency):** The design supports saved filter views (e.g., Lisa's "Unapproved Tools" view). This requires a user preferences storage API in Quick Desktop. Engineering effort: ~0.5 sprint if Quick Desktop has existing preferences infrastructure.

### Design Assumptions Documented

- Navigation is sidebar-based (7 primary + 6 sub-nav items), not tab-based.
- Governance actions happen inline from tool detail (split panel → modal), not from a separate policy management workflow.
- Cost estimates for vendors without APIs show confidence indicators to maintain trust.
- Maturity scoring is computed per-team and aggregated to org-level.

---

## Prototype Validation (v3 patch from Stage 5)

*Added by Prototype Builder stage (prototype-v1.html). Updates the canonical user flow based on the validated prototype.*

### Validated Prototype Flow

The prototype (prototype-v1.html, 107KB, single-file, zero external dependencies) validates the following end-to-end flow:

1. **Command Center** — hero KPI bar (5 metrics), shadow AI alert zone (4 alerts), dimension summary cards, recent activity feed. Entry point for all governance workflows.
2. **AI Inventory** — 18 AI tools across 8 vendors and 6 teams. Sortable, filterable, paginated table with tabs (All/Shadow AI/Approved/Blocked). Row click opens split panel with 4-tab detail view.
3. **Governance action** — "Apply Policy" from split panel triggers modal with Approve/Monitor/Block options. Completes in 3 clicks from landing.
4. **Cost Attribution** — CSS-based stacked bar by vendor, horizontal bar by team. Full cost table.
5. **Adoption & Maturity** — 5-level scorecard with Level 3 highlighted, team comparison bars.
6. **Admin Console** — 3 connected integrations (AWS, M365, OpenAI), notification toggles, team management.
7. **Audit Log** — 12 governance actions with search and filter.
8. **5 placeholder pages** (Integration Marketplace, Compliance Reports, Enforcement Rules, AI ROI Insights, Policy Templates) — each with realistic content, connector cards, and "Coming Soon" elements.

### Prototype Fidelity: 85%

Key gaps (acceptable for demo, needed for Eng v1): Cloudscape Property Filter tokens, skeleton loading states, URL deep-linking, full ARIA screen reader announcements, date range picker. See fidelity-report-v1.md for complete mapping.

### Navigation Surface Confirmed

13 navigable pages (7 primary + 6 sub-nav) — exceeds ServiceNow's ~8 primary sections and Datadog's ~6 sections. Prototype confirms the product feels like a product, not a feature.
