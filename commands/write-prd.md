---
description: Write a PRD from research artifacts and user context
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: "[topic] [--version N]"
---

# Write PRD

Run the PRD Writer skill for `$ARGUMENTS`.

1. Read the PRD Writer skill at `skills/prd-writer/SKILL.md` and follow its instructions exactly — including all v3.0.0 pre-writing steps (Product Thesis Contract, Context Reconciliation, Reference Prototype Preservation, Evidence Tags).
2. Locate the pipeline working directory for this topic. Read ALL available context: research artifacts, prior PRD versions, prototypes, debate outputs, user guidance.
3. If `--version N` is specified, this is an iteration on an existing PRD. Read the prior version and any critique/feedback to apply targeted fixes rather than rewriting from scratch.
4. Output: PRD markdown + PRD Self-Eval sidecar, saved to the pipeline working directory.
5. Convert to PDF after writing. Do NOT push product artifacts to GitHub.
