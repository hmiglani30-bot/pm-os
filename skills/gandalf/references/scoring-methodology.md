# Gandalf Scoring Methodology

## Origin
Adapted from coleam00/adversarial-dev Evaluator pattern. Modified for strategy/problem critique rather than code quality evaluation.

## Hybrid Scoring System

Each question is evaluated on TWO independent axes:

### Axis 1: Rubric Score (1-5)

| Score | Label | Definition | Example |
|:-----:|-------|-----------|---------|
| 1 | Missing | No answer, irrelevant answer, or empty assertion | "The TAM is large" with no numbers |
| 2 | Weak | Answer exists but is vague, unsupported, or generic | "The TAM is estimated at $X billion" with no source |
| 3 | Adequate | Clear answer with at least one piece of evidence | "IDC estimates the APM market at $X billion (2025 report), growing at Y% CAGR" |
| 4 | Strong | Specific answer with multiple evidence points and reasoning | Above + "Our segment (transaction analytics) is Z% of that, based on Datadog's public revenue breakdown" |
| 5 | Exceptional | Quantified, multi-sourced, addresses counterarguments proactively | Above + "Bears would argue the market is saturated, but the shift from on-prem to cloud APM (only 40% penetrated per Gartner) suggests..." |

### Axis 2: Evidence Score (Binary)

| Score | Definition |
|:-----:|-----------|
| 0 | Answer is opinion, assertion, or logical reasoning without external evidence |
| 1 | Answer cites at least one specific data point, research finding, customer quote, or competitor example |

"Evidence" means:
- Named source (report, article, company, person)
- Specific number (dollar amount, percentage, date)
- Direct quote or paraphrase with attribution
- Competitor feature with version/date

"Not evidence" means:
- "Industry experts agree..."
- "It's well known that..."
- "Many customers struggle with..."
- Logical reasoning alone (even if correct)

### Combined Pass/Fail

A question **passes** when BOTH conditions are met:
- Rubric Score >= 3
- Evidence Score = 1

This means a beautifully reasoned answer without evidence (Rubric 4, Evidence 0) **fails**.
And an evidence-rich but incoherent answer (Rubric 2, Evidence 1) also **fails**.

### Stage Pass/Fail

- **PASSED**: >= 8/10 questions pass
- **PASSED WITH FLAGS**: >= 6/10 questions pass, remaining flagged for human
- **MOVED FORWARD WITH FLAGS**: < 6/10 pass after 3 rounds, all failures flagged for human

The pipeline ALWAYS moves forward. The verdict determines how much human attention the flags need.

## Round Management

### Round Budget: 3 total

| Round | Purpose | What Happens |
|-------|---------|-------------|
| 1 | Initial evaluation | Score all 10 questions on current PRD. Provide specific feedback for failures. |
| 2 | Revision review | PRD Writer updates and resubmits. Re-score ONLY previously failing questions. |
| 3 | Final evaluation | Last chance. Re-score remaining failures. Everything still failing → flagged for human. |

### Feedback Quality Requirements

When a question fails, Gandalf's feedback must include:
1. **What's missing** — specific gap identified
2. **What "good" looks like** — example of what a passing answer would include
3. **Where to look** — suggest research direction (competitor, report type, data source)

Bad feedback: "Needs more evidence"
Good feedback: "The TAM claim has no source. A passing answer would cite a specific market research report (IDC, Gartner, or Forrester) with a dollar figure and growth rate. Try searching for '[topic] market size 2025 report.'"

## Scoring Calibration Examples

### Q1: TAM & Market

**Score 1 (Missing):**
"This is a big market opportunity." → No number, no source.

**Score 3 (Adequate):**
"The global APM market was valued at $5.8B in 2024 (Markets and Markets report), with 12% CAGR." → One source, one number.

**Score 5 (Exceptional):**
"The global APM market was $5.8B in 2024 (M&M), but the relevant subsegment is distributed tracing ($1.2B, Gartner 2024). Current penetration among enterprises > 1000 employees is 62% (Datadog S-1 implies this from their TAM calc). The underserved segment is mid-market (100-1000 employees) where penetration is ~25% (estimated from Lightstep and Honeycomb's public case studies targeting this segment). This gives us a $300M addressable opportunity." → Multiple sources, segmented analysis, counterpoint addressed.
