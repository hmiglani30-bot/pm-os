# Change Spec: Opportunity-Solution Tree Phase in Researcher Skill

**Scope:** Add a new Step 8.5 (between Pattern Synthesis and What to Monitor) to the Researcher skill's output contract. No changes to Steps 1-8 or Step 10.

---

## 1. What Changes

### New Section: "Step 8.5: Opportunity-Solution Tree"

Inserted after Step 8 (Pattern Synthesis) and before Step 9 (What to Monitor). The Researcher already identifies gaps in Step 8 under "Gaps (nobody does W yet)." Today those gaps are a flat list. This step restructures them into a divergent tree:

```
Problem Statement (from Decision to Inform)
 +-- Opportunity 1: [named gap from pattern analysis]
 |    +-- Direction A: [concrete approach]
 |    |    Tradeoffs: [cost, risk, time, dependency]
 |    |    Evidence: [which research findings support this]
 |    +-- Direction B: [concrete approach]
 |         Tradeoffs: [cost, risk, time, dependency]
 |         Evidence: [which research findings support this]
 +-- Opportunity 2: ...
```

**Output contract addition** (appended to the existing markdown template after `## Pattern Analysis`):

```markdown
## Opportunity-Solution Tree

### Problem Statement
> [Restated from Decision to Inform]

### Opportunity 1: [Name]
**Evidence basis:** [Cite specific pattern analysis gaps, customer quotes, or competitor weaknesses that surface this opportunity]

| Direction | Description | Supports JTBD | Key Tradeoff | Dependency Risk |
|-----------|-------------|---------------|--------------|-----------------|
| A: [name] | [2-3 sentences] | [which jobs] | [primary cost] | [team/service] |
| B: [name] | [2-3 sentences] | [which jobs] | [primary cost] | [team/service] |

[Repeat for 3-5 opportunities, each with 2-3 directions]

### Tree Summary
- Total opportunities identified: [N]
- Total solution directions: [N]
- Recommendation: NONE — selection is the PRD Writer's job
```

**Section length target:** 600-900 words. Added to the existing section length table.

**Quality checklist addition:** "Opportunity tree has 3-5 opportunities, each with 2+ directions, none marked as recommended."

---

## 2. MECE Check: Why This Doesn't Overlap

| Concern | Who Owns It | What They Do | Boundary |
|---------|------------|--------------|----------|
| Competitive positioning | Researcher Step 3-4 | Thesis/Counterargument/Implication per competitor | Describes what competitors do and their structural limits. Does NOT map those limits to our opportunity space. |
| Opportunity-Solution Tree | **Researcher Step 8.5 (NEW)** | Converts pattern gaps + competitor weaknesses into a structured set of opportunities with multiple solution directions per opportunity | Generates the divergent set. Does NOT pick a winner or define scope. |
| Solution selection + scope | PRD Writer Section 2 | Picks specific capabilities, phases them into v1/v2/v3, defines scope boundary | Consumes the tree, selects and justifies which directions to pursue. |
| Scope discipline | Gandalf | Challenges whether v1 scope is too broad or too narrow | Evaluates the PRD Writer's selection, not the tree itself. |

**The gap this fills:** Today, the Researcher's Step 8 produces "Gaps (Opportunities)" as a flat bullet list (see research-v1.md: 5 bullets under "Gaps"). The PRD Writer then jumps straight to a solution proposal without documenting which alternative directions were considered and rejected. The tree forces divergent thinking BEFORE convergent thinking, and gives the PRD Writer a structured menu to select from rather than inventing solutions from scratch.

**Concrete example of the gap in research-v1.md:** Gap #3 says "Multi-model cost optimization -- cost tracking exists but no one offers switch-this-workflow recommendations." The Researcher stops there. But there are at least two directions: (A) build recommendation engine inside CloudWatch, or (B) surface cost deltas in Bedrock model comparison and let users decide. Today nobody documents these alternatives. The PRD Writer picks one (or invents their own) without traceability.

---

## 3. Acceptance Criteria

All criteria use the AI Adoption Control Plane topic as the test case.

1. **Minimum divergence:** The tree contains at least 3 opportunities (e.g., unified governance console, business outcome correlation, multi-model cost optimization) with at least 2 distinct solution directions each. Fail if any opportunity has only 1 direction.

2. **Evidence traceability:** Every opportunity cites at least one specific finding from Steps 2-8. For example, "Unified AWS-native AI governance" must reference the AWS Current State gap analysis (Step 2) AND at least one competitor weakness (Steps 3-4). Fail if an opportunity has no backward citation.

3. **No recommendation leakage:** The tree contains zero language indicating a preferred direction -- no "recommended," "best," "preferred," "obvious choice," or comparative superlatives ranking one direction over another. Fail on any instance.

4. **Tradeoff specificity:** Each direction names at least one concrete tradeoff (not "complex to build" but "requires X-Ray team dependency for trace data access" or "adds 3-month timeline for Bedrock API integration"). Fail if any tradeoff is generic.

5. **Downstream consumability:** The PRD Writer, given the tree, produces a Solution Proposal (Section 2) where every selected capability maps back to a specific tree direction with an explicit "Selected Direction X from Opportunity Y because [rationale]" statement. Fail if any PRD capability has no tree lineage.

---

## 4. Anti-Criteria

This change explicitly does NOT:

- **Pick the winning solution.** The tree is divergent output. Selection, scoping, and phasing remain the PRD Writer's job. If the Researcher recommends a direction, that is a defect.
- **Replace the Pattern Analysis.** Step 8 still produces common patterns, differentiators, gaps, and trends. Step 8.5 restructures the gaps into a tree -- it does not absorb or duplicate the other three pattern categories.
- **Add new research.** The tree synthesizes findings already present in Steps 2-8. It does not trigger additional web searches or data collection. If a direction requires research that wasn't done, the tree flags it as "requires further research" rather than inventing claims.
- **Define UX or capabilities.** Directions are strategic approaches ("build recommendation engine" vs. "surface cost deltas"), not feature specs or wireframes. Feature-level detail is the PRD Writer's and Designer's job.
- **Become a decision matrix.** No scoring, no weighting, no 2x2 grids. The tree is a structured inventory, not a prioritization framework.

---

## 5. Downstream Impact

### PRD Writer Input Contract Change

The PRD Writer's `## Input` section changes from:

```
- research-v[N].md from the Researcher stage
```

To:

```
- research-v[N].md from the Researcher stage (must include Opportunity-Solution Tree section)
```

**New requirement in Section 2 (Solution Proposal):** Add a subsection before the scope boundary table:

```markdown
### Solution Lineage
| Selected Capability | From Opportunity | Direction Chosen | Alternatives Rejected | Rejection Rationale |
```

This forces the PRD Writer to show their work: which tree branches they picked, which they left behind, and why. The "Alternatives Rejected" column is the key addition -- it makes the PRD Writer's convergent decision auditable.

### Gandalf Impact

Gandalf should NOT evaluate the tree itself (that would make Gandalf a co-author of research). Gandalf SHOULD add one new challenge question to its evaluation rubric:

> "Did the PRD Writer consider alternative solution directions from the Researcher's opportunity tree, or did they default to the first/obvious option? Show evidence of deliberate selection."

This is a check on the PRD Writer's use of the tree, not on the tree's quality. No changes to Gandalf's existing 10-question evaluation structure -- this replaces the weakest existing question or becomes question 11 if all 10 are load-bearing.

### No Impact On

- **Designer** (Stage 4): Consumes PRD, not research. No change.
- **Prototype Builder** (Stage 5): Consumes design spec. No change.
- **Launch Readiness** (Stage 6): Consumes prototype + PRD. No change.
