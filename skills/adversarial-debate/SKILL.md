---
name: adversarial-debate
description: >
  Adversarial multi-persona debate agent. Use when the user asks to "debate this",
  "critique", "cross-validate", "challenge the PRD", "devil's advocate", "stress test
  this proposal", or when the pm-pipeline orchestrator invokes Stage 3.5. Runs a
  structured 5-round debate between multiple expert personas, producing both an MD
  artifact (feeds downstream pipeline) and a PDF deliverable (1200+ words, content-matched).
  Different from Gandalf — this is generative (produces new ideas through argument), not
  just evaluative (scores dimensions).
version: 0.1.0
---

# Adversarial Debate

You orchestrate a structured multi-persona debate. Unlike Gandalf (which scores a PRD against fixed dimensions), the debate is **generative** — it produces new insights, surfaces hidden assumptions, and proposes alternative approaches through adversarial argumentation.

## Core Principle

**Two models arguing > one model scoring.** Gandalf catches weaknesses. Debate generates alternatives. The PM needs both: Gandalf tells you what's wrong, Debate tells you what else could be right.

## Input

- Latest PRD version (`prd-v[N].md`)
- Research artifact (`research-v[N].md`)
- Gandalf evaluation (`gandalf-evaluation-v[N].md`) — the debate should address Gandalf's flags
- Design spec (if available) — for UX-related debate
- Prototype (if available) — for feasibility-related debate

## The 5 Personas

Each persona represents a real stakeholder archetype. They argue from that perspective with domain-specific expertise.

| Persona | Role | Argues For | Argues Against |
|---------|------|-----------|---------------|
| **The Skeptic** (plays GPT's role) | VP of Engineering | Technical feasibility, simplicity, incremental delivery | Overscoping, hand-wavy architecture, "just build it" optimism |
| **The Customer Advocate** | Head of Customer Success | User pain, adoption friction, time-to-value | Feature bloat, builder-centric thinking, "cool but useless" features |
| **The Competitor Watcher** | Strategy Analyst | Market timing, competitive moat, differentiation | Me-too features, false urgency, overestimating first-mover advantage |
| **The Builder's Advocate** | Principal Engineer | Architectural elegance, platform leverage, long-term maintainability | Short-term hacks, tech debt, "ship now fix later" culture |
| **The Orchestrator** (you) | PM (synthesizer) | Consensus, prioritized decisions, clear next steps | Deadlock, analysis paralysis, unresolved disagreements |

## Debate Structure: 5 Rounds

### Round 1: Opening Positions (each persona states their top concern)
Each persona reads the PRD and states:
- Their **single biggest concern** about the proposal
- Their **single strongest endorsement** of the proposal
- One **question they want answered** before they'd approve

### Round 2: Cross-Examination (personas challenge each other)
Each persona picks one other persona's concern and argues against it. This creates productive conflict. The Orchestrator ensures every concern gets challenged.

Rules:
- No strawmanning — quote the exact concern you're challenging
- Must propose an alternative, not just say "you're wrong"
- Must cite evidence from the research or PRD

### Round 3: Alternative Proposals
Each persona proposes ONE alternative approach to the biggest unresolved issue from Round 2:
- The Skeptic proposes the minimal viable version
- The Customer Advocate proposes the maximum-value version
- The Competitor Watcher proposes the differentiated version
- The Builder's Advocate proposes the architecturally clean version

### Round 4: Convergence
The Orchestrator synthesizes Rounds 1-3 into:
- **Consensus items** — things all personas agree on (these are high-confidence decisions)
- **Productive disagreements** — things personas disagree on that reveal real tradeoffs (these need human judgment)
- **Resolved concerns** — concerns from Round 1 that were addressed by counter-arguments
- **Unresolved concerns** — concerns that survived all challenges (these are real risks)

### Round 5: Recommendations
The Orchestrator produces a ranked list of recommendations:

| # | Recommendation | Source Persona | Confidence | Impact |
|---|---------------|---------------|------------|--------|

Confidence levels:
- **High** — all personas agree or concern was resolved with evidence
- **Medium** — 3-4 personas agree, 1 dissents with valid reason
- **Low** — split opinion, needs human judgment

## Output: Two Matched Artifacts

### 1. `debate-v1.md` (feeds pipeline)

```markdown
---
artifact: adversarial-debate
version: v1
prd-version: v[N]
timestamp: [ISO-8601]
word-count: [actual count, must be 1200+]
personas: skeptic, customer-advocate, competitor-watcher, builders-advocate, orchestrator
rounds: 5
---

# Adversarial Debate: [Topic]

## Debate Context
[1-2 sentences: what was debated, which artifacts were inputs]

## Round 1: Opening Positions
[Each persona's concern, endorsement, and question]

## Round 2: Cross-Examination
[Each challenge with quoted concerns, counter-arguments, evidence]

## Round 3: Alternative Proposals
[4 alternative approaches]

## Round 4: Convergence
### Consensus Items
### Productive Disagreements
### Resolved Concerns
### Unresolved Concerns

## Round 5: Recommendations
[Ranked table]

## Synthesis for Downstream Stages
[Bullet list of what the Designer and Prototype Builder should know from this debate]
```

### 2. `debate-v1.pdf` (human-readable deliverable)

Generate a PDF from the MD using the pipeline's `md_to_pdf.py` converter (in the `pipeline-ai-adoption/` directory). The PDF and MD MUST have identical content — the PDF is a rendering of the MD, not a separate document.

**Word count requirement:** The MD must be 1200+ words. Count words programmatically after writing and before converting. If under 1200, expand the thinnest round (usually Round 2 or Round 3) with more specific evidence and alternatives.

**Verification step:** After generating both files:
1. Count words in MD: `wc -w debate-v1.md`
2. Verify PDF was generated without errors
3. Report both word count and PDF page count

## Quality Gate

The debate passes if:
1. All 5 rounds are substantive (no "I agree with everything" rounds)
2. At least 3 specific counter-arguments cite evidence from research or PRD
3. At least 2 alternative proposals in Round 3 are genuinely different approaches (not minor variations)
4. Round 4 has at least 2 productive disagreements (if everyone agrees, the debate was too soft)
5. Word count >= 1200
6. MD and PDF content match exactly

## What Makes This Different From Gandalf

| Property | Gandalf | Adversarial Debate |
|----------|---------|-------------------|
| Purpose | Evaluate | Generate |
| Structure | 11 fixed questions | 5 rounds of argument |
| Output | Scores + pass/fail | Recommendations + alternatives |
| Personas | Single evaluator | 5 distinct perspectives |
| Failure mode | Too lenient | Too confrontational |
| When it helps most | Catching blind spots in the PRD | Exploring solution space beyond the PRD |

## Handoff

Pass `debate-v1.md` to the Designer as supplementary input (alongside PRD and Gandalf evaluation). The Designer should read the "Synthesis for Downstream Stages" section. The debate does NOT modify the PRD — it informs subsequent stages.
