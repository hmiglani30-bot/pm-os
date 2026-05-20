---
name: readme-writer
description: >
  README generator and validator for GitHub repos and plugin skills.
  Use when the user asks to "write README", "update README", "improve README",
  "create repo docs", "document this plugin", "does my README match what's built",
  or when any plugin is published and needs documentation. Produces READMEs that
  follow the PSB Method (Problem-Solution-Built) and validates that documentation
  matches actual repo contents.
version: 0.1.0
---

# README Writer

Generate and validate GitHub README files using the **PSB Method** — a structured approach that ensures every README answers three questions a visitor asks in the first 30 seconds: *What problem does this solve? What's the proposed solution? What's actually built?*

## The PSB Method (Problem-Solution-Built)

### Core Principle

Every README is a landing page. Visitors decide in 30 seconds whether to stay or bounce. The PSB Method front-loads the answers to the three questions that drive that decision:

1. **Problem** — What pain exists? Why should I care? (emotional hook)
2. **Solution** — What approach does this project take? (conceptual model)
3. **Built** — What's actually in the repo right now? (concrete inventory)

Most READMEs fail because they jump straight to installation instructions without establishing *why*. Others describe a vision without grounding it in what's actually shipped. PSB fixes both failure modes.

### Method in 300 Words

**Start with the Problem (2-3 sentences).** Name the specific pain point the project addresses. Use concrete language — not "improves productivity" but "PMs spend 40 hours writing PRDs that engineering ignores because they lack prototypes." This is the hook that makes someone keep reading.

**Describe the Solution (1 paragraph).** Explain the approach at the conceptual level — what does this project *do* about the problem? This is architecture, not features. "A 10-stage AI agent pipeline that takes a product idea from research through adversarial review to a working HTML prototype" tells the reader the shape of the solution without drowning them in details.

**Inventory What's Built (structured table or list).** Map every major component in the repo to what it does. Use a table — scannable beats narrative. Each row answers: component name, what it does, and where it fits in the solution. This is the proof that the solution isn't vaporware. Include version numbers so readers know maturity.

**Then layer supporting sections:** Quick Start (copy-paste commands), Architecture Diagram (how components connect), Example Output (what the pipeline produces), and Contributing guidelines. These come AFTER PSB because they only matter if PSB convinced the visitor to stay.

**Validate before shipping.** Walk the repo directory tree and confirm every component mentioned in the README exists, and every component in the repo is mentioned in the README. A README that claims features that don't exist, or omits features that do, erodes trust faster than having no README at all.

## Input

One or more of:
- A repo directory path to analyze
- An existing README to improve
- A skill SKILL.md file to document
- Verbal description of the project

## Process

### Step 1: Repo Inventory

Walk the actual repo structure. For each component found:
- **Name:** File or directory name
- **Type:** Command, skill, agent, reference, config, eval run, etc.
- **Version:** From frontmatter or package.json
- **One-liner:** What it does (from description field or first paragraph)

```bash
# For plugins
find . -name "SKILL.md" -o -name "*.md" -path "*/commands/*" -o -name "plugin.json" | sort
```

Store this as `repo-inventory` — it's the source of truth for validation.

### Step 2: Extract PSB Content

From the repo inventory and any existing docs:

**Problem extraction:**
- Look for motivation statements in SKILL.md files, CLAUDE.md, or existing README
- Look for "pain point", "problem", "why", "motivation" keywords
- If nothing explicit: infer from what the tool does — what was painful before it existed?

**Solution extraction:**
- Read the orchestrator/pipeline command if one exists
- Read the plugin.json description
- Synthesize: what's the overall approach?

**Built extraction:**
- Direct from repo-inventory (Step 1)
- Group by type (commands, skills, references, eval runs)
- Include version numbers

### Step 3: Write README Sections

Follow this exact section order:

```markdown
# [Project Name]

[1-line value proposition — what it does in plain English]

## The Problem

[2-3 sentences. Concrete pain. Who experiences it. What it costs them.]

## The Solution

[1 paragraph. Conceptual approach. How the pieces fit together. Architecture-level, not feature-level.]

## What's Built

[Table: every component, what it does, version, status]

| Component | Type | What It Does | Version |
|-----------|------|-------------|---------|

## How It Works

[Pipeline/workflow diagram or step-by-step explanation of how components connect.
 Use numbered steps or a text-based flow diagram.]

## Quick Start

[Copy-paste commands to install and run. Maximum 5 lines.]

## Example Output

[What does the pipeline/tool actually produce? List the artifacts with 1-line descriptions.]

## Architecture

[How stages/components connect. Text flow diagram or mermaid.]

## Eval Runs

[If the repo includes eval runs or example outputs, describe them.]

## Contributing

[How to add skills, extend the pipeline, or contribute.]

## Credits

[Architecture inspirations, dependencies, acknowledgments.]
```

### Step 4: Validate README Against Repo

This is the critical differentiator. Run two validation checks:

**Coverage check (completeness):**
- For every item in repo-inventory: is it mentioned in the README?
- Flag any component that exists in the repo but is missing from the README
- Flag any component mentioned in the README that doesn't exist in the repo

**Accuracy check (truthfulness):**
- For every version number in the README: does it match the actual SKILL.md frontmatter?
- For every description in the README: does it match what the component actually does?
- For every stage/step mentioned: does the orchestrator actually implement it?

**Output validation report:**

```markdown
## Validation Report

### Coverage
- Components in repo: [N]
- Components in README: [M]
- Missing from README: [list]
- In README but not in repo: [list]
- Coverage score: [M/N]%

### Accuracy
- Version mismatches: [list]
- Description mismatches: [list]
- Accuracy score: [X/Y checks passed]

### Verdict: PASS / FAIL
[PASS if coverage >= 90% AND accuracy = 100%]
```

### Step 5: Skill-Level READMEs (if requested)

For individual skills within a plugin, produce a mini-README that follows the same PSB structure but scoped to the skill:

```markdown
# [Skill Name]

[1-line: what this skill does]

## Problem It Solves

[What was painful before this skill existed?]

## How It Works

[The skill's process — what steps it follows, what it produces]

## Input / Output

| Input | Required | Source |
|-------|----------|--------|

| Output | Format | Description |
|--------|--------|-------------|

## Trigger Phrases

[When does this skill activate?]

## Version History

| Version | Changes |
|---------|---------|
```

## Output

- `README.md` — the complete README file
- `readme-validation.md` — validation report (coverage + accuracy)
- If skill-level READMEs requested: one per skill

## Quality Gate

The README passes if:
1. All three PSB sections are present and substantive (not placeholder)
2. Problem section names a specific pain point (not generic)
3. Solution section describes the approach (not just lists features)
4. What's Built table has every repo component with correct versions
5. Validation report shows >= 90% coverage and 100% accuracy
6. Quick Start section has copy-paste-ready commands
7. Total length is 500-1500 words (comprehensive but scannable)

## Rules

- **Validate before delivering.** Never ship a README without running the coverage and accuracy checks.
- **Tables over bullets.** Component inventories use tables. Scannable beats narrative.
- **Problem before solution.** Always. The hook matters more than the details.
- **Match what's built, not what's planned.** The README documents current state. Future plans go in a Roadmap section, clearly labeled.
- **No jargon without context.** If a term (e.g., "MECE FAQs", "Gandalf gate") appears, explain it in parentheses on first use.
- **Version numbers are mandatory.** Every component listed must show its current version.
- **Update on every push.** If skills or commands change, the README must be revalidated.

## Eval Learnings Log

(None yet — v0.1.0)
