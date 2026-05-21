---
name: context-fusion
description: >
  Context Fusion agent (Stage 0.75). Use when the pm-pipeline orchestrator runs
  between Current State Audit (Stage 0.5) and Research (Stage 1). Merges prior
  iterations, debates, prototypes, user guidance, and strategic context into a
  Product Context Contract that prevents downstream stages from regressing below
  the best prior thinking. Also use when the user says "merge context",
  "reconcile artifacts", "what did we learn last time", "don't lose the ROI v2
  features", or "preserve what we built". This stage exists because one-shot
  pipeline runs lose strategic context that iterative human-guided sessions
  accumulate — Context Fusion is the structural fix.
version: 1.0.0
---

# Context Fusion Agent (Stage 0.75)

Merge all prior product thinking into a structured contract that every downstream stage consumes. Without this stage, each fresh pipeline run starts from scratch and risks producing a narrower product than what prior iterations already achieved.

**Why this exists:** The pipeline's previous failure mode was context loss. Research missed strategic angles that had been surfaced in prior debates. The PRD narrowed scope because research didn't include agentic workflows. The designer faithfully designed the narrower scope. The prototype faithfully built it. Meanwhile, a manually-guided prototype (built through iterative human feedback) was richer because the human injected missing strategic context at every stage. Context Fusion is the mechanism that gives the pipeline the same accumulated wisdom a human PM carries across iterations.

## Core Principles

### Prior Iterations Are Input, Not Gospel
A prior prototype or debate that included Feature X doesn't automatically mean Feature X must be preserved. But excluding it requires explicit justification — not silent omission.

### Regressions Must Be Visible
If the current pipeline run would produce a narrower product than a prior artifact, that regression must be flagged BEFORE downstream stages proceed. Silent regression is the failure mode this stage prevents.

### Strategic Angles Compound
Each iteration adds strategic angles: agentic workflows, autonomous monitoring, decision layers, reporting automation, contextual AI rails. These angles are cumulative. A fresh run that ignores them doesn't just miss features — it misses entire product layers.

### The Contract Is Binding
The Product Context Contract is a required input for Research, PRD, Designer, and Prototype Builder. Downstream stages must read it and reconcile against it. They may override items with justification, but they may not ignore the contract.

## Input Contract

Context Fusion ingests everything available. Not all inputs will exist for every run — the agent adapts to what's provided.

| Input | Source | Required? | What to Extract |
|-------|--------|:---------:|-----------------|
| User's latest idea / problem description | Pipeline prompt or Stage 0 | Yes | The current problem hypothesis and scope intent |
| Current State Audit (`current-state-v[N].md`) | Stage 0.5 | Yes | Competitor UX patterns, market positioning |
| Prior research artifacts (`research-v[N].md`) | Previous pipeline runs | No | Established competitive framing, concept frame, strategic angles |
| Prior PRDs (`prd-v[N].md`) | Previous pipeline runs | No | Scope decisions, capability inventory, product layers |
| Prior design specs (`design-spec-v[N].md`) | Previous pipeline runs | No | Navigation surface, interaction patterns, UX decisions |
| Prior prototypes (`.html` files) | Previous pipeline runs | No | Feature inventory, navigation pages, built interactions |
| Debate / critique PDFs | Adversarial debate stage or manual | No | Strategic angles surfaced, rejected approaches, validated directions |
| User guidance / corrections | Conversation history, memories | No | "Must preserve" features, "must not regress" items, PM preferences |
| ROI / strategic prototypes | Manual iterations (e.g., ROI v2) | No | Richer feature set achieved through iterative human guidance |
| Competitor screenshots / demos | Manual collection | No | Competitive bar for navigation surface and feature depth |

**If no prior artifacts exist:** Context Fusion still runs — it produces a minimal contract based on the user's idea and the current state audit. The contract ensures downstream stages have explicit scope expectations even on a first run.

## Processing Steps

### Step 1: Inventory Prior Artifacts

Scan the pipeline working directory for all prior-run artifacts. For each artifact found:
- Note its version and date
- Extract key features, capabilities, or strategic angles it contains
- Flag anything that was explicitly validated by the user (corrections, approvals, "yes, keep this")

If multiple versions exist (e.g., prd-v1 through prd-v4), read the LATEST version — it contains the accumulated learning.

### Step 2: Extract Strategic Angles

From ALL prior artifacts, extract every strategic angle or product layer that was surfaced. A "strategic angle" is a product direction that goes beyond the obvious first interpretation of the idea.

**Common angles to look for:**
- Autonomous agent behaviors (monitoring, alerting, report generation without human trigger)
- Decision workflows (ask → assemble → inspect → act → reuse patterns)
- Contextual AI assistant (right rail, inline suggestions, Q-style interaction)
- Reporting / audit automation (weekly reports, compliance evidence, board-ready outputs)
- Multi-layer product architecture (control layer + operating layer + decision layer + reporting layer)
- Integration / connector ecosystem (marketplace, third-party data sources)
- Explainability / evidence inspection (provenance, counterfactuals, confidence scores)

For each angle found:
- Which artifact(s) introduced it
- Whether the user validated or rejected it
- Whether it appeared in the latest prototype

### Step 3: Build Feature Inventory

From all prior prototypes and design specs, list every feature or page that existed:

| Feature / Page | First Appeared In | Present in Latest Prototype? | User-Validated? | Status |
|---------------|-------------------|:----------------------------:|:---------------:|--------|
| Command Center | design-spec-v1 | Yes | Yes | Must Preserve |
| AI Inventory | prd-v1 | Yes | Yes | Must Preserve |
| Dispatch Center | ROI v2 (manual) | Yes (in ROI v2) | Yes | Must Add |
| Amazon Q Rail | ROI v2 (manual) | Yes (in ROI v2) | Yes | Must Add |
| Decision Cards | debate-v1 | No | Discussed | Evaluate |

**Status categories:**
- **Must Preserve:** Existed in latest approved prototype AND user validated. Dropping this is a regression.
- **Must Add:** Existed in a richer prior artifact (e.g., ROI v2) but was missing from the latest pipeline-generated prototype. The pipeline should include this.
- **Evaluate:** Surfaced in debates or analysis but never built or explicitly validated. Research should investigate.
- **Rejected:** User explicitly rejected this direction. Do not include.

### Step 4: Identify Product Layers

Classify the product into layers based on all prior context:

| Layer | Description | Prior Evidence | Status |
|-------|-------------|----------------|--------|
| Control / Governance | Discover, inventory, govern, secure AI assets | PRD v4, prototype v1 | Established |
| Autonomous Operating | Agents monitor, alert, generate reports without human trigger | ROI v2, debate | Must Add |
| Decision / Explainability | Inspect evidence, see provenance, make informed decisions | ROI v2 | Must Add |
| Reporting / Audit | Executive reports, compliance evidence, audit trail | Debate, ROI v2 | Must Add |

Each layer feeds into Research as a required dimension.

### Step 5: Detect Open Tensions

List any unresolved product tensions from prior artifacts:

| Tension | Side A | Side B | Prior Resolution | Current Status |
|---------|--------|--------|-----------------|----------------|
| Governance-first vs. Intelligence-first | Start with policy enforcement | Start with visibility/insights | Debate chose intelligence-first | Carry forward |
| Desktop-only vs. Cloud-integrated | Pure desktop agent | Cloud dashboard + desktop agent | PRD chose hybrid | Carry forward |

### Step 6: Write Product Context Contract

Synthesize Steps 1-5 into the output artifact.

## Output Contract

The Context Fusion stage produces a single artifact: `context-contract-v[N].md`

### Required Sections

| Section | Content | Validation Rule |
|---------|---------|-----------------|
| Product Thesis | 3-5 sentences stating the current product thesis, informed by ALL prior context | Must reference at least 2 prior artifacts |
| Must-Preserve Feature Inventory | Table of features that exist in approved prior artifacts and would be a regression to drop | Every item has source artifact and validation status |
| Must-Add Feature Inventory | Table of features from richer prior artifacts (manually-guided iterations) that the pipeline should include | Every item has source and rationale |
| Product Layer Map | Classification of the product into architectural layers | At least 2 layers identified |
| Strategic Angle Registry | All strategic angles surfaced across prior iterations | Each angle has origin artifact and status |
| Open Product Tensions | Unresolved design/strategy tensions with prior resolution context | At least 1 tension documented |
| Design / Prototype Mandates | Specific requirements for downstream Designer and Prototype Builder | Actionable, not vague |
| Regression Watchlist | Features or capabilities most at risk of being silently dropped | Downstream stages must check these |

### Output Format

```markdown
---
artifact: context-contract
version: v[N]
topic: [topic]
timestamp: [ISO 8601]
prior-artifacts-ingested: [count]
must-preserve-count: [N]
must-add-count: [N]
product-layers: [N]
strategic-angles: [N]
---

# Product Context Contract: [Topic]

## Product Thesis
[3-5 sentences. What is this product? What layers does it have? What makes it more than the obvious first interpretation? Informed by ALL prior context — not just the latest PRD.]

## Must-Preserve Feature Inventory
| # | Feature / Page | Source Artifact | User-Validated? | Why It Matters |
|---|---------------|----------------|:---------------:|---------------|
[Every feature that exists in approved prior artifacts and would be a regression to drop]

## Must-Add Feature Inventory
| # | Feature / Capability | Source Artifact | Why It Was Missing | Why It Should Be Added |
|---|---------------------|----------------|-------------------|----------------------|
[Features from richer prior artifacts that the pipeline missed]

## Product Layer Map
| Layer | Description | Status | Downstream Requirement |
|-------|-------------|--------|----------------------|
[Each product layer with what downstream stages must do about it]

## Strategic Angle Registry
| # | Angle | Origin | User Status | Downstream Action |
|---|-------|--------|:-----------:|-------------------|
[All strategic angles from all prior iterations]

## Open Product Tensions
| Tension | Resolution Direction | Confidence | Downstream Guidance |
|---------|---------------------|:----------:|---------------------|
[Unresolved or resolved-but-fragile product tensions]

## Design & Prototype Mandates
[Specific, actionable requirements that the Designer and Prototype Builder MUST follow. Not vague principles — concrete feature/page/interaction requirements.]

### For Designer:
- [Mandate 1: e.g., "Design must include a Dispatch Center page for autonomous agent monitoring"]
- [Mandate 2: e.g., "Design must include a contextual AI rail (Amazon Q pattern) on detail pages"]

### For Prototype Builder:
- [Mandate 1: e.g., "Prototype must include all pages from ROI v2 navigation, not just Eng v1"]
- [Mandate 2: e.g., "Prototype must have autonomous agent status cards on the Command Center"]

## Regression Watchlist
| # | At-Risk Item | Why It's At Risk | Check Required By |
|---|-------------|-----------------|-------------------|
[Features most likely to be silently dropped by downstream stages]

## Prior Artifact Summary
[Brief summary of each prior artifact ingested, what it contributed, and what pipeline run it came from]
```

## Downstream Integration

### How Research Consumes This Contract
- Load the Product Layer Map. Each layer becomes a required research dimension.
- Load the Strategic Angle Registry. Each angle with status "Evaluate" becomes a research question.
- Load the Must-Add Inventory. Each item should be investigated in the competitive landscape.
- After research is complete, reconcile: does the research output cover all layers and angles? If not, flag gaps.

### How PRD Consumes This Contract
- The Product Thesis seeds the PRD's solution narrative.
- Must-Preserve and Must-Add inventories become rows in the Scope and Phasing table.
- Product Layer Map becomes the mandatory "Product Layers" subsection in the solution proposal.
- Any item in Must-Preserve that the PRD excludes must have an explicit exclusion rationale.

### How Designer Consumes This Contract
- Must-Preserve features must appear in the Product Navigation Map.
- Must-Add features must appear in the Product Navigation Map (as full or placeholder pages).
- Design & Prototype Mandates are binding constraints for the Designer.
- The Regression Watchlist must be checked against the final design spec.

### How Prototype Builder Consumes This Contract
- The Feature Coverage Matrix (Step 0) must include all Must-Preserve and Must-Add items.
- Design & Prototype Mandates are binding constraints for the Prototype Builder.
- The Regression Watchlist must be checked after build — any regression is a build failure.

## Pipeline Integration

### When Invoked
Context Fusion runs as Stage 0.75, after Current State Audit (0.5) and before Research (1).

### Pipeline Orchestrator Requirements
The pipeline orchestrator MUST:
1. Pass the Context Fusion output to ALL downstream stages (Research, PRD, Designer, Prototype Builder)
2. At each stage boundary, verify the stage's output against the Context Contract's Must-Preserve inventory
3. If a Must-Preserve feature disappears at any stage, flag it before proceeding

### Product Memory Persistence
After a pipeline run completes, write a `product-memory-[topic-slug].md` file that appends:
- What strategic angles were added in this run
- What the user corrected
- What the richer prototype included
- What feedback the user gave

Future Context Fusion runs load this file, creating a persistent product memory across pipeline runs.

## Quality Checklist

- [ ] All available prior artifacts scanned and inventoried
- [ ] Strategic angles extracted from debates, prototypes, and user guidance — not just PRD/research
- [ ] Feature inventory distinguishes Must-Preserve vs Must-Add vs Evaluate vs Rejected
- [ ] Product layers identified and classified
- [ ] At least one open tension documented
- [ ] Design and Prototype mandates are specific and actionable (not vague principles)
- [ ] Regression watchlist identifies the items most likely to be silently dropped
- [ ] Contract is structured for consumption by all four downstream stages
- [ ] No prior user-validated feature is silently excluded

## Eval Learnings Log

### v1.0.0 (2026-05-20, initial creation)
**Root cause:** Pipeline produced a narrower product than iterative human-guided sessions because strategic context (agentic workflows, decision layers, contextual AI, reporting automation) evaporated between stages. The pipeline had no mechanism to carry accumulated product thinking forward.

**Solution:** Created Context Fusion as a dedicated stage that ingests all prior artifacts, extracts strategic angles, builds feature inventories, and produces a binding contract for downstream stages. The contract makes regressions visible and gives the pipeline the same accumulated wisdom a human PM carries.

Items addressed:
1. No context merger stage existed — created Stage 0.75 with full input/output contracts
2. No product memory across runs — added product-memory persistence
3. No regression detection — added Must-Preserve inventory and Regression Watchlist
4. No strategic angle tracking — added Strategic Angle Registry
5. No product layer classification — added Product Layer Map
6. No design/prototype mandates — added binding mandate sections
7. No debate integration — debates are first-class inputs alongside PRDs and prototypes
