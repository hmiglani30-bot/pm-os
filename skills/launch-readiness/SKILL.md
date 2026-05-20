---
name: launch-readiness
description: >
  Launch Readiness agent. Use when the user asks to "prepare for eng meeting",
  "create eng spec", "write acceptance criteria", "plan rollout", "package for engineering",
  or when the pm-pipeline orchestrator invokes Stage 6. Produces eng handoff artifact
  with spec, acceptance criteria, sprint breakdown, phased rollout, monitoring plan,
  rollback procedures, and meeting deck outline.
version: 0.2.0
---

# Launch Readiness

Package all pipeline artifacts into an engineering handoff. This is the bridge between product design and engineering execution.

Adapted from phuryn/pm-skills go-to-market and launch readiness frameworks.

## Input Contract

Every input MUST be provided. Fail loudly if any are missing.

| Input | Source | Required Fields | Validation |
|-------|--------|----------------|------------|
| PRD (`prd-v[N].md`) | Stage 2 | JTBD list, success metrics, persona definitions | Must contain ≥1 JTBD with ID (e.g., JTBD-1) |
| Gandalf evaluation (`gandalf-evaluation-v[N].md`) | Stage 3 | Risk table, flagged open items | Must contain risk severity ratings |
| Design spec (`design-spec-v[N].md`) | Stage 4 | Component list, interaction flows, design decisions with IDs | Must contain ≥1 design decision (e.g., DD-1) |
| Validated prototype (`prototype-v[N].html`) | Stage 5 | Working HTML, JS console clean | Must open without JS errors |

## Output Contract

| Section | Required | Min Words | Max Words | Validation Rule |
|---------|----------|-----------|-----------|-----------------|
| Executive Summary | Yes | 75 | 150 | 3 sentences: what, why, timeline |
| 1. Engineering Spec | Yes | 400 | 800 | Every component must map to a design spec section |
| 2. Acceptance Criteria | Yes | 300 | 600 | Every AC must use GIVEN/WHEN/THEN; every AC must trace to a JTBD or DD |
| 3. Sprint Breakdown | Yes | 200 | 400 | ≥2 sprints; each sprint has scope, deliverables, dependencies |
| 4. Dependency RACI | Yes | 150 | 300 | Every integration point has R, A, C, I assigned |
| 5. Phased Rollout | Yes | 150 | 300 | ≥3 phases; each has rollback trigger and procedure |
| 6. Rollback Procedures | Yes | 150 | 300 | One procedure per rollout phase; includes feature flag, data, and service rollback |
| 7. Data Migration Plan | Yes | 150 | 300 | Schema changes, migration scripts, backward compatibility, zero-downtime strategy |
| 8. Monitoring & Alerting Plan | Yes | 200 | 400 | Dashboards, alarms, runbook links per component |
| 9. Security Review Checklist | Yes | 100 | 200 | IAM, cross-account trust, encryption, permissions |
| 10. Tech Debt Register | Yes | 100 | 200 | Prototype shortcuts that need proper engineering |
| 11. Success Metrics | Yes | 100 | 200 | Restate PRD metrics with instrumentation |
| 12. Meeting Deck Outline | Yes | 100 | 200 | Structured agenda ≤ 30 min |
| 13. Consolidated Risk Register | Yes | 100 | 200 | Risks from all pipeline stages merged |
| 14. Open Questions | Yes | 50 | 150 | Each question has an owner |
| **Total** | | **3,000** | **5,000** | Word count checked before delivery |

## Output Sections

### 1. Engineering Spec
Translate the PRD and design spec into engineering-facing language:
- System components to build/modify (map each to design spec section)
- API contracts (request/response schemas, error codes, versioning)
- Data model changes (new tables, columns, indexes, FK relationships)
- Integration points with existing services (with dependency RACI reference)
- Performance requirements (latency, throughput, availability SLAs)

### 2. Acceptance Criteria
For each user-facing feature in the design spec, write testable acceptance criteria.

**Format:**
```
[AC-N] Traces to: JTBD-X / DD-Y
GIVEN [precondition]
WHEN [action]
THEN [expected result]
```

**Traceability rule:** Every AC MUST include a `Traces to:` line referencing at least one PRD JTBD ID or design spec decision ID. If an AC cannot trace to either, flag it as an open question.

Cover:
- Happy path for every major flow
- Error states identified in the design spec
- Edge cases from the Gandalf evaluation's risk section
- Performance thresholds
- Security-sensitive flows (auth, permissions, cross-account)

### 3. Sprint Breakdown
Break the engineering work into 2-week sprints with explicit scope.

| Sprint | Scope | Deliverables | Dependencies | Exit Criteria |
|--------|-------|-------------|-------------|---------------|
| S1 | Foundation | Data model, API stubs, feature flags | None | Schema deployed to dev, flags toggleable |
| S2 | Core logic | Business logic, service integration | S1 complete | Unit tests pass, integration tests pass |
| S3 | UI + polish | Frontend components, error handling | S2 complete | E2E tests pass, design review sign-off |
| S4 | Hardening | Perf tuning, monitoring, docs | S3 complete | Load test passes, runbooks reviewed |

Adjust sprint count to feature complexity. Each sprint must have clear exit criteria.

### 4. Dependency RACI
Map every integration point and cross-team dependency.

| Dependency | Responsible | Accountable | Consulted | Informed | Timeline |
|-----------|------------|-------------|-----------|----------|----------|
| [Service/Team] | [Who does the work] | [Who owns the decision] | [Who provides input] | [Who needs to know] | [When needed by] |

### 5. Phased Rollout Plan
Break the feature into shippable phases. Each phase MUST include a rollback trigger.

| Phase | Scope | Duration | Success Gate | Rollback Trigger |
|-------|-------|----------|-------------|-----------------|
| 0 (Internal) | Feature flag, internal team only | 1 week | No P0 bugs, < 100ms p99 | Any P0 bug or > 200ms p99 |
| 1 (Beta) | Selected customers, opt-in | 2 weeks | < 1% error rate, CSAT > 4.0 | Error rate > 2% or CSAT < 3.5 |
| 2 (GA) | All customers | Ongoing | Metric targets from PRD met | Metric regression > 10% from baseline |

### 6. Rollback Procedures
One procedure per rollout phase. Each must address three layers:

| Layer | Rollback Action | Estimated Time | Owner |
|-------|----------------|----------------|-------|
| Feature flag | Disable flag via [system] | < 1 min | On-call eng |
| Data | [Backward-compatible migration / revert script] | [time] | DB owner |
| Service | [Redeploy previous version / revert config] | [time] | Service owner |

Include: pre-rollback validation checks, post-rollback smoke tests, communication plan (who to notify).

### 7. Data Migration Plan
For any new tables, schema changes, or data transformations:

- **Schema changes:** New tables, altered columns, new indexes (with DDL or migration script references)
- **Migration strategy:** Online vs. offline, backfill approach, estimated duration
- **Backward compatibility:** Can old code read new schema? Can new code read old schema?
- **Zero-downtime approach:** Blue-green, shadow writes, dual-read strategy
- **Rollback:** How to reverse the migration if needed
- **Data validation:** Post-migration integrity checks

### 8. Monitoring & Alerting Plan
This is a CloudWatch team product. The monitoring plan must be first-class.

| Component | Dashboard | Key Metrics | Alarm | Threshold | Runbook |
|-----------|-----------|-------------|-------|-----------|---------|
| [API/Service] | [CW Dashboard name] | Latency p50/p99, error rate, throughput | [Alarm name] | [Trigger condition] | [Link] |

Include:
- Pre-launch baseline capture (what are current numbers before rollout?)
- Canary alarms for Phase 0
- Composite alarms for Phase 1+ (combine error rate + latency + availability)
- Log insights queries for debugging
- X-Ray / Application Signals service map expectations

### 9. Security Review Checklist
- [ ] IAM policies follow least-privilege (list specific actions and resources)
- [ ] Cross-account trust boundaries documented
- [ ] Data encryption at rest and in transit specified
- [ ] PII handling and data classification confirmed
- [ ] API authentication and authorization model reviewed
- [ ] Input validation and injection prevention addressed
- [ ] Audit logging for sensitive operations enabled
- [ ] Dependency vulnerability scan clean

### 10. Tech Debt Register
Capture every shortcut taken during prototyping that needs proper engineering.

| ID | Shortcut | Location | Proper Solution | Priority | Sprint Target |
|----|----------|----------|----------------|----------|---------------|
| TD-1 | [What was hacked] | [Prototype file/line] | [Production approach] | P1/P2/P3 | S[N] |

Sources: prototype code review, design spec TODOs, Gandalf evaluation flags.

### 11. Success Metrics (from PRD)
Restate the PRD's success metrics with engineering-specific instrumentation:

| Metric | Type | Target | Instrumentation | Dashboard |
|--------|------|--------|----------------|-----------|
| [North Star from PRD] | [Counter/Gauge/Histogram] | [Threshold] | [How to measure] | [Where to monitor] |

### 12. Meeting Deck Outline
Structure for the eng alignment meeting:

1. **Problem recap** (2 min) — From PRD persona/JTBD
2. **Competitive context** (2 min) — From research, why now
3. **Solution overview** (3 min) — From PRD solution section
4. **Design walkthrough** (5 min) — Live prototype demo
5. **Engineering spec** (5 min) — Components, APIs, data model
6. **Sprint plan** (3 min) — From sprint breakdown
7. **Phased rollout** (2 min) — From rollout plan + rollback triggers
8. **Monitoring plan** (2 min) — Dashboards, alarms, runbooks
9. **Open questions** (4 min) — From Gandalf flags + design open items
10. **Next steps** (2 min) — Timeline, ownership, S1 kickoff

### 13. Consolidated Risk Register
Merge risks from all pipeline stages:

| Source | Risk | L | I | Mitigation | Owner |
|--------|------|---|---|------------|-------|
| PRD | ... | ... | ... | ... | PM |
| Gandalf | ... | ... | ... | ... | PM |
| Design | ... | ... | ... | ... | UX |
| Technical | ... | ... | ... | ... | Eng |
| Security | ... | ... | ... | ... | SecEng |
| Data Migration | ... | ... | ... | ... | DB Owner |

### 14. Open Questions for Engineering
Items flagged by Gandalf or Designer that need eng input. Each must have an owner.

| # | Question | Source | Owner | Due By |
|---|----------|--------|-------|--------|
| 1 | ... | Gandalf / Design / Security | [Name/Role] | [Date] |

## Output Format

Frontmatter, then sections 1-14 in order, then Appendix. Use this frontmatter:

```yaml
---
artifact: launch-readiness
version: v1
prd-version: v[N]
design-version: v[N]
prototype-version: v[N]
timestamp: [ISO 8601]
status: draft | reviewed | ready
word-count: [N]
traceability-complete: true | false
---
```

Section order: Executive Summary, then Sections 1-14 as defined above, then Appendix with artifact links (Research, PRD, Gandalf, Design, Prototype). Respect per-section word counts from the Output Contract table.

## Quality Checklist
- [ ] Every acceptance criterion is testable (GIVEN/WHEN/THEN)
- [ ] Every AC has a `Traces to:` referencing a PRD JTBD or design spec decision
- [ ] Rollout plan has explicit success gates AND rollback triggers per phase
- [ ] Rollback procedures cover feature flag, data, and service layers
- [ ] Sprint breakdown has ≥2 sprints with exit criteria
- [ ] Dependency RACI covers every integration point in the eng spec
- [ ] Monitoring plan includes dashboards, alarms, and runbook links
- [ ] Security checklist has all items addressed (not just listed)
- [ ] Tech debt register captures every prototype shortcut
- [ ] Data migration plan addresses backward compatibility
- [ ] Meeting deck outline totals ≤ 30 minutes
- [ ] Risk register consolidates ALL risks from all pipeline stages
- [ ] Open questions have clear owners and due dates
- [ ] Total word count is 3,000-5,000 words
- [ ] `traceability-complete` flag is set in frontmatter

## Eval Learnings Log

| Version | Date | Gap Found | Fix Applied |
|---------|------|-----------|-------------|
| v0.1.0 → v0.2.0 | 2026-05-19 | No sprint breakdown — jumped from rollout to meeting deck | Added Section 3: Sprint Breakdown with exit criteria |
| v0.1.0 → v0.2.0 | 2026-05-19 | No dependency RACI — "integration points" without ownership | Added Section 4: Dependency RACI table |
| v0.1.0 → v0.2.0 | 2026-05-19 | No tech debt register — prototype shortcuts ignored | Added Section 10: Tech Debt Register |
| v0.1.0 → v0.2.0 | 2026-05-19 | No monitoring/alerting plan — ironic for CloudWatch team | Added Section 8: Monitoring & Alerting Plan with dashboards, alarms, baselines |
| v0.1.0 → v0.2.0 | 2026-05-19 | No rollback procedure — phased rollout with no fallback | Added Section 6: Rollback Procedures (flag, data, service layers) |
| v0.1.0 → v0.2.0 | 2026-05-19 | No data migration plan — schema changes without strategy | Added Section 7: Data Migration Plan |
| v0.1.0 → v0.2.0 | 2026-05-19 | No security review checklist — IAM/permissions unspecified | Added Section 9: Security Review Checklist |
| v0.1.0 → v0.2.0 | 2026-05-19 | No section length targets — v1 output was 1,200 words vs 3,000-5,000 target | Added Output Contract with per-section min/max word counts |
| v0.1.0 → v0.2.0 | 2026-05-19 | No evidence requirements — ACs don't trace to PRD/design | Added traceability rule: every AC must reference JTBD-X or DD-Y |
