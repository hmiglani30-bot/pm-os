# Change Spec: External Integration Layer (Linear Publish)

**Scope:** Extend Launch Readiness (v0.2.0) with structured ticket output + optional Linear MCP push  
**Author:** PM Pipeline  
**Date:** 2026-05-19  
**Status:** Proposed  

---

## 1. What Changes

Two additions to the pipeline, neither modifying existing sections 1-14:

### 1a. New Output Section 15: Structured Ticket Payload

After Section 14 (Open Questions), Launch Readiness emits a `## 15. Linear Ticket Payload` section containing machine-parseable ticket objects derived from the Sprint Breakdown (Section 3). Format:

Each ticket object has: `type` (epic|task), `title`, `description`, `estimate`, `labels[]`, `blockedBy[]`.

**Derivation rules:** 1 epic from the Executive Summary feature name. N child tasks, one per Sprint Breakdown row. Title = `S{N} — {Name}: {Scope, 60 chars}`. Description = Deliverables + Exit Criteria + Dependencies verbatim from the row. Estimate = 1 point per sprint. Labels = `pm-pipeline` + `sprint-{N}`. Blocking relations parsed from the Dependencies column (e.g., "S1 complete" maps to blockedBy S1's ticket).

### 1b. New Optional Pipeline Step 6b: Linear Publish

A post-Stage-6 step invoked only when:
1. The user explicitly requests it (`--publish linear` flag or interactive prompt)
2. Linear MCP tools are available in the session

Execution sequence: (1) create epic via `save_issue` with title, description, team, labels; (2) create each child task with `parentId` = epic's returned ID; (3) set `blockedBy` using returned IDs; (4) append created identifiers (e.g., APM-123...) to the artifact as `## 16. Linear Sync Log`.

---

## 2. MECE Check: No Overlap with Existing Sprint Breakdown

- **Section 3** = human-readable planning table for the eng meeting deck. Audience: engineers. Always produced.
- **Section 15** = machine-parseable ticket schema derived from Section 3. Audience: the publish step or manual copy-paste. Always produced, zero cost.
- **Step 6b** = API calls to Linear. Audience: Linear workspace. Only on explicit request.

**Manual today:** After the eng meeting, Ashu re-reads the sprint breakdown and manually creates Linear tickets -- titles, descriptions, parent-child, blocking relations. For AI Control Plane (8 sprints): 9 tickets, 7 blocking relations, ~30 min of mechanical work.

**Automated after:** Section 15 generated deterministically from Section 3. Step 6b pushes to Linear in one batch. 30 minutes becomes one confirmation prompt.

---

## 3. Acceptance Criteria

**AC-1: Ticket count matches sprint count.**  
GIVEN a launch-readiness artifact with N rows in the Sprint Breakdown table,  
WHEN Section 15 is generated,  
THEN it contains exactly N+1 ticket objects (1 epic + N tasks), each with non-empty title, description, and labels.

**AC-2: Blocking relations are correct.**  
GIVEN sprint S2 has Dependencies = "S1 complete" and S3 has Dependencies = "S2 complete",  
WHEN Section 15 is generated,  
THEN S2's ticket has `blockedBy: [S1-ref]` and S3's ticket has `blockedBy: [S2-ref]`, forming a valid DAG with no cycles.

**AC-3: Linear tickets are created with correct hierarchy.**  
GIVEN Section 15 contains 1 epic + N tasks and the user confirms publish,  
WHEN Step 6b executes against Linear MCP,  
THEN `save_issue` is called N+1 times, each child's `parentId` references the epic's returned ID, and all returned identifiers are logged in Section 16.

**AC-4: Publish requires explicit user confirmation.**  
GIVEN the pipeline completes Stage 6 in interactive mode,  
WHEN the user has NOT passed `--publish linear` or responded "yes" to the publish prompt,  
THEN Step 6b does NOT execute and no `save_issue` calls are made.

**AC-5: Graceful degradation without Linear MCP.**  
GIVEN the Linear MCP is not connected in the session,  
WHEN the user requests `--publish linear`,  
THEN the pipeline logs "Linear MCP not available — Section 15 generated but publish skipped" and completes normally with Section 15 intact in the artifact.

---

## 4. Anti-Criteria (Explicit Exclusions)

- **No auto-create.** Tickets are never created without explicit user confirmation per session. Section 15 is always generated; Step 6b is always gated.
- **No bidirectional sync.** This is write-once, not a sync engine. Ticket edits in Linear are not pulled back into the markdown artifact. No update/delete operations.
- **No markdown replacement.** The launch-readiness artifact (Sections 1-14) remains the canonical source. Section 15 is additive. Removing Linear does not degrade the core artifact.
- **No team/project inference.** Step 6b requires the user to specify the Linear team name. It does not guess from context or default silently.
- **No custom field mapping.** V1 maps only: title, description, estimate, labels, parentId, blockedBy. Custom fields (priority, cycle, milestone, assignee, project) are out of scope -- users set those in Linear after creation.
- **No other PM tools.** This spec covers Linear only. Jira/Asana/GitHub Issues are not in scope.

---

## 5. Tool Dependencies

### Required MCP Tools (Step 6b only)

- **`save_issue`** (required): Create epic and child tasks with parentId, blockedBy, labels.
- **`list_issues`** (nice-to-have): Pre-publish duplicate check by title prefix.
- **`create_issue_label` / `list_issue_labels`** (nice-to-have): Create `pm-pipeline` and `sprint-N` labels if missing.

### Graceful Degradation

Section 15 has **zero external dependencies** -- pure markdown generation from Section 3. Works in every session.

Step 6b runtime behavior: (1) MCP connected: prompt for team name, confirm, execute. (2) MCP not connected: skip with log, Section 15 remains for manual use. (3) `save_issue` fails mid-batch: log successes with IDs + failures with errors, no rollback, user retries failed tickets.

### Optionality Guarantee

Neither addition alters the existing pipeline contract. The orchestrator (`pm-pipeline.md`) needs no changes. Section 15 appends after Section 14 within Launch Readiness. Step 6b is a post-stage hook following the feedback loop pattern (non-blocking side effect).
