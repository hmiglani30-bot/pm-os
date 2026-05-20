---
artifact: design-spec
version: v1
prd-version: v1
timestamp: 2026-05-20T18:00:00Z
status: draft
design-context: enterprise
patterns-applied: Salesforce+Datadog
skill-version: 0.3.0
---

# Design Spec: Quick Desktop AI Control Tower

## Executive Summary

This design spec defines the end-to-end experience for the Quick Desktop AI Control Tower — a cross-vendor AI governance capability embedded within Amazon Quick Desktop. The design targets enterprise IT operations leaders (primary: Lisa Nakamura, Director of Digital Workplace) who need to discover shadow AI, enforce governance policies, attribute costs, and measure adoption maturity from a single desktop-native console. The experience follows Salesforce+Datadog enterprise patterns (dense information surfaces, contextual data surfacing, lateral navigation) implemented through Cloudscape Design System components. The design covers seven navigable sections spanning five governance dimensions (Discover, Observe, Govern, Secure, Measure) plus Admin Console and Integration Marketplace, meeting or exceeding ServiceNow's five-pillar navigation surface.

## Design Context

**Type:** Enterprise
**Patterns Applied:** Salesforce+Datadog Hybrid
**Component Library:** Cloudscape Design System
**Primary Persona:** Lisa Nakamura, Director of Digital Workplace (medium-high technical sophistication, manages 8 IT ops staff, not writing CloudWatch queries)
**Secondary Persona:** David Park, VP Engineering (high technical sophistication, former SRE)

---

## Phase 1: First Principles Design

### Primary User Task

Gain complete visibility into organizational AI tool usage — what AI exists, what it costs, whether it complies with policy, and whether the investment is delivering value — and take governance action directly from the desktop agent employees already use daily.

### Information Priority

1. **Governance health at a glance** — aggregate KPIs (total AI tools discovered, % governed, total spend, compliance rate, maturity score) displayed as a hero bar the moment the user enters the Control Tower. This answers the CEO's question in 5 seconds.
2. **Shadow AI alerts** — newly discovered unapproved tools and active security risk notifications, surfaced as a priority attention zone below the hero bar. This is the "aha" moment that drives adoption.
3. **AI inventory drill-down** — the complete catalog of AI tools with per-tool detail (who uses it, cost, compliance status, risk level) accessible via table with split-panel detail. This is the working surface for daily governance.
4. **Trend and cost data** — adoption trends over time, cost attribution by team/vendor, maturity progression — the reporting layer that supports quarterly reviews and executive presentations.
5. **Policy and configuration** — governance policy management, integration setup, and admin settings — accessed less frequently but critical for initial setup and ongoing tuning.

### Critical User Journey

| Step | User Action | System Response | Data Shown |
|------|------------|-----------------|------------|
| 1 | Opens Quick Desktop, navigates to AI Control Tower via sidebar | Control Tower Command Center loads with pre-aggregated data | Hero KPI bar: 247 AI tools, $182K/mo spend, 72% governed, 3 active risks, maturity level 3 |
| 2 | Scans the shadow AI alert zone | System highlights 4 newly discovered unapproved tools from the last 7 days | Tool names, team using them, data sensitivity risk, recommended action |
| 3 | Clicks an unapproved tool (e.g., "Jasper AI — Marketing") | Split panel opens with tool detail | Tool profile: 12 users, $2.4K/mo estimated cost, no governance policy, medium data risk, discovery source (desktop detection) |
| 4 | Clicks "Apply Policy" on the tool detail | Policy selection modal appears with recommended governance action | Options: Approve (add to sanctioned list), Monitor (track but don't block), Block (add to restricted list + notify users) |
| 5 | Selects "Approve with conditions" and configures data sensitivity nudge | System creates policy, schedules user notifications | Confirmation: policy applied, 12 affected users will see compliant-usage nudge within 24 hours |
| 6 | Navigates to Cost Attribution tab | Cost dashboard loads with cross-vendor breakdown | Stacked bar by vendor (AWS Bedrock $48K, Copilot $72K, OpenAI $38K, Others $24K), table by team with per-user drill-down |
| 7 | Returns to Command Center, verifies updated governance % | KPI hero bar refreshes (73% governed, 3→2 active risks) | Updated metrics reflecting the policy action just taken |

### Decision Points

| Decision | Data Required | Design Element |
|----------|--------------|----------------|
| Should this AI tool be approved or blocked? | Tool name, vendor, user count, data sensitivity assessment, cost estimate, comparable approved alternatives | Split-panel tool detail with risk assessment card + "Apply Policy" action button |
| Which team is overspending on AI? | Cost-by-team breakdown, vendor attribution, per-user cost, trend vs. prior period | Cost Attribution dashboard with horizontal bar chart by team, drill-down table |
| Is the organization improving its governance posture? | Maturity score trend, % governed trend, compliance rate over time, number of open risks | Command Center sparklines in hero bar + Maturity tab with 5-level scorecard |
| Should we consolidate redundant AI tools? | Tools with overlapping capabilities, user overlap between tools, cost comparison | AI Inventory with "Duplicate Detection" badge and comparison view in split panel |
| Are governance nudges effective or annoying? | Override rate, nudge acceptance rate, user feedback, compliance trend post-nudge | Governance tab metrics section with override-rate anti-metric prominently displayed |

### Minimum Viable Interaction

**2 clicks from landing to the "aha" moment:**
1. Click "AI Control Tower" in Quick Desktop sidebar navigation → Command Center loads with all KPIs and shadow AI alerts
2. Click any shadow AI alert → full tool detail with governance action options

**3 clicks from landing to governance action:**
3. Click "Apply Policy" → policy applied, users notified

---

## Phase 2: Pattern Reality Check

### Applied Patterns

**Salesforce — Contextual Data Surfacing:** The AI Inventory page follows the Salesforce record-page pattern. Clicking any AI tool opens a split-panel detail view that proactively surfaces related data: users of the tool, cost data, compliance status, similar tools, governance history, and recommended actions. The user never needs to navigate away to find context about a tool — everything related to it appears in the detail panel.

**Datadog — Information Density:** The Command Center hero bar packs five KPIs with sparkline trends into a single row, following Datadog's "maximum signal per pixel" principle. The AI Inventory table uses sparklines-in-table-cells for usage trends (per Datadog's enterprise density rule), allowing Lisa to scan adoption patterns across 50+ tools without opening individual detail views.

**Datadog — Connectedness Rather Than Consistency:** Every data point is a portal. Click a cost number → navigate to Cost Attribution filtered to that tool. Click a team name → see all tools that team uses. Click a risk alert → see the tool, the policy violation, and the affected users. Lateral, data-driven navigation throughout.

**Salesforce — Configuration Over Customization:** Saved views for the AI Inventory (Lisa's "Unapproved Tools" view, David's "Engineering AI Stack" view). Collection Preferences on every table for column visibility and density. Dashboard layout is opinionated by default but configurable per user.

### Layout Rationale

**Command Center as hub, not just a dashboard:** The Command Center exists because Lisa's #1 JTBD is answering the CEO's AI question in under 5 minutes. A hub pattern (KPI hero bar → alert zone → dimension cards linking to sections) is chosen over a blank dashboard builder because (a) Lisa is medium-high technical but not building custom dashboards, (b) the PRD explicitly states "pre-configured and opinionated," and (c) ServiceNow's Command Center pattern is table stakes. The hub earns its place by being the single screen that answers "what's the state of our AI?"

**Split-panel detail over full-page navigation:** The AI Inventory uses a split panel (Cloudscape Split Panel component) rather than navigating to a separate detail page because (a) enterprise users need to compare tools by switching between rows quickly, (b) the Datadog "connectedness" principle says context should never be lost, and (c) Cloudscape's Split Panel is the standard pattern for list-detail in AWS consoles.

**Sidebar navigation over top nav:** Cloudscape App Layout uses sidebar navigation, and all AWS console products follow this pattern. Additionally, the seven-section navigation is too deep for horizontal tabs but fits naturally in a collapsible sidebar.

**Hero KPI bar over separate metrics page:** The five governance dimensions each have a KPI that matters most. Showing all five in a hero bar above the fold means Lisa never needs to navigate to a separate metrics page for the executive summary. This follows the Datadog principle of density — the answer to "how are we doing" is visible in 0 clicks after entering the Control Tower.

### Alternatives Considered

| Decision | Chosen | Alternative A | Alternative B | Why Chosen Wins |
|----------|--------|--------------|--------------|-----------------|
| Information architecture | Hub + section navigation (7 sections in sidebar) | Single-page dashboard with tabs | Wizard-style guided flow | Hub + sections provides both at-a-glance executive summary AND deep-dive capability. Single-page dashboard can't accommodate 7 sections without tab overload. Wizard forces linear flow when Lisa often enters mid-workflow (e.g., from a Slack question). |
| Tool detail pattern | Split panel (side position) | Full-page tool detail | Modal overlay | Split panel preserves list context (see other tools while viewing detail). Full-page loses context. Modal blocks interaction with the underlying page. |
| Command Center layout | Pre-configured opinionated KPI hub | Blank dashboard builder (Grafana-style) | Card grid with drag-and-drop | Lisa doesn't build dashboards — she answers CEO questions. Opinionated defaults serve the 80% case; Cloudscape Collection Preferences handle the 20% customization need. |
| Governance action UX | Inline "Apply Policy" in split panel detail | Separate policy management page | Bulk action toolbar on table | Inline action follows Salesforce's "act where you are" principle. Separate page adds 2+ clicks. Bulk action exists too (for power users), but the primary flow is individual tool governance from the detail panel. |
| Cost visualization | Stacked bar by vendor + table by team | Pie chart by vendor | Treemap by team/tool | Stacked bar handles 5+ vendors without the pie chart > 5 slices anti-pattern. Table provides the drill-down density enterprise users need. Treemap is visually interesting but harder to read precise values. |

### Cloudscape Component Mapping

| UI Element | Cloudscape Component | Notes |
|-----------|---------------------|-------|
| Page shell | App Layout | Side navigation, split panel, content area. Breadcrumbs in header. |
| Primary navigation | Side Navigation | 7 items: Command Center, AI Inventory, Governance, Security, Cost Attribution, Adoption & Maturity, Admin Console. Expandable sections for Integration Marketplace, Compliance Reports, Enforcement. |
| KPI hero bar | Container + Box + Column Layout | 5 stat cards in a row using Box with SpaceBetween. Each card: metric value, label, sparkline, trend indicator. |
| Alert zone | Flashbar | Dismissible alert items for shadow AI discoveries, policy violations, risk alerts. Type: warning/error/info. |
| AI tool table | Table + Collection Preferences + Property Filter | Sortable, filterable, paginated. Columns: tool name, vendor, users, monthly cost, compliance status, risk level, trend sparkline. |
| Tool detail | Split Panel | Side position on L/XL, bottom on M. Tabs inside: Overview, Users, Cost, Compliance, Activity Log. |
| Policy action | Modal (via Button trigger) | Form inside modal: policy type (approve/monitor/block), conditions, notification settings. |
| Cost charts | Container wrapping custom chart HTML | Stacked bar (by vendor), horizontal bar (by team). Chart.js or inline SVG with Cloudscape color tokens. |
| Maturity scorecard | Cards (in Grid layout) | 5 maturity level cards, current level highlighted. Each card: level name, criteria checklist, % progress to next level. |
| Date range selector | Date Range Picker | Global time filter affecting all data views. Presets: Last 7 days, 30 days, 90 days, Custom. |
| Breadcrumbs | Breadcrumb Group | AI Control Tower > [Section] > [Subsection] |
| Page headers | Header | H1 with description, counter badge, action buttons |
| Governance policy table | Table + Collection Preferences | Rows: policy rules. Columns: rule name, scope (org/team/user), AI tools affected, enforcement level, status. |
| Integration cards | Cards (in Grid layout) | Per-connector cards: logo, name, status badge (connected/disconnected/error), user count, last sync. |
| Empty states | Box with illustration | Custom empty-state components per section with CTA and value prop. |
| Notification settings | Form (within Container) | Notification channel, frequency, severity threshold per alert type. |
| Tabs within sections | Tabs | Used inside Command Center (Overview, Trends), AI Inventory (All Tools, Shadow AI, Approved, Blocked). |

---

## Phase 3: Design Checklist + Audits

### 3A. Core Design Checklist

| # | Criterion | Score | Evidence |
|---|-----------|:-----:|----------|
| 1 | Task Clarity | 5 | Primary task (answer CEO's AI question) achievable in 2 clicks: open Control Tower → read hero KPI bar. Governance action (approve/block tool) in 3 clicks. |
| 2 | Information Hierarchy | 5 | Hero KPI bar is the most visually prominent element (largest type, top of page). Shadow AI alerts are second (Flashbar with warning color). Drill-down table is third. Navigation is subordinate in sidebar. |
| 3 | Progressive Disclosure | 4 | Command Center shows summary → click section for detail → click row for split panel → click action for modal. Complexity hidden at each level. Deducted 1 point: advanced policy conditions might need better progressive reveal. |
| 4 | Layout Rationale | 5 | Every layout decision documented with WHY in Phase 2 (hub pattern for CEO-question JTBD, split panel for context preservation, sidebar for 7-section depth, hero bar for zero-click executive summary). |
| 5 | Alternatives Considered | 5 | Five major layout decisions each evaluated against 2+ alternatives with rejection rationale (hub vs. blank dashboard, split panel vs. full page, pre-configured vs. builder, inline action vs. separate page, stacked bar vs. pie chart). |
| 6 | Pattern Consistency | 5 | 100% Cloudscape components. App Layout, Table, Split Panel, Property Filter, Flashbar, Modal, Cards, Tabs — all standard Cloudscape patterns. No custom components that deviate from the design system. |
| 7 | Stickiness | 4 | Morning briefing alert zone creates daily check-in habit. Shadow AI discovery provides ongoing "aha" moments. Maturity score gamification. Nudge override rate creates feedback loop. Deducted 1: could add digest email/notification for off-platform return trigger. |
| 8 | Error States | 4 | Empty states designed per section (empty inventory, no integrations, no policies). Loading skeletons for data fetch. Error Flashbar for API failures. Timeout handling with retry. Deducted 1: partial data states could be more granular. |
| 9 | Expert vs. Novice | 5 | Novice: Command Center hub answers questions visually, 5-stage onboarding, empty states with CTAs. Expert: Property Filter with query syntax, keyboard shortcuts, saved views, collection preferences for density, bulk actions. |
| 10 | Accessibility | 4 | WCAG AA target. Cloudscape components are pre-validated for contrast. ARIA landmarks defined. Keyboard nav spec included. Screen reader announcements defined. Deducted 1: charts need pattern/shape differentiation for colorblind users — specified but needs implementation verification. |

**Checklist Score: 10/10 pass (>= 3)**

### 3B. Nielsen Heuristic Audit

| # | Heuristic | Score | Evidence | Remediation |
|---|-----------|:-----:|----------|-------------|
| H1 | Visibility of System Status | 5 | Hero KPI bar updates on every data refresh. Loading skeletons during fetch. Flashbar notifications for async operations (policy applied, scan complete). Date range picker shows active time window. Last-refreshed timestamp visible. | — |
| H2 | Match Between System and Real World | 4 | Uses Lisa's language: "shadow AI" (not "unclassified assets"), "approved/blocked" (not "allow-listed/deny-listed"), "monthly cost" (not "token consumption"). Five governance dimensions match industry framing. | Minor: ensure all vendor names use common brand names (ChatGPT not "OpenAI API"), maturity levels use plain English. |
| H3 | User Control and Freedom | 4 | Policy actions are reversible (approve → block → approve). Split panel closes with X or Esc. Filters clear with "Clear All" button. Modal has Cancel. Governance nudge dismissal persists. | Minor: add "Undo" toast after policy changes with 10-second reversal window. |
| H4 | Consistency and Standards | 5 | 100% Cloudscape components ensure internal consistency. Table patterns identical across Inventory, Governance, Security sections. Split panel behavior identical everywhere. Follows AWS console conventions. | — |
| H5 | Error Prevention | 4 | Destructive actions (block tool, delete policy) require confirmation modal with impact summary ("This will affect 12 users"). Governance nudge thresholds have sensible defaults. Integration setup validates credentials before saving. | Minor: add "Are you sure?" for bulk policy actions affecting 50+ users. |
| H6 | Recognition Rather Than Recall | 5 | Property Filter shows token suggestions (tool names, vendors, teams). Saved views remember filter state. Breadcrumbs show current location. Side navigation highlights active section. Recently viewed tools shown in Command Center. | — |
| H7 | Flexibility and Efficiency of Use | 4 | Keyboard shortcuts (/ for search, Esc for close panel). Saved views for repeated queries. Collection Preferences for column density. Bulk actions for expert users. | Add: Ctrl+K command palette for quick navigation, recent items list. |
| H8 | Aesthetic and Minimalist Design | 4 | Cloudscape's design system enforces visual discipline. Hero bar shows 5 KPIs (not 15). Table columns are configurable (hide low-value columns). Sparklines replace full charts in table cells for density without clutter. | Minor: Command Center dimension cards could be trimmed from 5 to top 3 on first load, with "Show all" toggle. |
| H9 | Help Users Recognize, Diagnose, and Recover from Errors | 4 | Error Flashbar messages include: what failed, why (plain language), and a retry CTA. Integration errors show "Test Connection" button. Discovery errors show "Retry Scan" option. | Add: error codes with documentation links for IT admins troubleshooting integration failures. |
| H10 | Help and Documentation | 4 | Contextual help icons (?) on complex elements (maturity scoring methodology, cost estimation approach). Onboarding tour for first-time users. Empty states include documentation links. | Add: searchable help panel (Cloudscape Drawer) with FAQ and quick-start guides. |

**Heuristic Score: 10/10 pass (>= 3)**

### 3C. Interaction State Matrix

| Element | Default | Hover | Pressed/Active | Focus (keyboard) | Disabled |
|---------|---------|-------|----------------|-------------------|----------|
| Primary button ("Apply Policy") | `$color-background-button-primary-default`, white text, 2px border-radius, cursor:default | `$color-background-button-primary-hover`, white text, cursor:pointer | `$color-background-button-primary-active`, white text, scale(0.98) | `$color-background-button-primary-default` + 2px `$color-border-control-focus` outline offset 2px, cursor:default | `$color-background-button-primary-disabled`, `$color-text-button-primary-disabled`, cursor:not-allowed, opacity:1 |
| Table row | `$color-background-container-content`, `$color-text-body-default` | `$color-background-dropdown-item-hover`, cursor:pointer | `$color-background-item-selected`, `$color-border-item-selected` left border, `$color-text-body-default` | `$color-background-container-content` + 2px `$color-border-control-focus` outline, cursor:default | `$color-text-status-inactive`, cursor:not-allowed |
| Filter chip (Property Filter token) | `$color-background-badge-icon`, `$color-text-body-default`, pill shape | `$color-background-dropdown-item-hover`, cursor:pointer | `$color-background-item-selected`, border highlight | 2px `$color-border-control-focus` outline | `$color-background-input-disabled`, `$color-text-status-inactive` |
| Navigation link (sidebar) | `$color-text-body-default`, no background | `$color-background-dropdown-item-hover` | `$color-background-item-selected`, `$color-border-item-selected` left bar, `$color-text-link-primary-default` | 2px `$color-border-control-focus` outline | N/A (nav items are never disabled, hidden instead) |
| Split panel toggle (row click) | N/A (triggered by table row click) | See table row hover state | Split panel slides in, row gets selected state | Via table row focus → Enter triggers panel | N/A |
| Tab | `$color-text-body-default`, transparent background, bottom border:none | `$color-text-link-primary-hover`, cursor:pointer | `$color-text-link-primary-default`, 2px bottom border `$color-border-tab-active` | 2px `$color-border-control-focus` outline | `$color-text-status-inactive`, cursor:not-allowed |
| Date range picker trigger | `$color-background-input-default`, `$color-border-control-default`, `$color-text-body-default` | `$color-border-control-hover` | `$color-border-control-focus`, dropdown opens | `$color-border-control-focus` 2px outline | `$color-background-input-disabled`, `$color-text-status-inactive` |
| Icon button (help ?, close X) | `$color-text-interactive-default`, transparent background | `$color-background-dropdown-item-hover`, `$color-text-interactive-hover` | `$color-text-interactive-active`, scale(0.95) | 2px `$color-border-control-focus` outline | `$color-text-status-inactive`, cursor:not-allowed |
| Toggle (dark mode) | Track: `$color-background-toggle-default`; thumb: white; label: `$color-text-body-default` | Track: `$color-background-toggle-hover` | Track: `$color-background-toggle-checked-default`; thumb slides right | 2px `$color-border-control-focus` outline around track | Track: `$color-background-toggle-disabled`; cursor:not-allowed |
| Alert dismiss button (Flashbar) | `$color-text-interactive-default`, transparent | `$color-background-dropdown-item-hover` | `$color-text-interactive-active`, flash removed with fade-out | 2px `$color-border-control-focus` outline | N/A (dismiss always available) |

### 3D. Keyboard Navigation Spec

**Tab Order (Command Center page):**
1. Skip to main content link → main content area
2. Side navigation items (7 sections) → vertical arrow key navigation within
3. Date range picker → opens on Enter/Space
4. Hero KPI cards (5) → arrow keys between cards, Enter to drill into section
5. Flashbar alert items → Tab between alerts, Enter to view detail, Delete/Backspace to dismiss
6. Dimension summary cards → Tab between cards, Enter to navigate to section
7. Recent activity table → Tab to table, then arrow keys for row navigation
8. Split panel (if open) → Tab cycles through panel tabs, panel content, close button

**Keyboard Shortcuts:**

| Shortcut | Action | Scope | Conflict Check |
|----------|--------|-------|----------------|
| `/` or `Ctrl+K` | Focus global search / property filter | Global | No conflict — standard web pattern |
| `Esc` | Close split panel / modal / drawer | Contextual | Standard |
| `Enter` | Activate focused element / open split panel for focused row | Universal | Standard |
| `Arrow Up/Down` | Navigate table rows / navigation items | Within component | Standard |
| `Arrow Left/Right` | Navigate tabs / KPI cards | Within component | Standard |
| `Ctrl+Enter` | Submit / apply filters | Within filter | No conflict |
| `?` (Shift+/) | Open help drawer | Global | No conflict with browser |
| `g then c` | Go to Command Center | Global (vim-style) | No conflict |
| `g then i` | Go to AI Inventory | Global (vim-style) | No conflict |
| `g then g` | Go to Governance | Global (vim-style) | No conflict |

**Focus Management Rules:**
- When modal opens: focus moves to first focusable element (usually modal title or first form field). Modal traps focus — Tab cycles within modal only.
- When split panel opens: focus moves to panel heading. Split panel does NOT trap focus — Tab can leave panel back to main content.
- When split panel closes (via X or Esc): focus returns to the table row that triggered it.
- When Flashbar alert is dismissed: focus moves to next alert item, or to main content if no alerts remain.
- On page load / route change: announce page title via `aria-live="polite"`, focus moves to `<h1>`.
- Skip links: "Skip to main content" (bypasses sidebar nav), "Skip to results" (bypasses KPI bar and alerts, lands on primary table).

### 3E. Anti-Pattern Validation

| # | Anti-Pattern | Status | Notes |
|---|-------------|--------|-------|
| 1 | Mystery meat navigation (icons without labels) | Absent | Side navigation uses text labels for all 7 sections. Icons accompany labels but never replace them. Collapsed sidebar (M breakpoint) uses icon+tooltip, not icon alone. |
| 2 | Infinite scroll without progress indicator | Absent | All tables use pagination (Cloudscape Table pagination). Page count and total items displayed. |
| 3 | Hamburger menu hiding primary navigation | Absent | Sidebar nav is always visible on L/XL breakpoints. On S/XS, collapsed but accessible via hamburger — acceptable for mobile as standard responsive pattern, with all items immediately visible on expand. |
| 4 | Modal on top of modal (nested modals) | Absent | Design enforces single-modal rule. Policy action modal is the only modal surface; any secondary choices use inline expandable sections within the modal, not nested modals. |
| 5 | Confirm-shaming (guilt-trip copy on cancel buttons) | Absent | Cancel buttons use neutral "Cancel" label. No "No, I don't want to govern my AI" type copy. |
| 6 | Pagination that loses scroll position | Absent | Cloudscape Table pagination preserves scroll position. Page navigation does not reset scroll. |
| 7 | Auto-playing content without user initiation | Absent | No auto-playing animations, videos, or carousels. Sparklines render statically. Data refreshes on user action or configurable auto-refresh interval (default: manual). |
| 8 | Ambiguous destructive actions (delete without confirmation) | Absent | All destructive actions (block tool, delete policy, remove integration) require confirmation modal with impact summary. |
| 9 | Truncated content with no way to see full text | Absent | Long tool names truncate with ellipsis and show full name on hover tooltip. Table cells with truncated content show full text in split panel detail. |
| 10 | Ghost buttons for primary actions (low-contrast CTAs) | Absent | Primary actions use Cloudscape Primary Button (high contrast, filled). Secondary actions use Cloudscape Normal Button. No ghost buttons for important actions. |
| 11 | Data table without sortable columns | Absent | All table columns are sortable. Default sort: risk level (descending) for Security, cost (descending) for Cost Attribution, name (ascending) for AI Inventory. |
| 12 | Time-based UI without timezone clarity | Absent | All timestamps display in user's local timezone with "(UTC-5)" or equivalent suffix. Date range picker shows timezone. Governance activity log shows absolute timestamps with timezone. |
| 13 | Search with no empty-result guidance | Absent | Property Filter empty results show: "No tools match your filter" with suggestions: "Try removing filters" and "Check if the Discovery Engine has completed its scan." |
| 14 | Settings that require page reload to take effect | Absent | All settings apply immediately via API call with optimistic UI update. Policy changes propagate with a Flashbar confirmation ("Policy updated — changes will reach user devices within 24 hours"). |

### 3F. Data Visualization Decision Matrix

| Data Point | Viz Chosen | Why | Alternative | Why Rejected |
|-----------|-----------|-----|------------|--------------|
| Total AI tools discovered (KPI) | Stat card with sparkline | Single KPI — stat card is the canonical pattern. Sparkline shows 30-day trend without dedicating a full chart. | Counter only | No trend context; a number alone doesn't show direction. |
| % AI tools governed (KPI) | Stat card with gauge arc | Percentage metric — gauge arc conveys progress toward 100% goal intuitively. | Stat card with sparkline | Gauge better communicates "progress toward target" than a line for percentage metrics. |
| Monthly AI spend (KPI) | Stat card with sparkline | Dollar amount over time — sparkline shows spend trend compactly. | Bar chart | Too much space for a single aggregate metric. |
| AI spend by vendor | Stacked bar chart (vertical, 5 vendors) | Categorical composition — stacked bar shows both total and per-vendor contribution. ≤5 vendors = vertical stacked bar works. | Pie chart | Pie chart difficult to compare similar-sized segments; stacked bar enables precise reading. |
| AI spend by team | Horizontal bar chart | Categorical comparison with 10+ teams — horizontal bar handles long team names and >7 categories. | Vertical bar | Team names truncate in vertical bar x-axis labels; horizontal is more readable for many categories. |
| Tool usage trend (per-tool) | Sparkline in table cell | Datadog density rule: sparklines-in-table-cells for correlated scanning. Each row gets a usage sparkline. | Separate line chart per tool | 50+ separate charts is unreadable; sparklines in table enable pattern recognition at a glance. |
| Maturity distribution across teams | Horizontal stacked bar (5 levels) | Shows composition of maturity levels across teams — composition/proportion → stacked bar. | Donut chart | Donut works for one team; stacked bar compares across multiple teams simultaneously. |
| Risk alerts over time | Line chart (area fill) | Time-series trend for monitoring risk alert volume over time. Area fill emphasizes cumulative impact. | Bar chart | Bars obscure continuous daily trend in risk data. |
| Compliance rate trend | Line chart | Time-series trend — clean line shows whether compliance is improving. | Area chart | Area implies cumulative/volume which doesn't apply to a percentage rate. |
| Tool inventory (all tools) | Table with sort/filter | >5 columns of structured data per tool — table is the only appropriate pattern. Table supports sort, filter, pagination. | Card grid | Cards waste space for data-dense records; table is 3-5x more space-efficient for enterprise users. |
| Policy violations by type | Horizontal bar (ranked) | Showing rank/top-N violation types — horizontal bar with rank ordering. | Pie chart | Anti-pattern: pie with >5 slices. |
| Discovery source breakdown | Donut chart (3 segments) | Composition with exactly 3 sources (desktop detection, vendor API, manual) — donut appropriate for ≤5 slices. | Stacked bar | Overkill for 3 categories; donut is simpler and more intuitive for simple composition. |

### 3G. Micro-Interaction Spec

| Interaction | Trigger | Animation | Duration | Easing | Purpose |
|------------|---------|-----------|----------|--------|---------|
| Split panel open | Click table row / detail link | Slide in from right (translateX(100%) → translateX(0)) | 200ms | ease-out | Reveal detail without losing list context |
| Split panel close | Click X / press Esc | Slide out to right (translateX(0) → translateX(100%)) | 150ms | ease-in | Quick exit, return focus to trigger row |
| Tab switch | Click tab | Fade content swap (opacity:0 → opacity:1) | 100ms | ease-in | Fast, no layout shift |
| Modal open | Click action button | Fade in (opacity:0 → opacity:1) + scale(0.95 → 1) + backdrop fade | 200ms | ease-out | Draw focus, indicate overlay |
| Modal close | Click X / Esc / Cancel / backdrop | Fade out (opacity:1 → opacity:0) + backdrop fade | 150ms | ease-in | Quick exit, return focus |
| Filter apply | Click Apply / press Enter | Table body fades (opacity:0.5) during data load, then fades back (opacity:1) | 150ms fade + data load time | ease-in-out | Signal results are updating |
| Flashbar notification appear | System event (discovery, policy change) | Slide in from top (translateY(-100%) → translateY(0)) | 300ms | cubic-bezier(0.34, 1.56, 0.64, 1) | Attract attention without blocking work |
| Flashbar notification dismiss | Click dismiss / auto-timeout | Fade out + collapse height (height → 0, opacity → 0) | 200ms | ease-in | Smooth removal, no layout jump |
| Loading state | Data fetch begins | Skeleton screen replaces content (pulse animation on gray blocks) | Immediate swap, pulse: 1.5s loop | ease-in-out (pulse) | Preserve layout, indicate progress |
| KPI sparkline load | Data arrives | Draw-in from left (stroke-dashoffset animation) | 400ms | ease-out | Visual interest, draw attention to trend |
| Sidebar nav hover | Mouse enter nav item | Background color fade to hover state | 100ms | ease-in | Responsive feedback |
| Policy action confirm | Click "Apply" in modal | Button shows spinner → success checkmark → modal closes | 200ms spinner, 300ms check, 150ms close | ease-out | Confirm action completed before modal disappears |
| Page transition | Click sidebar nav item | Current content fades out, new content fades in | 100ms out + 100ms in | ease-in-out | Smooth, no layout shift |

**Rules enforced:**
- No animation > 400ms (except skeleton pulse loop which is a loading indicator, not a transition).
- All animations use CSS transitions, no JS animation libraries.
- Loading states use skeleton screens, never spinners (except inline button spinners for short async actions).
- No layout shift during transitions — elements do not reflow.
- All animations respect `prefers-reduced-motion: reduce` — if set, instant swaps replace all transitions.

### 3H. Responsive Breakpoint Specs

| Component / Region | XL (>= 1600) | L (1200-1599) | M (992-1199) | S (688-991) | XS (< 688) |
|-------------------|---------------|---------------|--------------|-------------|-------------|
| App Layout navigation | Side nav expanded (text + icons) | Side nav expanded (text + icons) | Side nav collapsed (icons only + tooltip on hover) | Side nav hidden, hamburger menu | Side nav hidden, hamburger menu |
| Split panel | Side position, 400px width | Side position, 360px width | Bottom position, 50% height | Bottom position, collapsed by default | Hidden; "View detail" navigates to full-page detail view |
| Hero KPI bar | 5 cards in single row | 5 cards in single row | 3 cards in row 1, 2 in row 2 | 2 cards per row (3 rows) | 1 card per row (stacked), compact variant |
| AI Inventory table | All 8 columns visible | All 8 columns visible | Hide: trend sparkline, discovery source (6 columns) | Hide: trend, source, risk level (5 columns) | Card view replaces table — one card per tool |
| Property filter | Full inline, all tokens visible | Full inline, all tokens visible | Compact — collapsed advanced options | Full-width stacked above table | Full-width stacked, simplified to search bar + dropdown |
| Cost attribution charts | Side-by-side (vendor bar + team bar) | Side-by-side | Stacked vertically | Stacked vertically, reduced labels | Sparklines only, table with key metrics |
| Maturity scorecard | 5 cards in single row | 5 cards in single row | 3 + 2 row layout | 2 + 2 + 1 row layout | Vertical stack, 1 card per row |
| Date range picker | Inline in header bar | Inline in header bar | Dropdown trigger in header | Dropdown trigger, full-width picker on open | Full-width picker, separate screen |
| Flashbar alerts | Full-width, multi-line allowed | Full-width, multi-line allowed | Full-width, single-line with "Show more" | Full-width, single-line truncated | Full-width, stacked vertically |
| Governance policy table | All 6 columns | All 6 columns | 4 columns (hide: affected tools count, last modified) | 3 columns (name, enforcement, status) | Card view |

**Enterprise note:** Quick Desktop AI Control Tower is primarily used on L and XL breakpoints (desktop IT admin workstation). L is the optimization target. M is graceful degradation for laptop screens. S and XS provide usable access for on-the-go checks from tablets/phones but are not the primary use case.

### 3I. Accessibility Depth

**ARIA Landmarks:**

| Landmark | Element | Role | Label |
|----------|---------|------|-------|
| Main content | `<main>` | `main` | AI Control Tower |
| Navigation | `<nav>` (sidebar) | `navigation` | AI Control Tower navigation |
| Search | Property filter bar | `search` | Filter AI tools |
| Complementary | Split panel | `complementary` | Tool detail panel |
| Banner | Page header with breadcrumbs | `banner` | AI Control Tower header |
| Alert region | Flashbar container | `alert` (with `aria-live="polite"`) | Notifications |

**Focus Management Rules:**
- On page load: focus goes to `<h1>` (page title). Screen reader announces page name.
- On route change (sidebar nav click): announce new page title via `aria-live="polite"` region, move focus to new `<h1>`.
- On filter apply: announce result count ("[N] AI tools match your filter") via `aria-live="polite"`.
- On error: announce error message via `aria-live="assertive"`, move focus to Flashbar error.
- On split panel open: move focus to panel heading. On close: return focus to trigger row.
- On modal open: move focus to modal title. On close: return focus to trigger button.
- On Flashbar alert arrive: announce via `aria-live="polite"` ("New alert: [summary]"). Do not steal focus.

**Screen Reader Announcements:**

| Event | Announcement | Priority |
|-------|-------------|----------|
| Data loading | "Loading AI tool inventory" | polite |
| Data loaded | "[N] AI tools loaded" | polite |
| Filter applied | "[N] tools match your filter" | polite |
| Error occurred | "Error: [message]. Retry available." | assertive |
| Tool selected | "[Tool name] selected, detail panel open" | polite |
| Policy applied | "Policy applied to [tool name]. [N] users affected." | polite |
| Shadow AI discovered | "New shadow AI detected: [tool name] used by [team]" | polite |
| Destructive action confirm | "Are you sure? This will block [tool name] for [N] users." | assertive |

**Color and Contrast:**
- All text meets WCAG AA: 4.5:1 for normal text, 3:1 for large text (Cloudscape design tokens pre-validated).
- Status indicators never rely on color alone: risk levels use icon + text label (🔴 Critical, 🟡 Medium, 🟢 Low) rendered as Cloudscape StatusIndicator component with both color and text.
- Charts use Cloudscape color tokens AND pattern fills (diagonal lines, dots, crosshatch) for colorblind accessibility.
- Focus indicators use 2px solid outline with `$color-border-control-focus` — visible on all backgrounds.

### 3J. Wayfinding & Navigation

**Breadcrumb Spec:**
```
AI Control Tower > [Section Name] > [Subsection/Tab]
```
- Breadcrumbs always visible in page header (Cloudscape Breadcrumb Group).
- Every segment except current page is a clickable link.
- On XS/S: truncate to last 2 segments with "..." overflow showing full path on tap.

**Page Location Indicators:**
- Active sidebar nav item highlighted with `$color-border-item-selected` left bar and `$color-background-item-selected` background.
- Page `<title>` follows: `[Current Page] - AI Control Tower - Quick Desktop`
- URL reflects current state for deep-linking (see below).

**Deep-Link Strategy:**

| State | URL Parameter | Example |
|-------|--------------|---------|
| Active section | `/ai-control-tower/[section]` | `/ai-control-tower/inventory` |
| Active tab | `?tab=[tab-id]` | `?tab=shadow-ai` |
| Applied filter | `?filter=[encoded]` | `?filter=vendor%3DOpenAI` |
| Selected tool | `?selected=[tool-id]` | `?selected=chatgpt-plus-marketing` |
| Time range | `?start=[ts]&end=[ts]` | `?start=2026-04-20&end=2026-05-20` |
| Split panel open | `?detail=[tool-id]` | `?detail=jasper-ai-marketing` |
| Maturity level focus | `?level=[1-5]` | `?level=3` |

Every meaningful UI state is deep-linkable. Lisa shares URLs in Slack ("look at this shadow AI tool"), pastes in runbook documentation, and bookmarks her "Unapproved Tools" filter view. If a state can't be linked, it's a broken workflow.

**Navigation Hierarchy:**
- **Primary:** Cloudscape Side Navigation — 7 sections (persistent, collapsible)
- **Secondary:** Cloudscape Tabs within content area (e.g., AI Inventory tabs: All, Shadow AI, Approved, Blocked)
- **Tertiary:** Segmented control for view variants (e.g., Cost Attribution: By Vendor / By Team / By Tool)
- Never more than 3 navigation levels without breadcrumbs (enforced by breadcrumb spec above).

### 3K. First-Time User Experience

**Progressive Onboarding Flow:**

| Stage | Trigger | What User Sees | Goal |
|-------|---------|---------------|------|
| 1. Empty state | First visit, no integrations connected | Illustrated empty Command Center: "Welcome to AI Control Tower" hero with value prop ("Discover every AI tool your organization uses"), 3-step setup wizard CTA (Connect integrations → Enable desktop detection → Set first policy), link to documentation. | Connect first integration and enable discovery. |
| 2. Discovery in progress | First integration connected, scan running | Command Center shows progress bar: "Scanning your organization... Found 12 tools so far." KPI hero bar populates incrementally. "Next step" banner: "Enable desktop detection to find shadow AI." | Build anticipation; show immediate value; guide to next step. |
| 3. First results | Discovery complete, data populated | Optional tooltip walkthrough (5 steps): (1) Hero KPI bar, (2) Shadow AI alerts, (3) Click a tool for detail, (4) Apply a policy, (5) Check Cost Attribution. Dismissible, re-triggerable from Help menu. | Show the full governance workflow end-to-end. |
| 4. Feature discovery | After 1 week of use | Subtle dot indicators on un-visited sidebar sections. "Did you know?" contextual tips on unused features (e.g., first visit to Maturity tab: "Your organization is at Level 2 — here's how to reach Level 3"). | Expand usage breadth beyond Command Center and Inventory. |
| 5. Power user | Regular usage (2+ weeks) | Keyboard shortcut hints appear on hover (e.g., hover over search bar shows "Tip: Press / to focus"). Saved view suggestions ("You filter by 'unapproved' often — save this view?"). Collection Preferences prompt for table density. | Increase efficiency for returning users. |

**Empty State Design (per section):**

- **Command Center (no data):** Illustration of a radar scanning for AI tools. Headline: "Your AI radar is ready." Body: "Connect your first integration to start discovering AI tools across your organization." CTA: "Connect Integration" (primary), "Learn More" (link). Shows what the dashboard will look like when populated (ghost/skeleton version of KPIs).
- **AI Inventory (no tools):** Illustration of an empty magnifying glass. Headline: "No AI tools discovered yet." Body: "Once the Discovery Engine runs, this table will show every AI tool in use — including shadow AI you didn't know about." CTA: "Run Discovery Scan" (primary), "Import tools manually" (secondary).
- **Governance (no policies):** Illustration of a shield outline. Headline: "No governance policies configured." Body: "Set your first policy to start governing AI usage. We recommend starting with an approved tool list." CTA: "Create First Policy" (primary), "Use recommended defaults" (secondary).
- **Cost Attribution (no cost data):** Illustration of a calculator. Headline: "No cost data available yet." Body: "Connect vendor admin APIs to see cross-vendor AI spend. Supported: AWS Bedrock, M365 Copilot, OpenAI." CTA: "Connect Billing Source" (primary).
- **Integrations (none connected):** Card grid showing available connectors (AWS, M365, OpenAI) with "Connect" buttons and estimated setup time per connector.

**Onboarding Dismissal:**
- All onboarding elements (tooltips, banners, dot indicators) can be permanently dismissed.
- Dismissal state persists in user preferences (stored via Quick Desktop's user settings API).
- "Getting Started" link in the Help menu (Cloudscape Help Panel) lets users re-trigger the onboarding tour.

**Enterprise FTUX approach:** Emphasis on competence, not delight. Configuration options visible from step 1. Documentation links prominent. Assume Lisa is skilled but unfamiliar with THIS product's specific workflow.

---

## Product Navigation Map

| # | Page/Section | Nav Label | Nav Icon | Proto v1 State | Eng v1 State | Competitor Precedent |
|---|-------------|-----------|----------|---------------|-------------|---------------------|
| 1 | Command Center | Command Center | Dashboard icon | Full — KPI hero bar, alert zone, dimension cards, recent activity | Full | ServiceNow: Dashboard hub; Datadog: Overview dashboard |
| 2 | AI Tool Inventory | AI Inventory | Search/magnifying glass icon | Full — table with split-panel detail, shadow AI tab, approved/blocked tabs | Full | ServiceNow: Discover pillar; Datadog: Traces list |
| 3 | Governance Policies | Governance | Shield icon | Full — policy table, create/edit policy, nudge configuration, compliance rate | Full | ServiceNow: Govern pillar |
| 4 | Security & Risk | Security | Lock icon | Full — risk alerts table, data sensitivity heatmap, threat detail panel | Full | ServiceNow: Secure pillar; Splunk: AI Defense |
| 5 | Cost Attribution | Cost Attribution | Dollar sign icon | Full — vendor breakdown chart, team breakdown chart, per-tool cost table | Full | ServiceNow: Measure pillar (cost); Datadog: per-token cost |
| 6 | Adoption & Maturity | Adoption | Chart-trending-up icon | Full — 5-level maturity scorecard, team comparison, adoption trend charts | Full | ServiceNow: Measure pillar (adoption). No competitor has maturity scoring. |
| 7 | Admin Console | Admin | Gear icon | Full — integration management, notification settings, team/user management, data retention config | Full | ServiceNow: Admin; Datadog: Integrations settings |
| 8 | Integration Marketplace | Integrations (sub-nav under Admin) | Puzzle piece icon | Placeholder — connector catalog cards with "Connect" for top 3, "Coming Soon" for 10+ others with logos and descriptions | Eng v1: top 3 connectors only | ServiceNow: 30+ integrations marketplace |
| 9 | Compliance Reports | Reports (sub-nav under Governance) | Document icon | Placeholder — report template previews with "Generate" button (mock export), sample report PDF preview | Not in Eng v1 | ServiceNow: Compliance frameworks |
| 10 | Enforcement Rules | Enforcement (sub-nav under Governance) | Shield-check icon | Placeholder — enforcement rule builder with nudge/block/kill switch toggles, sample policy rule visualization | Eng v1: simplified rules only | ServiceNow: Kill switches, real-time enforcement |
| 11 | AI ROI Insights | ROI Insights (sub-nav under Adoption) | Lightbulb icon | Placeholder — mock productivity correlation cards ("Teams using ChatGPT complete reports 40% faster"), sample data layout | Not in Eng v1 | ServiceNow: Measure pillar (just launched) |
| 12 | Policy Templates | Templates (sub-nav under Governance) | Template icon | Placeholder — NIST AI RMF, EU AI Act, SOC 2 template cards with "Apply Template" buttons, template detail preview | Not in Eng v1 | ServiceNow: 5 NIST/EU AI Act frameworks |
| 13 | Activity Audit Log | Audit Log (sub-nav under Admin) | List icon | Full — governance action log with timestamp, user, action, target, filterable | Full | ServiceNow: Activity log |

**Completeness check:** 13 navigation sections (7 primary + 6 sub-navigation). ServiceNow's AI Control Tower has 5 pillars + dashboard + admin + integrations = ~8 primary sections. Datadog's LLM Observability has ~6 sections. Our 13 sections (7 primary in sidebar + 6 sub-nav items) exceeds both competitors' navigation surface. Proto v1 has 8 fully functional pages + 5 placeholder pages = 13 total navigable pages.

---

## 5-Minute Demo Script

| Step | Time | Page | Action | What to Say | Why It Matters |
|------|------|------|--------|-------------|----------------|
| 1 | 0:00 | Command Center | Land on AI Control Tower | "This is your AI operations cockpit — everything about your organization's AI starts here." | Sets context, establishes the "cockpit, not control tower" positioning. Shows this is a product, not a feature. |
| 2 | 0:20 | Command Center | Point to hero KPI bar | "At a glance: 247 AI tools discovered, $182K monthly spend across 5 vendors, 72% governed, maturity level 3. This is the answer to the CEO's question — no more 2-week investigations." | Demonstrates immediate executive-level value. Addresses JTBD #1 directly. |
| 3 | 0:40 | Command Center | Point to shadow AI alerts | "These are tools our Discovery Engine found that IT didn't know about — 4 new shadow AI tools in the last week. That's the 82% problem in action." | The "aha" moment. Shows discovery capability and the urgency it creates. |
| 4 | 1:00 | AI Inventory | Click nav → AI Inventory | "Let's drill into what AI we actually have. This is every AI tool in the organization — shadow and sanctioned — with usage, cost, and risk per tool." | Shows the full discovery breadth. Enterprise data density. |
| 5 | 1:20 | AI Inventory | Click "Shadow AI" tab | "I can filter to just shadow AI — 23 unapproved tools across 8 teams. Marketing has 6 alone." | Shows the governance gap in concrete terms. |
| 6 | 1:40 | AI Inventory | Click "Jasper AI" row → split panel opens | "Click any tool for the full picture: 12 users, $2.4K/month estimated, no governance policy, medium data risk. And here's the action — I can approve, monitor, or block it right here." | Shows data depth per entity AND governance action in context. The split-panel pattern. |
| 7 | 2:10 | AI Inventory → Governance | Click "Apply Policy" → configure → confirm | "I'll approve Jasper with a data sensitivity nudge — users will get a gentle reminder when pasting sensitive data. Not a block; a guide." | Demonstrates the "cockpit" governance model — guide, don't just block. Key differentiator. |
| 8 | 2:40 | Governance | Navigate to Governance page | "Here's where I manage all governance policies. Approved tools, blocked tools, nudge rules, and compliance rate — 72% and climbing." | Shows governance as a managed system, not ad-hoc decisions. |
| 9 | 3:00 | Cost Attribution | Navigate to Cost Attribution | "Now the CFO's question: what are we spending? $182K/month across AWS Bedrock, Copilot, OpenAI, and others. Broken down by team — Engineering is $68K, Marketing is $31K. Per-tool, per-team, per-vendor." | Addresses JTBD #3. Cross-vendor cost visibility that no one else offers. |
| 10 | 3:30 | Adoption & Maturity | Navigate to Adoption & Maturity | "This is what nobody else shows you: your AI maturity score. We're at Level 3 — Adopting. Here's exactly what we need to do to reach Level 4: improve cost attribution coverage to 80% and enforce policies on all shadow AI." | Prescriptive maturity model — unique differentiator. Answers "what should we do next?" |
| 11 | 4:00 | Integration Marketplace | Navigate to Admin → Integrations | "We have 3 vendor integrations live today — Bedrock, Copilot, OpenAI. Coming soon: Anthropic, Google, Jasper, and 10+ more. One marketplace, all your AI vendors." | Shows the vision — cross-vendor is the moat. Placeholder pages demonstrate roadmap credibility. |
| 12 | 4:30 | Command Center | Return to Command Center | "Full circle — from that CEO question to governed AI in under 5 minutes. Discover, govern, measure, optimize. All from the same desktop agent your employees already use." | Ties the narrative together. Reinforces the "cockpit" positioning and the product loop. |

**Script quality test:** Reading the "What to Say" column top-to-bottom tells a coherent product story: discover what AI exists → see the shadow AI problem → drill into specific tools → take governance action → manage policies → understand costs → measure maturity → see the integration vision → full circle. This is a product narrative (discover → understand → govern → measure → optimize), not a feature list.

**Demo touches 7 different pages/sections** (Command Center, AI Inventory, Governance, Cost Attribution, Adoption & Maturity, Integration Marketplace, back to Command Center), exceeding the minimum 4-page requirement.

---

## Stickiness Design

**Daily Habit Loop:**
1. **Trigger:** Morning notification from Quick Desktop: "AI Control Tower: 2 new shadow AI tools detected overnight. 1 policy violation alert." (Leverages Quick Desktop's proactive notification system.)
2. **Action:** Open Command Center → scan hero KPIs and alert zone (10 seconds).
3. **Variable Reward:** Shadow AI discoveries create curiosity ("what did my teams adopt now?"). Governance % increasing creates progress satisfaction. New risk alerts create urgency.
4. **Investment:** Each policy configured, each tool approved/blocked increases switching cost. Governance history builds institutional memory that's expensive to replicate elsewhere.

**Weekly Return Triggers:**
- Monday morning digest: "Last week: 3 new tools discovered, compliance improved 2%, AI spend up $4K. Your maturity score: unchanged at Level 3."
- Governance nudge effectiveness report: "Your nudges were accepted 73% of the time this week. Top accepted: data sensitivity nudge on ChatGPT."

**Monthly Return Triggers:**
- Executive summary auto-generated for Lisa's CEO report: pre-formatted AI governance summary exportable as PDF.
- Maturity advancement notification: "Congratulations — Engineering team reached Level 4 (Optimizing)."

**Switching Cost Amplifiers:**
- Governance policy library grows over time — recreating policies in another tool is days of work.
- Historical trend data (adoption curves, cost trends, compliance trajectory) creates irreplaceable longitudinal value.
- Integration configurations (API keys, team mappings, notification rules) are investment that doesn't transfer.

---

## Error & Edge States

| State | Design Treatment |
|-------|-----------------|
| Empty state (no data) | Illustrated empty state per section (see FTUX section 3K). Each includes: what page will show when populated, why it's empty, primary CTA to fix it, documentation link. Never a blank page or generic "No data" message. |
| Error state (API failure) | Flashbar error at top of affected section: "Unable to load [data type]. [Plain language reason]. [Retry button]." Stale data stays visible with a "Data from [timestamp]" badge rather than replacing content with an error screen. |
| Loading state | Skeleton screen matching the final layout (gray pulsing blocks in place of KPIs, table rows, charts). Preserves spatial layout so no layout shift when data arrives. Never spinners (Cloudscape pattern). |
| Partial data (some integrations connected, others not) | Dashboard shows available data with "Connect [vendor] to see [data type]" inline prompts where data is missing. Cost Attribution shows connected vendors' data with "Connect OpenAI to see remaining $38K spend" prompt. |
| Timeout (slow API response > 5s) | After 5s: skeleton screen adds "Taking longer than expected..." text. After 15s: timeout error with retry button. Background data fetch continues — if data arrives after timeout message, it replaces the error automatically. |
| Permission denied | Inline message: "You don't have permission to [action]. Contact your Quick Desktop admin to request [specific permission]." Never a generic 403 page. |
| Discovery in progress | Animated progress indicator in Command Center: "Discovery scan in progress... [X] tools found so far. Estimated completion: [time]." Partial results display as they arrive. |
| Integration disconnected | Integration card shows "Disconnected" badge in red. Affected data in dashboard shows "[Vendor] data unavailable — reconnect integration" inline where vendor data would appear. |
| Stale data (> 24h since last refresh) | Yellow warning banner: "Data last refreshed [timestamp]. Some information may be outdated. [Refresh now] button." Does not block access to existing data. |

---

## Handoff Notes for Prototype Builder

**Key interactions to implement (priority order):**
1. Sidebar navigation between all 13 pages (7 primary + 6 sub-nav). Every page must be reachable.
2. Command Center hero KPI bar with 5 stat cards (static mock data, no sparkline animation needed in prototype).
3. AI Inventory table with sort (click column headers), filter (property filter with vendor/team/status tokens), pagination (10 per page), and row click → split panel.
4. Split panel with tabbed detail view (Overview, Users, Cost, Compliance tabs) showing realistic mock data per tool.
5. "Apply Policy" modal triggered from split panel — form with radio buttons (Approve/Monitor/Block) and confirmation.
6. Tab switching on AI Inventory (All / Shadow AI / Approved / Blocked) filtering the table.
7. Cost Attribution page with mock charts (stacked bar by vendor, horizontal bar by team).
8. Maturity scorecard with 5 level cards (current level highlighted).
9. Dark mode toggle in top-right corner.

**Responsive behavior:** Optimize for L breakpoint (1200-1599px). Split panel side position. Sidebar expanded.

**Mock data requirements:**
- 15-20 AI tools across 5 vendors (AWS Bedrock, Microsoft Copilot, OpenAI ChatGPT, Anthropic Claude, Jasper AI) and 6 teams (Engineering, Marketing, Sales, Finance, Legal, HR).
- Realistic names, costs, user counts, risk levels. Shadow AI tools (unapproved) should make up ~30% of inventory.
- 5-6 governance policies (varying enforcement levels).
- Cost data: total ~$182K/month distributed across vendors and teams.

**Placeholder pages:** Integration Marketplace, Compliance Reports, Enforcement Rules, AI ROI Insights, Policy Templates — each needs sidebar nav entry, page header, realistic content preview with "Coming Soon" elements where appropriate. These are NOT blank pages.

**Keyboard shortcuts:** Implement / for search focus and Esc for split panel close at minimum.

---

## Feedback to PRD

### Assumptions Made Where PRD Was Ambiguous

1. **Navigation structure:** PRD mentions "a dedicated section within Quick Desktop" but doesn't specify navigation architecture. Design assumes a sidebar navigation within the AI Control Tower section (not tabs), with 7 primary sections + 6 sub-sections, matching enterprise console patterns.

2. **Governance action flow:** PRD describes "approve, monitor, or block" but doesn't specify the UX for applying policies. Design assumes an inline action model (act from the tool detail panel) rather than a separate policy management workflow. Both exist but inline is the primary flow.

3. **Cost estimation UX:** PRD mentions "estimates costs from usage patterns" for vendors without cost APIs. Design assumes these estimates are shown with a confidence indicator ("Estimated — based on usage patterns") to maintain CFO trust, as PRD FAQ Q16 implies but doesn't fully specify the UI treatment.

4. **Maturity score visibility:** PRD defines the 5-level model but doesn't specify whether it's per-org or per-team. Design implements both: org-level aggregate on Command Center, per-team breakdown on Adoption & Maturity page.

### UX Constraints That May Require PRD Scope Changes

1. **Proto v1 needs 13 pages to feel like a product.** The PRD's scope table lists 14 capabilities but doesn't map to navigation pages. The design adds 5 placeholder pages (Integration Marketplace, Compliance Reports, Enforcement Rules, AI ROI Insights, Policy Templates) to Proto v1 scope. This doesn't change Eng v1 scope but extends the prototype surface. PRD Section "Scope Boundary" should be updated to reflect the 13-page navigation map.

2. **Audit log is essential for enterprise governance.** PRD doesn't explicitly mention an activity audit log, but enterprise governance buyers (CISO, compliance) require one. Design adds "Activity Audit Log" as an Eng v1 page under Admin. This is a new Eng v1 requirement.

### Interaction Patterns That Imply New Requirements

1. **Deep-linking requires URL state management.** The design specifies that every UI state (filters, selected tool, active tab, time range) must be deep-linkable via URL parameters. This has engineering implications: the frontend must serialize/deserialize UI state from URLs, and the routing framework must support complex query parameters.

2. **Saved views require user preferences storage.** The design includes saved filter views (e.g., Lisa's "Unapproved Tools" view). This requires a user preferences API that may not exist in Quick Desktop today. PRD should add this as a dependency.

3. **Keyboard shortcuts require a shortcut manager.** The vim-style navigation shortcuts (g+c, g+i, g+g) and the / for search require a global keyboard shortcut system. This is a small but non-trivial engineering effort.
