---
artifact: prototype-notes
version: v1
design-spec-version: v1
timestamp: 2026-05-20T19:00:00Z
status: validated
mode: vision
---

# Prototype Notes: Quick Desktop AI Control Tower

## Components Used

| Component | Usage | Interactive? |
|-----------|-------|:------------:|
| App Layout (sidebar + main) | Page shell with persistent sidebar navigation | Yes — nav switching |
| Side Navigation (13 items) | 7 primary + 6 sub-nav sections | Yes — page routing |
| Header with breadcrumbs | Top bar with breadcrumb trail + dark mode toggle | Yes — toggle |
| Stat Cards (KPI hero bar) | 5 governance dimension KPIs with sparklines | No — display only |
| Flashbar (alerts) | Shadow AI discovery alerts, 4 items | Yes — dismissible |
| Table (AI Inventory) | 18 AI tools, sortable/filterable/paginated | Yes — sort, filter, paginate |
| Tabs (Inventory filter) | All / Shadow AI / Approved / Blocked | Yes — filter table |
| Split Panel | Tool detail with 4 tabs, slide-in from right | Yes — open/close, tab switch |
| Modal (Apply Policy) | Governance action: Approve/Monitor/Block | Yes — radio select, confirm |
| Cards (Maturity scorecard) | 5-level maturity visualization | No — display only |
| Bar charts (CSS) | Cost by vendor (stacked), by team (horizontal) | No — display only |
| Toggle switches | Admin notification settings | Yes — on/off toggle |
| Search/Filter bar | Text search for inventory and audit log | Yes — filters data |

## Mock Data Summary

- 18 AI tools across 8 vendors and 6 teams
- Cost range: $0 (Amazon Q Developer free tier) to $4,800/month (Bedrock Claude)
- Status distribution: 9 approved, 7 unapproved (shadow AI), 2 monitored
- Risk distribution: 10 low, 6 medium, 2 high
- Discovery source: 9 via API integration, 9 via desktop detection
- Total monthly cost: ~$19,820 (mock data for prototype; $182K in dashboard represents org-wide aggregate)

## Interactions Implemented

1. Sidebar navigation switches between all 13 pages
2. Dark mode toggle swaps full color theme
3. Table sorting by clicking column headers (toggles asc/desc)
4. Text search filters table rows in real-time
5. Tab switching filters inventory (All/Shadow/Approved/Blocked)
6. Pagination with 10 items per page, prev/next controls
7. Row click opens split panel with tool detail
8. Split panel tabs switch content (Overview/Users/Cost/Compliance)
9. "Apply Policy" button opens modal with form
10. Modal close via X button, Cancel, or overlay click
11. "/" keyboard shortcut focuses search bar
12. Esc keyboard shortcut closes split panel and modal
13. Alert dismiss buttons remove individual alerts
14. Admin toggle switches flip on/off

## Validation Results

- [x] Structural validation: PASS (HTML balanced, JS syntax valid, < 500KB)
- [x] Zero external dependencies: PASS (no CDN, no external scripts/styles)
- [x] 13 pages navigable: PASS (all nav items map to page containers)
- [x] Edge-case data: PASS (empty search returns "no results", pagination handles boundaries)
- [x] Interaction testing: PASS (sort, filter, tabs, split panel, modal all functional)
- [x] Dark mode: PASS (full theme swap via CSS custom properties)
- [x] Performance: PASS (107KB file size, instant render from inline data)

## Known Limitations

- No Cloudscape CDN (pure CSS implementation avoids React dependency)
- Property filter is text search, not Cloudscape Property Filter tokens
- No loading/skeleton states (data is static)
- No URL state management / deep-linking
- No date range picker
- Simplified ARIA (main + nav landmarks present, missing search/complementary roles)
- Charts are CSS divs, not interactive chart library
