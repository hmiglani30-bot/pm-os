---
artifact: launch-readiness
version: v2
prd-version: v1 + gandalf-fixes-v1.1
design-version: v2
prototype-version: v2
timestamp: 2026-05-19T20:00:00Z
status: draft
word-count: ~5000
traceability-complete: true
---

# Launch Readiness v2: CloudWatch AI Control Plane

## Executive Summary

CloudWatch AI Control Plane is a new top-level page within the CloudWatch console that gives operations and compliance teams a unified view of all AI workloads across their AWS Organization, including governance health, cost intelligence, guardrail monitoring, and maturity scoring. The feature addresses a validated market gap where 72% of enterprises run AI in production yet 60% lack governance tooling. Proposed timeline: 8 sprints (16 weeks) from kickoff to GA, with internal dogfood at Sprint 3, private beta at Sprint 5, and GA at Sprint 8.

---

## 1. Engineering Spec

### 1.1 AI Workload Discovery Service (New) — maps to Design Spec: Summary Cards, Workload Table, Flashbar

Serverless pipeline that discovers AI workloads across an AWS Organization using three data sources:

- **CloudTrail Events:** Bedrock (`InvokeModel`, `ApplyGuardrail` from `bedrock.amazonaws.com`) and SageMaker (`CreateEndpoint`, `InvokeEndpoint` from `sagemaker.amazonaws.com`). Typed first-party events with near-100% accuracy.
- **Resource Groups Tagging API:** Tagged AI resources for team/cost-center attribution.
- **Architecture:** EventBridge rule -> Lambda -> DynamoDB (workload registry) + S3 (historical snapshots). Cross-account via Organizations delegated admin pattern (Security Hub precedent), read-only IAM roles in member accounts.

**Refresh cadence:** Near-real-time for new workload detection (EventBridge within 5 min). Batch aggregation for cost and health metrics every 15 min. Guardrail status cached for 5 min.

**Detection accuracy target:** >95% for Bedrock and SageMaker workloads. Third-party AI detection explicitly deferred to v2.

### 1.2 Governance Engine (New) — maps to Design Spec: Guardrails Tab, Maturity Section

Links guardrail configurations to discovered workloads:

- **Integration points:** Bedrock Guardrails API (`ListGuardrails`, `GetGuardrail`), SageMaker Model Cards API
- **Data model:** `workload_id` to `guardrail_id[]` mapping with enforcement status, trigger counts, and history
- **Maturity scoring:** Rule-based engine (not ML) that scores organizations 1-5 based on: guardrail coverage %, enforcement policy presence, audit log completeness, cross-account governance status, and automated remediation adoption. Computed on-read from observable signals, no separate ML training pipeline required.

### 1.3 Cost Aggregation Service (Extension) — maps to Design Spec: Cost Tab, Cost Intelligence Side Nav Page

Extends CloudWatch cost capabilities for AI-specific breakdowns:

- **Data source:** Cost Explorer API with `SERVICE` filter for Bedrock and SageMaker
- **Aggregation dimensions:** Per-workload, per-model, per-account, per-team (via resource tags)
- **Optimization engine:** Identifies workloads eligible for batch inference, provisioned throughput, or reserved capacity. Generates actionable recommendations with estimated savings.

### 1.4 Console Frontend (New Page) — maps to Design Spec: Full Component Mapping (Section: Phase 2)

Single-page React app on Cloudscape v3.x at `console.aws.amazon.com/cloudwatch/home#ai-control-plane`. Full component mapping per design-spec-v2.md Phase 2. Data fetching via React Query (30s table poll, 5 min charts). URL-based state for deep-linkable filters/sort. L breakpoint primary, M/S/XS degrade gracefully.

### API Contracts

| Endpoint | Method | Request | Response | Error Codes |
|----------|--------|---------|----------|-------------|
| `/ai-control-plane/workloads` | GET | Paginated list with filter, sort, time range params | 403, 500, 429 |
| `/ai-control-plane/workloads/{id}` | GET | Detail: metrics, guardrails, cost, timeline | 404, 403, 500 |
| `/ai-control-plane/maturity` | GET | Org maturity: level, progress, actions, peer benchmark | 403, 500 |
| `/ai-control-plane/maturity/config` | PUT | Update scoring weights and exclusions (admin) | 403, 400, 500 |
| `/ai-control-plane/reports/compliance` | POST | Async report generation (PDF/CSV) | 403, 500 |
| `/ai-control-plane/reports/{id}` | GET | Report status and download URL | 404, 403, 500 |
| `/ai-control-plane/settings` | GET/PUT | Discovery, cross-account, notification config | 403, 400, 500 |

All endpoints versioned via `X-Api-Version` header.

### Data Model

**WorkloadRegistry (DynamoDB):** PK `ACCOUNT#{accountId}`, SK `WORKLOAD#{workloadId}`. Key attributes: `name`, `service` (Bedrock|SageMaker), `model`, `region`, `healthStatus`, `guardrailIds[]`, `guardrailCoverage` (0-100), `costLast30d`, `costTrend` (7 daily values), `invocationCount30d`, `latencyP50/P99` (ms), `errorRate` (%), `team` (from tags), `lastActive`, `discoveredAt`, `isNew` (within 7 days). GSIs: `HealthStatusIndex` (healthStatus -> workloadId), `AccountTeamIndex` (team -> accountId + workloadId).

### Performance Requirements

| Metric | Target | Rationale |
|--------|--------|-----------|
| Page load (100 workloads) | < 2s P95 | CloudWatch console SLA |
| Split Panel render | < 500ms P95 | Perceived-instant interaction |
| Property Filter response | < 200ms P95 | Client-side on cached data |
| Cross-account discovery | < 5 min for new workloads | EventBridge near-real-time |
| Cost aggregation freshness | < 15 min | Acceptable for governance |
| API availability | 99.95% | CloudWatch console target |
| Concurrent users per account | 50 | Scale based on beta data |

---

## 2. Acceptance Criteria

### Fleet Overview

[AC-1] Traces to: JTBD-1 / JTBD-2
GIVEN a user with AI Control Plane enabled and discovered workloads across multiple accounts
WHEN they navigate to CloudWatch > AI Control Plane
THEN they see 4 summary cards (Total Workloads, Guardrail Coverage %, Unhealthy count, Monthly AI Cost) with data rendered within 2 seconds

[AC-2] Traces to: JTBD-1 / DD-Flashbar
GIVEN 1 or more new AI workloads detected since the user's last visit
WHEN the page loads
THEN a Flashbar notification shows "[N] new AI workloads detected since your last visit" with a link that filters the table to new workloads only

[AC-3] Traces to: JTBD-3 / DD-Table-Sort
GIVEN the workload table is displayed with no user-applied filters
WHEN the table renders
THEN rows are sorted by health status: error first, then warning, then healthy, ensuring anomalies are immediately visible

### Table Interactions

[AC-4] Traces to: DD-Property-Filter
GIVEN the Property Filter input is focused
WHEN the user begins typing or clicks the input
THEN a suggestion dropdown shows filterable properties (service, health, guardrail status, account) with available values

[AC-5] Traces to: DD-Property-Filter
GIVEN the user adds a filter token (e.g., "Health = Error")
WHEN the filter is applied
THEN only matching workloads are shown, a filter token appears, and a screen reader announcement states "[N] workloads match your filter"

[AC-6] Traces to: DD-Table-Sort
GIVEN the workload table with sortable column headers
WHEN the user clicks a column header
THEN the table sorts ascending on first click, descending on second, with a visible sort indicator and `aria-sort` attribute updated

### Split Panel Detail

[AC-7] Traces to: JTBD-1 / DD-Split-Panel
GIVEN the workload table
WHEN the user clicks any row or presses Enter on a focused row
THEN a bottom Split Panel (40% viewport height) opens with slide-up animation (200ms ease-out), showing 4 tabs: Overview, Guardrails, Cost, Timeline, and focus moves to the panel close button

[AC-8] Traces to: JTBD-3 / DD-Guardrails-Tab
GIVEN a workload with no guardrails configured
WHEN the user views the Guardrails tab in the Split Panel
THEN a warning Alert shows "No guardrail configured for this workload" with an "Enable Guardrail" link that deep-links to the Bedrock console with the model ARN pre-filled

[AC-9] Traces to: JTBD-2 / DD-Cost-Tab
GIVEN a workload selected in the Split Panel
WHEN the user switches to the Cost tab
THEN they see daily cost bar chart, total cost (30d), cost per invocation, and optimization recommendations if applicable

[AC-10] Traces to: JTBD-1 / DD-Split-Panel
GIVEN the Split Panel is open
WHEN the user presses Escape or clicks the close button
THEN the panel closes with slide-down animation (150ms), and focus returns to the table row that triggered it

### Governance Maturity

[AC-11] Traces to: JTBD-4 / DD-Maturity-Section
GIVEN the user scrolls below the workload table
WHEN the Maturity section renders
THEN they see: current level (1-5) with label, segmented progress bar showing progress to next level, 3 recommended actions as cards, and peer benchmark comparison

[AC-12] Traces to: JTBD-4 / DD-Maturity-Section
GIVEN the organization is below Level 3 with guardrail coverage below 80%
WHEN maturity recommendations render
THEN the first recommended action addresses guardrail coverage gap with specific workload names and estimated effort

### Compliance and Export

[AC-13] Traces to: JTBD-4 / DD-Button-Dropdown
GIVEN the Actions dropdown menu
WHEN the user clicks "Generate Compliance Report"
THEN a modal appears to configure report scope (date range, accounts, format), and on confirmation, a Flashbar shows "Generating report..." with the report available for download when complete

### Error and Edge States

[AC-14] Traces to: DD-Empty-State
GIVEN no AI workloads have been discovered
WHEN the page loads
THEN an illustrated empty state shows "No AI workloads detected" with an "Enable AI Control Plane" primary button and documentation link

[AC-15] Traces to: DD-Error-State
GIVEN cross-account permission failures for some accounts
WHEN the page loads
THEN an error Alert shows "Unable to load data for [N] accounts" with account IDs and a "Fix Permissions" link that deep-links to the required IAM policy, while available accounts render normally

[AC-16] Traces to: DD-Loading-State
GIVEN data is being fetched
WHEN the page is loading
THEN skeleton screens render for table rows and charts (no spinners), preserving layout stability

### Accessibility

[AC-17] Traces to: DD-Keyboard-Nav
GIVEN the AI Control Plane page is loaded
WHEN the user navigates via keyboard only
THEN all interactive elements are reachable via Tab, table rows navigable via Arrow keys, Split Panel tabs switchable via Arrow Left/Right, and all keyboard shortcuts (/, Esc, r, ?) function as specified

[AC-18] Traces to: DD-Accessibility
GIVEN a screen reader is active
WHEN state changes occur (filter applied, panel opened, data loaded)
THEN appropriate aria-live announcements fire as specified in the design spec screen reader announcement table

---

## 3. Sprint Breakdown

| Sprint | Duration | Scope | Deliverables | Dependencies | Exit Criteria |
|--------|----------|-------|-------------|-------------|---------------|
| S0 — Spike | 2 weeks | Technical validation: CloudTrail event query across 10 sandbox accounts, DynamoDB schema design, cross-account IAM role template | Go/no-go decision doc, IAM CloudFormation StackSet template, latency benchmarks | None | Discovery latency < 5 min at 10-account scale; IAM template validated; DynamoDB schema reviewed |
| S1 — Foundation | 2 weeks | DynamoDB tables deployed, EventBridge rules, Lambda discovery function, feature flags, API stubs for all 7 endpoints | Working discovery pipeline in dev; API gateway with stub responses; feature flag toggleable | S0 complete | Schema deployed to dev; feature flag ON/OFF works; discovery Lambda processes test events |
| S2 — Core Backend | 2 weeks | Discovery service connected to real CloudTrail, Governance Engine (guardrail mapping + maturity scoring), Cost Aggregation service | End-to-end discovery for Bedrock workloads; guardrail status populated; cost data flowing | S1 complete | Unit tests pass (>80% coverage); integration tests pass for Bedrock discovery; maturity score computes correctly for test org |
| S3 — Frontend + Dogfood | 2 weeks | Console frontend: App Layout, Table, Property Filter, Summary Cards, Date Range Picker. Connect to live APIs. Internal dogfood begins. | Working console page with real data for CloudWatch APM team accounts | S2 complete; Cloudscape v3 available | Page renders with live data; table sorts/filters work; no P0 bugs; internal team using daily |
| S4 — Detail + Polish | 2 weeks | Split Panel (4 tabs), Flashbar notifications, keyboard navigation, accessibility (ARIA landmarks, screen reader announcements), skeleton loading | Full interaction model; accessibility audit passes; all 18 AC testable | S3 complete | E2E tests pass for all AC; accessibility audit passes WCAG AA; design review sign-off |
| S5 — Beta Launch | 2 weeks | Cross-account hardening, compliance report generation, beta onboarding flow, monitoring dashboards deployed, beta customer onboarding (10-15 customers) | Beta-ready build; monitoring in place; 10+ beta customers active | S4 complete; beta customer list finalized | < 1% API error rate; CSAT > 4.0; discovery handles 500+ workloads per org |
| S6 — Hardening | 2 weeks | Performance tuning (load test at 100-account scale), maturity section polish, responsive breakpoints (M, S), error state handling, runbook creation | Load-test-validated build; runbooks reviewed; responsive down to S breakpoint | S5 feedback incorporated | P95 page load < 2s at 100 accounts; all error states render correctly; runbooks complete |
| S7-S8 — GA Prep + Launch | 2 weeks | Public Preview label, What's New post, documentation, GA flip, post-launch monitoring | GA-ready build in all target regions | S6 complete; security review passed | All PRD success metrics instrumented; < 0.1% ticket rate in Preview; marketing approved |

---

## 4. Dependency RACI

| Dependency | Responsible | Accountable | Consulted | Informed | Timeline |
|-----------|------------|-------------|-----------|----------|----------|
| CloudTrail event access (Bedrock/SageMaker) | APM Eng Lead | APM PM | CloudTrail team | Bedrock PM | S0 (spike validation) |
| Bedrock Guardrails API (ListGuardrails, GetGuardrail) | APM Eng | APM PM | Bedrock Guardrails team | Bedrock PM | S2 (integration) |
| Bedrock Guardrails batch status API (feature request) | Bedrock Guardrails team | Bedrock PM | APM PM | APM Eng | S4 (needed for scale) |
| SageMaker endpoint discovery (InvokeEndpoint events) | APM Eng | APM PM | SageMaker team | SageMaker PM | S2 (integration) |
| Cost Explorer API (AI-specific filters) | APM Eng | APM PM | Cost Explorer team | FinOps PM | S2 (integration) |
| Organizations delegated admin setup | APM Eng Lead | APM PM | IAM team, Organizations team | Security team | S1 (foundation) |
| CloudFormation StackSet for cross-account IAM roles | APM Eng | APM Eng Lead | IAM team | Customer success | S1 (foundation) |
| Cloudscape Design System v3 components | Frontend Eng | APM Eng Lead | Cloudscape team | UX | S3 (frontend build) |
| CloudWatch RUM integration (usage metrics) | APM Eng | APM PM | RUM team | Analytics | S5 (beta monitoring) |
| Security review (cross-account trust model) | Security Eng | Security Lead | APM Eng Lead | APM PM | S5 (before beta) |
| Bedrock console deep-link for guardrail creation | Bedrock Frontend team | Bedrock PM | APM PM | UX | S4 (split panel links) |
| What's New post and documentation | Tech Writer | APM PM | Marketing | All stakeholders | S7 (GA prep) |

---

## 5. Phased Rollout

| Phase | Scope | Duration | Success Gate | Rollback Trigger |
|-------|-------|----------|-------------|-----------------|
| 0 — Internal Dogfood | Feature flag ON for CloudWatch APM team only (2-3 accounts) | 2 weeks (S3-S4) | No P0/P1 bugs; page load < 2s P95; discovery accuracy > 95% for Bedrock workloads | Any data integrity issue (wrong workload-account mapping) or P0 security bug |
| 1 — Private Beta | 10-15 enterprise customers, opt-in via feature flag, cross-account enabled | 3 weeks (S5-S6) | < 1% API error rate; CSAT > 4.0/5; guardrail coverage tracks correctly; handles 500+ workloads/org | CSAT < 3.5 or > 40% of beta users disable within first week |
| 2 — Public Preview | All customers, "Preview" label in console, What's New post | 4 weeks (S7+) | Guardrail coverage delta +5pp in 50% of orgs; MAU > 1,000; Cost Intelligence used by > 30% of active users | Negative press about accuracy; P0 security issue in cross-account access |
| 3 — GA | Remove Preview label, all regions, pricing decision finalized | Ongoing | All PRD success metrics at target; < 0.1% ticket rate for data accuracy | N/A (iterate on feedback) |

---

## 6. Rollback Procedures

### Phase 0 and Phase 1 Rollback

| Layer | Rollback Action | Estimated Time | Owner |
|-------|----------------|----------------|-------|
| Feature flag | Disable `ai-control-plane-enabled` flag via internal feature flag service | < 1 min | On-call eng |
| Data | DynamoDB workload registry is append-only; no customer data mutation. Disable EventBridge rule to stop new writes. | < 5 min | Eng Lead |
| Service | Redeploy previous Lambda version via CodeDeploy automatic rollback. Revert API Gateway stage to prior deployment. | < 10 min | On-call eng |

### Phase 2 Rollback

| Layer | Rollback Action | Estimated Time | Owner |
|-------|----------------|----------------|-------|
| Feature flag | Disable flag for all non-beta customers; beta customers retain access | < 1 min | On-call eng |
| Data | Same as Phase 0/1 — no destructive data changes | < 5 min | Eng Lead |
| Service | Revert console frontend deployment via CloudFront invalidation + S3 rollback to prior version | < 15 min | Frontend eng |
| Communication | Notify customers via console banner: "AI Control Plane temporarily unavailable for maintenance" | < 30 min | PM + Support |

**Pre-rollback:** Confirm trigger conditions sustained >5 min (not transient spike). **Post-rollback smoke tests:** (1) AI Control Plane shows "not available" for disabled users, (2) existing CloudWatch unaffected, (3) DynamoDB writes stopped. **Communication:** On-call notifies PM within 15 min; PM notifies beta customers within 1 hour; post-incident review within 48 hours.

---

## 7. Data Migration Plan

### Schema Changes

- **New DynamoDB table:** `WorkloadRegistry` with partition key `ACCOUNT#{accountId}`, sort key `WORKLOAD#{workloadId}`, and two GSIs (`HealthStatusIndex`, `AccountTeamIndex`). Created via CloudFormation.
- **No existing table modifications.** AI Control Plane reads from existing CloudTrail, CloudWatch Metrics, and Cost Explorer data stores. The only new storage is the workload registry cache.

### Migration Strategy

Online, append-only. One-time backfill Lambda scans 90 days of CloudTrail events (< 2 hours for < 1000 workloads). Ongoing sync via EventBridge with idempotent upserts (conditional writes on `discoveredAt`).

### Backward Compatibility

Old console code does not read `WorkloadRegistry` (zero impact). New code falls back to empty state if table is empty. `schemaVersion` attribute enables future attribute additions with defaults.

### Zero-Downtime Approach

Table creation and backfill during S1 (weeks before frontend reads). Feature flag gates all access. No cutover moment.

### Rollback

Drop DynamoDB table via CloudFormation stack deletion. No other systems depend on it. Feature flag hides UI.

### Data Validation

Post-backfill: compare registry count against `ListEndpoints` / `ListFoundationModels` per account (delta < 5%). Continuous: daily Lambda checks registry vs CloudTrail distinct workloads; alert if drift > 10%.

---

## 8. Monitoring and Alerting Plan

Before Phase 0, capture baseline metrics for existing CloudWatch console pages (EC2, Lambda) as comparison benchmarks.

### Dashboards and Alarms

| Component | Dashboard | Key Metrics | Alarm Name | Threshold | Runbook |
|-----------|-----------|-------------|------------|-----------|---------|
| Discovery Service | AI-CP-Discovery | EventBridge delivery latency, Lambda duration P99, Lambda errors, DynamoDB write latency | AI-CP-Discovery-Errors | Lambda error rate > 1% for 5 min | `runbooks/ai-cp-discovery.md` |
| Discovery Service | AI-CP-Discovery | Discovery latency (new workload to registry) | AI-CP-Discovery-Latency | P95 > 10 min for 15 min | `runbooks/ai-cp-discovery.md` |
| Governance Engine | AI-CP-Governance | Guardrail API call latency, Guardrail API errors, maturity computation time | AI-CP-Guardrail-API-Errors | Bedrock Guardrails API error rate > 5% for 5 min | `runbooks/ai-cp-governance.md` |
| Cost Aggregation | AI-CP-Cost | Cost Explorer API latency, aggregation job duration, data freshness | AI-CP-Cost-Stale | Data freshness > 30 min | `runbooks/ai-cp-cost.md` |
| Console Frontend | AI-CP-Frontend (RUM) | Page load P50/P95/P99, JS error rate, API call latency, Split Panel render time | AI-CP-PageLoad-Slow | P95 page load > 4s for 10 min | `runbooks/ai-cp-frontend.md` |
| Console API | AI-CP-API | Request count, error rate (4xx, 5xx), latency P50/P99, throttle count | AI-CP-API-Errors | 5xx rate > 0.5% for 5 min | `runbooks/ai-cp-api.md` |
| Cross-Account | AI-CP-CrossAccount | IAM role assumption failures, per-account error rate | AI-CP-CrossAccount-Failures | > 5% of org accounts failing for 15 min | `runbooks/ai-cp-crossaccount.md` |

### Canary Alarms (Phase 0)

- Synthetic canary executes the critical user journey every 5 min: load page, verify summary cards render, click table row, verify Split Panel opens, close panel.
- Canary alarm: any canary failure triggers page to on-call.

### Composite Alarms (Phase 1+)

- **AI-CP-Degraded:** ALARM when (API-Errors OR PageLoad-Slow) AND NOT CrossAccount-Failures (isolates platform issues from customer IAM issues)
- **AI-CP-Critical:** ALARM when API-Errors AND Discovery-Errors (compound failure indicating systemic issue)

### Log Insights Queries

- Discovery failures: `filter @message like /DiscoveryError/ | stats count() by bin(5m)`
- Slow API calls: `filter @duration > 2000 | sort @duration desc`
- Cross-account errors: `filter errorCode like /AccessDenied/ | stats count() by accountId`

### Application Signals

AI Control Plane APIs registered as Application Signals service with dependency map (Bedrock, SageMaker, DynamoDB, Cost Explorer, CloudTrail). SLO: 99.9% availability, P99 < 3s for workload list API.

---

## 9. Security Review Checklist

- [x] **IAM least-privilege:** Lambda role scoped to specific actions (`cloudtrail:LookupEvents`, `dynamodb:PutItem/GetItem/Query`, `bedrock:ListGuardrails/GetGuardrail`, `sagemaker:ListEndpoints`). No `*` resources.
- [x] **Cross-account trust:** Delegated admin role grants read-only access only. Trust policy restricted to admin account ID.
- [x] **Encryption at rest:** DynamoDB AWS-managed KMS. S3 SSE-S3.
- [x] **Encryption in transit:** HTTPS TLS 1.2+ for all API calls.
- [x] **PII handling:** Stores ARNs, account IDs, model names, costs only. No prompt/response content. Classification: AWS Confidential.
- [x] **API auth:** IAM SigV4. New actions: `cloudwatch:GetAIControlPlaneData`, `cloudwatch:PutAIControlPlaneConfig` (admin).
- [x] **Input validation:** Server-side filter validation. Signed opaque pagination tokens. DynamoDB query params sanitized.
- [x] **Audit logging:** All API calls to CloudTrail. Report generation logged with user, scope, timestamp.
- [ ] **Dependency scan:** S5. Lambda deps scanned via `npm audit` / `pip audit` in CI.

---

## 10. Tech Debt Register

| ID | Shortcut | Location | Proper Solution | Priority | Sprint Target |
|----|----------|----------|----------------|----------|---------------|
| TD-1 | Simplified bar charts instead of Line/Area charts | Prototype: Cost tab, Overview tab | Integrate Chart.js or lightweight D3 subset for proper time-series line charts (latency) and area charts (error rate) | P2 | S4 |
| TD-2 | No compliance report modal | Prototype: Actions dropdown | Build Cloudscape Modal with report configuration (date range, accounts, format selection) | P1 | S4 |
| TD-3 | No skeleton loading on initial page load | Prototype: page load | Implement Cloudscape skeleton screens for table, cards, and charts during initial data fetch | P1 | S3 |
| TD-4 | Saved views not implemented | Prototype: Property Filter | Implement saved view persistence (account-level settings storage via Cloudscape user preferences API) | P2 | S6 |
| TD-5 | No Collection Preferences dialog | Prototype: Table header | Implement column visibility, page size, and sort defaults via Cloudscape Collection Preferences component | P2 | S4 |
| TD-6 | Static maturity section (non-interactive) | Prototype: Maturity section | Connect maturity score to live Governance Engine data; implement action completion tracking with Flashbar success animation | P1 | S4 |
| TD-7 | Mock data instead of live API | Prototype: all components | Replace all inline mock data with React Query hooks calling live API endpoints | P0 | S3 |
| TD-8 | No right-click context menu | Prototype: Table rows | Add "Copy workload ARN" and "Open in Bedrock/SageMaker console" to right-click context menu for power users | P3 | S6 |
| TD-9 | URL deep-linking not functional | Prototype: URL bar | Implement URL state management: filter, sort, selected workload, tab, time range all reflected in URL params | P1 | S3 |

---

## 11. Success Metrics

| Metric | Type | Target | Instrumentation | Dashboard |
|--------|------|--------|----------------|-----------|
| Guardrail Coverage Delta | North Star (Gauge) | +15pp org-wide after 90 days | `GuardrailCoveragePercent` custom metric emitted every 15 min by Governance Engine | AI Control Plane > Maturity tab |
| Weekly Active Users | Engagement (Counter) | 5,000 by month 3 | CloudWatch RUM page views on `/ai-control-plane/*` | AI-CP-Frontend RUM dashboard |
| Time-to-Insight | Efficiency (Histogram) | < 30s to assess fleet health | RUM custom timing: page load to first Split Panel open | AI-CP-Frontend RUM dashboard |
| Maturity Level Progression | Outcome (Gauge) | 20% of orgs up 1 level in 90 days | `MaturityLevel` metric per org, emitted daily | AI Control Plane > Maturity tab |
| Cost Optimization Actions | Revenue (Counter) | 10% of users take a cost action/month | Click tracking on optimization CTAs | CloudWatch Events + QuickSight |
| False Positive Rate | Anti-metric (Gauge) | < 5% | "Not an AI workload" feedback button -> `FalsePositiveRate` metric | AI-CP-Discovery dashboard |
| Cross-Account Permission Errors | Anti-metric (Gauge) | < 2% of orgs | `CrossAccountError` metric per org | AI-CP-CrossAccount dashboard |

**Phase gates:**
- Month 4: If WAU > 3,000 and measurable retention lift, evaluate tiered pricing (Scenario C from gandalf-fixes).
- Month 6: If Guardrail Coverage Delta < +10pp AND WAU < 2,000, narrow scope to Bedrock-only.

---

## 12. Meeting Deck Outline (30 min)

| # | Section | Time | Content Source | Speaker |
|---|---------|------|---------------|---------|
| 1 | Problem Recap | 2 min | PRD: Maya Chen persona, JTBD-1/JTBD-2, 72% production AI / 60% governance gap | PM |
| 2 | Competitive Context | 2 min | PRD: ServiceNow AI Control Tower (30+ integrations, $100M+ M&A), Datadog LLM Obs (no governance), our cloud-native moat | PM |
| 3 | Solution Overview | 3 min | PRD: 5 capabilities (Discovery, Dashboard, Guardrails, Cost Intelligence, Maturity). V1 vs V2 scope boundary. | PM |
| 4 | Design Walkthrough | 5 min | Live prototype demo: landing page > summary cards > filter to unhealthy > click row > Split Panel tabs > maturity > export | PM + UX |
| 5 | Engineering Spec | 5 min | This doc Section 1: 4 components, API contracts, data model, perf targets. Security Hub precedent for cross-account. | Eng Lead |
| 6 | Sprint Plan | 3 min | This doc Section 3: 8 sprints, S0 spike, S3 dogfood, S5 beta, S7-S8 GA. Key dependencies. | PM + Eng Lead |
| 7 | Rollout and Rollback | 2 min | This doc Sections 5-6: 4-phase rollout with gates, 3-layer rollback per phase | Eng Lead |
| 8 | Monitoring Plan | 2 min | This doc Section 8: dashboards, canary, composite alarms, Application Signals SLO | Eng Lead |
| 9 | Open Questions | 4 min | This doc Section 14: CloudTrail volume spike, Bedrock batch API, DynamoDB vs Timestream, regional availability | All |
| 10 | Next Steps | 2 min | S0 kickoff: 2-week spike scope, ownership assignments, design review date | PM |

**Total: 30 minutes**

---

## 13. Consolidated Risk Register

| # | Source | Risk | L | I | Mitigation | Owner |
|---|--------|------|---|---|------------|-------|
| R1 | Gandalf Q7 | CloudTrail event volume at enterprise scale (>1M events/day) may cause discovery latency > 5 min | M | H | Batch processing with EventBridge Pipes; S0 spike to validate at scale. Security Hub handles comparable volume. | Eng Lead |
| R2 | Gandalf Q9 | Discovery accuracy < 90% for SageMaker custom endpoints | M | M | V1 limited to Bedrock + SageMaker managed models; custom endpoint discovery in v2 with allow-list | PM |
| R3 | Gandalf Q9 | Dashboard P95 load > 8s with > 200 workloads | L | H | Client-side pagination + server-side caching; table loads first, charts async | Eng Lead |
| R4 | Gandalf Q9 | Maturity model rejected by > 40% of users | M | M | Opt-in, dismissible; progression framing not grades; peer benchmarks. Pivot trigger defined. | PM + UX |
| R5 | Gandalf Q10 | Free tier creates expectation feature is always free | M | M | Position as "included with CloudWatch" not "free"; Scenario C pricing ready for v2 | PM + Marketing |
| R6 | PRD | ServiceNow launches cross-cloud AI governance before our GA | M | H | Differentiate on AWS-native depth (VPC metrics, CloudTrail events, IAM integration) | PM |
| R7 | PRD | IAM cross-account role setup friction causes > 50% abandon rate | M | H | One-click CloudFormation StackSet; template linked in Settings; guided setup wizard | Eng Lead |
| R8 | Design | Split Panel content overload with 4 tabs | L | M | Beta user research to validate; add/remove tabs based on usage data | UX |
| R9 | Design | Maturity score perceived as judgmental | L | M | Positive language ("3 actions to Level 3"); admin-configurable; below-fold placement | PM + UX |
| R10 | Technical | DynamoDB cost at scale (>10K workloads, 15-min refresh) | L | L | On-demand pricing initially; evaluate reserved capacity post-beta | Eng Lead |
| R11 | Technical | Bedrock Guardrails API rate limits during polling | M | M | Cache guardrail status 5 min; batch API feature request filed; exponential backoff | Eng Lead |
| R12 | Security | Cross-account IAM role escalation vulnerability | L | H | Security review in S5; read-only permissions only; trust policy restricted to admin account ID | Security Eng |
| R13 | Data Migration | Backfill Lambda timeout for large orgs (>5K workloads) | L | M | Paginated backfill with continuation tokens; Step Functions for orchestration if single Lambda insufficient | Eng Lead |

---

## 14. Open Questions for Engineering

| # | Question | Source | Owner | Due By |
|---|----------|--------|-------|--------|
| OQ-1 | Can we sustain < 5 min discovery latency at 1M+ CloudTrail events/day? Spike required. | Gandalf Q7 | Eng Lead | S0 (Week 2) |
| OQ-2 | DynamoDB vs Timestream for workload registry? DynamoDB for structured queries, Timestream for time-series cost/metrics. | Technical | Eng Lead | S0 (Week 2) |
| OQ-3 | How complete is SageMaker endpoint discovery via CloudTrail for custom endpoints with non-standard names? | Technical | Eng Lead + SageMaker team | S1 (Week 4) |
| OQ-4 | Can Bedrock Guardrails team build a batch status API? Current per-workload `GetGuardrail` is rate-limit risky at 500+ workloads. | Dependency | PM (file feature request) | S2 (Week 6) |
| OQ-5 | CloudFormation StackSet approach for cross-account IAM roles: exact policy scope and deployment mechanism? | Dependency | Eng Lead + IAM team | S1 (Week 4) |
| OQ-6 | Regional availability for v1: all commercial regions or Bedrock-available regions only? How do we handle Bedrock feature gaps per region? | Scope | PM + Eng Lead | S1 (Week 4) |
| OQ-7 | Does Bedrock console accept deep-link parameters for guardrail creation (pre-filled model ARN)? Required for Split Panel "Enable Guardrail" CTA. | Design/Dependency | PM + Bedrock Frontend team | S3 (Week 8) |
| OQ-8 | Saved view persistence: localStorage (per-browser) or account-level settings storage? Impacts portability and cross-device experience. | Design | PM + Eng Lead | S4 (Week 10) |
| OQ-9 | EU AI Act alignment: does maturity model need to map to EU AI Act risk classification? Legal review required. | PRD | Legal + PM | S5 (Week 12) |

---

## Appendix: Artifact Links

| Stage | Artifact | Version | Status |
|-------|----------|---------|--------|
| 1 — Research | research-v1.md | v1 | Complete |
| 2 — PRD | prd-v1.md | v1 | Complete |
| 2a — Gandalf Fixes | prd-v1-gandalf-fixes.md | v1.1 | Complete |
| 3 — Gandalf | gandalf-evaluation-v1.md | v1 | Passed with flags (7/10) |
| 4 — Design | design-spec-v2.md | v2 | Complete (checklist 4.6/5, heuristics 4.2/5) |
| 5 — Prototype | prototype-v2.html + prototype-notes-v2.md | v2 | Validated (100% components, 87.5% interactions) |
| 6 — Launch Readiness | This document (launch-readiness-v2.md) | v2 | Draft |
