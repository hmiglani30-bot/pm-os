---
description: Run a multi-persona adversarial debate on a PRD or design decision
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: "[topic or PRD path]"
---

# Adversarial Debate

Run the Adversarial Debate skill for `$ARGUMENTS`.

1. Read the Adversarial Debate skill at `skills/adversarial-debate/SKILL.md` and follow its instructions exactly.
2. Read the artifact to debate (PRD, design spec, or prototype). If a topic is given instead of a path, locate the relevant artifact in the pipeline directory.
3. Run 5 rounds of structured debate between 5 expert personas:
   - UX Researcher
   - CIO / Enterprise Buyer
   - Principal Engineer
   - Product Manager (challenger role)
   - Orchestrator (synthesizes, scores, identifies convergence)
4. Each round: all personas argue, Orchestrator scores alignment and identifies open threads.
5. Output: debate transcript as PDF, saved to the pipeline working directory.
