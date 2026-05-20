# 25 MECE FAQ Framework

## Method

Generate exactly 25 FAQs that are Mutually Exclusive and Collectively Exhaustive across 8 categories. The categories ensure full coverage; the exclusivity rule ensures no redundancy.

### Categories (MECE Coverage)

| # | Category | Description | Target Count |
|---|----------|-------------|-------------|
| 1 | Customer & Problem | Who is this for? Why now? How painful is the status quo? | 3-4 |
| 2 | Solution & Approach | What are we building? What's the technical approach? | 3-4 |
| 3 | Scope & Boundaries | What's in/out of v1? What's the phased plan? | 2-3 |
| 4 | Competitive & Market | How does this compare? What's the market context? | 2-3 |
| 5 | Metrics & Success | How do we measure success? What are the targets? | 2-3 |
| 6 | Technical & Architecture | How does this integrate? What are the dependencies? | 3-4 |
| 7 | Business & Strategy | What's the business case? Pricing impact? TAM? | 2-3 |
| 8 | Risks & Mitigation | What could go wrong? How do we de-risk? | 2-3 |

Total: exactly 25 FAQs.

### Response Length Calibration

Each FAQ answer should be one of three lengths. The agent decides based on complexity:

| Length | Word Count | When to Use |
|--------|-----------|-------------|
| Short | ~100 words | Simple factual questions, yes/no with brief rationale |
| Medium | ~180 words | Questions requiring context + evidence + conclusion |
| Long | ~250 words | Complex questions requiring multi-part analysis |

### Decision Heuristic for Length
- Can it be answered with a single data point? → **Short** (100w)
- Does it need "on one hand / on the other hand"? → **Medium** (180w)
- Does it require a framework, comparison, or multi-step reasoning? → **Long** (250w)

### Writing Rules
1. **Plain language first.** Define jargon on first use.
2. **Lead with the answer.** Don't build up to it.
3. **Cite evidence.** Reference research findings, metrics, or competitor data.
4. **Be specific.** "Reduces investigation time by 40%" not "significantly improves efficiency."
5. **Acknowledge uncertainty.** If the answer requires validation, say so.

### Example FAQ

**Q: Why can't customers just use the existing trace view for this?**
(Category: Customer & Problem | Length: Medium ~180w)

The existing trace view shows individual trace details but forces customers to manually correlate across traces to identify patterns. In our research, we found that SREs spend an average of 23 minutes per incident switching between trace view, metrics, and logs to build a mental model of what happened. Datadog's Transaction Analytics (launched 2023) demonstrated that providing an aggregated transaction-level view reduced mean-time-to-resolution by 35% for their enterprise customers.

Our solution differs from extending the existing trace view because the unit of analysis is different: trace view operates on individual spans, while transaction search operates on aggregated transaction patterns. Trying to bolt aggregation onto the existing span-oriented UI would create a confusing hybrid that serves neither use case well. ServiceNow's attempt to do exactly this in 2024 resulted in their lowest CSAT scores for the ITOM module.

### Anti-Patterns to Avoid
- **Softball questions** ("Why is this a great idea?") — every question should be one a skeptical VP would ask
- **Duplicate angles** ("How is this different from X?" and "Why not just use X?" are the same question)
- **Vague answers** ("This will be faster" without quantification)
- **Missing the "so what?"** — every answer should connect back to customer value or business impact
