---
artifact: design-spec
version: v1
prd-version: v1 + gandalf-fixes-v1.1
timestamp: 2026-05-19T15:45:00Z
status: draft
design-context: enterprise
patterns-applied: Salesforce+Datadog
component-library: Cloudscape Design System
---

# Design Spec: CloudWatch AI Control Plane

## Executive Summary

We're creating a new top-level page within the CloudWatch console that gives operations and compliance teams a single-pane view of all AI workloads across their AWS Organization. The experience follows a hub-and-spoke model: landing page (hub) shows the fleet view — all AI workloads, governance health, cost summary, maturity score — and clicking any workload opens a detail panel (spoke) with deep metrics, guardrail status, and cost breakdown. The design prioritizes information density (Datadog pattern) with contextual data surfacing (Salesforce pattern), all built in Cloudscape components.

## Design Context
**Type:** Enterprise (ops teams, SRE, compliance officers)
**Patterns Applied:** Salesforce + Datadog hybrid
**Component Library:** Cloudscape Design System
**Primary User:** Maya Chen — Sr. Cloud Operations Lead managing 4 SREs, 6+ AI deployments across her org

## Phase 1: First Principles Design

### Primary User Task
See the health, cost, and governance status of all AI workloads across my AWS Organization in one view, and drill into any workload that needs attention.

### Information Priority
1. **Governance health** — How many AI workloads have guardrails? What % are covered? (North Star metric)
2. **Anomalies** — Which workloads are unhealthy right now? (errors, latency spikes, guardrail triggers)
3. **Cost** — What's the total AI spend this month? Which workloads cost the most? Any optimization opportunities?
4. **Maturity score** — Where is our org on the AI governance maturity ladder? What's the next recommended action?
5. **Discovery** — What new AI workloads were detected since last visit?

### Critical User Journey

| Step | User Action | System Response | Data Shown | Cloudscape Component |
|------|------------|-----------------|------------|---------------------|
| 1 | Navigate to CloudWatch → AI Control Plane | Landing page renders with fleet overview | All 5 information priorities at a glance | App Layout + Content Layout |
| 2 | Scan the top summary bar | Instant health check — green/yellow/red | 4 stat cards: Total workloads, Guardrail coverage %, Unhealthy count, Monthly cost | Cards in a Grid |
| 3 | Notice a red Status Indicator on 2 workloads | Eye drawn to anomaly row in table | Table row highlighted with Status Indicator | Table + Status Indicator |
| 4 | Click the unhealthy workload row | Split Panel opens from bottom showing detail | Model info, guardrail config, recent alerts, cost breakdown, latency chart | Split Panel + Tabs + Line Chart |
| 5 | See "Guardrail not configured" alert | Inline Alert with action button | Alert with "Enable Guardrail" button linking to Bedrock console | Alert + Button |
| 6 | Close detail, check maturity score | Scroll to maturity section or click tab | Current level, recommended next actions, peer benchmark | Container + Progress Bar |
| 7 | Export compliance report | Click "Generate Report" in actions dropdown | PDF/CSV of all AI assets, governance status, guardrail history | Button Dropdown + Flashbar |

**Minimum viable interaction: 0 clicks to see governance health (landing page auto-loads), 1 click to see workload detail.**

### Decision Points

| Decision | Data Required | Design Element |
|----------|--------------|----------------|
| "Is my AI fleet healthy?" | Guardrail coverage %, unhealthy count, top anomalies | Top summary cards + Status Indicators in table |
| "Which workload needs attention?" | Health status, error rate, guardrail triggers sorted by severity | Table sorted by health status (unhealthy first) |
| "Is this workload properly governed?" | Guardrail config, enforcement history, compliance status | Split Panel detail with Guardrail tab |
| "Are we overspending on AI?" | Cost by model/team/workload, optimization recommendations | Cost Intelligence tab with bar charts |
| "Can I prove governance to auditors?" | Complete AI inventory, guardrail history, enforcement logs | Export action → compliance report |

## Phase 2: Pattern Reality Check

### Applied Patterns

**Datadog Information Density:**
- The landing page table shows ALL AI workloads with inline health, cost, and governance columns — no drill-down required for the quick scan. Expert users can assess fleet health in one glance.
- Table supports Property Filter for complex queries ("show me all Bedrock workloads without guardrails in us-east-1 costing >$500/month").
- Small multiple sparklines in the table cells for latency/error trends without clicking.

**Datadog Connectedness:**
- Every data point is a portal. Click a model name → see all workloads using it. Click a team tag → see all their AI assets. Click a guardrail → see all workloads it protects.
- Time range picker is global — changing it updates all panels, charts, and status simultaneously.

**Salesforce Contextual Surfacing:**
- Split Panel detail auto-surfaces related data: when viewing a Bedrock workload, the panel shows the guardrail config, recent enforcement events, cost trend, AND the most recent CloudTrail events for that model — all without asking.
- "You might need" intelligence: if a workload has no guardrail, the panel proactively shows "Recommended: Enable content moderation guardrail" with a one-click link.

**Salesforce Configuration Over Customization:**
- Users can save filtered table views ("My team's workloads", "Ungoverned assets", "Top cost workloads").
- Collection Preferences let users choose which columns to show, page size, and default sort.
- Maturity score recommendations are configurable — admins can set org-level governance policies.

### Layout Rationale

**Why a single-page table with split panel (not a multi-page wizard or card grid):**
Ops teams live in tables. CloudWatch's existing service pages (EC2, Lambda, RDS) all use the table + split panel pattern. Maya's muscle memory expects: scan table → click row → see detail. Breaking this pattern (e.g., card-based dashboard like ServiceNow) would add cognitive load for users who already know CloudWatch.

**Why summary cards at top (not a sidebar):**
The Datadog pattern places summary metrics above the data table so they're visible without scrolling. This gives Maya her "10-second health check" (scan 4 numbers) before she even looks at individual workloads. A sidebar would compete with the Split Panel for horizontal space.

**Why tabs in the Split Panel (not nested pages):**
The split panel has 4 tabs: Overview, Guardrails, Cost, Timeline. This keeps Maya in context — she can switch between a workload's health, governance, and cost without losing her place in the table above. Datadog uses this exact pattern for trace detail views.

**Why maturity score is below the table (not above):**
The maturity score is a strategic metric, not an operational one. Maya checks it weekly, not per-incident. Putting it below the table means it's visible when scrolling but doesn't compete with the operational data she needs first. For Raj (CISO), the maturity section has its own nav tab in the side navigation so he can jump directly to it.

### Alternatives Considered

| Decision | Chosen | Alternative A | Alternative B | Why Chosen Wins |
|----------|--------|--------------|--------------|-----------------|
| Landing page layout | Table + Split Panel | Card grid (ServiceNow style) | Multi-tab dashboard (Datadog style) | Matches existing CloudWatch muscle memory; table scales to 500+ workloads |
| Detail view | Bottom Split Panel | Side drawer | Full-page detail | Bottom panel keeps table visible; side drawer too narrow for charts |
| Governance view | Inline columns in main table | Separate "Governance" page | Toggle between "Health" and "Governance" views | Single table reduces navigation; Property Filter handles view switching |
| Maturity score placement | Below-fold section | Top-level tab | Modal/wizard | Below-fold = always visible but not dominant; tab would hide it from discovery |
| Cost view | Tab in Split Panel + dedicated side nav page | Inline sparklines only | Separate cost console | Split Panel tab for quick glance; dedicated page for cost analysis |
| Cross-account | Account dropdown filter in table | Per-account dashboard switching | Aggregated-only (no account drill-down) | Dropdown filter = one interaction to scope; supports both fleet and single-account view |

### Cloudscape Component Mapping

| UI Element | Cloudscape Component | Configuration Notes |
|-----------|---------------------|-------------------|
| Page shell | **App Layout** | Side nav with: Overview, Cost Intelligence, Maturity, Settings. Tools panel for help/preferences. |
| Page header | **Content Layout** with Header | Title: "AI Control Plane". Description: "Monitor and govern AI workloads across your organization." |
| Summary stats | **Cards** in **Grid** (4 columns) | Total Workloads, Guardrail Coverage %, Unhealthy, Monthly AI Cost |
| Workload table | **Table** + **Collection Preferences** + **Pagination** | Columns: Name, Service (Bedrock/SageMaker), Model, Account, Health Status, Guardrail Status, Cost (30d), Last Active |
| Table filtering | **Property Filter** | Filterable properties: service, model, account, health status, guardrail status, team tag, cost range |
| Health badges | **Status Indicator** | Healthy (green), Warning (yellow), Error (red), Unknown (grey) |
| Time range | **Date Range Picker** | Global — changes update all panels. Default: Last 7 days. |
| Workload detail | **Split Panel** (bottom, 40% height) | 4 tabs: Overview, Guardrails, Cost, Timeline |
| Detail overview tab | **Key Value Pairs** + **Line Chart** | Model info, invocation count, latency P99, error rate chart |
| Guardrails tab | **Table** (nested) + **Alert** | List of applied guardrails, enforcement history. Alert if no guardrail configured. |
| Cost tab | **Bar Chart** + **Key Value Pairs** | Cost by day (bar), total, per-invocation, optimization suggestion |
| Timeline tab | **Table** (events) | CloudTrail events for this workload, sorted by time |
| Maturity section | **Container** + **Progress Bar** + **Cards** | Current level (1-5), progress to next level, recommended actions as Cards |
| Compliance export | **Button Dropdown** | "Actions" → Generate Compliance Report (PDF), Export CSV, Schedule Report |
| New workload alerts | **Flashbar** | "3 new AI workloads detected since your last visit" with "View" link |
| Empty state | **Box** with illustration | "No AI workloads detected. Enable AI Control Plane in Settings to start discovering AI assets." |
| Error state | **Alert** (error variant) | "Unable to load AI workload data for 2 accounts. Check cross-account permissions." with "Fix Permissions" link. |
| Loading state | **Spinner** within each Container | Skeleton loading for table, spinner for charts. Table loads first (fastest), charts load async. |

## Phase 3: Design Checklist

| # | Criterion | Score (1-5) | Evidence |
|---|-----------|:-----------:|----------|
| 1 | Task Clarity | **5** | Primary task (fleet health check) requires 0 clicks — visible on landing. Workload detail = 1 click. |
| 2 | Information Hierarchy | **5** | Summary cards (most important) → table (actionable) → maturity (strategic). Visual weight matches priority. |
| 3 | Progressive Disclosure | **4** | Table shows summary → Split Panel shows detail → tabs show specialized views. Maturity score hidden below fold. Could add collapsible sections in Split Panel tabs. |
| 4 | Layout Rationale | **5** | Every major decision documented with "why chosen wins" in alternatives table. |
| 5 | Alternatives Considered | **5** | 6 decisions with 2+ alternatives each, all documented above. |
| 6 | Pattern Consistency | **5** | 100% Cloudscape components. Matches existing CloudWatch pages (EC2, Lambda) for muscle memory. |
| 7 | Stickiness | **4** | New workload detection alerts (Flashbar) create "what's new" pull. Saved views create personalization. Maturity score creates goal-seeking behavior. Missing: no notification/email for new workloads yet. |
| 8 | Error States | **4** | Empty, error, loading states all designed. Missing: partial data state (some accounts succeed, some fail) — added as inline per-row error indicators. |
| 9 | Expert vs. Novice | **4** | Property Filter + Collection Preferences serve experts. Summary cards + maturity recommendations serve novices. Missing: onboarding tour for first-time users. |
| 10 | Accessibility | **3** | Cloudscape is WCAG AA compliant by default. Status Indicators use both color and icon (not color-only). Table is keyboard-navigable. Need to verify Split Panel keyboard flow and screen reader announcements. |

**Checklist Score: 10/10 pass (all >= 3). Average: 4.4/5.**

## Stickiness Design

**Habit loop 1: "What's new" pull**
Every visit, the Flashbar shows newly detected AI workloads since last session. This creates a daily check habit — "what new AI did my teams deploy?" The new-workload count is also shown in the CloudWatch side navigation badge.

**Habit loop 2: Maturity progression**
The maturity score creates a game-like progression mechanic. "You're at Level 2 — enable guardrails on 3 more workloads to reach Level 3." Each recommended action is concrete and achievable. Completing an action triggers a Flashbar success message.

**Habit loop 3: Cost alerting**
Weekly cost summary notifications (via CloudWatch Alarms). "Your AI spend increased 23% this week, driven by fraud-detection model." Creates a weekly return pattern even when nothing is broken.

## Error & Edge States

| State | Design Treatment |
|-------|-----------------|
| **Empty state** (no AI workloads) | Box with illustration: "No AI workloads detected." CTA: "Enable AI Control Plane" button. Subtext explains what gets discovered. |
| **Error state** (cross-account failure) | Alert (error) at top of table: "Unable to load data for 2 accounts." List accounts. "Fix Permissions" button → IAM console. |
| **Loading state** | Skeleton loading for table rows. Spinner for charts. Table loads first (data from cache), charts load async (fresh aggregation). |
| **Partial data** | Per-row Status Indicator shows "Data unavailable" for accounts with permission issues. Table still renders available accounts. |
| **No guardrails configured** | In Split Panel Guardrail tab: Alert (warning) with "This workload has no guardrails configured" + "Enable Guardrail" button linking to Bedrock Guardrails console with pre-filled model ARN. |
| **Stale data** | Timestamp label in table header: "Last updated: 3 minutes ago" + "Refresh" button. Tooltips on metrics show data freshness. |
| **First-time user** | Onboarding Flashbar: "Welcome to AI Control Plane. Here's what you can do:" → 3 quick actions (View workloads, Check governance, Export report). Dismissible. |

## Handoff Notes for Prototype Builder

### Critical Interactions to Implement
1. **Table row click → Split Panel open** with smooth animation (bottom panel, 40% viewport height)
2. **Split Panel tabs** switching between Overview/Guardrails/Cost/Timeline
3. **Property Filter** with at least 3 filterable properties (service type, health status, guardrail status)
4. **Date Range Picker** that updates all visible data
5. **Summary cards** at top with real numbers from the research data
6. **Status Indicators** in table cells (green/yellow/red with icons)

### Data to Mock
Use realistic data derived from the research:
- 12-15 AI workloads across 3-4 accounts
- Mix of Bedrock (Claude, Titan) and SageMaker models
- 3 workloads healthy, 2 warning (high latency), 1 error (guardrail not configured), rest healthy
- Cost range: $50-$5,000/month per workload
- Guardrail coverage: 68% (to show gap from 80% target)

### Responsive Behavior
- Desktop (1200px+): Full table + side nav + split panel
- Tablet (768-1199px): Table with horizontal scroll, split panel full-width
- Mobile (375-767px): Card view instead of table, split panel becomes full-page overlay

### Component Versions
Use Cloudscape React components from `@cloudscape-design/components` v3.x. For the HTML prototype, CDN links:
```html
<link rel="stylesheet" href="https://d1l2xqwxk0m6bj.cloudfront.net/3.0/cloudscape-design/style.css">
```
