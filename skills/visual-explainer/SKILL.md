---
name: visual-explainer
description: >
  Visual Explainer agent. Use when the user asks to "explain [concept] visually",
  "create an explainer", "build an interactive walkthrough", "teach me [feature]",
  "break down [concept]", "visual guide for [topic]", "product explainer",
  "explain how [product] works", or when any pipeline stage needs to produce a
  learning artifact. Generates explanation-led single-file interactive HTML with
  narrative arc, typed concept maps, scenario-based quizzes, structural analogies,
  and progressive disclosure — all grounded in cognitive science. v1.0.0 is
  explanation-led (not component-led): the Explanation Plan determines what to
  teach and in what order BEFORE any HTML is written.
version: 1.0.0
---

# Visual Explainer Agent

Generate single-file interactive HTML explainers that teach concepts through narration + visuals + quizzes + analogies. The output is a self-contained `.html` file that opens in any browser — no build step, no dependencies beyond CDN-hosted Chart.js.

**v1.0.0 core change: Explanation-led, not component-led.** The previous version started from components (concept map, tabs, quiz blocks) and filled them with content. This version starts from an Explanation Plan — what the audience needs to learn, in what order, through what narrative — and then selects components to serve the explanation. Components are tools, not templates.

## Content Type Classification (Step -1)

Before anything else, classify the input:

| Content Type | Description | Explanation Strategy | Example |
|-------------|-------------|---------------------|---------|
| **Product Explainer** | Explains a product/feature — what it does, who it's for, how it works, why it matters | Problem → Solution → How It Works → Architecture → Differentiation → Value | "Explain Amazon Quick AI Control Tower" |
| **Concept Explainer** | Teaches an abstract concept — what it is, why it matters, how it relates to other concepts | Definition → Why It Matters → How It Works → Examples → Edge Cases → Misconceptions | "Explain distributed tracing" |
| **Process Explainer** | Teaches a workflow or sequence — steps, decisions, branching | Start → Steps → Decisions → Outcomes → Variations → Pitfalls | "Explain the CI/CD pipeline" |
| **Comparison Explainer** | Compares alternatives — when to use each, tradeoffs | Criteria → Option A → Option B → Head-to-Head → Decision Guide | "Compare SLOs vs SLAs vs SLIs" |
| **Architecture Explainer** | Explains a system's structure — layers, components, data flow, integration points | Problem → Components → Relationships → Data Flow → Failure Modes → Scale | "Explain the OpenTelemetry architecture" |

Each type has a different natural narrative arc. The Explanation Plan must follow the arc for its type.

## Audience Detection

Detect or infer the audience before planning:

| Audience | Signals | Depth | Analogy Sources | Quiz Style |
|----------|---------|-------|----------------|------------|
| **Executive / Non-technical** | "explain to leadership", "board presentation", "for my CIO" | Outcome-first, minimal architecture, focus on business impact | Business analogies (supply chain, retail, finance) | Scenario: "Your CEO asks you..." |
| **PM / Business** | "product explainer", pipeline artifact, "for stakeholders" | Problem-led, competitive context, feature walkthrough | Product analogies (Salesforce, ServiceNow, familiar enterprise tools) | Scenario: "A customer asks why..." |
| **Technical / Engineering** | "how does it work", "architecture", "explain the system" | Architecture-first, data flow, edge cases, failure modes | Engineering analogies (databases, networking, compilers) | Scenario: "Your service is throwing..." |
| **Mixed / General** | No clear signal, or broad topic | Layered — Quick Take for execs, Deep Dive for engineers | Mixed — start simple, get technical | Progressive — recall → comprehension → application |

The audience determines analogy source domains, quiz difficulty baseline, and how much architecture detail to show.

## Cognitive Science Foundation (Non-Negotiable Design Rules)

These 5 pillars are research-backed. Every design decision must satisfy at least one. Violating any is a quality failure.

### Pillar 1: Dual Coding Theory (Paivio, 1971)
The brain stores visuals two ways (image + verbal label) vs text one way. Pictures are recalled 6-600x better than text alone.

**Design rule:** Every concept gets BOTH a visual AND a verbal explanation, side by side, in the same viewport. No text-only sections. No unlabeled diagrams.

### Pillar 2: Mayer's Multimedia Principles (Mayer, 2009)

| Principle | Rule | Implementation |
|-----------|------|---------------|
| **Coherence** | Cut extraneous info (reduces cognitive load 30-50%) | Max 3 bullet points per card, max 2 sentences per intro |
| **Signaling** | Highlight key elements with arrows, color, labels | Every diagram has labeled annotations — no bare visuals |
| **Spatial Contiguity** | Related words and pictures physically close | Visual and explanation in same viewport, never "see below" |
| **Segmenting** | Break complex info into learner-paced chunks | 4-level tab system (Quick Take → Overview → Detail → Deep Dive) |
| **Multimedia** | Words + pictures always, never text-only | Every section has a visual component |
| **Personalization** | Conversational tone, not formal | Use "you" and "your", not "the user" |

### Pillar 3: Testing Effect / Retrieval Practice (Roediger & Karpicke, 2006)
Quizzes improve retention 30-50% vs passive review. Key design rules:
- **Desirable difficulty:** Questions should be just outside comfort zone
- **Explanatory feedback:** Every wrong answer teaches WHY it's wrong
- **Interleaving:** Mix questions across concepts in the final quiz
- **Spaced placement:** Quiz after every 2-3 sections
- **3-tier difficulty:** Recall → Comprehension → Application

### Pillar 4: Analogy-Based Learning (Gentner's Structure-Mapping Theory)
Map unfamiliar concepts to familiar source domains. Analogies must be **structural, not surface-level**: map 3 specific attributes from source → target, not just "it's like a highway."

**Design rule:** Every major concept gets a mandatory "Think of it like..." analogy box. Each analogy must:
1. Name the source domain explicitly (and choose it based on audience — see Audience Detection)
2. Map 3 specific structural attributes (not vague resemblances)
3. State where the analogy breaks down (the "but unlike..." caveat)

**Anti-pattern:** "Shadow AI is like an iceberg — most is hidden." This is a surface metaphor, not a structural analogy.
**Pattern:** "Shadow AI is like unauthorized building extensions in a city. (1) Each resident adds them for convenience → each team adopts AI tools for productivity. (2) The city planning office can't track them → IT can't inventory them. (3) When the fire inspector comes, the city is liable → when the auditor comes, the company is liable. But unlike building extensions, shadow AI can be detected remotely through endpoint monitoring."

### Pillar 5: Schema Theory & Concept Adjacency (Bartlett, Piaget)
New knowledge is retained when anchored to existing schema. The concept adjacency map builds neural scaffolding.

**Design rule:** Every explainer includes a Concept Map — an interactive node graph showing how the explained concept connects to related concepts. Nodes must be typed (see Typed Concept Map below).

## Explanation Plan (Step 0 — MANDATORY GATE)

**This is the v1.0.0 structural change.** Before writing ANY HTML, produce a complete Explanation Plan. The plan determines what to teach and in what order. Components serve the plan — the plan does not serve components.

### Explanation Plan Structure

```markdown
## Explanation Plan

### Teaching Objective
[One sentence: "After reading this, the audience will understand [X] well enough to [Y]."]

### Audience
[Detected audience type + key signals]

### Content Type
[Product / Concept / Process / Comparison / Architecture]

### Narrative Arc
[The natural arc for this content type, customized to the specific topic]

| # | Section | What the Audience Learns | Why It's Here (Narrative Position) | Visual Type | Analogy |
|---|---------|-------------------------|-----------------------------------|------------|---------|
| 1 | [title] | [learning outcome] | [Sets up the problem / Defines the concept / Shows how it works / etc.] | [specific visual] | [specific analogy or "none — concept already familiar"] |
| 2 | [title] | [learning outcome] | [Builds on section 1 by...] | [specific visual] | [if new concept] |
| ... | | | | | |

### Concept Inventory
[Every concept that will be introduced, with:]
| Concept | Type | Defined In Section | First Visualized In | Prerequisite Concepts |
|---------|------|-------------------|--------------------|-----------------------|

**Rule:** A concept must be DEFINED before it is VISUALIZED. A concept must be VISUALIZED before it is QUIZZED.

### Concept Map Plan
[Center node + all adjacent nodes, typed by category:]
| Node | Type | Color | Connects To | Edge Label | Section Link |
|------|------|-------|-------------|------------|-------------|

**Node types for concept maps:**
- **Persona** (cyan) — who uses or is affected by this
- **Problem** (red) — what pain or gap exists
- **Capability** (accent/copper) — what the product/concept does
- **Data Source** (blue) — where information comes from
- **System Component** (purple) — technical building blocks
- **Competitor** (yellow) — alternative approaches
- **Metric** (green) — how success is measured
- **Risk** (red-bg) — what can go wrong

### Quiz Plan
| # | After Section | Difficulty | Question Type | Tests Concept | Persona-Grounded? |
|---|--------------|------------|---------------|---------------|:-----------------:|
| 1 | 1-2 | Recall | Definition | [concept] | No |
| 2 | 1-2 | Recall | Identify | [concept] | No |
| 3 | 1-2 | Comprehension | "Why" | [concept] | Optional |
| 4 | 3-4 | Comprehension | Compare | [concepts] | Yes |
| ... | | | | | |
| 15 | Final | Application | Scenario | [multiple concepts] | Yes — name the persona |

**Quiz question types:**
- **Definition (Recall):** "What is X?" — basic identification
- **Identify (Recall):** "Which of these is an example of X?"
- **"Why" (Comprehension):** "Why does X matter for Y?" — tests understanding, not memory
- **Compare (Comprehension):** "How does X differ from Y?" — tests conceptual boundaries
- **Scenario (Application):** "Lisa (IT Director) sees X in her dashboard. What should she do?" — tests ability to apply knowledge in context. MUST name a realistic persona.
- **Misconception (Application):** "A colleague says X. What's wrong with that claim?" — tests depth

**Minimum 4 scenario-based questions.** At least 2 must name a persona from the source material.

### Analogy Inventory
| Concept | Source Domain | Why This Domain (Audience Match) | 3 Structural Mappings | Where Analogy Breaks |
|---------|-------------|--------------------------------|----------------------|---------------------|

### "So What" Synthesis Plan
[What's the single most important takeaway? How will the final section tie everything together?]
```

**Quality gate:** If the Explanation Plan cannot fill the Narrative Arc table coherently — if sections feel parallel rather than sequential — the plan needs revision before proceeding.

## Core Design Patterns

### Pattern 1: Narrative Arc (not Parallel Sections)

**v0.2.0 failure mode:** Sections were parallel — each covered a topic independently. There was no narrative progression. Reading section 4 didn't require section 3.

**v1.0.0 rule:** Sections must form a narrative arc appropriate to the content type:

**Product Explainer Arc:**
1. The Problem (pain, scale, urgency) — "Why does this matter?"
2. The Vision (what if this problem were solved?) — "Imagine if..."
3. How It Works (capabilities, architecture) — "Here's how"
4. Who Benefits (personas, journeys) — "Meet the people"
5. System Under the Hood (architecture, data flow) — "What makes it tick"
6. Competitive Landscape (alternatives, differentiation) — "Why this approach"
7. The Path Forward (roadmap, maturity) — "Where this is going"
8. Synthesis ("So What" — the single takeaway) — "Here's what to remember"

**Concept Explainer Arc:**
1. The Definition (precise, jargon-free) → 2. Why It Matters (consequences of not understanding) → 3. How It Works (mechanism) → 4. Examples (concrete instances) → 5. Edge Cases (where intuition fails) → 6. Misconceptions (common errors) → 7. Related Concepts (adjacency) → 8. Synthesis

**Each section explicitly builds on the previous.** State the connection: "Now that you understand [section N], let's see [section N+1]."

### Pattern 2: Progressive Disclosure (4 Levels)
- **Quick Take** (15 sec): Hero stats + concept map + 1 key diagram
- **Overview** (1 min): Key concepts with visuals + analogy bridges
- **Detail** (3 min): Data, comparisons, evidence tables
- **Deep Dive** (10 min): Architecture, edge cases, competitive analysis

### Pattern 3: One Visual Type Per Concept
Match the visual to the concept type:

| Concept Type | Best Visual | When to Use |
|-------------|------------|------------|
| Process / sequence | Funnel or flow diagram | Pipeline stages, user journeys |
| Hierarchy / layers | Architecture stack | Tech stacks, platform layers |
| Comparison | Split diagram or comparison table | Us vs. competitor, before vs. after |
| Relationships | Typed concept map (node graph) | System dependencies, concept adjacency |
| Progress / maturity | Maturity ladder | Adoption levels, readiness stages |
| Quantitative | Chart.js bar/line/radar | Market data, metrics, benchmarks |
| Decision | Flowchart with branches | Build vs. buy, go/no-go |
| Timeline | Horizontal timeline | Feature evolution, competitor moves |
| Analogy mapping | Analogy bridge (source ↔ target) | New concepts mapped to familiar ones |
| **System architecture** (v1.0.0) | Layer diagram with data flow arrows | Product internals, platform structure |
| **Customer journey** (v1.0.0) | Horizontal swim-lane with personas | End-to-end user experience across touchpoints |
| **Definition** (v1.0.0) | Definition card with icon + key attributes | New term introduction, concept boundary-setting |

### Pattern 4: Typed Concept Map (v1.0.0 — replaces generic concept map)

The concept map is NOT decorative. Each node represents a typed entity from the source material. The map is a functional navigation tool and a schema-building device.

**Node typing rules:**
- Every node has a type from the Concept Inventory (persona, problem, capability, data source, system component, competitor, metric, risk)
- Node color comes from type, not arbitrary assignment
- Edge labels are semantic: "causes", "solves", "measures", "threatens", "enables", "competes with", "feeds into"
- Clicking a node scrolls to the section where that concept is DEFINED (not just mentioned)
- Hovering shows a 1-sentence definition tooltip

**Node color mapping:**
| Type | Color Variable | Background | Border |
|------|---------------|------------|--------|
| Persona | `--cyan` | rgba(23,162,184,0.08) | rgba(23,162,184,0.35) |
| Problem | `--red` | rgba(192,57,43,0.08) | rgba(192,57,43,0.3) |
| Capability | `--accent` | rgba(204,120,92,0.08) | rgba(204,120,92,0.35) |
| Data Source | `--blue` | rgba(41,128,185,0.08) | rgba(41,128,185,0.4) |
| System Component | `--accent2` | rgba(124,111,205,0.08) | rgba(124,111,205,0.4) |
| Competitor | `--yellow` | rgba(212,160,23,0.08) | rgba(212,160,23,0.3) |
| Metric | `--green` | rgba(42,157,98,0.08) | rgba(42,157,98,0.3) |
| Risk | `--red` (darker) | rgba(192,57,43,0.1) | rgba(192,57,43,0.35) |
| Center (main topic) | `--accent` | rgba(204,120,92,0.12) | var(--accent) |

**Minimum requirements:**
- Center node = the topic being explained
- At least 6 adjacent nodes spanning at least 3 different types
- Every edge has a semantic label
- Every node links to a section

### Pattern 5: Analogy Bridge (enhanced v1.0.0)

Each analogy bridge must have:
1. **Source domain** explicitly named, chosen for audience match
2. **3 structural mappings** — specific attribute-to-attribute (not vague resemblance)
3. **"Where it breaks" caveat** — every analogy has limits, state them
4. **Visual side-by-side** with labeled mapping arrows

CSS class: `.analogy-bridge` — see `references/component-library.md`

### Pattern 6: Quiz System (v1.0.0 — scenario-grounded)

15 questions across 4 quiz blocks, but with new quality requirements:

| Placement | After | # Qs | Difficulty | Focus | Persona Required? |
|-----------|-------|:----:|------------|-------|:-----------------:|
| Quiz 1 | Sections 1-2 | 3 | Recall | "What is X?" / "Which is X?" | No |
| Quiz 2 | Sections 3-4 | 4 | Comprehension | "Why does X matter?" / "How does X differ from Y?" | At least 1 |
| Quiz 3 | Sections 5-6 | 4 | Application | "Given scenario Y, what would you do?" | At least 2 |
| Final | End | 4 | Interleaved | Mix of all levels, cross-section | At least 1 |

**Question quality rules:**
- Never "Which of these is true?" — that's lazy recall
- Never "All of the above" or "None of the above" — these test test-taking, not knowledge
- Scenario questions MUST name a realistic persona: "Raj (Head of IT Ops) notices..." not "A user notices..."
- Wrong answer explanations must teach through the mistake (1-2 sentences explaining WHY it's wrong and WHAT the right reasoning is)
- Final quiz interleaves topics across ALL sections

### Pattern 7: "Why This Matters" Callouts
Before each visual section, a highlighted callout connecting to the audience's actual work:
```html
<div class="why-callout">
  <span class="why-label">WHY THIS MATTERS</span>
  <p>[1 sentence connecting to the audience's actual work or decision]</p>
</div>
```

### Pattern 8: "So What" Synthesis Section (NEW v1.0.0)

The final section before the last quiz. NOT a summary — a synthesis that connects everything:

1. **The single most important takeaway** (one sentence, bold)
2. **How the pieces fit together** (2-3 sentences connecting the narrative arc)
3. **What to do with this knowledge** (1-2 sentences — specific next actions for the audience)
4. **The open question** (1 sentence — what remains unresolved or worth watching)

This section prevents the explainer from ending with a whimper. The audience should leave with a clear "so what."

### Pattern 9: Definition Cards (NEW v1.0.0)

When introducing a new concept for the first time, use a definition card:

```html
<div class="definition-card">
  <div class="def-icon">[emoji or icon]</div>
  <div class="def-content">
    <h4 class="def-term">[Term]</h4>
    <p class="def-definition">[Plain-language definition, max 2 sentences]</p>
    <div class="def-attributes">
      <span class="def-attr"><strong>Type:</strong> [persona/capability/system/etc.]</span>
      <span class="def-attr"><strong>Key property:</strong> [most important attribute]</span>
      <span class="def-attr"><strong>Common misconception:</strong> [what people get wrong]</span>
    </div>
  </div>
</div>
```

Use definition cards for the first 3-5 key concepts, then transition to inline definitions for familiarity.

## Design System

### The Dark Theme (mandatory)

```css
:root {
  --bg: #0d0d0f;
  --surface: #17171a;
  --surface2: #1e1e22;
  --surface3: #252529;
  --border: #2e2e35;
  --text: #e8e8ed;
  --text-muted: #8888a0;
  --text-dim: #5a5a70;
  --accent: #cc785c;       /* warm copper — primary actions, highlights */
  --accent2: #7c6fcd;      /* purple — secondary, labels */
  --green: #2a9d62;        /* success, correct answers */
  --green-bg: rgba(42,157,98,0.12);
  --red: #c0392b;          /* failure, wrong answers */
  --red-bg: rgba(192,57,43,0.1);
  --yellow: #d4a017;       /* warning, WIP */
  --yellow-bg: rgba(212,160,23,0.12);
  --blue: #2980b9;         /* info, technical domain */
  --cyan: #17a2b8;         /* tertiary, user domain */
}
```

### Typography
- Font: `-apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif`
- Body: 15px, line-height 1.7
- Headings: font-weight 600, letter-spacing -0.02em
- Labels/eyebrows: 11-12px, uppercase, letter-spacing 0.06-0.12em

### Layout
- Max-width: 1200px centered
- Padding: 48px horizontal (20px on mobile)
- Section spacing: 64px margin-top
- Card border-radius: 12px
- **Spatial contiguity:** visual and its text explanation must fit in one viewport (~700px)
- **Content density rule (v1.0.0):** Every viewport-height of scrolling must deliver at least one new insight. If a section is mostly chrome (borders, spacing, decorative elements) without substance, it needs rewriting.

### Required Components (see references/component-library.md)
Every explainer must include:
1. **Scroll progress bar** (fixed top, gradient accent→accent2)
2. **Sticky nav** with section tabs (backdrop-filter blur)
3. **Hero section** with 3-5 key stats (big numbers) and 1-sentence summary
4. **Typed Concept Map** (interactive node graph with typed nodes, after hero)
5. **At least 5 visual sections** following the narrative arc (not parallel)
6. **Analogy bridges** for every major new concept (minimum 3, each with 3 structural mappings + caveat)
7. **Definition cards** for first 3-5 key concepts
8. **"Why This Matters" callouts** before each section
9. **Tab panels** for 4-level progressive disclosure
10. **4 quiz blocks** with 15 total questions (minimum 4 scenario-based with named personas)
11. **Score tracker** with running score and final personalized feedback
12. **"So What" synthesis section** before final quiz
13. **Footer** with generation timestamp

## Input Sources

The Visual Explainer can be invoked on:
- **A pipeline artifact** (research, PRD, design spec) → Product Explainer type
- **A concept** (how guardrails work, what SLOs mean) → Concept Explainer type
- **A comparison** (us vs. competitors, before vs. after) → Comparison Explainer type
- **A process** (how the pipeline works, deployment flow) → Process Explainer type
- **An architecture** (system internals, platform layers) → Architecture Explainer type

## Build Process

### Step 0: Explanation Plan (MANDATORY GATE — do not skip)

Before writing any HTML, produce the complete Explanation Plan (see structure above). The plan must include:
- Teaching objective (one sentence)
- Audience detection
- Content type classification
- Full narrative arc table (sections, learning outcomes, narrative position, visual types, analogies)
- Concept inventory with definition order and prerequisites
- Typed concept map plan
- Quiz plan with 15 questions, difficulty progression, persona grounding
- Analogy inventory with structural mappings and caveats
- "So What" synthesis plan

**Quality gate:** Read the Narrative Arc table top-to-bottom. If it tells a coherent story (each section builds on the previous), proceed. If sections feel interchangeable or parallel, revise the plan.

### Step 1: Content Outline Validation

Validate the Explanation Plan against the source material:
- Every claim in the plan must be traceable to the source artifact
- Every statistic in the hero section must come from the source, not be invented
- Every quiz answer must be derivable from the explainer content
- Every analogy source domain must be appropriate for the detected audience

### Step 2: Build HTML

Single file. All CSS in `<style>`, all JS at bottom in `<script>`. Only external dependency: Chart.js via CDN.

Structure:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Topic] — Visual Explainer</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <style>/* Full design system + component styles from component-library.md */</style>
</head>
<body>
  <div class="scroll-progress" id="scrollProgress"></div>
  <nav class="sticky-nav">...</nav>
  <section class="hero">...</section>
  <div class="container">
    <!-- Typed Concept Map (functional, not decorative) -->
    <!-- Sections following Narrative Arc — each builds on previous -->
    <!-- Definition cards for first key concepts -->
    <!-- Quiz 1 (recall) after sections 1-2 -->
    <!-- Quiz 2 (comprehension) after sections 3-4 -->
    <!-- Quiz 3 (application) after sections 5-6 -->
    <!-- "So What" Synthesis section -->
    <!-- Final Quiz (interleaved) -->
    <!-- Score summary -->
  </div>
  <footer class="footer">...</footer>
  <script>/* All interactive JS */</script>
</body>
</html>
```

**Content density enforcement (v1.0.0):**
- Every section must introduce at least one NEW insight, data point, or concept
- No section should be pure visual with no explanatory text
- No section should be pure text with no visual
- Decorative chrome (gradient lines, animated dots, etc.) should not exceed 10% of any section's vertical space
- If a section can be removed without breaking the narrative arc, it shouldn't exist

### Step 3: Validate

Open in browser and verify:

**Structural checks:**
- [ ] Scroll progress bar works
- [ ] Sticky nav highlights active section on scroll
- [ ] All tabs switch correctly (4 levels per section)
- [ ] All collapsibles expand/collapse
- [ ] Responsive at 375px width
- [ ] No JS console errors
- [ ] All hover states work

**Concept Map checks (v1.0.0):**
- [ ] Every node is typed (has the correct color for its type)
- [ ] Every edge has a semantic label (not just connecting lines)
- [ ] Clicking a node scrolls to the section where that concept is DEFINED
- [ ] Hovering a node shows a 1-sentence definition tooltip
- [ ] At least 6 nodes spanning at least 3 types

**Narrative checks (v1.0.0):**
- [ ] Sections follow the narrative arc (not parallel/interchangeable)
- [ ] Each section explicitly references what was learned in the previous section
- [ ] Definition cards appear BEFORE concepts are visualized or quizzed
- [ ] "So What" synthesis section exists before the final quiz
- [ ] Every section delivers at least one new insight (no padding)

**Quiz checks (v1.0.0):**
- [ ] All 15 quiz questions score correctly
- [ ] At least 4 questions are scenario-based with named personas
- [ ] Every wrong answer has explanatory feedback (1-2 sentences)
- [ ] Final quiz interleaves topics across all sections
- [ ] No "which is true" or "all of the above" questions
- [ ] Score tracker updates correctly

**Analogy checks (v1.0.0):**
- [ ] Every analogy has 3 structural mappings (not surface metaphors)
- [ ] Every analogy has a "where it breaks" caveat
- [ ] Source domains are appropriate for the detected audience
- [ ] At least 3 analogy bridges total

**Content quality checks (v1.0.0):**
- [ ] All data is real (from source artifact), not placeholder
- [ ] Hero stats come from source material
- [ ] Visual-to-insight ratio: every viewport of scrolling delivers substance
- [ ] "Why This Matters" callouts are specific to audience's work (not generic)
- [ ] Spatial contiguity: every visual + explanation fits in one viewport

## Output

Single file: `[topic-slug]-explainer.html` saved to the pipeline output directory.

Target: 1,200-2,000 lines of HTML. Under 1,200 = too shallow. Over 2,000 = probably padding.

## Quality Checklist

### Explanation Plan Quality
- [ ] Teaching objective stated in one sentence
- [ ] Audience detected and strategy adjusted
- [ ] Content type classified (product/concept/process/comparison/architecture)
- [ ] Narrative arc follows the appropriate arc for the content type
- [ ] Concept inventory complete with definition order and prerequisites
- [ ] No concept is quizzed before it is defined and visualized

### Narrative Quality
- [ ] Sections form a narrative arc (not parallel topics)
- [ ] Each section builds on the previous (explicit connection stated)
- [ ] "So What" synthesis exists and is substantive (not just a summary)
- [ ] Every viewport of scrolling delivers at least one new insight
- [ ] Content density > chrome density in every section

### Concept Map Quality
- [ ] Nodes are typed (persona, problem, capability, data source, system, competitor, metric, risk)
- [ ] Edges have semantic labels
- [ ] At least 6 nodes, 3+ types
- [ ] Click-to-scroll works for every node
- [ ] Hover tooltips show definitions

### Analogy Quality
- [ ] 3+ analogy bridges, each with 3 structural mappings
- [ ] Source domains are audience-appropriate
- [ ] Every analogy has a "where it breaks" caveat
- [ ] No surface metaphors masquerading as structural analogies

### Quiz Quality
- [ ] 15 questions, 4 blocks, 3-tier difficulty
- [ ] 4+ scenario-based questions with named personas
- [ ] 0 lazy questions ("which is true", "all of the above")
- [ ] Every wrong answer has 1-2 sentence explanatory feedback
- [ ] Final quiz interleaves across all sections

### Technical Quality
- [ ] Dual coding: every concept has visual + verbal, side by side
- [ ] Mayer's coherence: max 3 bullets per card, max 2 sentences per intro
- [ ] Mayer's signaling: every diagram has labeled annotations
- [ ] Mayer's spatial contiguity: visual + explanation in same viewport
- [ ] Hero section has 3-5 key stats from source material
- [ ] Dark theme with correct color palette
- [ ] Responsive at mobile widths
- [ ] No external dependencies except Chart.js CDN
- [ ] Total file size between 1,200-2,000 lines

## Eval Learnings Log

### v0.2.0 → v1.0.0 (2026-05-20, full structural rewrite based on user + GPT critique)

**Root cause:** v0.2.0 was component-led — it started from components (concept map, tabs, quiz blocks) and filled them with content. This produced explainers with good individual components but weak narrative coherence, shallow analogies, decorative concept maps, generic quizzes, and sections that felt parallel rather than sequential.

| # | Gap Identified | Fix Applied | Category |
|---|---------------|-------------|----------|
| 1 | Skill is component-led, not explanation-led | Added Explanation Plan as mandatory Step 0 gate — determines teaching objective, narrative arc, concept inventory before any HTML | Content Architecture |
| 2 | No content type classification | Added 5 content types (product/concept/process/comparison/architecture) with different narrative arcs | Content Architecture |
| 3 | No audience detection | Added audience detection (executive/PM/technical/mixed) that determines analogy sources, quiz difficulty, depth | Content Architecture |
| 4 | No product explainer template | Product Explainer arc: Problem → Vision → How → Who → Architecture → Competition → Path → Synthesis | Content Architecture |
| 5 | Sections are parallel, not sequential | Narrative Arc pattern requires each section to build on the previous with explicit connections | Content Architecture |
| 6 | No "what you'll learn" contract | Teaching objective is the first line of the Explanation Plan | Content Architecture |
| 7 | Concepts not defined before visualized | Concept Inventory tracks definition order and prerequisites — definition cards must appear before visualization | Problem & Concept Definition |
| 8 | No definition card component | Added Pattern 9: Definition Card with term, definition, type, key property, common misconception | Problem & Concept Definition |
| 9 | Concept maps are decorative | Typed Concept Map: nodes typed by category (persona/problem/capability/data source/system/competitor/metric/risk), edges labeled semantically | Concept Map Quality |
| 10 | Node types arbitrary | 8 explicit node types with color mapping and semantic meaning | Concept Map Quality |
| 11 | Edges have no semantics | Edge labels mandatory: "causes", "solves", "measures", "enables", etc. | Concept Map Quality |
| 12 | Quiz questions are generic recall | Minimum 4 scenario-based questions with named personas; banned "which is true" and "all of the above" | Quiz System |
| 13 | No persona-grounded quiz scenarios | Quiz plan requires persona grounding; scenarios must name realistic personas from source material | Quiz System |
| 14 | Analogies are surface-level | Structural analogy requirement: 3 attribute-to-attribute mappings + "where it breaks" caveat | Analogy System |
| 15 | No audience-appropriate source domain selection | Analogy source domains must match detected audience (business analogies for execs, engineering for technical) | Analogy System |
| 16 | No "so what" synthesis at end | Pattern 8: "So What" Synthesis — takeaway, connections, next actions, open question | Narrative Structure |
| 17 | Too much chrome, not enough substance | Content density rule: every viewport must deliver at least one new insight; decorative chrome max 10% of section height | Content Density |
| 18 | No system architecture diagram pattern | Added to visual type table; component-library.md updated with CSS pattern | Component Library |
| 19 | No customer journey pattern | Added swim-lane journey pattern to visual types | Component Library |
| 20 | Visual-to-insight ratio low | Explicit check: every section must introduce at least one NEW insight, data point, or concept | Content Density |
| 21 | No content outline validation before HTML | Step 1 validates plan against source material — stats must be real, quiz answers derivable | Build Process |
| 22 | File size target too small for v1.0.0 depth | Increased to 1,200-2,000 lines | Build Process |

**Preserved from v0.2.0:**
- 5 cognitive science pillars (Dual Coding, Mayer, Testing Effect, Analogy, Schema Theory)
- 4-level progressive disclosure (Quick Take → Overview → Detail → Deep Dive)
- Dark theme design system with CSS variables
- Score tracker with personalized final feedback
- Scroll progress bar, sticky nav, "Why This Matters" callouts
- Single-file HTML output with Chart.js CDN
