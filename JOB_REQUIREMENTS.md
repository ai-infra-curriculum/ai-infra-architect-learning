# AI Infrastructure Architect — Job Requirements

**Role level:** 45
**Generated:** 2026-10-08
**Window:** 2026-07-10 → 2026-10-08 (90 days)
**Sample:** 33 postings analyzed, 28 in-window confirmed (frequency denominator = 28)
**Prior sample:** 2026-09-08 (denominator 20)
**Employer overlap with prior sample:** 0 — this is a near-complete refresh.

## Executive summary

The market shape has not changed since the 2026-09 cycle. **Agentic AI / multi-agent orchestration (0.86)** and **enterprise LLM / RAG (0.82)** remain co-dominant and unchanged in surface area. Responsible AI / guardrails (0.61) and enterprise AI security (0.39) softened at headline but the **combined governance + security surface still exceeds 0.75** — the signal is intact, it is just distributed differently across postings this cycle. All headline requirements are already covered by the existing curriculum.

**No candidate NEW requirement clears the ≥0.30-frequency + ≥3-postings threshold that isn't already covered.** Four below-threshold observations are worth tracking:

- **LLM / agent evaluation frameworks (0.29, ↑ from 0.25)** — approaching but still below the 0.35 trigger the prior cycle set. Fold into existing `mod-306` observability and `mod-308` guardrails lectures.
- **MCP as explicit named protocol (0.21, ↑ from 0.15)** — reversed the prior cycle's "being absorbed into agentic" assessment. Still well below threshold.
- **Dedicated "AI Security Architect" job title (0.11, NEW title-level pattern)** — MetLife, Prudential, and BMO Platform & Fabrics are the carriers. Below threshold; covered by `mod-303`.
- **AI gateway as a named platform component (0.18, ↑ from 0.15)** — explicit "AI Gateway" / "model gateway" language hardening. Covered inside multi-LLM routing.

**One prior "watch" signal has DROPPED and is being downgraded:**

- **Architect-led AI developer tooling rollout (0.07, ↓ from 0.20)** — the "NEW pattern" flagged last cycle did not harden in the subsequent window. Likely a short-lived Q2/Q3-2026 blip. Downgrade from "tracked-below-threshold" to "not currently a signal."

**One prior prediction did NOT come true:**

- **Sovereign AI / on-prem private LLM hosting** was predicted last cycle to cross 0.30 "if trajectory continues." It actually dropped to 0.07. No action needed; current `mod-302` coverage remains appropriate.

**Recommendation:** zero net-new modules, exercises, or projects this cycle. See `.aicg/curriculum-plan-delta.json` (empty arrays).

## Requirements — covered by this role's curriculum

### Agentic AI and multi-agent orchestration — freq 0.86 ↑
- **Coverage:** [`lessons/mod-308-llm-rag`](lessons/mod-308-llm-rag) (plus the 2026-07-proposed exercise-06 on agentic orchestration + MCP governance, which remains unmerged — see Methodology notes)
- **Named frameworks in-window:** LangGraph, LangChain, CrewAI, AutoGen, Semantic Kernel, Google ADK/NGA, Temporal (as orchestrator)
- **Named sub-patterns in-window:** A2A (Agent-to-Agent), MCP (Model Context Protocol), memory governance, tool-use governance
- **Evidence:** Mastercard, Microsoft, UnitedHealth, Tiger Analytics, Accenture (BE+US), Cognizant (×2), GE Vernova, DIRECTV, CACI, FinThrive, LPL, Priceline, MetLife, Deloitte (×2), Wells Fargo, Disney, Verizon, KPMG, Salesforce, Fidelity
- **Delta:** +0.01 vs 2026-09. Flat at the headline. Framework convergence (LangChain / LangGraph / CrewAI / Semantic Kernel) continues.

### Enterprise LLM platform + RAG at scale — freq 0.82 ↓ (from 1.00)
- **Coverage:** [`lessons/mod-308-llm-rag`](lessons/mod-308-llm-rag), [`projects/project-303-llm-rag-platform`](projects/project-303-llm-rag-platform)
- **Evidence:** Microsoft, UnitedHealth, Tiger Analytics, Accenture (BE+US), Cognizant (×2), GE Vernova, DIRECTV, CACI, FinThrive, Snowflake, LPL, Priceline, Accenture, Deloitte (×2), Wells Fargo, Disney, Verizon, KPMG, Fidelity
- **Delta:** -0.18. Still dominant. The dip is composition — specialized AI Security Architect postings (MetLife, Prudential) and platform-infrastructure postings (BMO Platform & Fabrics, PwC) do not foreground RAG. For generalist AI Architect roles it remains near-universal.

### Responsible AI, guardrails, and AI governance — freq 0.61 ↓ (from 0.75)
- **Coverage:** [`lessons/mod-308-llm-rag`](lessons/mod-308-llm-rag), [`lessons/mod-303-security-compliance`](lessons/mod-303-security-compliance), [`lessons/mod-306-enterprise-mlops`](lessons/mod-306-enterprise-mlops)
- **Evidence:** Mastercard, UnitedHealth, Cognizant (×2), MetLife, Prudential, Priceline, Wells Fargo, Fidelity, BMO, Accenture (US), KPMG, Salesforce, Deloitte (×2), Verizon, Microsoft (implicit via evaluation)
- **Delta:** -0.14. Still above threshold. Combined with enterprise AI security below, governance surface is >0.75.

### Vector database architecture — freq 0.46 ↓ (from 0.65)
- **Coverage:** [`lessons/mod-308-llm-rag`](lessons/mod-308-llm-rag)
- **Named DBs in-window:** Pinecone, Weaviate, Milvus, pgvector, QDrant, Azure AI Search, Redis, ChromaDB, Elasticsearch, Cosmos DB
- **Evidence:** Tiger Analytics, GE Vernova, DIRECTV, CACI, Cognizant (×2), FinThrive, LPL, Priceline, Wells Fargo, PwC, Verizon, Deloitte (Life Sci)

### Enterprise AI security architecture — freq 0.39 ↓ (from 0.70)
- **Coverage:** [`lessons/mod-303-security-compliance`](lessons/mod-303-security-compliance), [`projects/project-305-security-framework`](projects/project-305-security-framework)
- **Evidence:** Mastercard, BMO, MetLife, Accenture (US), PwC, Prudential, Salesforce, Verizon (partially), FinThrive, Fidelity, Priceline
- **Delta:** -0.31. The signal is splitting into two surfaces: (a) generalist architect roles fold security into governance language; (b) a dedicated "AI Security Architect" sub-category is emerging (see tracked signal below). `mod-303` covers both. The combined guardrails + security surface still exceeds 0.75.

### Multi-cloud architecture (AWS / Azure / GCP) — freq 0.36 ↓ (from 0.65)
- **Coverage:** [`lessons/mod-302-multicloud-hybrid`](lessons/mod-302-multicloud-hybrid), [`projects/project-302-multicloud-infrastructure`](projects/project-302-multicloud-infrastructure)
- **Delta:** -0.29. 2026-10 sample skews toward single-hyperscaler specialization (Microsoft, KPMG=AKS, Snowflake, Verizon=Vertex AI). Still above the 0.30 threshold.

### Architecture governance, ADRs, and reference architectures — freq 0.36 ~
- **Coverage:** [`lessons/mod-301-enterprise-architecture`](lessons/mod-301-enterprise-architecture), [`lessons/mod-309-arch-communication`](lessons/mod-309-arch-communication)
- **Evidence:** Accenture (US) ("blueprints"), UnitedHealth, Fidelity, Prudential, Salesforce, PwC, FinThrive, Priceline, Mastercard, LPL

### Team leadership, mentoring, cross-team initiatives — freq 0.36 ↓↓ (from 0.80)
- **Coverage:** [`lessons/mod-309-arch-communication`](lessons/mod-309-arch-communication)
- **Delta:** -0.44. Large drop — mostly sampling composition (the 2026-09 denominator-20 was heavy on Principal/Director postings that explicitly scope mentorship as a top-3 responsibility; 2026-10 includes more Platform Architect and AI Security Architect postings where mentorship is implicit). Combined "leadership-flavored" language (set standards, mentor, enterprise direction) is >0.60. Coverage holds.

### Ships code — production-grade async Python and prototypes — freq 0.32 ~
- **Coverage:** existing project deliverables in [`lessons/mod-308-llm-rag`](lessons/mod-308-llm-rag) and [`lessons/mod-306-enterprise-mlops`](lessons/mod-306-enterprise-mlops)
- **Note:** Continues to hover above threshold. "Not limited to high-level design" (LPL) is now explicit JD language.

### AI/ML observability — freq 0.36 ~ (delegated)
- **Owner:** MLOps Engineer track ([`../ai-infra-mlops-learning/CURRICULUM.md`](../ai-infra-mlops-learning/CURRICULUM.md))
- **Architect context:** [`lessons/mod-306-enterprise-mlops`](lessons/mod-306-enterprise-mlops) topic "Model monitoring and observability architecture"
- **Named tools in-window:** OpenTelemetry, LangSmith, LangFuse, Arize, LLM observability (generic)

### Enterprise MLOps / LLMOps platform architecture — freq 0.29 ↓ (from 0.55)
- **Coverage:** [`lessons/mod-306-enterprise-mlops`](lessons/mod-306-enterprise-mlops), [`projects/project-301-enterprise-mlops-platform`](projects/project-301-enterprise-mlops-platform)
- **Note:** The signal is migrating from generic "MLOps platform" phrasing to specific capability names (prompt management, model registries, model gateways, evaluation pipelines) which show up tagged under adjacent requirements. Combined capability language is >0.50.

### Multi-LLM provider portfolio and AI-gateway / model-routing — freq 0.29 ↓
- **Coverage:** [`lessons/mod-308-llm-rag`](lessons/mod-308-llm-rag)
- **Note:** The AI-gateway sub-pattern (named "AI Gateway" / "model gateway") is HARDENING even as the general multi-LLM language softens. See tracked signal below.

### Kubernetes at enterprise scale — freq 0.07 ↓ (delegated)
- **Owner:** ML Platform Engineer track ([`../ai-infra-ml-platform-learning/CURRICULUM.md`](../ai-infra-ml-platform-learning/CURRICULUM.md))
- **Architect context:** platform-selection and topology decisions inside `mod-302` and `mod-306`.

### Executive communication and stakeholder management — freq 0.21 ↓
- **Coverage:** [`lessons/mod-309-arch-communication`](lessons/mod-309-arch-communication)
- **Note:** Explicit mostly in consulting-firm postings this cycle.

### MCP governance and tool-use platforms — freq 0.21 ↑ (from 0.15)
- **Coverage:** [`lessons/mod-308-llm-rag`](lessons/mod-308-llm-rag) (prior-cycle proposed exercise-06)
- **Evidence:** DIRECTV, GE Vernova, LPL, Mastercard, Deloitte (Anthropic/Claude), Verizon
- **Note:** The prior cycle predicted MCP would be "absorbed into agentic orchestration" and lose its named signal. The 2026-10 sample REVERSED that — MCP is explicitly named more often. Still well below the 0.30 threshold.

### Compliance frameworks — freq 0.18 ↓ (from 0.30)
- **Coverage:** [`lessons/mod-303-security-compliance`](lessons/mod-303-security-compliance), [`projects/project-305-security-framework`](projects/project-305-security-framework)
- **Named frameworks in-window:** EU AI Act, NIST AI RMF, ISO 42001, OSFI E-23, OCC, HIPAA, FedRAMP, IL-5, OWASP Top 10 for LLM Applications, MITRE ATLAS, GDPR, DORA
- **Note:** OWASP LLM Top 10 and MITRE ATLAS are now routinely named for AI-specific threat modeling — a new sub-pattern inside the compliance surface.

### Enterprise data platform architecture (lakehouse, streaming) — freq 0.18 ↓
- **Coverage:** [`lessons/mod-307-data-architecture`](lessons/mod-307-data-architecture), [`projects/project-304-data-platform`](projects/project-304-data-platform)
- **Note:** Continues the delegation trajectory. Still material for AI Data Architect sub-category (GE Vernova explicit).

### Fine-tuning strategy — freq 0.11 ↓
- **Coverage:** [`lessons/mod-308-llm-rag`](lessons/mod-308-llm-rag) topic "Fine-tuning vs RAG vs prompt engineering tradeoffs"
- **Note:** Techniques firmly in ML Engineer scope; architect retains the trade-off decision.

### FinOps and AI cost optimization — freq 0.11 ↓
- **Coverage:** [`lessons/mod-304-cost-finops`](lessons/mod-304-cost-finops)
- **Note:** Capability is being subsumed into model-routing / AI-gateway requirements (Mastercard, Priceline name cost as a routing dimension).

### Sovereign AI / data-residency / on-prem private LLM hosting — freq 0.07 ↓ (from 0.20)
- **Coverage:** [`lessons/mod-302-multicloud-hybrid`](lessons/mod-302-multicloud-hybrid), [`lessons/mod-303-security-compliance`](lessons/mod-303-security-compliance)
- **Note:** The 2026-09 prediction that this would cross 0.30 did NOT come true. Signal is weaker, not stronger. Carriers this cycle: CACI (IL-5) and UnitedHealth (hybrid on-prem OpenShift). Monitor but no action.

### Data governance, lineage, catalog — freq 0.07 ↓
- **Coverage:** [`lessons/mod-307-data-architecture`](lessons/mod-307-data-architecture)

### Emerging AI technology evaluation and vendor selection — freq 0.07 ~
- **Coverage:** [`lessons/mod-310-emerging-tech`](lessons/mod-310-emerging-tech)

### High availability and disaster recovery for AI — freq 0.04 ~
- **Coverage:** [`lessons/mod-305-ha-dr`](lessons/mod-305-ha-dr), [`projects/project-302-multicloud-infrastructure`](projects/project-302-multicloud-infrastructure)
- **Note:** Near-zero as verbatim JD language but implicit in every enterprise architect role.

### TOGAF / enterprise architecture frameworks — freq 0.00 ↓
- **Coverage:** [`lessons/mod-301-enterprise-architecture`](lessons/mod-301-enterprise-architecture)
- **Note:** Fell to zero in this sample. Postings favor "reference architectures" and "blueprints" as the deliverable language, not the TOGAF credential. Retain as foundational.

### GPU cluster architecture — freq 0.00 (delegated)
- **Primary owner:** AI Infrastructure Performance Engineer (level 35, [`../ai-infra-performance-learning/CURRICULUM.md`](../ai-infra-performance-learning/CURRICULUM.md))
- **Note:** The 2026-10 sample happened not to include hyperscaler-adjacent architect postings. Signal is composition-dependent; capability is not gone from the market.

### Feature stores / real-time feature serving — freq 0.00 ~
- **Coverage:** [`lessons/mod-306-enterprise-mlops`](lessons/mod-306-enterprise-mlops) (retained for classical-ML learners)

## Requirements — out of scope for this role

### Edge AI / on-device — freq 0.00
Absent from enterprise AI Architect scope. Direct edge learners to a separate Edge AI track.

### Sustainability / green AI — freq 0.00
Absent from candidate demand. Awareness-level coverage remains in `mod-310`.

## New signals tracked (below threshold — no additions this cycle)

### LLM / agent evaluation frameworks — freq 0.29 ↑
LangSmith, LangFuse, Arize, RAGAS, DeepEval, Braintrust, offline benchmarks + online quality metrics. Up from 0.25. Still below the 0.35 trigger the prior cycle set.

**Recommendation:** continue to absorb into `mod-306` (observability) and `mod-308` (safety / guardrails) lecture content. If this crosses 0.35 next cycle, add a dedicated exercise.

**Evidence:** Microsoft, Verizon, KPMG, Priceline, Cognizant (Agentic Remote), Wells Fargo, Deloitte (×2).

### Dedicated "AI Security Architect" as a distinct JD category — freq 0.11 NEW
Title-level emergence: MetLife "Sr. AI & Agentic Security Architect", Prudential "AI Security Architect", BMO "Principal Engineer, AI Platform & Fabrics" (functionally an AI-platform-security role). Below the frequency threshold but at the 3-posting floor.

**Recommendation:** monitor. If this grows to 0.20+ next cycle, consider branching the Senior Architect track to include an AI Security Architecture specialization pathway. NOT a 2026-10 action.

**Evidence:** MetLife, Prudential, BMO.

### Agentic security patterns — freq 0.18 ~
SPIFFE/SPIRE-like workload identity for agents, prompt firewalls, agent permissions, sandboxed tool execution, MITRE ATLAS threat modeling. Flat vs 2026-09.

**Recommendation:** absorb into existing `mod-303` lectures as agent-specific security patterns. No new module. If this crosses 0.30 next cycle, add a dedicated exercise on agentic security.

**Evidence:** MetLife, Prudential, BMO, Mastercard, PwC.

### AI gateway as architect-owned platform component — freq 0.18 ↑
"AI Gateway" / "model gateway" / "inference gateway" now named as explicit platform capabilities in financial-services and consulting architect JDs. Rose from 0.15 → 0.18.

**Recommendation:** light-touch coverage inside existing `mod-308` multi-LLM section remains sufficient. No standalone track.

**Evidence:** BMO, Priceline, PwC, UnitedHealth (×2).

## Signals downgraded this cycle

### Architect-led adoption of AI developer tooling — freq 0.07 ↓↓ (from 0.20)
The "NEW pattern" the prior cycle flagged did NOT harden. Only Disney (Claude Code / Cursor / Copilot) and Deloitte-Anthropic (Claude Agent SDK) explicitly scope this. Likely a short-lived Q2/Q3-2026 blip. **Downgrade from "tracked-below-threshold" to "not currently a signal."** Monitor but do not continue to flag.

### SLM (small language model) strategy — freq 0.00
Still absent. Not a signal.

## External resources for out-of-scope items

None this cycle — no requirement was found that (a) applies to this role and (b) has no learning path within the ecosystem.

## Sampled postings (in-window, 28 total)

| Employer | Title | URL | Posted |
|---|---|---|---|
| Mastercard | Principal Agentic Platforms Architect | https://builtin.com/job/principal-agentic-platforms-architect/11009633 | within 90 days (removed 2026-10-07) |
| Microsoft | Principal AI Architect - M365 IC3 Team | https://apply.careers.microsoft.com/careers/job/1970393556959677 | 2026-10-07 |
| UnitedHealth Group (Optum Tech) | Principal Architect - Remote | https://careers.unitedhealthgroup.com/job/minnetonka/principal-architect-remote/34088/101406133952 | 2026-10-01 |
| UnitedHealth Group (Optum Tech) | Principal AI/ML Platform Engineer - Remote | https://careers.unitedhealthgroup.com/job/eden-prairie/principal-ai-ml-platform-engineer-remote/34088/100730962096 | 2026-09-16 |
| Accenture (US) | Advanced AI Architect | https://www.accenture.com/us-en/careers/jobdetails?id=R00330053_en | ~2026-09 (anticipated open until 2026-10-02) |
| Accenture (Belgium) | AI LLM Technology Architecture Associate Director | https://www.accenture.com/be-en/careers/jobdetails?id=R00345451_en | ~2026-09-30 |
| MetLife | Sr. AI & Agentic Security Architect | https://talents.vaia.com/companies/metropolitan-life-insurance-company/sr-ai-agentic-security-architect-158994349/ | 2026-08-06 |
| Deloitte | Agentic AI Engineer - Anthropic/Claude | https://apply.deloitte.com/en_US/careers/JobDetail/Agentic-AI-Engineer-Anthropic-Claude/365634 | ~2026-09 (recruiting ends 2026-10-30) |
| Deloitte | AI Solutions Architect - Life Sciences | https://apply.deloitte.com/en_US/careers/JobDetail/AI-Solutions-Architect-Life-Sciences/357404 | ~2026-09 (recruiting ends 2026-10-30) |
| Wells Fargo | Principal Engineer, AI Engineering | https://builtin.com/job/principal-engineer-ai-engineering/10699655 | ~2026-09 (reposted 9 days ago) |
| The Walt Disney Company | Director, AI Enablement & Legal Engineering | https://www.disneycareers.com/en/job/burbank/director-ai-enablement-and-legal-engineering/391/101107920944 | 2026-09-24 |
| Verizon | Principal Conversational & Agentic AI Architect | https://mycareer.verizon.com/jobs/r-1095664/principal-conversational-agentic-ai-architect/ | ~2026-09 |
| KPMG LLP | AI Architect - Director | https://www.kpmguscareers.com/jobdetail/?jobId=133595 | ~2026-09 |
| PwC | AI Platform Architect | https://freehire.me/jobs/ai-platform-architect-pwc-l4ff4n5g | 2026-09-23 |
| Salesforce | Principal Data and AI Architect | https://builtin.com/job/principal-data-and-ai-architect/11172148 | ~2026-09 (24 days ago) |
| Prudential | AI Security Architect | https://freehire.me/jobs/ai-security-architect-prudential-6l3ogsmd | 2026-09-23 |
| Fidelity International | Lead Enterprise AI Architect | https://freehire.me/jobs/lead-enterprise-ai-architect-fil-h2kayuvm | 2026-08-27 |
| Tiger Analytics | Lead AI Architect & Delivery Manager | https://apply.workable.com/j/16441577E7 | 2026-09-29 |
| Cognizant | Gen AI Architect (Agentic AI & LLM) Remote | https://careers.cognizant.com/us-en/jobs/00070546971/gen-ai-architect-agentic-ai-llm-remote/ | 2026-09-25 |
| Cognizant | Gen AI Architect (Chennai) | https://careers.cognizant.com/us-en/jobs/00069577201/gen-ai-architect/ | 2026-09-18 |
| GE Vernova | Principal AI Data Architect | https://careers.gevernova.com/principal-ai-data-architect/job/R5053705 | 2026-09-22 |
| DIRECTV | Principal AI Architect | https://jobs.directv.com/job/el-segundo/principal-ai-architect/390/100996441104 | ~2026-09-23 |
| CACI | AI Platform Architect | https://caci.wd1.myworkdayjobs.com/External/job/Remote-Any-State/AI-Platform-Architect_332344 | 2026-09-18 |
| FinThrive | Lead AI Architect | https://jobs.dayforcehcm.com/finthrive/candidateportal/jobs/8252 | 2026-09-11 |
| Snowflake | Senior AI/ML Architect, Applied Field Engineering | https://jobs.ashbyhq.com/snowflake/95cf7159-efd2-400c-b29e-bdd86c9c9eb2 | 2026-08-13 (updated 2026-10-03) |
| LPL Financial | Principal AI Architect | https://lplfinancial.wd1.myworkdayjobs.com/CFN/job/Fort-MillCharlotte/Principal-AI-Architect_R-052957 | 2026-08-14 (updated 2026-09-04) |
| Priceline | Principal Enterprise Architect, AI Platform | https://careers.priceline.com/job/r5671/ | within 90 days (active) |
| BMO (Bank of Montreal) | Principal Engineer, AI Platform & Fabrics | https://bmo.wd3.myworkdayjobs.com/en-US/External/job/Chicago-Heights-IL-USA/Principal-Cloud-Engineer-AI_R260025275 | active (deadline 2026-10-29) |

## Methodology notes

- **Window:** 2026-07-10 → 2026-10-08 (90 days).
- **Sample:** 33 postings surfaced; 28 confirmed in-window + architect-scope.
- **Dropped:** 2 engineer-scope postings (BlackRock "AI Infrastructure Engineer" — IaC-focused engineer work; Palo Alto Networks Sr Principal AI Software Engineer — >6 months old); 1 duplicate UnitedHealth Principal Architect posting (two Workday office listings for the same role).
- **Frequency denominator:** 28 (strict confirmed-only).
- **Employer overlap with prior sample:** 0 — this is a near-complete refresh of the posting pool. Treat deltas ≤ 0.20 as sampling composition noise unless the signal is already borderline. GE Vernova and BMO have NEW postings in this cycle (different req IDs and titles from 2026-09).
- **Older-but-reposted:** Snowflake (2026-08-13, updated 2026-10-03), LPL Financial (2026-08-14, updated 2026-09-04), MetLife (2026-08-06), Fidelity International (2026-08-27), and Priceline (undated active listing) all have origin-posted dates older than 60-90 days but were last re-listed or confirmed active within the window; included per the "reposted or still-active" convention from prior cycles.
- **Standing freshness-depth caveat:** the 2026-07 and 2026-09 cycles both proposed a `mod-308` exercise-06 on agentic orchestration + MCP governance. That proposal remains unmerged (only 5 exercises exist in `mod-308` as of 2026-10-08). This is a freshness / depth gap in the material under an existing covered requirement, not a new-requirement gap. Addressing it is a different proposal than this job-requirements packet.
