# Enterprise Design Patterns: Salesforce + Datadog Hybrid

## When to Apply
Apply these patterns when the product targets expert users, ops/SRE teams, enterprise IT, or when users need information density, cross-data correlation, and deep configurability over simplicity.

## Datadog Principles

### Information Density Over Aesthetics
- Expert users want maximum signal per pixel. Whitespace is wasted space.
- Dashboards pack metrics, logs, traces, and alerts into a single view.
- Small multiples (repeated mini-charts) enable pattern recognition at a glance.
- **Design implication:** Don't fear density. If the user is an expert, give them everything on one screen. Let THEM decide what to collapse, not you.

### Connectedness Rather Than Consistency
- Related data stays visually linked even across views. Click a metric spike → see correlated logs → see the trace that caused it.
- Navigation is lateral (data-driven) not hierarchical (menu-driven).
- "What's related to this?" is always one click away.
- **Design implication:** Every data point should be a portal. Clicking anything should show its connections, not just its details.

### Collaborative Investigation
- Shared dashboards, notebooks, and annotations.
- "What happened here?" flows are built for teams, not individuals.
- Timestamps are universal anchors — everything correlates on time.
- **Design implication:** Design for the war room. Multiple people looking at the same screen. Time is the universal axis.

## Salesforce Principles

### Contextual Data Surfacing
- Record pages show related data automatically. View a customer → see their tickets, purchases, interactions.
- Lightning Design System compound components: record pages with related lists, kanban views, activity timelines.
- "You might also need" intelligence without explicit search.
- **Design implication:** When showing entity X, proactively surface everything related to X. The user shouldn't have to navigate to find context.

### Configuration Over Customization
- Users configure their experience through preferences and saved views.
- Admin-level customization for org-wide defaults.
- Report builder lets users create their own views without engineering support.
- **Design implication:** Build the framework, not the final layout. Give users the tools to arrange their own workspace.

### Gradual Backward-Compatible Improvements
- Never break existing workflows. When upgrading a component, the old version coexists.
- Migration is optional and gradual. Power users choose when to adopt new features.
- **Design implication:** Every change must be additive, not disruptive. New features appear alongside existing ones, not instead of them.

## Combined Lens: Enterprise Evaluation Criteria

When evaluating a design for enterprise context:

1. **Information density:** Can the user see all relevant data without scrolling? If not, what's hidden and why?
2. **Cross-data navigation:** Can the user pivot from any data point to related data in ≤ 1 click?
3. **Configurability:** Can the user save views, set defaults, and customize the layout?
4. **Team collaboration:** Does the design support multiple people investigating the same issue simultaneously?
5. **Backward compatibility:** Can this be adopted incrementally without breaking existing workflows?
6. **Expert efficiency:** Does the design have keyboard shortcuts, query languages, or bulk actions for power users?
