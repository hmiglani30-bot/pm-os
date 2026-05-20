---
name: visual-explainer
description: >
  Visual Explainer agent. Use when the user asks to "explain [concept] visually",
  "create an explainer", "build an interactive walkthrough", "teach me [feature]",
  "break down [concept]", "visual guide for [topic]", or when any pipeline stage
  needs to produce a learning artifact. Generates single-file interactive HTML
  with narration, diagrams, tabs, quizzes, analogy bridges, concept maps, and
  progressive disclosure — all grounded in cognitive science.
version: 0.2.0
---

# Visual Explainer Agent

Generate single-file interactive HTML explainers that teach concepts through narration + visuals + quizzes + analogies. The output is a self-contained `.html` file that opens in any browser — no build step, no dependencies beyond CDN-hosted Chart.js.

## Cognitive Science Foundation (Non-Negotiable Design Rules)

These 5 pillars are research-backed. Every design decision must satisfy at least one. Violating any is a quality failure.

### Pillar 1: Dual Coding Theory (Paivio, 1971)
The brain stores visuals two ways (image + verbal label) vs text one way. Pictures are recalled 6-600x better than text alone. Half the cerebral cortex is dedicated to visual processing.

**Design rule:** Every concept gets BOTH a visual AND a verbal explanation, side by side, in the same viewport. No text-only sections. No unlabeled diagrams.

### Pillar 2: Mayer's Multimedia Principles (Mayer, 2009)
12 principles for multimedia learning. The 6 that matter most for explainers:

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
- **Desirable difficulty:** Questions should be just outside comfort zone — not trivial, not impossible
- **Explanatory feedback:** Every wrong answer teaches WHY it's wrong (strengthens the correct memory trace)
- **Interleaving:** Mix questions across concepts (not grouped by section) for deeper encoding
- **Spaced placement:** Quiz after every 2-3 sections, not just at the end (spaced retrieval)
- **3-tier difficulty:** Recall → Comprehension → Application (progressive challenge)

### Pillar 4: Analogy-Based Learning (Gentner's Structure-Mapping Theory)
Map unfamiliar concepts to familiar source domains. Analogies create "cognitive bridges" — the brain processes the new concept through existing neural pathways of the familiar domain.

**Design rule:** Every major concept gets a mandatory "Think of it like..." analogy box with a visual side-by-side showing source domain → target domain mapping.

Example:
> "Think of AI guardrails like highway guardrails — they don't steer the car (the model), they prevent it from going off the cliff (harmful outputs). The guardrail doesn't know where you're going; it just knows where you shouldn't be."

### Pillar 5: Schema Theory & Concept Adjacency (Bartlett, Piaget)
New knowledge is retained when anchored to existing schema. Showing how a new concept relates to adjacent known concepts builds the neural scaffolding for long-term storage.

**Design rule:** Every explainer includes a Concept Adjacency Map — an interactive node graph showing how the explained concept connects to related concepts. This is the "mental model anchor" placed after the hero section.

## Core Design Patterns

### Pattern 1: Narration-First, Visual-Second
Every section follows this flow:
1. **Eyebrow label** (category/context in small caps)
2. **"Why This Matters" callout** — 1 sentence connecting to the user's actual work/decision
3. **Section title** (what you'll learn)
4. **Intro paragraph** (plain English, max 2 sentences — Mayer's coherence)
5. **Visual** (diagram, chart, table — must be labeled per signaling principle)
6. **Analogy bridge** (if this section introduces a new concept)
7. **Detail cards** (collapsible or tabbed — segmenting principle)

Never show a visual without narrating what it means first. Never narrate without a visual to anchor it.

### Pattern 2: Progressive Disclosure (4 Levels)
Start with the simplest mental model. Add complexity in layers:
- **Quick Take** (15 sec): Hero stats + concept adjacency map + 1 diagram
- **Overview** (1 min): Key concepts with visuals + analogy bridges
- **Detail** (3 min): Data, comparisons, evidence tables
- **Deep Dive** (10 min): Architecture, edge cases, competitive analysis, full data

Each level is a tab. Users who get it fast stop at Quick Take. Power users go to Deep Dive. Nobody is overwhelmed.

### Pattern 3: One Visual Type Per Concept
Match the visual to the concept type:

| Concept Type | Best Visual | When to Use |
|-------------|------------|------------|
| Process / sequence | Funnel or flow diagram | Pipeline stages, user journeys |
| Hierarchy / layers | Architecture stack | Tech stacks, platform layers |
| Comparison | Split diagram or comparison table | Us vs. competitor, before vs. after |
| Relationships | Mental map (node graph) | System dependencies, concept adjacency |
| Progress / maturity | Maturity ladder | Adoption levels, readiness stages |
| Quantitative | Chart.js bar/line/radar | Market data, metrics, benchmarks |
| Decision | Flowchart with branches | Build vs. buy, go/no-go |
| Timeline | Horizontal timeline | Feature evolution, competitor moves |
| Analogy mapping | Analogy bridge (source ↔ target) | New concepts mapped to familiar ones |

Never use two visual types for the same concept. Never use a chart when a diagram is clearer.

### Pattern 4: Concept Adjacency Map (mandatory)
Placed immediately after the hero section. An interactive node graph showing:
- **Center node:** The concept being explained (accent color)
- **Adjacent nodes:** Related concepts (color-coded by domain)
  - Technical concepts: blue
  - Business concepts: copper/accent
  - Governance/compliance: purple
  - User/persona: cyan
- **Edges:** Labeled relationships ("depends on", "enables", "competes with", "part of", "measured by")
- **Interaction:** Clicking a node scrolls to the section that covers it. Hovering shows a 1-sentence tooltip.

This gives the learner the big picture BEFORE any detail — building schema scaffolding per Pillar 5.

### Pattern 5: Analogy Bridge Component (mandatory per new concept)
Visual side-by-side showing:
```
┌──────────────────┐       ┌──────────────────┐
│  SOURCE DOMAIN   │──→──→──│  TARGET DOMAIN   │
│  (familiar)      │  maps  │  (new concept)   │
│                  │  to    │                  │
│  Highway         │       │  AI System        │
│  guardrails      │───→───│  guardrails       │
│                  │       │                  │
│  Don't steer     │───→───│  Don't choose     │
│  the car         │       │  the model output │
│                  │       │                  │
│  Prevent going   │───→───│  Prevent harmful  │
│  off the cliff   │       │  content          │
└──────────────────┘       └──────────────────┘
```

CSS class: `.analogy-bridge` — source on left (blue), bridge arrows in center, target on right (accent).

Each analogy bridge maps 3 specific attributes from source → target. Not vague metaphors — structural mappings per Gentner.

### Pattern 6: Quiz System (10-15 questions, spaced throughout)
Not just mid + end. New placement pattern based on spaced retrieval research:

| Placement | After | # Questions | Difficulty | Focus |
|-----------|-------|:-----------:|------------|-------|
| Quiz 1 | Sections 1-2 | 3 | Recall | "What is X?" — can you name/identify? |
| Quiz 2 | Sections 3-4 | 4 | Comprehension | "Why does X matter?" — can you explain? |
| Quiz 3 | Sections 5-6 | 4 | Application | "Given scenario Y, what would you do?" |
| Final Quiz | End | 4 | Interleaved | Mix of all levels, questions from ALL sections |

Total: 15 questions across 4 quiz blocks.

**Question design rules:**
- Never "Which of these is true?" (lazy recall). Ask "Why does this approach win over alternatives?"
- Every wrong answer gets 1-2 sentence explanatory feedback teaching through the mistake
- Final quiz interleaves topics (Q1 from section 1, Q2 from section 5, Q3 from section 3) for deeper encoding
- Include at least 2 scenario-based questions: "Maya (ops lead) sees X on her dashboard. What should she do?"

**Score tracker:** Running score at bottom of each quiz block + visual progress bar. Final score summary at end with personalized feedback:
- 12-15 correct: "Expert level — you could present this to stakeholders"
- 8-11 correct: "Solid grasp — review the sections flagged below"
- 0-7 correct: "Review recommended — re-read the Overview tab in each section"

### Pattern 7: "Why This Matters" Callouts
Before each visual section, a highlighted callout box:
```html
<div class="why-callout">
  <span class="why-label">WHY THIS MATTERS</span>
  <p>[1 sentence connecting to the user's actual work or decision]</p>
</div>
```
Grounds abstract concepts in practical relevance. Activates the brain's relevance filter — information flagged as "useful to me" gets stronger encoding.

## Design System

### The Dark Theme (mandatory)
Proven design system from the towards-jarvis explainer:

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
- Analogy text: 14px italic for source domain, 14px bold for target domain

### Layout
- Max-width: 1200px centered
- Padding: 48px horizontal (20px on mobile)
- Section spacing: 64px margin-top
- Card border-radius: 12px
- All surfaces have subtle border (1px solid var(--border))
- Hover states: border-color lighten, subtle translateX/scale
- **Spatial contiguity:** visual and its text explanation must fit in one viewport height (~700px)

### Required Components (see references/component-library.md)
Every explainer must include:
1. **Scroll progress bar** (fixed top, gradient accent→accent2)
2. **Sticky nav** with section tabs (backdrop-filter blur)
3. **Hero section** with 3-5 key stats (big numbers) and 1-sentence summary
4. **Concept Adjacency Map** (interactive node graph, after hero)
5. **At least 4 visual sections** using different visual types
6. **Analogy bridges** for every major new concept (minimum 3)
7. **"Why This Matters" callouts** before each section
8. **Tab panels** for 4-level progressive disclosure
9. **Collapsible sections** for deep dives
10. **4 quiz blocks** with 15 total questions (spaced, interleaved, 3-tier difficulty)
11. **Score tracker** with running score and final personalized feedback
12. **Footer** with generation timestamp

## Input Sources

The Visual Explainer can be invoked on:
- **A pipeline artifact** (research, PRD, design spec) → explains the product/feature
- **A concept** (how guardrails work, what SLOs mean) → teaches the concept
- **A comparison** (us vs. competitors, before vs. after) → visualizes the contrast
- **A process** (how the pipeline works, how deployment works) → shows the flow

## Build Process

### Step 1: Content Outline
Before writing any HTML, define:
- **Title and 1-sentence summary** (hero)
- **3-5 key stats** (hero numbers — pick the most surprising/important data points)
- **Concept adjacency map structure** (center node + 5-8 adjacent nodes with labeled edges)
- **Section breakdown** (5-8 sections, each with concept type, visual type, and analogy)
- **Analogy inventory** (minimum 3 analogies mapping familiar → new concepts)
- **Quiz questions** (15 total across 4 blocks, 3-tier difficulty)
- **Tab structure** (Quick Take / Overview / Detail / Deep Dive per section)

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
  <style>/* Full design system + component styles */</style>
</head>
<body>
  <div class="scroll-progress" id="scrollProgress"></div>
  <nav class="sticky-nav">...</nav>
  <section class="hero">...</section>
  <div class="container">
    <!-- Concept Adjacency Map -->
    <!-- Sections: why-callout → narration → visual → analogy → detail tabs -->
    <!-- Quiz 1 (recall) after sections 1-2 -->
    <!-- Quiz 2 (comprehension) after sections 3-4 -->
    <!-- Quiz 3 (application) after sections 5-6 -->
    <!-- Final Quiz (interleaved) at end -->
    <!-- Score summary -->
  </div>
  <footer class="footer">...</footer>
  <script>
    /* Scroll progress, tab switching, collapsibles, quiz logic with
       scoring + feedback, Chart.js charts, nav highlighting,
       concept map click-to-scroll, score tracker */
  </script>
</body>
</html>
```

### Step 3: Validate
Open in browser and verify:
- [ ] Scroll progress bar works
- [ ] Sticky nav highlights active section on scroll
- [ ] Concept adjacency map nodes are clickable (scroll to section)
- [ ] All tabs switch correctly (4 levels per section)
- [ ] All collapsibles expand/collapse
- [ ] All 15 quiz questions score correctly (green correct, red + explanation for wrong)
- [ ] Score tracker updates correctly across all 4 quiz blocks
- [ ] Final score shows personalized feedback message
- [ ] All analogy bridges render with 3 structural mappings each
- [ ] "Why This Matters" callouts appear before every section
- [ ] Charts render with real data (not placeholder)
- [ ] Responsive at 375px width (mobile)
- [ ] No JS console errors
- [ ] All hover states work (cards, nav items, diagram elements, concept map nodes)
- [ ] Spatial contiguity: every visual + explanation fits in one viewport

## Output

Single file: `[topic-slug]-explainer.html` saved to the pipeline output directory.

Target: 1,000-1,800 lines of HTML. Under 1,000 = too shallow. Over 1,800 = probably repeating patterns.

## Quality Checklist
- [ ] Dual coding: every concept has BOTH visual AND verbal, side by side
- [ ] Concept adjacency map present after hero with clickable nodes
- [ ] At least 4 different visual types used
- [ ] At least 3 analogy bridges with 3 structural mappings each
- [ ] Progressive disclosure via 4-level tabs (Quick Take → Overview → Detail → Deep Dive)
- [ ] 4 quiz blocks with 15 total questions across 3 difficulty tiers
- [ ] Quiz questions interleaved in final block (not grouped by section)
- [ ] Every wrong quiz answer has 1-2 sentence explanatory feedback
- [ ] Score tracker with personalized final feedback
- [ ] "Why This Matters" callout before every section
- [ ] Mayer's coherence: max 3 bullets per card, max 2 sentences per intro
- [ ] Mayer's signaling: every diagram has labeled arrows/annotations
- [ ] Mayer's spatial contiguity: visual + explanation in same viewport
- [ ] Hero section has 3-5 key stats with big numbers
- [ ] Sticky nav with active section highlighting
- [ ] Scroll progress bar
- [ ] Dark theme with correct color palette
- [ ] Responsive at mobile widths
- [ ] No external dependencies except Chart.js CDN
- [ ] All data is real (from source artifact), not placeholder
- [ ] Total file size between 1,000-1,800 lines

## Eval Learnings Log

### v0.1.0 → v0.2.0 (2026-05-19)
1. No cognitive science foundation — added 5 research-backed pillars as non-negotiable design rules
2. Quiz too shallow (6 questions) — expanded to 15 across 4 blocks with 3-tier difficulty
3. No analogy-based learning — added mandatory analogy bridge component per new concept
4. No concept adjacency map — added interactive node graph for schema building
5. No "Why This Matters" relevance callouts — added before every section
6. Progressive disclosure only 3 levels — expanded to 4 (Quick Take 15s, Overview 1min, Detail 3min, Deep Dive 10min)
7. No Mayer's principles encoded — added coherence, signaling, spatial contiguity, segmenting as explicit constraints
8. No score tracking — added running score + personalized final feedback
9. No quiz explanatory feedback — added 1-2 sentence teaching-through-mistake for wrong answers
10. No interleaved quiz questions — added final quiz that mixes across all sections
11. File size target too small — expanded to 1,000-1,800 lines to accommodate new components
