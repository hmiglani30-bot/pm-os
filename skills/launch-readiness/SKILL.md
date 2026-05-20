---
name: launch-readiness
description: >
  Launch Readiness agent. Use when the user asks to "prepare for eng meeting",
  "create eng spec", "write acceptance criteria", "plan rollout", "package for engineering",
  or when the pm-pipeline orchestrator invokes Stage 6. Produces eng handoff artifact
  with spec, acceptance criteria, phased rollout, and meeting deck outline.
version: 0.1.0
---

# Launch Readiness

Package all pipeline artifacts into an engineering handoff. This is the bridge between product design and engineering execution.

Adapted from phuryn/pm-skills go-to-market and launch readiness frameworks.

## Input
- Approved PRD (`prd-v[N].md`)
- Gandalf evaluation (`gandalf-evaluation-v[N].md`)
- Approved design spec (`design-spec-v[N].md`)
- Validated prototype (`prototype-v[N].html`)

## Output Sections

### 1. Engineering Spec
Translate the PRD and design spec into engineering-facing language:
- System components to build/modify
- API contracts (if applicable)
- Data model changes
- Integration points with existing services
- Performance requirements (latency, throughput, availability)

### 2. Acceptance Criteria
For each user-facing feature in the design spec, write testable acceptance criteria:

**Format:**
```
GIVEN [precondition]
WHEN [action]
THEN [expected result]
```

Cover:
- Happy path for every major flow
- Error states identified in the design spec
- Edge cases from the Gandalf evaluation's risk section
- Performance thresholds

### 3. Phased Rollout Plan
Break the feature into shippable phases:

| Phase | Scope | Duration | Success Gate |
|-------|-------|----------|-------------|
| 0 (Internal) | Feature flag, internal team only | 1 week | No P0 bugs, < 100ms p99 |
| 1 (Beta) | Selected customers, opt-in | 2 weeks | < 1% error rate, CSAT > 4.0 |
| 2 (GA) | All customers | Ongoing | Metric targets from PRD met |

### 4. Success Metrics (from PRD)
Restate the PRD's success metrics with engineering-specific instrumentation:

| Metric | Instrumentation | Dashboard |
|--------|----------------|-----------|
| [North Star] | [How to measure] | [Where to monitor] |

### 5. Meeting Deck Outline
Structure for the eng alignment meeting:

1. **Problem recap** (2 min) — From PRD persona/JTBD
2. **Competitive context** (2 min) — From research, why now
3. **Solution overview** (3 min) — From PRD solution section
4. **Design walkthrough** (5 min) — Live prototype demo
5. **Engineering spec** (5 min) — Components, APIs, data model
6. **Phased rollout** (3 min) — From rollout plan
7. **Open questions** (5 min) — From Gandalf flags + design open items
8. **Next steps** (2 min) — Timeline, ownership, first sprint scope

### 6. Risk Register (consolidated)
Merge risks from all pipeline stages:

| Source | Risk | Likelihood | Impact | Mitigation | Owner |
|--------|------|-----------|--------|------------|-------|
| PRD | ... | ... | ... | ... | PM |
| Gandalf | ... | ... | ... | ... | PM |
| Design | ... | ... | ... | ... | UX |
| Technical | ... | ... | ... | ... | Eng |

## Output Format

```markdown
---
artifact: launch-readiness
version: v1
prd-version: v[N]
design-version: v[N]
prototype-version: v[N]
timestamp: [ISO 8601]
status: draft | reviewed | ready
---

# Launch Readiness: [Feature Name]

## Executive Summary
[3 sentences: what we're building, why, and the proposed timeline]

## 1. Engineering Spec
[System components, APIs, data model, integrations, performance requirements]

## 2. Acceptance Criteria
### [Feature/Flow 1]
- GIVEN ... WHEN ... THEN ...
[...]

### [Feature/Flow 2]
[...]

## 3. Phased Rollout
| Phase | Scope | Duration | Success Gate |
|-------|-------|----------|-------------|
[...]

## 4. Success Metrics & Instrumentation
| Metric | Type | Target | Instrumentation | Dashboard |
|--------|------|--------|----------------|-----------|
[...]

## 5. Meeting Deck Outline
[Structured agenda with time allocations]

## 6. Consolidated Risk Register
| Source | Risk | L | I | Mitigation | Owner |
|--------|------|---|---|------------|-------|
[...]

## 7. Open Questions for Engineering
[Items flagged by Gandalf or Designer that need eng input]

## Appendix: Artifact Links
- Research: research-v[N].md
- PRD: prd-v[N].md
- Gandalf: gandalf-evaluation-v[N].md
- Design: design-spec-v[N].md
- Prototype: prototype-v[N].html
```

## Quality Checklist
- [ ] Every acceptance criterion is testable (GIVEN/WHEN/THEN)
- [ ] Rollout plan has explicit success gates per phase
- [ ] Meeting deck outline totals ≤ 30 minutes
- [ ] Risk register consolidates ALL risks from all pipeline stages
- [ ] Open questions have clear owners
