---
name: research-librarian
description: >
  Shared research utility callable by any agent in the pipeline. Use when any agent
  needs to "look up", "search for", "find data on", "verify a claim", "check competitor",
  or perform any web research. This is NOT a pipeline stage — it's a utility that other
  agents call on demand.
version: 0.1.0
---

# Research Librarian

Shared research utility for the PM pipeline. Any agent can invoke this to perform web research, verify claims, or gather data.

## When to Use
- Researcher agent: primary research during Stage 1
- PRD Writer: when Gandalf challenges a claim and the writer needs evidence
- Gandalf: when evaluating whether cited evidence is accurate
- Designer: when looking up Cloudscape components or design patterns
- Any agent that needs to verify a fact or find data

## Research Methods

### Method 1: Web Search
Use WebSearch for broad topic exploration:
- Competitor features and announcements
- Market data and analyst reports
- User forums and community discussions
- Technical documentation

### Method 2: Targeted Fetch
Use WebFetch for specific known sources:
- Competitor product pages
- AWS documentation
- Cloudscape component library (cloudscape.design)
- GitHub repos

### Method 3: Cross-Reference
When a claim is made without evidence:
1. Search for the claim
2. Find at least 2 independent sources
3. If sources conflict, note the discrepancy
4. Return: claim, sources, confidence level (high/medium/low)

## Output Format

Always return structured results:

```markdown
## Research Result: [Query]

**Query:** [What was asked]
**Method:** [Web Search / Targeted Fetch / Cross-Reference]
**Confidence:** [High / Medium / Low]

### Findings
[Concise findings with inline citations]

### Sources
1. [Source title](URL) — [relevance note]
2. [Source title](URL) — [relevance note]

### Caveats
[Any limitations, contradictions, or data freshness concerns]
```

## Rules
- ALWAYS cite sources. No uncited claims.
- Prefer primary sources (official docs, company blogs) over secondary (news articles, analyst speculation)
- Flag when data is older than 6 months
- If you can't find evidence for a claim, say so explicitly — don't fabricate
- Keep results concise. The calling agent needs data, not a novel.
