---
artifact: launch-readiness
version: v1
prd-version: v1 + gandalf-fixes-v1.1
design-version: v1
prototype-version: v1
timestamp: 2026-05-19T17:00:00Z
status: draft
---

# Launch Readiness: CloudWatch AI Control Plane

## Executive Summary

We are building a new top-level page in the CloudWatch console — the AI Control Plane — that gives operations and compliance teams a single-pane view of all AI workloads across their AWS Organization, including governance health, cost intelligence, and maturity scoring. The feature addresses a critical gap: enterprises deploying AI across multiple accounts have no centralized way to monitor, govern, or audit their AI fleet. Proposed timeline: 12-week build to GA, with internal dogfood in Week 4 and beta in Week 8.

## 1. Engineering Spec

### System Components

**1.1 AI Workload Discovery Service (new)**
Serverless pipeline that discovers AI workloads across an AWS Organization:
- **Data sources:** CloudTrail management events (Bedrock: `InvokeModel`, `CreateModelCustomizationJob`; SageMaker: `CreateEndpoint`, `InvokeEndpoint`), Service Catalog, and Resource Groups Tagging API
- **Architecture:** EventBridge rule → Lambda function → DynamoDB (workload registry) → S3 (historical snapshots)
- **Cross-account:** Uses AWS Organizations delegated administrator pattern (same as Security Hub) with IAM roles in member accounts. The central account assumes role in each member account to read CloudTrail events.
- **Refresh frequency:** Near-real-time for new workloads (EventBridge events within 5 min), batch aggregation for cost and metrics (every 15 min)
- **Detection accuracy target:** >95% for Bedrock and SageMaker workloads (CloudTrail typed events are deterministic for these services)

**1.2 Governance Engine (new)**
Maps guardrail configurations to discovered workloads:
- **Integration:** Bedrock Guardrails API (`ListGuardrails`, `GetGuardrail`) and SageMaker Model Cards API
- **Data model:** Links `workload_id` → `guardrail_id[]` with enforcement status tracking
- **Maturity scoring:** Rule-based engine (not ML) that scores organizations 1-5 based on: guardrail coverage %, enforcement policy presence, audit log completeness, cross-account governance, automated remediation

**1.3 Cost Aggregation Service (extension of existing)**
Extends CloudWatch Cost Intelligence to include AI-specific cost breakdowns:
- **Data source:** Cost Explorer API with `SERVICE` filter for Bedrock and SageMaker
- **Aggregation:** Per-workload, per-model, per-account, per-team (via tags)
- **Optimization engine:** Identifies workloads eligible for batch inference, provisioned throughput, or reserved capacity

**1.4 Console Frontend (new page)**
Single-page React application built on Cloudscape Design System:
- **URL:** `console.aws.amazon.com/cloudwatch/home#ai-control-plane`
- **Components:** App Layout + Table + Split Panel + Property Filter + Cards + Status Indicators (see design-spec-v1.md for complete component mapping)
- **Data fetching:** React Query with 30s polling interval for table, 5min for charts
- **State management:** URL-based state for filters/sort (shareable deep links)

### API Contracts

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ai-control-plane/workloads` | GET | List all discovered AI workloads with health, guardrail, cost summary |
| `/ai-control-plane/workloads/{id}` | GET | Workload detail: metrics, guardrail config, cost breakdown, timeline |
| `/ai-control-plane/workloads/{id}/timeline` | GET | CloudTrail events for a specific workload |
| `/ai-control-plane/maturity` | GET | Organization maturity score, level, recommended actions |
| `/ai-control-plane/maturity/config` | PUT | Update maturity scoring configuration (admin only) |
| `/ai-control-plane/reports/compliance` | POST | Generate compliance report (async, returns S3 pre-signed URL) |
| `/ai-control-plane/settings` | GET/PUT | Cross-account config, discovery settings, notification preferences |

### Data Model

```
WorkloadRegistry (DynamoDB)
├── PK: ACCOUNT#{accountId}
├── SK: WORKLOAD#{workloadId}
├── name: string
├── service: "Bedrock" | "SageMaker"
├── model: string
├── region: string
├── healthStatus: "healthy" | "warning" | "error"
├── guardrailIds: string[]
├── guardrailCoverage: number (0-100)
├── costLast30d: number
├── costTrend: number[] (7 daily values)
├── invocationCount30d: number
├── latencyP50: number (ms)
├── latencyP99: number (ms)
├── errorRate: number (percentage)
├── team: string (from resource tags)
├── lastActive: ISO8601
├── discoveredAt: ISO8601
├── isNew: boolean (discovered within 7 days)
└── GSI: HealthStatusIndex (healthStatus → workloadId)
```

### Performance Requirements

| Metric | Target | Rationale |
|--------|--------|-----------|
| Page load (table with 100 workloads) | < 2s P95 | CloudWatch console SLA |
| Split panel render (after row click) | < 500ms P95 | Perceived instant interaction |
| Property filter response | < 200ms P95 | Client-side filtering on cached data |
| Cross-account discovery latency | < 5 min for new workloads | Near-real-time via EventBridge |
| Cost aggregation freshness | < 15 min | Acceptable for cost data |
| API availability | 99.95% | CloudWatch console target |
| Concurrent users per account | 50 | Conservative; scale based on beta data |

## 2. Acceptance Criteria

### Fleet Overview (Landing Page)

- GIVEN a user with AI Control Plane enabled and 14 AI workloads across 4 accounts  
  WHEN they navigate to CloudWatch → AI Control Plane  
  THEN they see 4 summary cards (total workloads = 14, guardrail coverage = 68%, unhealthy = 2, monthly cost = $27.4K) within 2 seconds

- GIVEN 3 new AI workloads detected since the user's last visit  
  WHEN the page loads  
  THEN a Flashbar notification shows "3 new AI workloads detected" with a link to filter to new workloads

- GIVEN the workload table is displayed  
  WHEN the user has not applied any filters  
  THEN the table is sorted by health status (error first, then warning, then healthy)

### Table Interactions

- GIVEN the workload table with 14 rows  
  WHEN the user clicks a column header (Name, Service, Health, Cost)  
  THEN the table sorts ascending on first click, descending on second click, with a sort indicator icon

- GIVEN the Property Filter input  
  WHEN the user clicks the input field  
  THEN a suggestion dropdown shows filterable properties (service, health, guardrail, account)

- GIVEN the user adds filter "Health = Error"  
  WHEN the filter is applied  
  THEN only workloads with error health status are shown, and a filter token appears above the input

- GIVEN the user has applied 2 filters  
  WHEN they click the ✕ on one filter token  
  THEN that filter is removed and the table updates to reflect the remaining filter

### Split Panel Detail

- GIVEN the workload table  
  WHEN the user clicks any row  
  THEN a bottom split panel (40% viewport height) opens showing that workload's details with 4 tabs: Overview, Guardrails, Cost, Timeline

- GIVEN the split panel is open on the Overview tab  
  WHEN the user views the panel  
  THEN they see: service, model, account, region, team, health status, invocations (30d), latency P50/P99, error rate, and an invocation chart

- GIVEN a workload with health = "error"  
  WHEN the user views the Overview tab  
  THEN an inline error alert is shown explaining the issue (e.g., "Error rate 2.3% exceeds 1% threshold")

- GIVEN a workload with guardrail = "none"  
  WHEN the user views the Guardrails tab  
  THEN a warning alert is shown: "No guardrail configured" with an "Enable Guardrail" link to the Bedrock console

- GIVEN the split panel is open  
  WHEN the user clicks the ✕ close button  
  THEN the split panel closes and the table row is deselected

### Governance Maturity

- GIVEN the user scrolls below the workload table  
  WHEN they reach the Maturity section  
  THEN they see: current level (1-5) with label, progress bar to next level (%), and 3 recommended actions

- GIVEN the organization is at Level 2 with 68% guardrail coverage  
  WHEN the maturity section renders  
  THEN the first recommended action is "Enable guardrails on remaining 4 workloads" with expected impact "+28% coverage"

### Error & Edge States

- GIVEN no AI workloads are discovered  
  WHEN the page loads  
  THEN an empty state is shown: "No AI workloads detected" with an "Enable AI Control Plane" CTA

- GIVEN 2 of 4 accounts have cross-account permission failures  
  WHEN the page loads  
  THEN an error Alert is shown: "Unable to load data for 2 accounts" with a "Fix Permissions" link, and available accounts still render in the table

- GIVEN the page is loading  
  WHEN data is being fetched  
  THEN skeleton loading shows for table rows, and a spinner shows for charts

### Date Range & Export

- GIVEN the Date Range Picker in the header  
  WHEN the user clicks "30d"  
  THEN all data on the page (table metrics, charts, summary cards) updates to reflect the 30-day window

- GIVEN the Actions dropdown  
  WHEN the user clicks "Generate Compliance Report"  
  THEN a report generation starts asynchronously and a Flashbar shows "Report generating... Download will be available shortly"

## 3. Phased Rollout

| Phase | Scope | Duration | Success Gate | Rollback Trigger |
|-------|-------|----------|-------------|-----------------|
| 0 — Internal Dogfood | Feature flag ON for CloudWatch APM team only. 2-3 AWS accounts. | 2 weeks | No P0/P1 bugs. Page load < 2s P95. Discovery accuracy > 95% for Bedrock workloads. | Any data integrity issue (wrong workload ↔ account mapping) |
| 1 — Private Beta | 10-15 selected enterprise customers (opt-in via feature flag). Cross-account enabled. | 3 weeks | < 1% API error rate. CSAT > 4.0/5. Guardrail coverage metric tracks correctly across all customer accounts. Discovery handles 500+ workloads per org. | CSAT < 3.5, or > 40% of beta users disable within first week |
| 2 — Public Preview | All customers, labeled "Preview" in console. Marketing + What's New post. | 4 weeks | North Star (guardrail coverage delta) shows +5pp improvement in 50% of orgs. Monthly active users > 1,000. Cost Intelligence used by > 30% of active users. | Negative press or social media backlash about accuracy. P0 security issue in cross-account access. |
| 3 — GA | Remove "Preview" label. All customers, all regions. Tiered pricing decision made. | Ongoing | All PRD success metrics at target. < 0.1% ticket rate for data accuracy issues. | N/A — iterate based on customer feedback |

**Total: 12 weeks from code-complete to GA**

## 4. Success Metrics & Instrumentation

### North Star: Guardrail Coverage Delta

| Metric | Type | Target | Baseline | Instrumentation | Dashboard |
|--------|------|--------|----------|----------------|-----------|
| **Guardrail Coverage Delta** | North Star | +15pp org-wide after 90 days | 0% (no centralized tracking today) | `GuardrailCoveragePercent` CloudWatch custom metric per org, emitted every 15 min by Governance Engine | AI Control Plane → Maturity tab |
| Weekly Active Users | Engagement | 5,000 by month 3 | 0 | CloudWatch RUM page views on `/ai-control-plane/*` | CloudWatch RUM dashboard |
| Time-to-Insight | Efficiency | < 30s to assess fleet health | ~23 min (manual correlation) | RUM custom timing from page load to first split panel open | CloudWatch RUM dashboard |
| Maturity Level Progression | Outcome | 20% of orgs move up 1 level in 90 days | Level 1 (no centralized governance) | `MaturityLevel` metric per org, emitted daily | AI Control Plane → Maturity tab |
| Cost Optimization Actions | Revenue | 10% of users take a cost action per month | 0 | Click tracking on "batch eligible" / "optimize" CTAs | CloudWatch Events + QuickSight |

### Anti-Metrics

| Metric | Should NOT | Mechanism of Harm | Instrumentation |
|--------|-----------|-------------------|----------------|
| False positive workload detection | Exceed 5% | Misidentifying non-AI CloudTrail events as AI workloads | Feedback button "Not an AI workload" → `FalsePositiveRate` metric |
| Cross-account permission errors | Exceed 2% of orgs | IAM role assumption failures blocking data display | `CrossAccountError` metric per org |

### Phase Gates

- **v2 decision gate (Month 6):** If Guardrail Coverage Delta < +10pp AND WAU < 2,000, re-evaluate scope (potentially narrow to Bedrock-only)
- **Pricing decision gate (Month 4):** If WAU > 3,000 AND feature drives measurable retention improvement, evaluate tiered pricing per pricing scenarios in prd-v1-gandalf-fixes.md

## 5. Meeting Deck Outline (27 min total)

| # | Section | Time | Content Source | Speaker |
|---|---------|------|---------------|---------|
| 1 | Problem Recap | 2 min | PRD §1: Maya Chen persona, JTBD #1 (governance visibility), 23-min investigation time stat | PM |
| 2 | Competitive Context | 2 min | Research: ServiceNow AI Control Tower, Datadog LLM Observability, Dynatrace Davis AI. Why we must act now (Gartner AI TRiSM). | PM |
| 3 | Solution Overview | 3 min | PRD §2: 4 capabilities (Discovery, Governance Dashboard, Cost Intelligence, Maturity Score). Scope boundary table (v1 vs v2). | PM |
| 4 | Design Walkthrough | 5 min | **Live prototype demo.** Walk through: landing page → summary cards → filter to unhealthy → click row → split panel tabs → maturity section → export. | PM + UX |
| 5 | Engineering Spec | 5 min | This document §1: 4 system components, API contracts, data model, perf requirements. Focus on cross-account pattern (Security Hub precedent). | Eng Lead |
| 6 | Phased Rollout | 3 min | This document §3: 4-phase plan, success gates, rollback triggers. Ask: does 12-week timeline work? | PM + Eng Lead |
| 7 | Open Questions | 5 min | See §7 below. Key: CloudTrail event volume at scale, DynamoDB vs Timestream for workload registry, SageMaker endpoint discovery completeness. | All |
| 8 | Next Steps | 2 min | Sprint 1 scope: Discovery Service + basic table (no split panel). Ownership assignments. Design review scheduled. | PM |

## 6. Consolidated Risk Register

| # | Source | Risk | L | I | Mitigation | Owner |
|---|--------|------|---|---|------------|-------|
| R1 | Gandalf (Q7) | CloudTrail event volume at enterprise scale (>1M events/day) may cause discovery latency > 5 min target | Medium | High | Batch processing with EventBridge Pipes; 2-week technical spike before Sprint 1 to validate at scale | Eng Lead |
| R2 | Gandalf (Q9) | Discovery accuracy < 90% for SageMaker custom endpoints (non-standard model names) | Medium | Medium | v1 scope limited to Bedrock + SageMaker managed models; custom endpoint discovery in v2 with allow-list pattern | PM |
| R3 | Gandalf (Q9) | Dashboard P95 load time > 8s with > 200 workloads | Low | High | Client-side pagination + server-side caching; load table first, charts async | Eng Lead |
| R4 | Gandalf (Q10) | Free tier creates expectation that feature is always free; difficult to introduce pricing later | Medium | Medium | Ship as "included with CloudWatch" (not "free"); product messaging positions it as platform capability | PM + Marketing |
| R5 | PRD | Competitor (ServiceNow AI Control Tower) launches cross-cloud support before our GA | Medium | High | Differentiate on depth of AWS-native integration rather than breadth; AI Control Plane sees data ServiceNow can't (VPC-level metrics, CloudTrail events) | PM |
| R6 | PRD | IAM cross-account role setup friction causes > 50% of orgs to abandon setup | Medium | High | Automated setup via CloudFormation StackSet (one-click); template pre-built and linked in Settings page | Eng Lead |
| R7 | Design | Split panel content overload — too many tabs make detail view hard to parse | Low | Medium | Start with 4 tabs (Overview, Guardrails, Cost, Timeline); user research in beta to validate; add/remove tabs based on usage data | UX |
| R8 | Design | Maturity score perceived as judgmental by security teams ("you're only Level 2") | Low | Medium | Frame as "progression" not "score"; use positive language ("3 actions to Level 3" not "you're missing 3 things"); configurable by admins | PM + UX |
| R9 | Technical | DynamoDB cost for workload registry at scale (>10K workloads, 15-min refresh) | Low | Low | On-demand pricing initially; evaluate reserved capacity after beta usage patterns stabilize | Eng Lead |
| R10 | Technical | Bedrock Guardrails API rate limits during guardrail status polling | Medium | Medium | Cache guardrail status for 5 min; use batch API calls where available; exponential backoff | Eng Lead |

## 7. Open Questions for Engineering

| # | Question | Context | Owner | Deadline |
|---|----------|---------|-------|----------|
| OQ1 | Can we sustain < 5 min discovery latency at 1M+ CloudTrail events/day? | Requires technical spike. SecurityHub processes similar volumes — can we reuse their EventBridge Pipes pattern? | Eng Lead | Sprint 0 (Week 1-2) |
| OQ2 | DynamoDB vs Timestream for workload registry? | DynamoDB for structured queries + GSI; Timestream for time-series cost/metrics. Possibly both. | Eng Lead | Sprint 0 |
| OQ3 | How complete is SageMaker endpoint discovery via CloudTrail? | Custom endpoints may use generic `InvokeEndpoint` events without model identifiers. Need to test with 5+ real customer patterns. | Eng Lead + SageMaker team | Sprint 1 |
| OQ4 | Can we get Bedrock Guardrails team to build a batch status API? | Currently no batch API — we'd need to call `GetGuardrail` per workload. At 500+ workloads this is rate-limit-risky. | PM (file feature request) | Week 3 |
| OQ5 | What's the CloudFormation StackSet approach for cross-account role setup? | Need IAM policy scoped to read-only CloudTrail + Cost Explorer. Model after Security Hub's delegated admin pattern. | Eng Lead + IAM team | Sprint 1 |
| OQ6 | Regional availability for v1 — all commercial regions or subset? | Bedrock is available in fewer regions than SageMaker. Do we show "Bedrock not available in this region" or hide Bedrock features? | PM + Eng Lead | Sprint 1 |

## Appendix: Artifact Links

| Stage | Artifact | Status |
|-------|----------|--------|
| 1 — Research | research-v1.md | Complete (self-eval 6/6) |
| 2 — PRD | prd-v1.md + prd-v1-gandalf-fixes.md | Complete (12 weaknesses → skill v0.2.0) |
| 3 — Gandalf | gandalf-evaluation-v1.md | Complete (7/10 passed, 3 flags resolved) |
| 4 — Design | design-spec-v1.md | Complete (10/10 checklist, avg 4.4/5) |
| 5 — Prototype | prototype-v1.html + prototype-notes-v1.md | Complete (18/18 structural checks, 10 interactions) |
| 6 — Launch Readiness | This document | Draft |
