---
artifact: prototype-notes
version: v3
design-spec-version: v3
prd-version: v2
timestamp: 2026-05-19T23:55:00Z
skill-version: 0.2.0
---

# Prototype Notes: AI Control Plane v3

## Build Summary

Single-file HTML prototype (1,947 lines) implementing design-spec-v3. Built on Cloudscape Design System CSS custom properties with full dark mode, keyboard navigation, ARIA landmarks, and responsive breakpoints.

## v3 Changes from v2

### New: Cost Intelligence Page
- **Side nav page switching:** Clicking "Cost Intelligence" nav item shows dedicated page, hides Overview. Breadcrumb updates dynamically.
- **Cost summary cards:** 4-card grid (Total AI Spend, Spend Trend, Optimization Potential, Active Recommendations).
- **Cost by model chart:** Horizontal bar chart with tier coloring (premium = primary blue, standard = secondary, economy = tertiary). Model names rendered as labels. Legend below chart.
- **Cost by team chart:** Horizontal bar chart aggregating workload costs by team.
- **Recommendations table:** 3 rows (code-review-assistant, customer-support-bot, doc-summarizer) with columns: Workload, Current Model, Suggested Model, Accuracy Delta, Monthly Savings, Status (New/Applied/Dismissed).
- **30-day cost trend:** Bar chart with 30 data points.
- **Export button:** Announces action (no backend).

### New: Cost Recommendation Alert (Split Panel)
- **In-context Alert:** Appears at top of Cost tab for workloads with `hasReco: true` (customer-support-bot, code-review-assistant).
- **Content:** Model name, accuracy equivalence percentage, estimated monthly savings.
- **Actions:** "Show Details" navigates to Cost Intelligence page. "Dismiss" hides alert for that workload.
- **Cloudscape alignment:** Uses Alert (info) pattern per design spec.

### New: Confidence Column
- **Table column:** "Confidence" added between Health and Guardrail columns.
- **Badge states:** Verified (green, checkmark), Medium (yellow, dot), Unverified (yellow, warning icon).
- **Data mapping:** Bedrock workloads = high confidence; SageMaker with known models = medium; SageMaker with pattern-matched detection = unverified.
- **Sortable:** Column header sorts by confidence level.
- **Design spec alignment:** Implements PRD v2 Failure Scenario 1 (Discovery accuracy <90%) UX response.

## Fidelity Check: design-spec-v3 Requirements

| # | Requirement | Status | Notes |
|---|------------|--------|-------|
| 1 | Hub-and-spoke layout | PASS | Overview (hub) + split panel (spoke) |
| 2 | 4 summary cards | PASS | Total Workloads, Guardrail Coverage, Unhealthy Count, Monthly Cost |
| 3 | Workload table with sortable columns | PASS | 9 columns + confidence = 10 total |
| 4 | Property filter with suggestions | PASS | Service, Health, Guardrail, Account filters |
| 5 | Split panel with 4 tabs | PASS | Overview, Guardrails, Cost, Timeline |
| 6 | Dark mode | PASS | Full CSS custom property swap |
| 7 | Keyboard navigation | PASS | Tab, Arrow keys, Enter, Escape, / for filter, r for refresh |
| 8 | ARIA landmarks and labels | PASS | banner, navigation, main, complementary roles |
| 9 | Responsive breakpoints | PASS | Mobile card view, column hiding |
| 10 | Maturity section | PASS | Level 2, progress bar, 3 action cards |
| 11 | Flashbar notification | PASS | Dismissable, 3 new workloads |
| 12 | Actions dropdown | PASS | Report, CSV, Schedule |
| 13 | Date range picker | PASS | 1h, 6h, 1d, 7d, 30d |
| 14 | Sparkline charts | PASS | Summary cards + table rows |
| 15 | Empty state | PASS | When filters match nothing |
| 16 | Skip links | PASS | Skip to main content, skip to results |
| 17 | Live regions | PASS | polite + assertive for screen reader |
| 18 | Reduced motion | PASS | prefers-reduced-motion media query |
| 19 | v3: Cost recommendation Alert in Cost tab | PASS | Info alert with Show Details + Dismiss |
| 20 | v3: Cost Intelligence page | PASS | 4 summary cards, 2 bar charts, reco table, trend |
| 21 | v3: Confidence column | PASS | 3 badge states, sortable |
| 22 | v3: Page switching via side nav | PASS | Overview + Cost Intelligence pages |
| 23 | v3: Breadcrumb updates on page switch | PASS | Dynamic label |
| 24 | v3: Cost by model with tier coloring | PASS | premium/standard/economy |
| 25 | v3: Cost by team bar chart | PASS | Aggregated from workload data |
| 26 | v3: Recommendations table | PASS | 3 rows with status badges |

**Result: 26/26 PASS**

## Interactions Verified

| Interaction | Status |
|------------|--------|
| Table row click opens split panel | PASS |
| Split panel Escape to close | PASS |
| Tab switching with arrow keys | PASS |
| Filter suggestions on focus | PASS |
| Filter token add/remove | PASS |
| Sort by any column header | PASS |
| Dark mode toggle | PASS |
| Date range picker | PASS |
| Actions dropdown | PASS |
| Flashbar dismiss | PASS |
| Cost recommendation dismiss | PASS |
| Cost recommendation Show Details → Cost Intelligence page | PASS |
| Side nav page switching | PASS |
| Focus management (panel open → close button, panel close → trigger row) | PASS |

## Technical Notes

- **No external dependencies.** Single file, no CDN imports.
- **Mock data only.** 14 workloads with cost recommendations on 2 (customer-support-bot, code-review-assistant).
- **Cost Intelligence charts are DOM-rendered.** No canvas/SVG library. Horizontal bars via flex layout with percentage widths.
- **Cost trend uses randomized data** (9000-12000 range with upward drift) for visual fidelity.
- **Confidence mapping is hardcoded** per workload. In production, this would come from the Discovery service's confidence API.

## Feedback to Design (Stage 5 → Stage 4)

No design modifications required. All v3 design spec additions implemented as specified.

## Feedback to PRD (Stage 5 → Stage 2)

1. **Cost recommendation dismissal persistence:** The dismiss action currently hides the alert in-session only. PRD should specify whether dismissals persist across sessions (requires user preference storage in DynamoDB) or reset on each visit.
2. **Confidence badge on Cost Intelligence page:** The recommendations table doesn't show confidence per workload. If discovery confidence affects recommendation confidence, this should be visible.
3. **Team tag dependency:** Cost by Team chart renders empty if workloads lack team tags. PRD's onboarding flow should enforce or guide tagging before exposing this view.
