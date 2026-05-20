# PM Operating System Comparison: Ashu's PM Pipeline vs. GitHub's Top PM Systems

**Date:** 2026-05-19
**Scope:** Architecture, coverage, quality mechanisms, gap analysis, and recommendations

---

## 1. Architecture Comparison

### Ashu's PM Pipeline: Multi-Agent Sequential with Feedback Loops

Ashu's pipeline is a **6-stage sequential multi-agent system** with 8 specialized agents (Researcher v0.3.0, PRD Writer v0.2.0, Gandalf adversarial gate v0.1.0, Designer v0.2.0, Prototype Builder v0.2.0, Launch Readiness v0.2.0, Research Librarian utility, Visual Explainer utility). The orchestrator (`/pm-pipeline`) invokes agents in strict order, with three backward feedback loops: Design updates PRD (4 to 2), Prototype triggers fidelity check (5 to 4), and Prototype updates PRD experience section (5 to 2).

Key architectural decisions that distinguish this system:

- **Handoff contracts:** Each stage has deterministic input/output contracts. Stage 3 receives the full PRD plus a research summary, not the full research artifact. Stage 5 receives the full design spec but only the PRD executive summary. This is context pruning via named envelopes with max word counts per transition.
- **Token budgets per stage:** Each stage operates within a 3K-18K token budget, preventing context window blowout on long pipeline runs.
- **DEPENDENCY_GAP mechanism:** Downstream stages can flag missing upstream data without halting the pipeline. The missing data gets patched in parallel while the stage continues with what it has.
- **Never-block philosophy:** The pipeline always moves forward. Gandalf gets 3 rounds max, then flags unresolved questions for human review and advances. This is a deliberate trade: throughput over perfection, with human-in-the-loop for the hard calls.

### product-on-purpose/pm-skills: Modular Skill Library with Sprint Choreography

product-on-purpose takes a fundamentally different approach: **55 plug-and-play skills organized by the Triple Diamond framework** (Discover, Define, Develop, Deliver, Measure, Iterate), plus 15 tools implementing Foundation Sprint (2-day Knapp/Zeratsky strategic alignment) and Design Sprint (5-day Knapp/Zeratsky/Kowitz prototype-and-test) methodologies. There is no central orchestrator. Skills are independent, invoked individually or via CI-enforced family contracts that ensure skills within the same "family" (e.g., the 7 Foundation Sprint skills) pass structured data between each other.

Architecture trade-off: **maximum flexibility, minimum coordination overhead.** A PM picks the skills they need for their current task. There is no assumption that research must precede PRD writing, or that a gate must precede design. The PM is the orchestrator. This is a DAG where the PM manually wires the edges, not a pipeline where edges are hardcoded.

The MCP server variant (pm-skills-mcp, now in maintenance mode at v2.9.3) wraps these skills as 59 MCP tools, enabling programmatic chaining. But the recommended path is the file-based install, which is essentially a skill marketplace rather than an automated pipeline.

### phuryn/pm-skills: Workflow-Chained Plugin Ecosystem

Pawel Huryn's system is the largest by raw skill count: **65 PM skills and 36 chained workflows across 8 plugins** (pm-toolkit, pm-product-strategy, pm-product-discovery, pm-market-research, pm-data-analytics, pm-marketing-growth, pm-go-to-market, pm-execution). Each plugin packages skills that flow into each other. After any command completes, it suggests relevant next commands, creating an emergent workflow chain.

This is a **semi-guided DAG**. The system doesn't enforce stage order, but it does suggest the next logical step. The `/discover` command suggests `/strategy`; the `/strategy` command suggests `/write-prd`. It encodes proven PM frameworks from Teresa Torres (opportunity-solution trees), Marty Cagan (continuous discovery), and Alberto Savoia (pretotyping) directly into skill logic.

Architecture trade-off: **breadth over depth.** 100+ skills means coverage across the entire PM lifecycle, from market sizing to go-to-market to retrospectives. But each skill operates independently. There is no shared state between a `/competitor-analysis` run and a subsequent `/write-prd` run unless the PM manually feeds the output forward.

### evalops/agent-pm: FastAPI Multi-Agent Orchestrator with External Integrations

agent-pm is closest to Ashu's pipeline architecturally: a **multi-agent orchestrator** built on the OpenAI Agents SDK that turns product ideas into PRDs, ticket plans, and operational updates. It is a FastAPI service with dependency-injected connectors for Jira, GitHub, Slack, Gmail, Calendar, Google Drive, and Notion.

Key architectural features: Git-style PRD versioning with changelog generation, branching, blame, and approvals. Dry-run mode as a first-class guardrail. Background task queue (in-memory or Redis) with retries and adaptive auto-requeue. Prometheus metrics and structured logging for observability.

Architecture trade-off: **operational maturity over PM methodology depth.** agent-pm excels at the plumbing (versioning, integrations, observability, guardrails) but its PM methodology is thinner. It does not have an adversarial gate, no structured research framework, no design pattern system. It is an engineering-grade orchestrator that happens to do PM, rather than a PM methodology engine.

---

## 2. Coverage Matrix

| Stage | Ashu's Pipeline | product-on-purpose | phuryn/pm-skills | evalops/agent-pm |
|-------|:-:|:-:|:-:|:-:|
| **Market Research** | Researcher agent (v0.3.0) with 10-step framework, evidence tiers, triangulation | Discover phase skills | `/competitor-analysis`, `/market-sizing`, personas, segmentation | Basic — via `/plan` endpoint |
| **Strategy / Framing** | PRD Writer + 25 MECE FAQs | Foundation Sprint (7 skills), lean canvas, OKR writer | `/strategy`, Ansoff matrix, Porter's five forces, PESTLE, lean canvas, business model | Minimal — PRD output only |
| **PRD / Spec Writing** | PRD Writer (v0.2.0) with evidence density requirements, 5.5K-8K word targets | PRD family within Define phase | `/write-prd`, user stories, job stories, acceptance criteria | Automated PRD generation |
| **Critique / Gate** | Gandalf (v0.1.0) — 10 questions, hybrid scoring (rubric 1-5 + evidence 0/1), 3-round max | Pre-mortem skill | `/pre-mortem` risk analysis | Dry-run mode (operational, not strategic) |
| **Design / UX** | Designer (v0.2.0) — first principles then reality check against consumer/enterprise patterns | Define phase skills, UX-mock skills (from phuryn credit) | Design-ux-mocks plugin | Not covered |
| **Prototype** | Prototype Builder (v0.2.0) — single-file Cloudscape HTML, 18-point validation | Not covered | Not covered | Not covered |
| **Launch Readiness** | Launch Readiness (v0.2.0) — eng spec, ACs, phased rollout, meeting deck | Deliver phase skills | `/plan-launch`, rollout strategy, release notes | Ticket generation, comms |
| **Post-Launch / Growth** | Not covered | Measure + Iterate phases | `/growth-strategy`, cohort analysis, A/B test analysis, retention | Operational monitoring via Prometheus |
| **Go-to-Market** | Not covered | Marketing skills within Deliver | `/plan-gtm`, marketing launch, positioning, messaging | Slack/email comms |
| **Sprint Ceremonies** | Not covered | Foundation Sprint (7 skills) + Design Sprint (7 skills) + note-and-vote | Sprint planning, retrospectives, standups | Not covered |
| **Prioritization** | Not covered (except Gandalf scope discipline Q6) | RICE within Define phase | RICE, ICE, MoSCoW, Kano, Opportunity Score (9 frameworks) | Not covered |
| **Opportunity Discovery** | Not covered | Opportunity-solution tree within Discover | Opportunity-solution tree (Teresa Torres), assumption mapping | Not covered |
| **Data Analytics** | Not covered | Not covered | SQL generation, cohort analysis, A/B test design, statistical significance | Cost tracking hooks |
| **Stakeholder Mgmt** | Not covered | Meeting family (8 foundation skills) | Stakeholder mapping, RACI, alignment workshops | Slack/Calendar integration |
| **External Integrations** | None (file-based) | File-based, MCP server optional | File-based | Jira, GitHub, Slack, Gmail, Calendar, Drive, Notion |

---

## 3. Quality Mechanisms

### Scoring and Evidence Requirements

**Ashu's pipeline** has the most rigorous scoring system of the four. Gandalf uses a hybrid rubric: each of 10 questions gets a rubric score (1-5) AND an evidence score (binary 0/1). A question passes only if the rubric score is at least 3 AND evidence is cited. The stage passes at 8/10. The Researcher agent independently enforces evidence tiering (Tier 1-5) with a 40% Tier 1-2 minimum. The PRD Writer carries the same evidence density requirements forward. This creates a chain of evidence accountability across three stages.

**product-on-purpose** uses CI-enforced family contracts that validate skill outputs conform to expected schemas. Skills within a sprint family must pass structured data between each other, but there is no adversarial scoring of content quality. Quality is structural (did you produce the right artifact shape?) not substantive (is the content good?).

**phuryn/pm-skills** embeds proven frameworks directly into skill logic. The A/B test analysis skill includes statistical significance calculations with ship/extend/stop recommendations. The opportunity-solution tree skill enforces the Teresa Torres structure. Quality comes from framework fidelity rather than scoring.

**agent-pm** focuses on operational quality: dry-run mode, rate limiting, approval gates, Prometheus metrics, cost tracking. It can tell you how much a PRD generation cost and whether it completed, but it cannot tell you whether the PRD is strategically sound.

### Adversarial Review

Only Ashu's pipeline has a dedicated adversarial agent. Gandalf is modeled after the coleam00/adversarial-dev Evaluator pattern. The 10 predefined questions target specific strategic blind spots (TAM math, why-now timing, cannibalization risk, failure modes, pricing model). The 3-round protocol means the PRD Writer must defend its choices with evidence or accept the flag.

product-on-purpose and phuryn both have pre-mortem skills, but a pre-mortem is a creativity exercise ("imagine this failed — why?"), not an adversarial examination of evidence quality. There is no scoring, no pass/fail threshold, no multi-round interrogation.

agent-pm has no adversarial review at all. Its guardrails are operational (don't break Jira) not strategic (is this the right thing to build?).

### Self-Improvement

Ashu's pipeline has explicit eval learnings logs embedded in each skill. The Researcher skill evolved from v0.1.0 to v0.3.0 within a single pipeline run, adding pricing tables, customer voice requirements, evidence tiers, thesis/counterargument structure, section length targets, and hallucination sweeps based on weaknesses found during execution. This is self-improving at the skill level, not just the artifact level.

None of the other three systems have a self-improvement mechanism. product-on-purpose has version tags on releases. phuryn has a CONTRIBUTING.md for community contributions. agent-pm has changelog generation for PRDs. But none modify their own skill definitions based on run-time quality evaluations.

---

## 4. What They Have That Ashu's Pipeline Misses

### From product-on-purpose:
- **Sprint methodologies as first-class workflows.** The Foundation Sprint (2-day strategic alignment) and Design Sprint (5-day prototype-and-test) are fully choreographed 7-skill sequences. Ashu's pipeline has no equivalent for time-boxed group facilitation.
- **Measure and Iterate phases.** The Triple Diamond explicitly covers what happens AFTER launch. Ashu's pipeline ends at Launch Readiness (Stage 6) with no post-launch skill.
- **Meeting family skills.** 8 foundation skills for different meeting types (kickoff, standup, retrospective, review, etc.). Ashu's pipeline produces artifacts but has no facilitation tooling.

### From phuryn/pm-skills:
- **Prioritization framework library.** 9 frameworks (RICE, ICE, MoSCoW, Kano, Opportunity Score, etc.) with structured skill implementations. Ashu's Gandalf asks about scope discipline (Q6) but does not run a prioritization framework.
- **Opportunity-solution trees.** Teresa Torres continuous discovery methodology with outcome-to-experiment mapping. Ashu's Researcher finds opportunities; there is no structured tree connecting them to solutions and experiments.
- **Go-to-market and marketing launch skills.** Positioning, messaging, launch announcements, growth strategy. Ashu's pipeline ends at eng handoff.
- **Data analytics for PMs.** SQL generation, cohort analysis, A/B test design with sample size calculations and statistical significance. Ashu's pipeline has no quantitative post-launch analysis tooling.
- **Stakeholder management.** RACI matrices, alignment workshops, stakeholder mapping. Ashu's pipeline assumes alignment happens in the eng meeting (Step 5 of the 5-step process) but has no structured tooling for it.

### From evalops/agent-pm:
- **External system integrations.** Jira, GitHub, Slack, Gmail, Calendar, Google Drive, Notion connectors. Ashu's pipeline is entirely file-based. Ticket creation, status updates, and stakeholder notifications are manual.
- **PRD versioning with Git semantics.** Branching, blame, changelog generation, approvals. Ashu's pipeline has version incrementing (v1, v2, v3) but no branching, diff viewing, or structured approval workflow.
- **Observability and cost tracking.** Prometheus metrics, structured logging, trace browsing, cost per run. Ashu's pipeline tracks stage completion in pipeline-state.md but has no token cost tracking or performance metrics.
- **Background task queue.** Redis-backed retries, adaptive requeue, remediation playbooks. Ashu's pipeline is synchronous within a single session.

---

## 5. What Ashu's Pipeline Has That Others Don't

### Adversarial Gate with Hybrid Scoring
No other system has a dedicated adversarial agent with quantitative scoring. Gandalf's 10-question framework with rubric + evidence hybrid scoring and 3-round protocol is unique. Pre-mortems are the closest analog, but they are divergent brainstorming exercises, not convergent evidence examinations.

### Context Pruning with Named Envelopes
The explicit context management between stages (full artifact vs. summary vs. executive summary) with token budgets per stage is architecturally sophisticated. product-on-purpose's family contracts validate schema but don't manage context size. phuryn's skills are independent with no inter-skill context management. agent-pm presumably manages context internally but does not expose it as a configurable system.

### DEPENDENCY_GAP Parallel Patching
The mechanism where downstream stages flag missing upstream data for parallel patching is a production engineering pattern (eventual consistency) applied to PM workflows. No other system has this.

### Evidence Chain Across Stages
The evidence tier system (Tier 1-5) with a 40% Tier 1-2 minimum flows from Researcher through PRD Writer to Gandalf evaluation. This creates accountability for evidence quality that spans the entire pipeline. Other systems enforce quality within individual skills but not across them.

### Self-Improving Skills with Eval Logs
Skills that update their own definitions based on run-time quality evaluations is unique. The Researcher went from v0.1.0 to v0.3.0 in a single run, adding 13 specific improvements. This is meta-learning at the skill level.

### Prototype as Pipeline Stage
No other PM OS generates functional HTML prototypes as part of the pipeline. product-on-purpose and phuryn both stop at specs and artifacts. agent-pm generates tickets, not prototypes. Ashu's pipeline produces a validated, interactive Cloudscape HTML prototype with an 18-point validation checklist.

### Design Pattern System
The Designer agent's first-principles-then-reality-check sequence, with explicit consumer (Spotify + Stripe) and enterprise (Salesforce + Datadog) pattern libraries, is not found in any other system. Other systems have UX mock skills but no codified design philosophy system.

---

## 6. Recommendations: Gaps to Fill

The goal is to route new capabilities to existing agents wherever possible, avoiding duplication. Each recommendation identifies which existing agent should absorb the capability.

### Priority 1: Post-Launch Feedback Loop (NEW Stage 7)
**Gap:** Pipeline ends at Launch Readiness. No post-launch measurement.
**Recommendation:** Add a **Stage 7: Post-Launch Evaluator** agent. Input: success metrics from Launch Readiness + actual metrics data. Output: ship/iterate/kill verdict with evidence. This closes the loop that product-on-purpose's Measure/Iterate phases and phuryn's growth/analytics skills cover. Route A/B test analysis and cohort analysis into this agent rather than creating separate skills.

### Priority 2: Prioritization Framework (Route to Gandalf)
**Gap:** No structured prioritization beyond Gandalf's scope discipline question.
**Recommendation:** Extend Gandalf with a **Q11: Prioritization Rigor** question: "Show the RICE/ICE/weighted scoring for top-5 features. What would you cut if timeline shrinks 30%?" This leverages the existing adversarial pattern rather than creating a standalone prioritization agent. Add a RICE scoring template to Gandalf's references directory.

### Priority 3: Opportunity-Solution Tree (Route to Researcher)
**Gap:** Research finds opportunities but does not map them to solutions and experiments.
**Recommendation:** Add a **Step 8.5: Opportunity-Solution Mapping** to the Researcher skill, between Pattern Synthesis and What to Monitor. For each gap/opportunity identified, require: target outcome, 2-3 solution options, and 1 experiment per solution. This flows naturally from the existing pattern analysis.

### Priority 4: External Integration Layer (Route to Launch Readiness)
**Gap:** Pipeline is file-based. No ticket creation, status updates, or notifications.
**Recommendation:** Extend Launch Readiness to optionally generate structured outputs for Linear/Jira (acceptance criteria as ticket templates), Slack (summary notification), and Calendar (eng alignment meeting invite). Do NOT build a full integration layer like agent-pm. Instead, produce copy-paste-ready structured outputs that can be piped to existing tools. Low cost, high value.

### Priority 5: Stakeholder Alignment Toolkit (Route to Launch Readiness)
**Gap:** No RACI, stakeholder map, or alignment facilitation.
**Recommendation:** Add a **Stakeholder Map** section to Launch Readiness output: RACI matrix, key decision-makers, approval chain, and meeting agenda template. This is a natural extension of the eng meeting prep that Launch Readiness already does.

### Priority 6: Go-to-Market Brief (NEW Utility Agent)
**Gap:** No positioning, messaging, or marketing launch planning.
**Recommendation:** Add a **GTM Brief** utility agent (like Research Librarian — callable but not a pipeline stage). Invokable by Launch Readiness or standalone. Produces positioning statement, messaging hierarchy, and launch channel plan. This is net-new capability that does not fit cleanly into any existing agent.

### Lower Priority: Sprint Facilitation
**Gap:** No time-boxed group facilitation skills (Foundation Sprint, Design Sprint).
**Why lower:** Ashu's 5-step process is a personal workflow, not a group facilitation framework. Sprint skills solve a different problem (getting 5 people aligned in 2 days) than the pipeline solves (producing high-quality artifacts for eng handoff). Consider adding only if the eng alignment meeting (Step 5) consistently fails due to lack of pre-alignment.

---

## Summary Scorecard

| Dimension | Ashu's Pipeline | product-on-purpose | phuryn/pm-skills | evalops/agent-pm |
|-----------|:-:|:-:|:-:|:-:|
| **Architecture sophistication** | High (multi-agent, feedback loops, context pruning) | Medium (modular, family contracts) | Low (independent skills, suggested chaining) | High (FastAPI, DI, background queues) |
| **PM methodology depth** | High (evidence tiers, adversarial gates, design patterns) | High (Triple Diamond, sprint methodologies) | Very High (65 skills, 9 frameworks, Teresa Torres, Cagan, Savoia) | Low (PRD generation only) |
| **Quality assurance** | Very High (hybrid scoring, evidence chain, self-improvement) | Medium (CI contracts, schema validation) | Medium (framework fidelity) | Medium (operational guardrails) |
| **Lifecycle coverage** | Partial (research through launch readiness) | Full (discover through iterate) | Full (discovery through growth) | Partial (idea through tickets) |
| **Operational maturity** | Low (file-based, no integrations) | Medium (MCP server, CI) | Low (file-based) | Very High (Jira/Slack/GitHub, Prometheus, Redis) |
| **Prototype generation** | Yes (validated HTML) | No | No | No |
| **Self-improvement** | Yes (eval logs, version bumps) | No | No | No |

The net takeaway: Ashu's pipeline is the deepest system for the research-to-prototype span, with quality mechanisms that no other system matches. Its gaps are at the edges — pre-pipeline (opportunity discovery, prioritization) and post-pipeline (launch execution, growth measurement, external integrations). The recommendations above fill those edges by extending existing agents rather than duplicating what phuryn or product-on-purpose built as standalone skills.

---

**Sources:**
- [product-on-purpose/pm-skills](https://github.com/product-on-purpose/pm-skills) — 55 skills, Triple Diamond, Foundation Sprint, Design Sprint
- [phuryn/pm-skills](https://github.com/phuryn/pm-skills) — 65 skills, 36 workflows, 8 plugins, Teresa Torres / Cagan / Savoia frameworks
- [evalops/agent-pm](https://github.com/evalops/agent-pm) — OpenAI Agents orchestrator, Git-style PRD versioning, Jira/Slack/GitHub integrations
- [product-on-purpose/pm-skills-mcp](https://github.com/product-on-purpose/pm-skills-mcp/) — MCP server variant (maintenance mode, v2.9.3)
