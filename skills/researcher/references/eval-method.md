# PM Pipeline Evaluation Method (300 words)

## Purpose
Validate the plugin by running it on a real project end-to-end, scoring each stage's output, then improving the plugin based on findings.

## Method: Dual-Loop Evaluation

**Loop 1 — Automated Self-Eval (runs after each stage)**

Each stage's output is scored against its own quality checklist (already defined in every SKILL.md). After the artifact is produced, a verification pass runs the checklist and records:
- Pass/fail per criterion
- Specific gaps found
- Word count and structural compliance
- Evidence density (citations per 500 words)
- Time taken (turns consumed)

Score: percentage of checklist items passed. Target: >= 80%.

**Loop 2 — Human Review (runs after pipeline completes)**

The user reviews each artifact and scores on three dimensions:
1. **Usefulness** (1-5): Would I actually use this in my next eng meeting?
2. **Accuracy** (1-5): Are the claims true? Is the competitive data right?
3. **Completeness** (1-5): What's missing that I expected to see?

Plus free-text: "What would make this artifact better?"

**Improvement Protocol**

After both loops complete, synthesize findings into three categories:
1. **Skill instruction fixes** — unclear or missing guidance in the SKILL.md that caused a bad output
2. **Output format fixes** — sections that were empty, redundant, or in the wrong order
3. **Missing knowledge** — references or patterns the agent needed but didn't have

Apply fixes directly to the plugin files. Re-run the failing stage to verify the fix works. Package updated plugin.

**Success Criteria for v1**

The plugin passes evaluation when:
- All 6 stages produce artifacts (no stage crashes or blocks)
- Self-eval scores >= 80% on every stage
- Human review averages >= 3.5/5 across all artifacts
- Gandalf scoring produces differentiated results (not all 5s or all 1s)
- Total pipeline completes in < 45 minutes (autonomous mode)

**Iteration Cadence**

Run the pipeline → eval → improve → re-run the weakest stage → confirm fix. One cycle per session. Target: v1.0 plugin quality in 3 cycles.
