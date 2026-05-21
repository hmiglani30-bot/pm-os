---
description: Generate an interactive HTML visual explainer from product artifacts
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch
argument-hint: "[topic or artifact path]"
---

# Visual Explainer

Run the Visual Explainer skill for `$ARGUMENTS`.

1. Read the Visual Explainer skill at `skills/visual-explainer/SKILL.md` and follow its instructions exactly — including the mandatory Explanation Plan gate (Step 0).
2. Read the component library at `skills/visual-explainer/references/component-library.md` for CSS patterns.
3. Classify the content type (product/concept/process/comparison/architecture) and detect the audience before planning.
4. Produce the full Explanation Plan with narrative arc, concept inventory, typed concept map plan, quiz plan, and analogy inventory. Do NOT write HTML until the plan is complete.
5. Build a single-file HTML explainer (1,200-2,000 lines) following the plan.
6. Validate: open in browser, check JS console, verify all interactivity works.
7. Output: `[topic-slug]-explainer.html` saved to the pipeline working directory.
