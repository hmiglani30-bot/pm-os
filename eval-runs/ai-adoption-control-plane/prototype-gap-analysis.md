---
artifact: prototype-gap-analysis
version: v1
timestamp: 2026-05-20
comparison: roi-v2.html (ad-hoc GPT) vs prototype-v3.html (pm-os pipeline)
---

# Why the Pipeline Prototype Shipped Fewer Features Than the Ad-Hoc One

## The Numbers

| Metric | roi-v2.html (GPT ad-hoc) | prototype-v3.html (pm-os pipeline) |
|--------|--------------------------|-------------------------------------|
| Pages / navigation sections | 10 (Command Center, Inventory, Governance, Spend, Decisions, Actions, Connectors, Lenses, Approved Answers, Audit) | 2 (Workloads table, Cost Intelligence) |
| JavaScript functions | 65 | 31 |
| Interactive workflows | Decision wizard (5-step Ask→Assemble→Inspect→Act→Reuse), Connector setup, Policy creation, Case management, Bulk actions, Asset drawer, ROI drawer, Jira overlay, Onboarding wizard, Demo mode, Persona switching, Amazon Q chat | Filter/sort table, Split panel (4 tabs), Card/table view toggle, Cost recommendation dismiss, Dark mode |
| Data entities modeled | Workloads, connectors (11 providers), governance policies, violations, exceptions, cases, audit entries, lenses, approved answers, ROI sources | Workloads (14), cost recommendations |
| External library | Chart.js (3 chart instances) | None |

The gap isn't marginal — roi-v2 has roughly 5x the feature surface area. Both files are ~1,950 lines, but roi-v2 packs dramatically more functionality per line through denser UI patterns and more data entities.

## Root Cause Analysis

The pipeline didn't fail. It did exactly what it was told. That's the problem.

### 1. The PRD was a scope funnel, not a scope explorer

The PRD defined 5 capabilities (Discovery, Dashboard, Guardrails, Cost Intelligence, Maturity Score) with explicit v1/v2/v3 phasing. The Scope Boundary table on line 171 drew hard lines: connectors are v2, business outcome correlation is v2, cross-platform discovery is v2. The pipeline respected those boundaries faithfully.

The GPT ad-hoc process had no such table. When GPT proposed a connector page, nobody said "that's v2." When it suggested a decision wizard, nobody said "out of scope." The conversation was divergent — each iteration could expand the solution space. The pipeline is convergent — each stage narrows toward what was defined.

**The pipeline lacks a "scope expansion" mechanism.** Every stage takes the PRD's scope as gospel. No stage is empowered to say "the PRD scoped this for v2, but a lightweight version belongs in v1 because the prototype needs it to tell a coherent story."

### 2. The prototype skill builds to the design spec, not to a product vision

The Prototype Builder skill (Stage 5) has one job: translate the Design Spec into working HTML. Design-spec-v3 specified a workload table, split panel, and cost intelligence page. The prototype built exactly that — 26/26 validation checks passed.

In the GPT conversation, the prototype wasn't validating a spec. It was exploring a product. When the user said "what about governance?", GPT added a governance page. When the user said "this needs connectors," GPT built a connectors page. The prototype was the thinking medium, not the output artifact.

**The pipeline treats the prototype as a verification step ("does this match the spec?") rather than a discovery step ("what else does the product need?").** The ad-hoc process treats the prototype as a design tool.

### 3. No "product demo narrative" forcing function

roi-v2.html tells a story: you land on a command center, you see your AI estate, you drill into governance posture, you check spend, you make decisions through a structured workflow, you create action items, you connect external tools. It's a product tour.

prototype-v3.html is a feature implementation: here's a table of workloads, here's a detail panel, here's a cost page. It's technically correct but narratively flat. An eng team seeing prototype-v3 would understand the data model. An executive seeing roi-v2 would understand the product.

**The pipeline has no stage that asks: "If I had to demo this for 5 minutes, what navigation flow would I walk through?" That question forces you to build the connective tissue between features** — the command center that ties everything together, the stepper workflow that makes decisions feel guided, the audit log that shows the product has memory.

### 4. The Researcher underweighted competitor UX

Research-v1 and v2 analyzed ServiceNow's AI Control Tower capabilities at the feature level (discovery, governance, cost tracking). But roi-v2.html's richness came from studying ServiceNow's UX patterns — the stepper workflow, the connector marketplace, the case management system. These are interaction patterns, not features.

**The Research skill focuses on capabilities and market positioning, not on interaction pattern benchmarking.** The GPT conversation organically absorbed these patterns because the user shared competitive screenshots and said "do something like this."

### 5. Missing "kitchen sink" prototype stage

The ad-hoc process produced a maximalist prototype first, then would have scoped it down through critique. The pipeline produces a minimalist prototype first and relies on feedback loops to expand it. But the feedback loops (Stage 5→4→2) are designed for corrections, not expansions. They fix what's wrong, they don't add what's missing from a product experience perspective.

## Plugin Improvements to Close the Gap

### Improvement 1: Add a "Product Vision Prototype" stage before the spec-faithful prototype

Insert a Stage 4.5 or modify Stage 5 to have two modes:
- **Vision mode (first pass):** Build a maximalist prototype that includes lightweight versions of v2/v3 features. The goal is a demoable product narrative, not spec fidelity. Include navigation structure, placeholder pages, and interaction patterns for the full product — even features scoped for later phases.
- **Spec mode (second pass):** The current Stage 5 behavior. Build the production-faithful prototype that matches the design spec exactly.

The vision prototype is what the PM takes to the eng alignment meeting (Stage 6.5). The spec prototype is what engineering builds from.

### Improvement 2: Add "Interaction Pattern Benchmarking" to the Research skill

Add a step to the Researcher that specifically analyzes competitor UX patterns, not just capabilities. Output should include:
- Navigation patterns (sidebar structure, page hierarchy)
- Workflow patterns (wizards, steppers, guided flows)
- Data management patterns (bulk actions, drawers, overlays)
- Integration patterns (connector marketplaces, third-party hooks)

This gives the Designer concrete interaction vocabulary beyond what the PRD specifies.

### Improvement 3: Add a "Demo Narrative" section to the Design Spec

The Designer skill should include a mandatory section: "5-Minute Demo Script." This forces the designer to think about the product as a navigable experience, not a collection of components. If the demo script feels flat ("open the table, filter it, look at a detail panel"), it's a signal that the product surface area is too narrow for the problem being solved.

### Improvement 4: Modify the PRD Writer to include "Prototype Scope" distinct from "Engineering Scope"

The PRD's Scope Boundary table should have two columns: "Eng v1" (what gets built to production quality) and "Prototype v1" (what gets included in the demo prototype, even as lightweight placeholders). This lets the PM say "connectors are v2 for engineering, but the prototype should show a connectors page with 'coming soon' state so stakeholders can see the full product vision."

### Improvement 5: Add a "Product Completeness" Gandalf question

Add an 11th question to Gandalf: "If you built only what's in this PRD, would the resulting product feel complete to a first-time user? Or would it feel like a feature inside a product that doesn't exist yet?" This catches the prototype-v3 problem: it's a great feature (AI workload table with cost intelligence) but it doesn't feel like a product (an AI Adoption Command Center).

### Improvement 6: Competitor UX screenshot ingestion in Stage 0.5

The Current State Auditor already examines the existing product. Extend it to also accept competitor screenshots/demos as input. The auditor would then produce a "Competitor UX Patterns" section alongside the Pain Map, giving downstream stages a richer vocabulary of what "good" looks like in this space.

## Summary

The pipeline produced a higher-quality, more defensible artifact — every claim traces to research, every feature traces to the PRD, every interaction traces to the design spec. But it produced a narrower one. The ad-hoc GPT process produced a broader, more visionary artifact because it had no scope boundaries and used the prototype itself as a thinking tool.

The fix isn't to make the pipeline less disciplined. It's to add a divergent exploration phase (vision prototype) before the convergent execution phase (spec prototype), and to enrich upstream stages (research, PRD, design) with interaction pattern analysis and demo narrative requirements that naturally expand the solution surface.

Six plugin changes, all additive to the existing pipeline structure. No stages removed, no quality gates weakened. The pipeline keeps its rigor and gains the ad-hoc process's breadth.
