---
artifact: pipeline-flow-redesign
version: v1
timestamp: 2026-05-19T18:30:00Z
scope: Method definition (300w) → Stage 1, 3, 4 redefinition (800+w) → Context Pruning redesign
status: proposal
---

# Pipeline Flow Redesign: Handoff Contracts, Input Flexibility, and Context Pruning

## Part 1: The Method (How Stages Connect)

Every stage in the pipeline is a **contract**: it declares what it requires to start (input contract), what it guarantees when finished (output contract), and what it passes forward (handoff envelope). A handoff envelope is the specific slice of an artifact that the next stage actually needs — never the full artifact unless justified.

**Input acquisition** follows a fixed protocol at pipeline start. Stage 0 prompts the user with a structured intake:

1. **Text input (mandatory, never skippable):** Describe the idea, problem, or feature. Minimum 2 sentences.
2. **Optional enrichment (user chooses which, if any, to provide):**
   - Screenshots (demo account, competitor, current UX)
   - URLs (competitor pages, blog posts, analyst reports, documentation)
   - Files (existing PRDs, research, slide decks, customer feedback)
   - Voice/transcription (meeting notes, interview recordings)

The pipeline presents these as checkboxes: "Do you have any of these to share?" The user can skip all optional inputs. But the text input is the seed — without it, no stage can run.

**Cross-stage feedback** works through a **flag-and-patch** mechanism. If any downstream stage discovers the upstream artifact is missing required information, it emits a `DEPENDENCY_GAP` flag with: (a) what's missing, (b) which upstream section should contain it, (c) whether the gap blocks this stage or is a degraded-quality warning. The orchestrator routes the gap back to the responsible stage's skill for patching.

**Quality gates** at each transition validate that the output contract is met before the handoff envelope is assembled. Validation is structural (required sections present, minimum word counts met, required tables exist) and substantive (evidence density threshold, citation tier distribution). A stage cannot hand off until its output contract passes validation.

---

## Part 2: Stage Redefinitions

### Stage 1: Research — Redefined Input Contract

**Current problem:** Stage 1 assumes the input is a topic string. It has no mechanism to ingest screenshots, URLs, or files the user might provide. The user's idea gets flattened into a keyword.

**Redefined Input Contract:**

| Input Field | Required? | Format | How Stage 1 Uses It |
|-------------|-----------|--------|---------------------|
| `idea_text` | **Yes** | Free text (min 2 sentences) | Seeds the decision-to-inform framing and defines the research scope. The Researcher extracts: domain, implied competitors, target user, and problem hypothesis. |
| `screenshots[]` | No | Image files (PNG/JPG) | Analyzed for current UX state, feature gaps, error patterns, and competitor capabilities. Each screenshot is annotated with: what it shows, what's notable, what's missing. Screenshots become primary evidence (Tier 1) in the research artifact. |
| `urls[]` | No | Web URLs | Fetched and analyzed as starting sources. Each URL is classified by evidence tier. URLs accelerate Step 3-4 (competitor analysis) by providing pre-identified competitor pages, pricing pages, or documentation. |
| `files[]` | No | PDF, DOCX, MD, PPTX, CSV | Parsed for existing research, prior PRDs, customer feedback data, or competitive intelligence. Cited as Tier 1-2 sources if they contain primary data. |
| `constraints` | No | Free text | User-specified constraints: timeline, budget, team size, technical stack, compliance requirements. Passed to every downstream stage as immutable context. |

**Redefined Output Contract (what Stage 1 guarantees):**

The research artifact must contain these sections at minimum, each meeting the specified quality bar, or the output validation fails:

| Section | Required? | Minimum Quality Bar | Validated How |
|---------|-----------|--------------------|----|
| Decision to Inform | Yes | Single sentence, links to user's `idea_text` | String match against idea keywords |
| Executive Summary | Yes | 200-300 words, conclusion-first | Word count check |
| Own Product Gap Analysis | Yes | >= 1,500 words, names specific capabilities | Word count + entity extraction |
| Primary Competitor (Thesis/Counter/Implication) | Yes | >= 800 words, evolution timeline table present | Word count + table detection |
| Secondary Competitors (1+) | Yes | >= 400 words each, timeline table per competitor | Word count + table count |
| Market Data Table | Yes | >= 8 rows with Tier noted | Row count + Tier column present |
| Pricing Comparison Table | Yes | Entry for every named competitor | Row count >= competitor count |
| TAM Calculation | Yes | Bottoms-up math shown (not just a number) | Contains arithmetic operators |
| Customer Voice | Yes | >= 3 direct quotes with source attribution | Quote block count >= 3 |
| Key Takeaways for PRD | Yes | 5-7 items, each actionable | Item count in range |
| Evidence Tier Distribution | Yes | >= 40% Tier 1-2 | Percentage calculation |

**Handoff Envelope to Stage 2 (PRD Writer):**
- Full `research-v[N].md` (PRD Writer needs everything — this is the only stage that gets the full research)
- `user_inputs.md` — the original idea text, constraints, and any user-provided files/URLs (so PRD Writer can reference the user's own language and intent)

**Handoff Envelope to Stage 3 (Gandalf):**
- Research Summary (extracted): Executive Summary + Key Takeaways + Market Data Table + TAM + Pricing Table (approximately 1,500 words, not the full 5,000-7,500)
- This is enough for Gandalf to cross-reference PRD claims against evidence without drowning in detail

---

### Stage 3: Gandalf — Redefined Input Contract and Cross-Stage Feedback

**Current problem:** Gandalf receives "latest PRD + research summary" but has no structured way to validate that the PRD contains what it needs to answer the 10 critique questions. If the PRD is missing a TAM section, Gandalf scores Q1 as a fail — but the failure is an input gap, not a strategy gap. There's no mechanism to send the gap back upstream.

**Redefined Input Contract:**

| Input Field | Required? | Source Stage | How Gandalf Uses It |
|-------------|-----------|-------------|---------------------|
| `prd-v[N].md` | **Yes** | Stage 2 | Primary artifact under evaluation. Gandalf reads every section. |
| `research_summary` | **Yes** | Stage 1 (pruned) | Cross-references PRD claims against research evidence. Used for Q1 (TAM), Q2 (Why Now), Q5 (Moat), Q8 (Cannibalization). |
| `user_constraints` | **Yes** | Stage 0 | Adjusts scoring — if user specified "no pricing model yet," Q10 is scored with a lower bar (rubric 3 = acknowledges uncertainty with a plan to resolve). |
| `research_pricing_table` | **Yes** | Stage 1 (extracted) | Directly feeds Q10 (Pricing & Business Model). If research has no pricing data, Gandalf knows this is a pipeline gap, not a PRD gap. |
| `research_customer_voice` | **Yes** | Stage 1 (extracted) | Directly feeds Q3 (Customer Problem Depth). Gandalf checks if PRD customer scenarios trace back to real customer quotes from research. |

**Pre-Evaluation Structural Check (NEW):**

Before scoring, Gandalf runs a structural check against the PRD. For each of its 10 questions, it verifies the PRD section that should contain the answer actually exists and meets minimum depth:

| Question | Required PRD Section | Minimum Check |
|----------|---------------------|---------------|
| Q1: TAM | Quantitative data or FAQs | TAM number + math present |
| Q2: Why Now | Executive Summary or Problem Depth | Temporal trigger identified |
| Q3: Problem Depth | Persona + Problem Depth | >= 3 named scenarios |
| Q4: North Star | Success Metrics | Single metric + rejected alternatives |
| Q5: Moat | Competitive Differentiation | >= 1 structural advantage cited |
| Q6: Scope | Scope Boundary Table | Table exists with rationale column |
| Q7: Technical Feasibility | Solution Proposal or FAQs | Technical approach described |
| Q8: Cannibalization | Risks or FAQs | Existing services named |
| Q9: Failure Mode | Risks | >= 1 falsifiable scenario |
| Q10: Pricing | FAQs or Business section | Revenue path described |

If the structural check finds a section missing or below minimum depth, Gandalf emits a `DEPENDENCY_GAP` flag:

```
DEPENDENCY_GAP:
  question: Q1 (TAM)
  missing_from: prd-v1.md § Quantitative Data
  what_is_needed: Bottoms-up TAM calculation with math shown
  severity: BLOCKING (cannot score without this)
  suggested_source: research-v1.md § TAM Calculation
```

The orchestrator routes this back to the PRD Writer to patch. Gandalf proceeds to score the remaining questions while the patch is in progress (pipeline never blocks — it parallelizes the fix).

**Redefined Output Contract:**

Gandalf's output now includes two new sections beyond the score table:

| Section | Content | Consumed By |
|---------|---------|-------------|
| Detailed Scores (existing) | 10-row table with rubric + evidence + pass/fail | Orchestrator (state), Human (review) |
| Dependency Gaps Emitted | List of `DEPENDENCY_GAP` flags sent upstream | Orchestrator (routing), PRD Writer (patching) |
| **Evidence Map** (NEW) | For each passing question, the specific PRD section + research source that supported it | Stage 4 Designer (knows which claims are validated vs. flagged) |
| **Design-Relevant Flags** (NEW) | Subset of flags that affect UX decisions: scope cuts (Q6), failure modes (Q9), technical constraints (Q7) | Stage 4 Designer (direct input) |

**Handoff Envelope to Stage 4 (Designer):**
- `gandalf-evaluation-v[N].md` (full — Designer needs the evidence map and flags)
- `prd-v[N].md` (full — Designer needs personas, JTBD, solution proposal, scope boundary)
- `research_executive_summary` (300 words — competitive context for design patterns)
- `user_constraints` — passed through from Stage 0
- `gandalf_design_flags` — extracted subset: scope cuts, failure modes, technical constraints that constrain the design

---

### Stage 4: Designer — Redefined Input Contract and Output Guarantees

**Current problem:** The Designer skill receives "approved PRD + Gandalf evaluation" as a blob. It has no structured way to extract what it needs: personas for task analysis, JTBD for information hierarchy, scope boundary for what to design vs. omit, competitive context for pattern selection. The Designer re-reads the entire PRD and cherry-picks what it thinks matters — leading to inconsistent quality.

**Redefined Input Contract:**

| Input Field | Required? | Source Stage | Extracted From | How Designer Uses It |
|-------------|-----------|-------------|----------------|---------------------|
| `primary_persona` | **Yes** | Stage 2 | PRD § Primary Persona | Seeds Phase 1 first-principles (primary user task, information needs, expertise level) |
| `secondary_persona` | **Yes** | Stage 2 | PRD § Secondary Persona | Informs expert-vs-novice design decisions (Checklist #9) |
| `jtbd_ranked` | **Yes** | Stage 2 | PRD § JTBD (all, with ranking) | Directly maps to information priority hierarchy (what user sees first = JTBD #1) |
| `solution_capabilities` | **Yes** | Stage 2 | PRD § Solution Proposal (all capabilities) | Each capability becomes a UI element. The Designer maps capability → component. |
| `scope_boundary_table` | **Yes** | Stage 2 | PRD § Scope Boundary | Designer only designs what's in v1 column. Everything else is explicitly omitted. |
| `success_metrics` | **Yes** | Stage 2 | PRD § Success Metrics | North Star metric becomes the most prominent data point in the UI. Anti-metrics inform what NOT to optimize in the design. |
| `gandalf_evidence_map` | **Yes** | Stage 3 | Gandalf § Evidence Map | Designer knows which PRD claims are validated (design with confidence) vs. flagged (design with flexibility/configurability). |
| `gandalf_design_flags` | **Yes** | Stage 3 | Gandalf § Design-Relevant Flags | Scope cuts → omit from design. Failure modes → design error states for these specific scenarios. Technical constraints → design within feasibility bounds. |
| `competitive_context` | **Yes** | Stage 1 (pruned) | Research § Executive Summary + Primary Competitor Thesis | Informs pattern selection: if primary competitor uses card grid (ServiceNow), consider whether to match or differentiate. |
| `user_constraints` | If present | Stage 0 | Original user input | Timeline constraints affect design ambition (tight timeline = fewer custom components). Technical stack constraints affect component selection. |
| `user_screenshots` | If present | Stage 0 | User-provided images | Screenshots of current UX become the baseline for improvement. Designer annotates: what works (keep), what fails (redesign), what's missing (add). |

**Pre-Design Structural Check (NEW):**

Before starting Phase 1, the Designer validates that every required input field is present and meets minimum depth:

| Input Field | Minimum Check | If Missing |
|-------------|---------------|------------|
| `primary_persona` | >= 150 words, includes role + daily responsibilities + tools | Emit `DEPENDENCY_GAP` to PRD Writer. Design with assumed "senior ops engineer" persona (degraded quality). |
| `jtbd_ranked` | >= 3 JTBDs with frequency + severity | Emit gap. Design based on solution capabilities (inferior — no task priority). |
| `scope_boundary_table` | Table with v1/v2/v3 columns + rationale | Emit gap. Assume all capabilities are v1 (risk of over-design). |
| `gandalf_design_flags` | At least Q6 + Q9 flags present | Proceed without — these enhance but don't block design. |

**Redefined Output Contract:**

The design spec must contain these sections, each validated before handoff:

| Section | Required? | Minimum Quality Bar | Validated How |
|---------|-----------|--------------------|----|
| Primary User Task | Yes | Single sentence derived from JTBD #1 | Traces to `jtbd_ranked[0]` |
| Information Priority | Yes | >= 3 priorities, each linked to a JTBD or persona need | Priority count + JTBD cross-reference |
| Critical User Journey | Yes | 5-7 steps, each with User Action + System Response + Data Shown + Component | Step count + all 4 columns populated |
| Alternatives Considered | Yes | >= 2 alternatives per major layout decision, with "Why Chosen Wins" | Alternative count >= 2 per decision |
| Cloudscape Component Mapping | Yes | Every UI element maps to a named Cloudscape component | No unmapped elements |
| Design Checklist | Yes | 10/10 criteria scored, minimum 7/10 >= 3 | Score validation |
| Error & Edge States | Yes | >= 4 states designed (empty, error, loading, partial) | State count >= 4 |
| Stickiness Design | Yes | >= 2 habit loops described | Loop count >= 2 |
| Handoff Notes for Prototype | Yes | >= 4 critical interactions listed + mock data spec + responsive breakpoints | Section present with subsections |
| **Nielsen Heuristic Audit** (NEW) | Yes | All 10 heuristics scored 1-5 with evidence | 10 scores present |
| **Interaction State Spec** (NEW) | Yes | Hover, focus, active, disabled states for interactive components | States documented per component |
| **Keyboard Navigation Spec** (NEW) | Yes | Tab order, focus management, shortcuts for power users | Spec present |

**Handoff Envelope to Stage 5 (Prototype Builder):**
- `design-spec-v[N].md` (full — Prototype Builder needs everything)
- `prd_executive_summary` (200 words — context only, not design input)
- `gandalf_design_flags` — passed through so Prototype Builder knows which error states to build
- `user_screenshots` — if provided, Prototype Builder uses as visual reference for layout fidelity

**Handoff Envelope to Stage 6 (Launch Readiness):**
- `design_component_mapping` — extracted table (which Cloudscape components, which configurations)
- `design_interaction_list` — extracted list of all interactive behaviors (for acceptance criteria generation)
- `design_error_states` — extracted table (for edge case acceptance criteria)
- `design_checklist_scores` — summary row (for quality assessment)

---

## Part 3: Context Pruning Redesign

### Current Pruning (problems)

```
Stage 2 gets: research-v1.md (full)
Stage 3 gets: latest prd version (full) + research-v1.md (summary only)
Stage 4 gets: latest prd version (full) + gandalf-evaluation (full) + research (summary)
Stage 5 gets: design-spec (full) + prd (executive summary only)
Stage 6 gets: all artifacts (executive summaries) + design-spec (full) + prototype path
```

Problems: (1) "summary" is undefined — how long? what sections? (2) no extracted fields, just blobs. (3) no user context passed after Stage 0. (4) no feedback mechanism for missing data.

### Redesigned Pruning (with handoff envelopes)

Each arrow below is a **handoff envelope** — a named, validated slice of the upstream artifact. The orchestrator extracts these programmatically (section heading match + word count validation), not by asking the agent to "summarize."

```
STAGE 0 (User Intake)
  │
  ├─ idea_text (mandatory) ──────────────────────── persists to ALL stages
  ├─ screenshots[] (optional) ──────────────────── → Stage 1, Stage 4, Stage 5
  ├─ urls[] (optional) ─────────────────────────── → Stage 1
  ├─ files[] (optional) ────────────────────────── → Stage 1
  └─ constraints (optional) ────────────────────── persists to ALL stages
        │
        ▼
STAGE 1 (Research)
  │
  ├─ research-v[N].md (FULL) ──────────────────── → Stage 2 (only stage that gets full research)
  │
  ├─ research_summary ─────────────────────────── → Stage 3, Stage 6
  │   (Extracted: Exec Summary + Key Takeaways
  │    + Market Data Table + TAM + Pricing Table
  │    ≈ 1,500 words max)
  │
  ├─ research_competitive_context ─────────────── → Stage 4
  │   (Extracted: Exec Summary + Primary Competitor
  │    Thesis + Implication for Us ≈ 600 words max)
  │
  ├─ research_pricing_table ───────────────────── → Stage 3 (for Q10 evaluation)
  │
  └─ research_customer_voice ──────────────────── → Stage 3 (for Q3 evaluation)
        │
        ▼
STAGE 2 (PRD Writer)
  │
  ├─ prd-v[N].md (FULL) ──────────────────────── → Stage 3 (evaluates entire PRD)
  │                                                 → Stage 4 (needs personas, JTBD, solution, scope)
  │
  ├─ prd_executive_summary ────────────────────── → Stage 5, Stage 6
  │   (Extracted: Exec Summary section ≈ 200 words)
  │
  ├─ prd_personas ─────────────────────────────── → Stage 4 (extracted: primary + secondary persona sections)
  ├─ prd_jtbd_ranked ──────────────────────────── → Stage 4 (extracted: full JTBD section with rankings)
  ├─ prd_solution_capabilities ────────────────── → Stage 4 (extracted: full Solution Proposal section)
  ├─ prd_scope_boundary ───────────────────────── → Stage 4 (extracted: scope boundary table)
  ├─ prd_success_metrics ──────────────────────── → Stage 4, Stage 6 (extracted: metrics section)
  │
  └─ prd_risks_open_questions ─────────────────── → Stage 6 (extracted: risks + open questions)
        │
        ▼
STAGE 3 (Gandalf)
  │
  ├─ gandalf-evaluation-v[N].md (FULL) ────────── → Stage 4
  │
  ├─ gandalf_evidence_map ─────────────────────── → Stage 4 (extracted: which claims are validated)
  ├─ gandalf_design_flags ─────────────────────── → Stage 4, Stage 5
  │   (Extracted: Q6 scope cuts + Q7 tech constraints
  │    + Q9 failure modes ≈ 400 words max)
  │
  ├─ gandalf_score_summary ────────────────────── → Stage 6
  │   (Extracted: score table + verdict line ≈ 200 words)
  │
  └─ gandalf_dependency_gaps ──────────────────── → Orchestrator (routes back to Stage 2 for patching)
        │
        ▼
STAGE 4 (Designer)
  │
  ├─ design-spec-v[N].md (FULL) ───────────────── → Stage 5
  │
  ├─ design_component_mapping ─────────────────── → Stage 6 (extracted: component table)
  ├─ design_interaction_list ──────────────────── → Stage 6 (extracted: critical interactions from handoff)
  ├─ design_error_states ──────────────────────── → Stage 6 (extracted: error/edge state table)
  └─ design_checklist_scores ──────────────────── → Stage 6 (extracted: score summary row)
        │
        ▼
STAGE 5 (Prototype Builder)
  │
  ├─ prototype-v[N].html ─────────────────────── → Stage 6 (path only — not the HTML content)
  └─ prototype-notes-v[N].md ──────────────────── → Stage 6 (full — used for validation results + known limitations)
        │
        ▼
STAGE 6 (Launch Readiness)
  │
  Receives:
  ├─ prd_executive_summary (200w)
  ├─ prd_success_metrics (full section)
  ├─ prd_risks_open_questions (full section)
  ├─ gandalf_score_summary (200w)
  ├─ gandalf_design_flags (400w)
  ├─ design_component_mapping (table)
  ├─ design_interaction_list (list)
  ├─ design_error_states (table)
  ├─ design_checklist_scores (summary)
  ├─ prototype path + prototype-notes (full)
  ├─ research_summary (1,500w)
  └─ user_constraints (from Stage 0)
```

### Extraction Rules

Each handoff envelope has a deterministic extraction rule — no LLM summarization needed:

| Envelope | Extraction Method |
|----------|-------------------|
| `research_summary` | Concatenate sections: `## Executive Summary` + `## Key Takeaways for PRD` + `## Quantitative Data` (all subsections). Truncate at 1,500 words. |
| `research_competitive_context` | Concatenate: `## Executive Summary` + `## Primary Competitor: [Name]` → subsections `### Their Thesis` + `### Implication for Us` only. Truncate at 600 words. |
| `research_pricing_table` | Extract: `### Pricing Comparison` table only. |
| `research_customer_voice` | Extract: `## Customer Voice (Direct)` section only. |
| `prd_executive_summary` | Extract: `## Executive Summary` section. Truncate at 250 words. |
| `prd_personas` | Extract: `### Primary Persona` + `### Secondary Persona` sections. |
| `prd_jtbd_ranked` | Extract: `### Jobs to Be Done` section. |
| `prd_solution_capabilities` | Extract: `## 2. Solution Proposal` section (all subsections). |
| `prd_scope_boundary` | Extract: `### Scope Boundary` table. |
| `prd_success_metrics` | Extract: `## 3. Success Metrics` section (all subsections). |
| `prd_risks_open_questions` | Extract: `## 6. Risks & Open Questions` section. |
| `gandalf_evidence_map` | Extract: `## Questions That Passed` section. |
| `gandalf_design_flags` | Extract: rows for Q6, Q7, Q9 from score table + their `## Questions Flagged` entries if present. |
| `gandalf_score_summary` | Extract: `## Verdict` line + `## Detailed Scores` table. |
| `gandalf_dependency_gaps` | Extract: all `DEPENDENCY_GAP` blocks emitted during evaluation. |
| `design_component_mapping` | Extract: `### Cloudscape Component Mapping` table. |
| `design_interaction_list` | Extract: `### Critical Interactions to Implement` list from Handoff Notes. |
| `design_error_states` | Extract: `## Error & Edge States` table. |
| `design_checklist_scores` | Extract: `## Phase 3: Design Checklist` table + score summary line. |

### Cross-Stage Feedback Protocol

When any stage emits a `DEPENDENCY_GAP`:

1. Orchestrator logs the gap in `pipeline-state.md` under a new `## Dependency Gaps` section
2. Orchestrator invokes the responsible upstream skill with a `PATCH` instruction containing: the gap description + the section to update + the artifact version to patch
3. Upstream skill patches and emits `prd-v[N+1].md` (or `research-v[N+1].md`)
4. Orchestrator re-extracts the affected handoff envelope
5. Orchestrator delivers the updated envelope to the requesting downstream stage
6. Downstream stage re-scores only the affected question/section

**This happens in parallel with the downstream stage continuing to process non-blocked questions.** The pipeline never waits — it parallelizes fixes with continued evaluation.

### Token Budget per Stage

To prevent context window overflow, each stage has a maximum input token budget:

| Stage | Max Input | Breakdown |
|-------|-----------|-----------|
| 1 (Research) | ~3,000 tokens | idea_text + urls + constraints + file summaries |
| 2 (PRD Writer) | ~12,000 tokens | research (full, 5K-7.5K words) + user_inputs |
| 3 (Gandalf) | ~15,000 tokens | prd (full, 5.5K-8K words) + research_summary (1.5K) + extracted tables |
| 4 (Designer) | ~18,000 tokens | prd (full) + gandalf (full) + competitive context (600w) + constraints |
| 5 (Prototype Builder) | ~10,000 tokens | design-spec (full) + prd summary (200w) + design flags |
| 6 (Launch Readiness) | ~8,000 tokens | All extracted envelopes (no full artifacts except prototype-notes) |
