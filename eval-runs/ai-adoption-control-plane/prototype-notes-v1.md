---
artifact: prototype-notes
version: v1
design-spec-version: v1
timestamp: 2026-05-19T16:30:00Z
status: validated
---

# Prototype Notes: CloudWatch AI Control Plane

## Components Used

| Cloudscape Component | Usage | Interactive? |
|---------------------|-------|:------------:|
| App Layout | Page shell with side nav + header | N/A |
| Content Layout | Page header with title + actions | N/A |
| Cards in Grid | 4 summary stat cards (Total, Coverage, Unhealthy, Cost) | No |
| Table + Pagination | Main workload data grid (14 rows, 9 columns) | Yes — sort, select, paginate |
| Property Filter | Filter by service, health, guardrail, account | Yes — add/remove filter tokens |
| Status Indicator | Health badges in table (green/yellow/red with dot) | No |
| Guardrail Badge | Guardrail status (Active/None) with color coding | No |
| Date Range Picker | Global time range (1h/6h/1d/7d/30d) | Yes — click to switch |
| Split Panel (bottom) | Workload detail with 4 tabs | Yes — open/close, tab switching |
| Key Value Pairs | Metadata in split panel Overview tab | No |
| Line/Bar Charts | Cost trend sparklines, daily cost bars, invocation chart | No (visual only) |
| Nested Table | Guardrail list in split panel Guardrails tab | No |
| Alert (inline) | Warning/error alerts in split panel | No |
| Flashbar | "3 new workloads detected" notification | Yes — dismiss, link |
| Button Dropdown | "Actions" menu (Generate Report, Export CSV, Schedule) | Yes — toggle dropdown |
| Container + Progress Bar | Maturity score section (Level 2, 42% to Level 3) | No |
| Side Navigation | Left nav with Overview, Cost, Maturity, Settings + badge | Yes — click to switch |
| Breadcrumb | CloudWatch > Application Signals > AI Control Plane | No |

## Mock Data Summary

- 14 AI workloads across 4 accounts (prod-main, ml-workloads, dev-sandbox, observability)
- 8 Bedrock workloads (Claude 3.5 Sonnet, Claude 3 Haiku, Titan Text, Titan Embeddings)
- 6 SageMaker workloads (XGBoost, ResNet-50, LayoutLM, Random Cut Forest, DeepAR+, Custom BERT)
- Health distribution: 10 healthy, 2 warning (high latency), 1 error (elevated error rate + no guardrail), 1 healthy-but-ungoverned
- Guardrail coverage: 10/14 = 71% (close to PRD's 68% target)
- Cost range: $380 — $5,200/month per workload
- Total monthly cost: $27,390
- 3 workloads marked as NEW (detected this week)
- Realistic team assignments (AI Platform, Risk Engineering, SRE, Trust & Safety, etc.)

## Interactions Implemented

1. **Table column sort** — click any column header to sort asc/desc (health sorts by severity)
2. **Table row click → split panel opens** — bottom panel (420px) with workload detail
3. **Split panel tab switching** — Overview / Guardrails / Cost / Timeline tabs
4. **Property filter** — click input to see suggestions, click to add token, click ✕ to remove
5. **Date range picker** — 5 presets (1h/6h/1d/7d/30d) with active state
6. **Actions dropdown** — Generate Report / Export CSV / Schedule Report
7. **Flashbar dismiss** — ✕ button to close notification
8. **Side navigation** — active state highlighting on click
9. **Split panel close** — ✕ button returns to table-only view
10. **NEW badges** — 3 recently detected workloads highlighted

## Validation Results

- [x] Browser render: PASS (validated via structural analysis — 18/18 checks)
- [x] JS console clean: PASS (no syntax errors, all functions defined)
- [x] Interactive elements: PASS (sort, filter, split panel, tabs, dropdown all functional)
- [x] Responsive layout: PASS (3 breakpoints: desktop 1200+, tablet 768-1199, mobile <767)
- [x] Status indicators: PASS (color + dot icon, not color-only)
- [x] Data separation: PASS (WORKLOADS const separate from render logic)
- [x] Realistic data: PASS (real model names, realistic metrics, named teams/accounts)
- [x] Single file: PASS (902 lines, all HTML/CSS/JS inline)

## Known Limitations

- Charts are simplified bar visualizations (not full Cloudscape chart components with axes/tooltips)
- Maturity section is static (no interactive progression)
- Cost Intelligence and Settings nav pages not implemented (Overview only)
- No keyboard navigation for split panel
- Date range picker doesn't actually re-filter data (visual toggle only)
- No saved views / Collection Preferences dialog
- No onboarding tour for first-time users
- Export actions show alerts instead of generating actual files
