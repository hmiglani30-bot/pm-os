# Stage Notes — Cross-Stage Learning Log

## Stage 1 Notes (Research) — REWRITTEN for AI Control Tower framing
- Decision to inform: Should Quick Desktop build an integrated AI Control Tower capability for discovering, observing, governing, securing, and measuring enterprise AI adoption?
- Key insight: 82% of enterprises have unknown AI agents in infrastructure (CSA 2026). Quick Desktop's cross-vendor desktop presence is the ideal vantage point for shadow AI discovery — no other tool has this endpoint visibility.
- TAM: $492M (AI governance platform market, Gartner 2026), growing 45% CAGR to $1B+ by 2030. SAM: ~$200M (desktop-delivered governance). SOM: ~$12M Year 1.
- Pricing advantage: Quick at $20/user with free tier vs. ServiceNow enterprise ITSM contracts. Land-and-expand: free AI discovery → paid governance.
- Primary competitor: ServiceNow AI Control Tower — 5-pillar platform (Discover, Observe, Govern, Secure, Measure), 30+ integrations, kill switches, Action Fabric MCP Server. Counterargument: ITSM-centric, sits on top of cloud, no desktop/endpoint visibility.
- 5 key opportunities identified: (1) Desktop-level AI discovery, (2) Assistant-model governance (guide don't block), (3) Cross-vendor AI cost attribution, (4) AI adoption measurement/ROI, (5) Compliance automation
- Interaction pattern benchmarking: ServiceNow has 5-pillar navigation; Datadog has 6-section sidebar. Quick Desktop prototype needs 5-6 top-level sections minimum.
- **For PRD Writer:** Use the "cockpit, not control tower" positioning — Quick Desktop puts governance where employees work, not in an IT dashboard. Solution Lineage should trace to Opportunity-Solution Tree (5 opportunities, 12 directions). Dual-scope boundary critical: Proto v1 must show 5-pillar navigation (Discover, Observe, Govern, Secure, Measure) even if Eng v1 only builds Discovery + Observe.
- Customer voice: 76% CIOs say unchecked AI is serious concern, 54% C-suite say AI "tearing company apart," 29% employees sabotaging AI strategy, 65% experienced AI agent incidents

## Stage 0.5 Notes (Current State Audit)
- Amazon Quick Desktop launched April 28, 2026 in preview — very new product, limited user feedback available
- Key pain points identified: cold-start discoverability gap (no onboarding), notification overload risk, opaque knowledge graph, limited offline capability, integration setup friction
- Adjacent products: Quick Web app, Q Developer/Kiro CLI, M365 Extensions (preview), AWS services ecosystem
- Competitor UX patterns: Microsoft Copilot uses embedded sidebar in M365 apps; Google Gemini uses sidebar + @mentions; ChatGPT Desktop uses floating overlay; Claude Desktop uses conversation-first interface
- **For Researcher:** Quick is positioned as cross-vendor workflow agent (not competing with Copilot/Gemini directly but complementing them). Pricing undercuts at $20/user vs ~$30 for competitors. Focus research on the cross-app orchestration angle and the "AI that knows you" knowledge graph differentiation.
- **For PRD Writer:** The dual identity (web + desktop) creates UX complexity. Proto v1 needs minimum 6 pages to match competitor surface area. Mandatory interaction patterns: proactive notification center, cross-app command palette, knowledge graph visualization, integration marketplace, content creation studio.
- Grounding constraints: Must maintain continuity with Quick web experience; must support 50+ third-party integrations; must handle preview-phase instability gracefully; knowledge graph must be transparent and controllable

## Stage 0 Notes (Setup)
- Pipeline initialized for Amazon Quick Desktop App
- Mode: Standard (stages 0–6 with feedback loops)
- Amazon Quick is a desktop AI assistant/productivity app by Amazon, launched April 2026 in preview for macOS and Windows
- Key differentiators: proactive background operation, personal knowledge graph, cross-app integration (Slack, Teams, Google Workspace, Salesforce, etc.), local file access, content creation (presentations, dashboards, apps)
- Pricing: Free tier, Plus ($20/user/month), Professional, Enterprise tiers
- Major enterprise adopters: 3M, GoDaddy, AstraZeneca, BMW, Mondelez, NFL, Southwest Airlines, New York Life
- **For Auditor:** Focus on the desktop app specifically — local file access, proactive notifications, browser automation, cross-app integration UX
