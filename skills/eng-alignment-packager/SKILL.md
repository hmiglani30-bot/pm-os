---
name: eng-alignment-packager
description: >
  Engineering alignment package agent. Use when the user asks to "package for eng",
  "prep for eng meeting", "create eng deck", "alignment meeting", "present to engineering",
  or when the pm-pipeline orchestrator invokes Stage 6.5. Takes all pipeline artifacts
  and produces a meeting-ready package: a structured markdown doc + PPTX presentation
  that a PM can walk into a 30-minute eng alignment meeting with.
version: 0.1.0
---

# Engineering Alignment Packager

You produce the artifact a PM actually walks into the room with. The pipeline generates deep analysis docs (research, PRD, design spec, launch readiness) — but engineers don't read 30K words before a meeting. This skill distills the full pipeline output into a 30-minute meeting package.

## Core Principle

**The meeting is the deliverable.** If the PM can't present this in 30 minutes and get a go/no-go, the package failed. Every slide earns its place by answering a question engineers will actually ask.

## Input

All available pipeline artifacts (use latest versions):
- `current-state-v[N].md` — what exists today
- `research-v[N].md` — market context, competitors
- `prd-v[N].md` — problem, personas, capabilities, scope
- `gandalf-evaluation-v[N].md` — critique scores
- `debate-v[N].md` — adversarial debate recommendations
- `design-spec-v[N].md` — UX spec
- `prototype-v[N].html` — working prototype
- `launch-readiness-v[N].md` — eng spec, sprints, RACI, risks

## Output: Two Artifacts

### 1. `eng-alignment-v1.md` (structured meeting doc)

```markdown
---
artifact: eng-alignment
version: v1
meeting-duration: 30 min
timestamp: [ISO-8601]
---

# Eng Alignment: [Feature Name]

## 1. The Problem (3 min)
[2-3 sentences. Who hurts, why, how bad. Pull from PRD personas and JTBD.]
[1 key stat from research that makes the problem undeniable]

## 2. What Exists Today (2 min)
[From current-state audit. 3-4 bullet points on current product state.]
[Top 3 pain points from the Pain Map]

## 3. The Market (2 min)
[From research. TAM number, 1-2 key competitors, why now.]
[What happens if we don't build this — competitor risk]

## 4. The Proposal (5 min)
[From PRD. The 3-5 v1 capabilities, one sentence each.]
[What's explicitly NOT in v1 and why]
[North Star metric]

## 5. Live Prototype Walkthrough (5 min)
[Demo script: exact clicks, what to show, what to say at each step]
Step 1: Open prototype. Show landing page with summary cards.
Step 2: Point out [specific element]. Explain why it's designed this way.
Step 3: Click [workload row]. Show split panel.
Step 4: Navigate to [specific tab]. Show the key insight.
Step 5: Show [secondary feature]. Explain the v2 vision.

## 6. Key Engineering Decisions (5 min)
[From launch readiness. The 3-4 biggest architectural decisions.]
For each: what we chose, what we considered, why this won.

## 7. Sprint Plan (3 min)
[Compressed sprint table from launch readiness]
| Sprint | Duration | What Ships |
[Highlight: when dogfood starts, when beta starts, when GA]

## 8. Risks & Open Questions (3 min)
[Top 5 risks from the risk register — the ones engineers care about]
[Top 3 open questions that need eng input]

## 9. The Ask (2 min)
[What you need from this meeting:]
- Go/no-go on the approach
- Eng lead assignment
- Sprint 0 spike scope agreement
- Any blocking concerns raised now
```

### 2. `eng-alignment-v1.pptx` (presentation deck)

Use the `pptx` skill to create a Cloudscape-styled deck. Map each section above to 1-2 slides:

| Slide | Content | Notes |
|-------|---------|-------|
| 1 | Title: "[Feature Name] — Eng Alignment" | Date, PM name, 30 min |
| 2 | The Problem | Persona quote + key stat |
| 3 | Current State | Pain map top 3 |
| 4 | Market Context | TAM, top competitor, why now |
| 5-6 | The Proposal | v1 capabilities, scope boundary, North Star |
| 7 | Prototype Screenshot | Screenshot of the prototype landing page |
| 8 | Architecture Overview | From launch readiness eng spec, simplified |
| 9 | Sprint Plan | Compressed timeline with milestones |
| 10 | Risks & Open Questions | Top 5 risks, top 3 questions |
| 11 | The Ask | What decisions needed from this room |

**Slide design rules:**
- Max 6 bullet points per slide
- Every slide has a "so what" — not just data, but the implication
- No walls of text — if it takes >15 seconds to read, it's too much
- Use the prototype screenshot as the visual anchor (Slide 7)

## Quality Gate

The package passes if:
1. Total estimated presentation time is 28-32 minutes (not over, not under)
2. Every section traces to a specific pipeline artifact (no invented content)
3. The demo script in Section 5 references actual prototype elements (not generic)
4. "The Ask" is specific and actionable (not "let us know what you think")
5. The PPTX has 10-12 slides (not more — engineers tune out after 12)

## Handoff

This is the terminal artifact of the pipeline. It doesn't feed any downstream stage. The PM takes the PPTX into the meeting and uses the MD as their speaker notes.
