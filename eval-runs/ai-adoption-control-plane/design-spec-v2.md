---
artifact: design-spec
version: v2
prd-version: v1 + gandalf-fixes-v1.1
timestamp: 2026-05-19T17:00:00Z
status: draft
design-context: enterprise
patterns-applied: Salesforce+Datadog
component-library: Cloudscape Design System
skill-version: 0.2.0
---

# Design Spec: CloudWatch AI Control Plane

## Executive Summary

This spec defines the end-to-end experience for CloudWatch AI Control Plane -- a new top-level page within the CloudWatch console that gives operations and compliance teams a single-pane view of all AI workloads across their AWS Organization. The design follows a hub-and-spoke model: the landing page (hub) shows fleet-level governance health, anomalies, cost, and maturity scoring; clicking any workload opens a Split Panel (spoke) with deep metrics, guardrail status, and cost breakdown. Built on Cloudscape Design System with Salesforce contextual surfacing + Datadog information density patterns. This v2 adds Nielsen heuristic audit, interaction state definitions, keyboard navigation, accessibility depth, responsive breakpoint specs, data visualization rationale, micro-interactions, wayfinding, anti-pattern validation, and first-time user experience -- all missing from v1.

## Design Context

**Type:** Enterprise (ops teams, SRE, compliance officers)
**Patterns Applied:** Salesforce + Datadog hybrid
**Component Library:** Cloudscape Design System
**Primary User:** Maya Chen -- Sr. Cloud Operations Lead managing 4 SREs, 6+ AI deployments
**Secondary User:** Raj Patel -- CISO needing audit-ready governance evidence
**Gandalf Constraints:** Technical feasibility confirmed via Security Hub precedent (Fix 1); failure thresholds defined at 10% discovery error / 8s render / 40% maturity opt-out (Fix 2); v1 ships free as retention play (Fix 3).

---

## Phase 1: First Principles Design

### Primary User Task

See the health, cost, and governance status of all AI workloads across my AWS Organization in one view, and drill into any workload that needs attention.

### Information Priority

1. **Governance health** -- How many AI workloads have guardrails? What % are covered? (North Star metric: 80% target)
2. **Anomalies** -- Which workloads are unhealthy right now? (errors, latency spikes, guardrail triggers)
3. **Cost** -- Total AI spend this month, cost by workload, optimization opportunities
4. **Maturity score** -- Org's AI governance maturity level (1-5) and next recommended action
5. **Discovery** -- New AI workloads detected since last visit

### Critical User Journey

| Step | User Action | System Response | Data Shown |
|------|------------|-----------------|------------|
| 1 | Navigate to CloudWatch > AI Control Plane | Landing page renders with fleet overview | All 5 information priorities at a glance |
| 2 | Scan the top summary bar | Instant health check -- green/yellow/red | 4 stat cards: Total Workloads, Guardrail Coverage %, Unhealthy Count, Monthly Cost |
| 3 | Notice red Status Indicator on 2 workloads | Eye drawn to anomaly rows sorted to top | Table rows with Status Indicator badges |
| 4 | Click the unhealthy workload row | Split Panel slides in from bottom with detail | Model info, guardrail config, alerts, cost breakdown, latency chart |
| 5 | See "Guardrail not configured" alert in panel | Inline Alert with action button | "Enable Guardrail" linking to Bedrock console with pre-filled model ARN |
| 6 | Close panel, scroll to maturity section | Maturity section visible below table | Current level, recommended actions, peer benchmark |
| 7 | Export compliance report | Click Actions dropdown > Generate Report | PDF/CSV of all AI assets, governance status, guardrail history |

### Decision Points

| Decision | Data Required | Design Element |
|----------|--------------|----------------|
| "Is my AI fleet healthy?" | Guardrail coverage %, unhealthy count | Summary cards + table Status Indicators |
| "Which workload needs attention?" | Health status, error rate, sorted by severity | Table sorted unhealthy-first + Property Filter |
| "Is this workload governed?" | Guardrail config, enforcement history | Split Panel Guardrails tab |
| "Are we overspending on AI?" | Cost by model/team/workload | Split Panel Cost tab + Cost Intelligence side nav page |
| "Can I prove governance to auditors?" | Full AI inventory, guardrail history | Actions > Generate Compliance Report |

### Minimum Viable Interaction

0 clicks to see governance health (landing page auto-loads). 1 click for workload detail. 2 clicks for compliance report export.

---

## Phase 2: Pattern Reality Check

### Applied Patterns

**Datadog Information Density:** The landing page table shows ALL AI workloads with inline health, cost, and governance columns. Sparklines in table cells for latency/error trends. Property Filter supports complex queries ("Bedrock workloads without guardrails in us-east-1 costing >$500/month"). One dense view beats five separate pages.

**Datadog Connectedness:** Every data point is a portal. Click model name to see all workloads using it. Click team tag to filter. Global Date Range Picker updates all panels simultaneously. Time context is never lost.

**Salesforce Contextual Surfacing:** Split Panel auto-surfaces related data: guardrail config, recent enforcement events, cost trend, and CloudTrail events for the selected workload -- all without asking. Proactive recommendations: "Recommended: Enable content moderation guardrail" with one-click link when guardrail is missing.

**Salesforce Configuration Over Customization:** Saved table views ("My team's workloads", "Ungoverned assets"). Collection Preferences for columns, page size, sort order. Maturity recommendations configurable by admins.

### Layout Rationale

**Table + Split Panel (not card grid):** Ops teams live in tables. CloudWatch EC2, Lambda, and RDS pages all use table + split panel. Maya's muscle memory expects scan-click-detail. Card grids (ServiceNow style) waste vertical space at 500+ workloads.

**Summary cards at top (not sidebar):** Datadog places summary metrics above the data table for the "10-second health check." A sidebar would compete with Split Panel for horizontal space on L breakpoint.

**Tabs in Split Panel (not nested pages):** Four tabs (Overview, Guardrails, Cost, Timeline) keep Maya in context. She can switch between health/governance/cost without losing her place in the table. Datadog trace detail uses this exact pattern.

**Maturity score below table (not above):** Strategic metric checked weekly, not per-incident. Below the table means visible on scroll but not competing with operational data. Raj (CISO) has a dedicated Maturity side nav item to jump directly.

### Alternatives Considered

| Decision | Chosen | Alternative A | Alternative B | Why Chosen Wins |
|----------|--------|--------------|--------------|-----------------|
| Landing layout | Table + Split Panel | Card grid (ServiceNow) | Multi-tab dashboard (Datadog) | Matches CloudWatch muscle memory; scales to 500+ workloads |
| Detail view | Bottom Split Panel | Side drawer | Full-page detail | Bottom panel keeps table visible; side drawer too narrow for charts |
| Governance view | Inline columns in table | Separate Governance page | Toggle Health/Governance views | Single table reduces navigation; Property Filter handles view switching |
| Maturity placement | Below-fold section | Top-level tab | Modal wizard | Below-fold = always visible but not dominant; tab hides from accidental discovery |
| Cost view | Split Panel tab + dedicated nav page | Inline sparklines only | Separate cost console | Tab for quick glance; dedicated page for deep analysis |
| Cross-account | Account dropdown filter | Per-account switching | Aggregated-only | Dropdown = one interaction to scope; supports fleet and single-account views |

### Cloudscape Component Mapping

| UI Element | Cloudscape Component | Configuration Notes |
|-----------|---------------------|-------------------|
| Page shell | **App Layout** | Side nav: Overview, Cost Intelligence, Maturity, Settings. Tools panel for help/preferences. |
| Page header | **Content Layout** + **Header** | Title: "AI Control Plane". Description: "Monitor and govern AI workloads across your organization." |
| Summary stats | **Cards** in **Grid** (4-col) | Total Workloads, Guardrail Coverage %, Unhealthy, Monthly AI Cost. Each card has sparkline. |
| Workload table | **Table** + **Collection Preferences** + **Pagination** | Cols: Name, Service, Model, Account, Health, Guardrail Status, Cost (30d), Last Active. Default sort: Health (unhealthy first). |
| Table filtering | **Property Filter** | Properties: service, model, account, health status, guardrail status, team tag, cost range |
| Health badges | **Status Indicator** | Healthy=green, Warning=yellow, Error=red, Unknown=grey. Each uses icon + color (never color alone). |
| Time range | **Date Range Picker** | Global scope. Default: Last 7 days. Updating it refreshes all data. |
| Workload detail | **Split Panel** (bottom, 40% height) | 4 tabs: Overview, Guardrails, Cost, Timeline |
| Detail Overview tab | **Key Value Pairs** + **Line Chart** | Model info, invocation count, latency P99, error rate chart |
| Guardrails tab | **Table** (nested) + **Alert** | Applied guardrails, enforcement history. Alert if none configured. |
| Cost tab | **Bar Chart** + **Key Value Pairs** | Cost by day (bar), total, per-invocation, optimization suggestion |
| Timeline tab | **Table** (events) | CloudTrail events sorted by time |
| Maturity section | **Container** + **Progress Bar** + **Cards** | Level 1-5, progress to next, recommended actions as Cards |
| Compliance export | **Button Dropdown** | Actions > Generate Report (PDF), Export CSV, Schedule Report |
| New workload alerts | **Flashbar** (info) | "3 new AI workloads detected since your last visit" with View link |
| Empty state | **Box** + illustration | Illustration + "No AI workloads detected" + Enable CTA + docs link |
| Error state | **Alert** (error) | "Unable to load data for 2 accounts" + account list + Fix Permissions link |
| Loading | Skeleton screens within each Container | Table loads first (cached), charts load async. No spinners -- skeletons only. |

---

## Phase 3: Design Checklist + Audits

### 3A. Core Design Checklist

| # | Criterion | Score | Evidence |
|---|-----------|:-----:|----------|
| 1 | Task Clarity | **5** | Fleet health check = 0 clicks (landing page). Workload detail = 1 click. Compliance report = 2 clicks. |
| 2 | Information Hierarchy | **5** | Summary cards (most important) > table (actionable) > maturity (strategic). Visual weight matches priority. |
| 3 | Progressive Disclosure | **4** | Table shows summary > Split Panel shows detail > tabs show specialized views. Maturity below fold. Split Panel tabs could add collapsible sub-sections for expert data. |
| 4 | Layout Rationale | **5** | Every decision documented with WHY in Alternatives Considered table (6 decisions, 2+ alternatives each). |
| 5 | Alternatives Considered | **5** | 6 decisions, each with 2 alternatives and "Why Chosen Wins" rationale. |
| 6 | Pattern Consistency | **5** | 100% Cloudscape components. Matches CloudWatch EC2/Lambda page patterns for muscle memory. |
| 7 | Stickiness | **4** | Flashbar new-workload detection, maturity progression gamification, cost alerting via Alarms. Missing: email/SNS notification for new workloads (v2 feature). |
| 8 | Error States | **5** | Empty, error, loading, partial data, stale data, no-guardrail, and first-time states all designed. |
| 9 | Expert vs. Novice | **4** | Property Filter + Collection Preferences + keyboard shortcuts for experts. Summary cards + maturity recommendations + FTUX tour for novices. |
| 10 | Accessibility | **4** | Cloudscape is WCAG AA by default. Status Indicators use color + icon. Full keyboard nav spec, ARIA landmarks, screen reader announcements defined in this v2. |

**Checklist Score: 10/10 pass (all >= 3). Average: 4.6/5.**

### 3B. Nielsen Heuristic Audit

| # | Heuristic | Score | Evidence | Remediation |
|---|-----------|:-----:|----------|-------------|
| H1 | Visibility of System Status | **5** | Summary cards update on load. Status Indicators per workload. "Last updated: X min ago" timestamp on table. Skeleton screens during loading. Flashbar for async actions (report generation). | -- |
| H2 | Match Between System and Real World | **4** | Uses ops language: "workloads," "guardrails," "health." Maturity levels use progression language ("Aware > Managed > Optimized"), not internal codes. | Ensure Cost tab uses $/month not raw token counts as primary display. |
| H3 | User Control and Freedom | **4** | Split Panel closeable via X or Esc. Filters clearable with one click ("Clear all"). Date Range Picker resettable. Collection Preferences resettable to defaults. | Add "Undo" to Flashbar after dismissing onboarding elements. |
| H4 | Consistency and Standards | **5** | 100% Cloudscape components. Follows CloudWatch page conventions (table + split panel + property filter). Side nav matches CloudWatch structure. | -- |
| H5 | Error Prevention | **4** | Compliance report export confirms format before generating. Filter validation prevents impossible combinations (e.g., SageMaker + Bedrock-only guardrail type). Date Range Picker prevents future dates. | Add confirmation step for "Schedule Report" since it creates a recurring action. |
| H6 | Recognition Rather Than Recall | **5** | Property Filter shows available values as dropdowns. Saved views persist filter state. Breadcrumbs show current location. Recent filters shown in filter dropdown. | -- |
| H7 | Flexibility and Efficiency | **4** | Property Filter for complex queries. Collection Preferences for column customization. Saved views for repeat workflows. Keyboard shortcuts (see 3D). | Add "Copy workload ARN" to right-click context menu for power users. |
| H8 | Aesthetic and Minimalist Design | **4** | Summary cards show only 4 KPIs. Table columns are curated (8 default, more via preferences). Maturity section below fold to avoid clutter. | Monitor whether the 4 summary cards are sufficient or if users want to customize which KPIs appear. |
| H9 | Error Recovery | **4** | Error Alert shows affected accounts + "Fix Permissions" link. Partial data state renders available data + per-row "Data unavailable" indicator. Stale data state shows timestamp + Refresh button. | Ensure "Fix Permissions" deep-links to the exact IAM policy, not just the IAM console. |
| H10 | Help and Documentation | **3** | Info links on summary cards. Tooltip on maturity score explaining methodology. Empty state has docs link. | Add contextual help panel (Cloudscape Tools panel) with per-tab documentation and "Learn more" links on Property Filter operators. |

**Heuristic Score: 10/10 pass (all >= 3). Average: 4.2/5.**

### 3C. Interaction State Matrix

All states use Cloudscape design tokens. No custom state styles.

| Element | Default | Hover | Pressed/Active | Focus (keyboard) | Disabled |
|---------|---------|-------|----------------|-------------------|----------|
| Summary Card | `$color-background-container-content`, no shadow | `$color-background-container-hover`, subtle shadow elevation | `$color-background-container-active`, shadow removed | 2px `$color-border-control-focus` ring, offset 2px | 50% opacity, `not-allowed` cursor |
| Table Row | `$color-background-container-content`, no border | `$color-background-dropdown-item-hover`, pointer cursor | `$color-background-item-selected`, left 4px accent border | 2px `$color-border-control-focus` ring on row | Grey text, no hover, `default` cursor |
| Primary Button (Generate Report) | `$color-background-button-primary`, white text | `$color-background-button-primary-hover` (darker) | `$color-background-button-primary-active` | 2px focus ring around button | `$color-background-button-primary-disabled`, grey text, `not-allowed` |
| Property Filter Input | `$color-background-input-default`, 1px border | Border color intensifies to `$color-border-input-hover` | N/A (text input) | 2px focus ring, border changes to `$color-border-control-focus` | Grey background, no interaction |
| Filter Token/Chip | `$color-background-badge-color-default`, rounded | Background darkens, pointer cursor | Pressed background darker | 2px focus ring | 50% opacity, no dismiss X |
| Side Nav Item | `$color-text-body-secondary`, no background | `$color-background-dropdown-item-hover` | Active page: left 4px `$color-border-control-focus` accent, bold text | 2px focus ring | Grey text, `default` cursor |
| Split Panel Toggle | `$color-background-button-normal`, icon visible | Background `$color-background-button-normal-hover` | Panel open: icon rotates 180deg | 2px focus ring | Hidden (panel unavailable) |
| Tab (Split Panel) | `$color-text-body-secondary`, underline none | Text color darkens | Active: `$color-text-accent`, 2px bottom border accent | 2px focus ring around tab text | Grey text, no underline, `default` cursor |
| Date Range Picker | Standard input styling | Border hover effect | Calendar popup opens | 2px focus ring on input | Grey background, no calendar |
| Status Indicator Badge | Color per status + icon, no background | Tooltip appears with status text | N/A (non-interactive read-only) | N/A (read-only, skip in tab order) | N/A |
| Button Dropdown (Actions) | `$color-background-button-dropdown`, caret icon | Background darkens | Dropdown menu opens, caret rotates | 2px focus ring | Grey, `not-allowed` cursor |
| Pagination Controls | Text links for page numbers | Underline appears | Active page: bold, no link | 2px focus ring on each page link | Grey text for pages beyond range |

All transitions: 150ms ease-out. All focus rings: 2px solid `$color-border-control-focus`, 2px offset.

### 3D. Keyboard Navigation Spec

**Tab Order (top to bottom, left to right):**

1. Skip to main content link (hidden until focused)
2. Skip to results link (hidden until focused)
3. Side navigation items (Overview, Cost Intelligence, Maturity, Settings)
4. Header actions (Help, Preferences)
5. Date Range Picker
6. Property Filter input
7. Summary Cards (each card is a focusable region; Enter opens detail if applicable)
8. Table header row (Tab moves between sortable column headers; Enter toggles sort)
9. Table rows (Arrow Up/Down navigates rows; Enter opens Split Panel)
10. Pagination controls
11. Maturity section actions (if scrolled into view)
12. Split Panel content (when open): Close button > Tab bar > Active tab content > Action buttons

**Keyboard Shortcuts:**

| Shortcut | Action | Scope | Conflict Check |
|----------|--------|-------|----------------|
| `/` | Focus Property Filter input | Global (when no input focused) | No browser conflict |
| `Esc` | Close Split Panel or dismiss Flashbar | Contextual | Standard |
| `Enter` | Activate focused element / Open Split Panel for focused row | Universal | Standard |
| `Arrow Up/Down` | Navigate table rows | Within table | Standard |
| `Arrow Left/Right` | Switch tabs in Split Panel | Within tab bar | Standard |
| `Ctrl+Enter` | Apply current filter | Within Property Filter | No conflict |
| `r` | Refresh data | Global (when no input focused) | No browser conflict |
| `?` | Toggle help panel | Global (when no input focused) | No browser conflict |

**Focus Management Rules:**

- Split Panel opens: focus moves to the close button inside the panel, then user can Tab to panel content.
- Split Panel closes (Esc or close button): focus returns to the table row that triggered it.
- Flashbar appears: announced via `aria-live="polite"` but focus stays where it is (non-blocking).
- Modal (compliance report config): focus trapped inside modal. Esc closes. Focus returns to Actions button.
- Property Filter dropdown: focus trapped in dropdown list. Esc closes dropdown, returns focus to input.
- Skip links: "Skip to main content" targets the Property Filter. "Skip to results" targets the first table row.

### 3E. Anti-Pattern Validation

| # | Anti-Pattern | Status | Notes |
|---|-------------|--------|-------|
| 1 | Mystery meat navigation (icons without labels) | **Absent** | Side nav uses text labels + icons. Status Indicators have tooltips. |
| 2 | Infinite scroll without progress indicator | **Absent** | Table uses Pagination, not infinite scroll. Page count visible. |
| 3 | Hamburger menu hiding primary navigation | **Absent on L/XL** | Hamburger appears only at S/XS breakpoints where side nav collapses. Justified: mobile is secondary use case. |
| 4 | Modal on top of modal (nested modals) | **Absent** | Only one modal at a time (compliance report config). Split Panel is not a modal. |
| 5 | Confirm-shaming (guilt-trip copy on cancel) | **Absent** | Cancel buttons use neutral "Cancel" text. No manipulative copy. |
| 6 | Pagination that loses scroll position | **Absent** | Page change scrolls table to top (expected behavior). Filter state preserved across pages. |
| 7 | Auto-playing content without user initiation | **Absent** | No auto-play. Data loads on page visit (expected), but no animations or media auto-play. |
| 8 | Ambiguous destructive actions | **Absent** | No destructive actions in v1 (read-only console). Schedule Report has confirmation step. |
| 9 | Truncated content with no way to see full text | **Absent** | Long workload names truncate with ellipsis + tooltip showing full text. Model ARNs have copy button. |
| 10 | Ghost buttons for primary actions | **Absent** | Primary actions (Generate Report, Enable Guardrail) use Cloudscape Primary Button (solid fill). |
| 11 | Data table without sortable columns | **Absent** | All columns sortable via Collection Preferences. Default sort: Health status descending. |
| 12 | Time-based UI without timezone clarity | **Absent** | Date Range Picker shows timezone. All timestamps display in user's local timezone with UTC in tooltip. |
| 13 | Search with no empty-result guidance | **Absent** | Property Filter with zero results shows: "No workloads match your filter" + "Clear all filters" link + suggestion to broaden criteria. |
| 14 | Settings that require page reload | **Absent** | Collection Preferences and filter changes apply instantly. No page reload required. |

### 3F. Data Visualization Decision Matrix

| Data Point | Viz Chosen | Why This Type | Alternative Considered | Why Rejected |
|-----------|-----------|---------------|----------------------|--------------|
| Guardrail coverage (% of fleet) | **Stat card with radial progress** | Single KPI, progress toward 80% target is the primary insight | Donut chart | Donut adds visual noise for a single percentage; radial progress is simpler |
| Unhealthy workload count | **Stat card with trend arrow** | Single KPI, trend direction matters (up = worse) | Sparkline | Count is small integer; sparkline overkill for 0-20 range |
| Monthly AI cost | **Stat card with sparkline** | Single KPI + 30-day trend gives context (rising or falling) | Bar chart | Sparkline in card is denser; bar chart needs its own panel |
| Total workloads | **Stat card (plain number)** | Inventory count, no trend needed | N/A | Simplest possible display |
| Latency over time (Split Panel) | **Line chart** | Time-series continuous trend; P50/P95/P99 percentile lines | Bar chart | Bars obscure continuous trend and percentile overlays |
| Error rate over time (Split Panel) | **Area chart** | Time-series, area fill highlights anomaly spikes against baseline | Line chart | Area fill makes spikes more visually prominent than a thin line |
| Cost by day (Split Panel Cost tab) | **Vertical bar chart** | Daily cost is discrete per-day comparison, not continuous | Line chart | Daily cost is a sum per day, not a continuous measurement; bars are more accurate |
| Cost by model (Cost Intelligence page) | **Horizontal bar chart** | Categorical comparison across 5-15 models; horizontal labels readable | Vertical bar | Model names are long (e.g., "anthropic.claude-3-sonnet"); horizontal accommodates labels |
| Guardrail enforcement history | **Ranked table with sparkline column** | Detailed data (guardrail name, trigger count, trend) needs sort + filter | Stand-alone bar chart | Sparkline-in-table-cell is denser (Datadog pattern); lets user correlate guardrail name + trend in one scan |
| Latency/error sparklines in main table | **Inline sparklines in table cells** | Correlate metric trends across workload rows without leaving the table | Separate chart panel per workload | Enterprise density rule: one table with inline sparklines beats N separate charts |
| Maturity score | **Progress bar (segmented, 5 levels)** | Shows current position on a known 1-5 scale with clear target | Radial gauge | Progress bar maps linearly to 5 levels; radial gauge implies arbitrary scale |
| Peer benchmark (maturity) | **Horizontal bar showing org vs. peer median** | Simple comparison of two values on same axis | Scatter plot | Only 2 data points; scatter is overkill |

### 3G. Micro-Interaction Spec

| Interaction | Trigger | Animation | Duration | Easing | Purpose |
|------------|---------|-----------|----------|--------|---------|
| Split Panel open | Click table row or Enter on focused row | Slide up from bottom of viewport | 200ms | ease-out | Reveal detail while keeping table visible above |
| Split Panel close | Click X, press Esc | Slide down, fade | 150ms | ease-in | Quick exit, return focus to triggering row |
| Tab switch (Split Panel) | Click tab or Arrow Left/Right | Crossfade content area | 100ms | ease-in-out | Fast swap, no layout shift |
| Filter apply | Click Apply or Ctrl+Enter | Table body fades to 30% opacity, skeleton loads, then new data fades in | 150ms fade + data load + 150ms fade-in | ease-in-out | Signal results are updating without full-page reload |
| Filter clear | Click "Clear all" | Tokens slide out, table refreshes | 150ms | ease-out | Distinct from apply; tokens visually disappear |
| Summary card data update | Data refreshed (global time range change) | Number countup animation from old to new value | 300ms | ease-out | Draw attention to changed values; countup signals freshness |
| Flashbar appear | Page load / async event | Slide in from top, push content down | 300ms | spring (slight overshoot) | Attract attention without blocking; Cloudscape standard |
| Flashbar dismiss | Click X or auto-dismiss after 8s | Fade out, content slides up | 200ms | ease-in | Clean removal |
| Modal open (report config) | Click Generate Report | Fade in backdrop + scale(0.95>1.0) dialog | 200ms | ease-out | Overlay focus; draw attention to modal |
| Modal close | Click Cancel, X, or Esc | Fade out | 150ms | ease-in | Quick exit |
| Table sort | Click column header | Rows fade to 50%, re-sort, fade to 100% | 200ms total | ease-in-out | Signal reorder without layout jank |
| Skeleton loading | Data fetch begins | Content replaced by Cloudscape skeleton rectangles | Immediate (no animation) | N/A | Preserve layout, indicate loading state |
| Status Indicator tooltip | Hover or focus on badge | Tooltip fades in above element | 150ms | ease-out | Show full status text without click |

**Rules:**
- No animation exceeds 400ms.
- All loading states use skeleton screens, never spinners (Cloudscape convention).
- No layout shift during any transition. Elements do not reflow.
- All animations respect `prefers-reduced-motion: reduce` -- if set, all transitions are instant (0ms).

### 3H. Responsive Breakpoint Specs

| Component / Region | XL (>=1600px) | L (1200-1599px) | M (992-1199px) | S (688-991px) | XS (<688px) |
|-------------------|---------------|-----------------|----------------|---------------|-------------|
| App Layout side nav | Expanded with text+icon | Expanded with text+icon | Collapsed to icons only; expand on hover | Hidden; hamburger menu | Hidden; hamburger menu |
| Summary Cards grid | 4 columns, all visible | 4 columns, all visible | 2x2 grid (stacked) | 2x2 grid | 1 column (stacked vertically) |
| Property Filter | Full inline, all tokens visible | Full inline | Compact; advanced operators collapsed behind "+" button | Full-width stacked above table | Full-width stacked |
| Workload Table | All 8 columns visible | All 8 columns | Hide Cost and Last Active columns (6 visible) | Hide Cost, Last Active, Account (5 visible) | Card view replaces table (1 card per workload) |
| Table sparklines | Visible in Latency/Error columns | Visible | Hidden (columns too narrow) | Hidden | N/A (card view) |
| Split Panel | Bottom position, 40% height | Bottom position, 40% height | Bottom position, full width, 50% height | Bottom position, collapsed by default, expand to 70% | Full-screen overlay (navigate to detail page) |
| Split Panel charts | Full-size Line/Bar charts | Full-size | Charts stack vertically within tabs | Charts stack, reduced axis labels | Sparklines only; tap for full chart |
| Maturity section | Full width below table, cards in 3-col grid | Same as XL | Cards in 2-col grid | Cards in 1-col stack | Cards in 1-col stack |
| Date Range Picker | Inline in header area | Inline | Below header, full width | Full width, compact mode | Full width, compact mode |
| Compliance export button | In Actions dropdown, header area | Same | Same | Moves to bottom fixed bar | Bottom fixed bar |

**Enterprise note:** CloudWatch APM users primarily use L and XL breakpoints. Design target is L. M degrades gracefully. S and XS must not break but are secondary.

### 3I. Accessibility Depth

**ARIA Landmarks:**

| Landmark | Element | Role | Label |
|----------|---------|------|-------|
| Main content | `<main>` wrapping table + maturity section | `main` | AI Control Plane |
| Navigation | Side nav `<nav>` | `navigation` | AI Control Plane navigation |
| Search | Property Filter container | `search` | Filter AI workloads |
| Complementary | Split Panel | `complementary` | Workload detail panel |
| Banner | Page header (Content Layout) | `banner` | AI Control Plane header |
| Region | Summary cards container | `region` | Fleet health summary |
| Region | Maturity section | `region` | AI governance maturity |

**Focus Management Rules:**

- Page load: focus goes to the Property Filter input (primary interactive element; skip links available to jump to table).
- Route change (side nav click): announce new page title via `aria-live="polite"` region, move focus to page `<h1>`.
- Filter applied: announce result count via `aria-live="polite"`: "[N] workloads match your filter."
- Filter cleared: announce "All filters cleared. [N] workloads shown."
- Error occurred: announce error via `aria-live="assertive"`, move focus to the Alert component.
- Split Panel open: move focus to panel close button; announce "[Workload name] detail panel open."
- Split Panel close: return focus to the table row that triggered it.
- Modal open: trap focus inside modal. First focus: first interactive element.
- Modal close: return focus to Actions dropdown trigger.

**Screen Reader Announcements:**

| Event | Announcement | Priority |
|-------|-------------|----------|
| Page loaded | "AI Control Plane. [N] AI workloads across [M] accounts." | polite |
| Data loading | "Loading AI workload data" | polite |
| Data loaded | "[N] AI workloads loaded" | polite |
| Filter applied | "[N] workloads match your filter" | polite |
| Filter cleared | "All filters cleared. [N] workloads shown." | polite |
| Sort changed | "Table sorted by [column], [ascending/descending]" | polite |
| Split Panel opened | "[Workload name] detail panel open" | polite |
| Split Panel tab changed | "[Tab name] tab selected" | polite |
| Error loading accounts | "Error: Unable to load data for [N] accounts" | assertive |
| Report generation started | "Generating compliance report" | polite |
| Report ready | "Compliance report ready for download" | assertive |
| New workloads detected | "[N] new AI workloads detected since your last visit" | polite |

**Color and Contrast:**

- All text meets WCAG AA: 4.5:1 for normal text, 3:1 for large text (enforced by Cloudscape tokens).
- Status Indicators use icon + color: green checkmark (Healthy), yellow warning triangle (Warning), red exclamation circle (Error), grey question mark (Unknown). Never color alone.
- Charts use patterns/shapes in addition to color for the latency percentile lines (P50 solid, P95 dashed, P99 dotted) to support colorblind users.
- All interactive elements have visible focus indicators (2px ring, `$color-border-control-focus`).

### 3J. Wayfinding & Navigation

**Breadcrumb Spec:**
```
CloudWatch > AI Control Plane > [Current Tab/Page]
```
Example: `CloudWatch > AI Control Plane > Cost Intelligence`

- Breadcrumbs always visible in Content Layout header.
- Every segment except current page is a link.
- Mobile (XS/S): truncate to last 2 segments with "..." overflow menu.

**Page Location Indicators:**

- Active side nav item has left border accent (`$color-border-control-focus`) + bold text.
- Page `<title>`: `[Current Page] - AI Control Plane - CloudWatch`
- URL reflects current state for all meaningful UI states.

**Deep-Link Strategy:**

| State | URL Parameter | Example |
|-------|--------------|---------|
| Active side nav page | Path segment | `/cloudwatch/ai-control-plane/cost-intelligence` |
| Active tab (Split Panel) | `?tab=[tab-id]` | `?tab=guardrails` |
| Applied filter | `?filter=[encoded]` | `?filter=service%3Dbedrock%26health%3Derror` |
| Selected workload | `?selected=[id]` | `?selected=arn:aws:bedrock:us-east-1:123:model/claude-3` |
| Time range | `?start=[ts]&end=[ts]` | `?start=1716000000&end=1716086400` |
| Split Panel open | Implied by `?selected` | Panel auto-opens when `selected` param present |
| Table sort | `?sort=[col]&dir=[asc|desc]` | `?sort=cost&dir=desc` |
| Pagination | `?page=[n]` | `?page=3` |

Every meaningful UI state is deep-linkable. Users share URLs in Slack, paste in runbooks, and bookmark investigations.

**Navigation Hierarchy:**

- **Primary:** Cloudscape side navigation (persistent, collapsible). Items: Overview (default), Cost Intelligence, Maturity, Settings.
- **Secondary:** Tabs within the Split Panel (Overview, Guardrails, Cost, Timeline).
- **Tertiary:** Property Filter saved views as a segmented control above the filter bar.
- Max 3 navigation levels. Breadcrumbs always visible.

### 3K. First-Time User Experience

**Progressive Onboarding Flow:**

| Stage | Trigger | What User Sees | Goal |
|-------|---------|---------------|------|
| 1. Empty state | No AI workloads discovered / first visit, no data | Illustrated empty state with "Enable AI Control Plane" CTA. Explains: "When enabled, we'll automatically discover Bedrock and SageMaker workloads across your organization." Links to docs. | Get user to enable cross-account discovery |
| 2. Discovery in progress | Enabled but data still populating (first 24 hours) | Partial dashboard. Flashbar: "Discovery is running. Workloads will appear as they're found. Full discovery typically completes within 24 hours." Progress indicator. | Set expectation, prevent "nothing works" reaction |
| 3. Guided tour | First time with populated data (5+ workloads) | Optional 4-step tooltip tour: (1) "Summary cards show fleet health at a glance" (2) "Click any workload to see details" (3) "Use filters for complex queries" (4) "Check your maturity score for next steps." Dismissible at any step. | Teach primary workflow in <60 seconds |
| 4. Feature discovery | After 3+ visits with full data | Subtle blue dot badge on undiscovered side nav items (e.g., Cost Intelligence page if never visited). Badge disappears after first visit. | Expand usage breadth to secondary features |
| 5. Power user nudges | After 10+ visits or 5+ filter uses | Keyboard shortcut hints in tooltips: "Tip: Press / to quickly filter." Saved view suggestion: "You've used this filter 3 times -- save it as a view?" | Increase efficiency, deepen habit |

**Empty State Design (per page):**

| Page | Illustration | What It Will Show | Why It's Empty | CTA | Docs Link |
|------|-------------|-------------------|----------------|-----|-----------|
| Overview (no workloads) | Cloud + AI chip illustration | "This page will show all your AI workloads, their health, guardrail coverage, and costs." | "AI Control Plane hasn't been enabled yet, or no Bedrock/SageMaker workloads exist in your Organization." | "Enable AI Control Plane" (primary button) | "Learn about AI Control Plane" |
| Overview (no unhealthy) | Green checkmark illustration | N/A (this is the good state) | N/A | N/A | N/A |
| Cost Intelligence (no data) | Cost graph illustration | "Cost Intelligence will show AI spend by model, team, and workflow." | "Cost data takes up to 48 hours to populate after workloads are discovered." | "View workload discovery status" (link) | "Learn about AI cost tracking" |
| Maturity (no data) | Ladder/steps illustration | "Your organization's AI governance maturity score will appear here with recommended next actions." | "Maturity assessment requires at least 3 discovered workloads." | "View discovered workloads" (link) | "Learn about the maturity model" |
| Filter zero results | Magnifying glass illustration | N/A | "No workloads match your current filter." | "Clear all filters" (link) | N/A |

**Onboarding Dismissal:**
- All onboarding elements (tour, badges, nudges) can be permanently dismissed.
- Dismissal state persists in Cloudscape user preferences (stored in browser localStorage, synced to account settings).
- A "Tips & Tours" link in the Help panel (Cloudscape Tools panel) lets users re-trigger the guided tour.

---

## Stickiness Design

**Habit loop 1: "What's new" pull.** Every visit, Flashbar shows newly detected AI workloads since last session: "3 new AI workloads detected since your last visit." This creates a daily check habit. Count also shown as a badge on the CloudWatch side nav item.

**Habit loop 2: Maturity progression.** The 1-5 maturity score creates a goal-seeking mechanic: "You're at Level 2 -- enable guardrails on 3 more workloads to reach Level 3." Each recommended action is concrete ("Enable content moderation guardrail on fraud-detection-model -- estimated effort: 15 minutes"). Completing an action triggers a Flashbar success message + progress bar animation.

**Habit loop 3: Cost alerting.** Weekly cost summary via CloudWatch Alarms + SNS: "Your AI spend increased 23% this week, driven by fraud-detection model." Creates a weekly return even when nothing is broken. Links directly to Cost Intelligence page with the relevant time range pre-selected (deep link).

**Habit loop 4: Governance drift alerts.** Alert when a new workload is deployed without guardrails: "New Bedrock workload 'customer-support-bot' has no guardrails. Configure now?" This ties the habit loop to the North Star metric (guardrail coverage %).

## Error & Edge States

| State | Design Treatment |
|-------|-----------------|
| **Empty state** (no AI workloads) | Box with cloud+AI illustration. "No AI workloads detected." CTA: "Enable AI Control Plane" button. Subtext: what gets discovered. Link to docs. |
| **Error state** (cross-account failure) | Alert (error) top of table: "Unable to load data for 2 accounts: [account-ids]." "Fix Permissions" button deep-links to the specific IAM policy needed. |
| **Loading state** | Skeleton screens for table rows and charts. Table loads first (cached data from DynamoDB inventory). Charts load async. No spinners. |
| **Partial data** | Per-row Status Indicator "Data unavailable" for accounts with permission issues. Table renders available accounts. Alert banner: "Showing partial data. 2 accounts have permission issues." |
| **Stale data** | Timestamp label in table header: "Last updated: 3 min ago." Refresh button. Tooltip on metrics shows data freshness per-source. |
| **No guardrails** | Split Panel Guardrails tab: Alert (warning) "No guardrails configured for this workload." CTA: "Enable Guardrail" linking to Bedrock console with pre-filled model ARN. |
| **First-time user** | Guided tour (see 3K FTUX above). |
| **Permission denied** | Full-page Alert: "You don't have permission to view AI Control Plane. Required policy: cloudwatch:GetAIControlPlaneData." CTA: "Request access from your administrator" (copy-pastable policy JSON). |
| **Discovery in progress** | Flashbar info: "Discovery is running. Workloads appear as found. Full discovery: ~24 hours." Partial table renders with available data. |
| **Timeout** | Alert (warning): "Dashboard data is taking longer than expected. Showing cached data from [timestamp]." Retry button. |

## Handoff Notes for Prototype Builder

### Critical Interactions to Implement
1. **Table row click > Split Panel open** -- bottom panel, 40% height, slide-up animation (200ms ease-out).
2. **Split Panel tabs** -- Overview/Guardrails/Cost/Timeline with crossfade (100ms).
3. **Property Filter** -- at least 3 filterable properties (service type, health status, guardrail status) with token-based filtering.
4. **Date Range Picker** -- global, updates all visible data.
5. **Summary cards** with realistic data: Total Workloads (14), Guardrail Coverage (68%), Unhealthy (2), Monthly Cost ($12,400).
6. **Status Indicators** in table cells (green/yellow/red with icons, not color alone).
7. **Skeleton loading states** on initial load (not spinners).
8. **Keyboard nav**: `/` to focus filter, `Esc` to close panel, arrow keys in table.

### Data to Mock
- 12-15 AI workloads across 3-4 accounts.
- Mix: Bedrock (Claude 3 Sonnet, Claude 3 Haiku, Titan Embeddings) and SageMaker (custom fraud model, recommendation engine).
- Health distribution: 9 healthy, 2 warning (high latency), 2 error (no guardrail), 1 unknown.
- Cost range: $50-$5,000/month per workload. Total: ~$12,400/month.
- Guardrail coverage: 68% (below 80% target -- gap is visible).
- Maturity level: 2 ("Aware") with 3 recommended actions to reach Level 3.

### Responsive Priority
Build for L breakpoint (1200-1599px) first. Ensure M (992-1199px) degrades gracefully (hide low-priority columns). S/XS are stretch goals -- prototype can skip mobile card view.

### Component Versions
Cloudscape React components `@cloudscape-design/components` v3.x. For HTML prototype:
```html
<link rel="stylesheet" href="https://d1l2xqwxk0m6bj.cloudfront.net/3.0/cloudscape-design/style.css">
```

### Interaction States to Implement
At minimum, implement: table row hover + active, primary button hover + disabled, filter token hover + dismiss, Split Panel tab active state. Focus ring on all interactive elements.

---

## Feedback to PRD (End-to-End Experience Update)

### Assumptions Made Where PRD Was Ambiguous

1. **Split Panel position:** PRD says "detail panel" but doesn't specify position. Design chose bottom Split Panel (not side drawer) because table needs full width for 8 columns. PRD should confirm this.
2. **Maturity score visibility:** PRD describes maturity as a "prescriptive maturity model" but doesn't say whether it's default-visible or opt-in. Design places it below-fold on the Overview page and as a dedicated side nav item. If maturity should be more prominent (e.g., above the table), PRD should state this.
3. **Cross-account default view:** PRD says "cross-account by default" but doesn't specify whether the landing page shows all-accounts-aggregated or requires account selection. Design chose aggregated-by-default with account filter in Property Filter. PRD should confirm.
4. **Compliance report format:** PRD mentions "compliance report" but doesn't specify format. Design assumes PDF + CSV export options with a modal to configure scope (date range, accounts, workloads). PRD should specify required report fields.

### UX Constraints Requiring PRD Scope Changes

1. **Discovery latency expectation-setting:** The FTUX reveals that "discovery completes within 24 hours" needs to be a stated SLA in the PRD, not just a technical assumption. First-time users who see an empty dashboard after enabling will churn. PRD should add "Time to first data" as a success metric (target: <1 hour for Bedrock workloads, <24 hours for SageMaker).
2. **Maturity opt-out:** The failure scenario in gandalf-fixes (40% opt-out threshold) means the PRD should explicitly state maturity scoring is dismissible/optional, not mandatory on the dashboard. This affects how the feature is described in the PRD scope section.
3. **Permission denied state:** The PRD doesn't address what happens when a user has CloudWatch access but not the specific AI Control Plane IAM permission. Design added a Permission Denied empty state, but the PRD should define the IAM permission model (new managed policy vs. existing CloudWatch permissions).

### Interaction Patterns Implying New Requirements

1. **Saved views:** The design includes saved table views (e.g., "Ungoverned assets"). This implies a persistence layer for user preferences -- either localStorage (per-browser, not portable) or account-level settings storage. PRD should decide which.
2. **Deep-linking with filter state:** URL-encoded filter state means the Property Filter query syntax needs to be stable and documented. If users share filtered URLs in runbooks, changing the filter schema is a breaking change. PRD should add "filter URL stability" as a non-functional requirement.
3. **"Enable Guardrail" cross-console link:** The Split Panel links to Bedrock Guardrails console with a pre-filled model ARN. This requires Bedrock console to accept deep-link parameters for guardrail creation. PRD should confirm this cross-service deep-link is feasible or add it as a dependency.
4. **Governance drift alerting (habit loop 4):** The stickiness design includes alerts when new workloads lack guardrails. This implies a background monitoring job that checks new workloads against governance policies. This is not in v1 scope -- PRD should either add it or explicitly defer to v2.
