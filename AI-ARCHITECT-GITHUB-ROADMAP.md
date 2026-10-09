# AI Architect GitHub Roadmap for Rathesh R

> **Audience:** Internal execution plan. Do not treat this file as the public face of the profile.
>
> **Public surfaces:** [`README.md`](README.md) → [`docs/PRODUCT_BRIEF.md`](docs/PRODUCT_BRIEF.md) → [`docs/ROADMAP.md`](docs/ROADMAP.md) → ADRs and evaluation reports. Website and LinkedIn must link those canonical artifacts instead of duplicating them.
>
> **Working project name:** `reasoning-rag`  
> **GitHub account:** `ratheshr8`  
> **Profile repository:** `ratheshr8/ratheshr8`  
> **Flagship repository:** `ratheshr8/reasoning-rag`  
> **Profile positioning:** Rathesh R — AI Architecture & Engineering

This is an execution plan, not a claim that any capability has already been built. Treat the architecture as a set of hypotheses to validate with implementation and measured results. Keep the project independently designed and implemented. It may acknowledge public ideas such as hierarchical document trees and reasoning-based retrieval, including PageIndex, but must not copy PageIndex's code, branding, documentation, or imply affiliation.

## 1. North-star goals

### Portfolio goals

- Present a coherent, evidence-backed profile for AI Architect and AI Engineering roles.
- Demonstrate architecture judgment across AI application design, agentic systems, retrieval, evaluation, governance, security, and operations.
- Make the flagship project easy to understand, run, evaluate, and extend.
- Prefer a few maintained repositories with strong documentation and reproducible evidence over many thin demonstrations.
- Show the reasoning behind decisions through ADRs, trade-off analysis, and benchmark results.
- Map every public claim to a hireable skill and a concrete artifact (code, ADR, eval, or labeled design).

### Flagship product goal

Build a document question-answering system that can retrieve relevant evidence from long, structured documents primarily by navigating a document hierarchy and reasoning over its summaries and metadata. It should provide traceable citations and abstain when evidence is missing or weak.

“Vectorless” describes the primary retrieval path: vector similarity is not required for indexing or retrieval. It does not mean that every version must ban embeddings. Optional lexical, metadata, or vector-based baselines may be used for comparison, fallback experiments, or explicitly selected hybrid modes. State the retrieval mode clearly in every demo and benchmark.

### Success principles

1. **Evidence before claims:** every performance claim links to a reproducible evaluation.
2. **Small vertical slices:** each phase ends in a runnable, reviewable result.
3. **Provider-neutral core:** keep model and storage integrations behind interfaces where that reduces lock-in without creating needless abstraction.
4. **Safe by default:** treat document content as untrusted input and keep secrets out of source control.
5. **Independent work:** use PageIndex and related systems as prior art for study, not as implementation templates to copy.
6. **Showcase by skills:** visitors should see where each competency is demonstrated, not a wish list of future repositories.

## 2. Positioning and audience

### Public identity

Use a consistent identity across GitHub, LinkedIn, and `ratheshworld.com`:

**Name:** Rathesh R  
**GitHub:** `ratheshr8`  
**Headline (current, until the domain evidence gate is met):** AI Architecture & Engineering | Agentic Systems | AI Governance  
**Headline (allowed after the gate):** AI Architecture & Engineering | Agentic Systems | AI Governance | Healthcare and FinTech  
**Short positioning statement:** I design and build reliable AI systems, from retrieval and agent workflows to evaluation, governance, and production architecture.

### Headline evidence gate (Healthcare and FinTech)

Do not lead GitHub, LinkedIn, or `ratheshworld.com` with Healthcare or FinTech until all of the following are true:

1. A public, labeled **synthetic or reference-only** case study exists (not employer or customer data).
2. The artifact states that it is a portfolio prototype, not regulated production experience.
3. The case study includes a threat model or domain-aware design notes that a reviewer can inspect.
4. The claim can be traced from the profile README to that artifact in one click.

Until then, keep domain words out of headlines, bios, and featured-project blurbs. Use only domains that reflect demonstrated work.

### Audience

- Hiring managers and engineering leaders evaluating architecture depth.
- AI engineers looking for practical patterns they can reproduce.
- Technical peers reviewing design choices and evaluation quality.
- Potential collaborators interested in evidence-grounded document intelligence.

### Portfolio narrative

Tell one story: **designing trustworthy AI systems from architecture through measurable implementation**. The flagship explores reasoning-first retrieval. Supporting repositories should demonstrate complementary skills such as governance, agent lifecycle, domain reference architectures, and specification-driven engineering. Do not publish all of these as empty shells; release them only when each has a useful, finished slice. Do not pin a repository that fails the release bar in Section 5.

## 3. Skills showcase map

Every hireable skill the profile claims must point to a public artifact. Until that artifact exists, list the skill as **planned** on internal docs only — not as a featured proof on the profile README.

| Skill | Primary proof in `reasoning-rag` | Visible from | Secondary proof (after flagship M5) |
| --- | --- | --- | --- |
| AI system design | Architecture diagram and ADRs | M1–M2 | Governance or agentic SDLC repo |
| Retrieval / RAG judgment | Tree-first vs lexical/vector baselines | M3, M5 | Evaluation report |
| Agentic / planning | Bounded planner, budgets, inspectable traces | M4 | Agentic SDLC playground |
| Evaluation / quality | Versioned dataset and failure analysis | M5 | Smoke eval in CI |
| Governance / risk | Threat model, abstention, limitations | M3, M6 | Governance reference architecture |
| Security | Prompt-injection tests, citation validation, secret hygiene | M6 | `SECURITY.md` and dependency scanning |
| Ops / platform thinking | Observability fields, cost/latency, provider interface | M5–M6 | Control plane only if the scope is distinct |
| Spec / harness engineering | Schemas, fixtures, quality gates | M1, M5 | Spec/harness mini-repo |
| Communication | Profile README, case study, milestone posts | M0, M7 | Website project page |

### Public skill proofs (ship these first)

- **After M2:** tree visualization and provenance note (architecture skill).
- **After M3:** one demo trace with a citation and an abstention (trustworthiness skill).
- **After M5:** benchmark report with cost and latency (evaluation skill).
- **After M6:** tagged release, security notes, and limitations (release judgment).
- **Only then (M8):** one complementary repository for a *different* skill cluster — not healthcare, harness, and control plane in parallel.

## 4. GitHub profile setup

### Public surface hierarchy

Hiring managers land in this order. Keep each layer thinner than the one below it, and link down rather than copying.

1. **Profile README** (`ratheshr8/ratheshr8`) — role, three featured items with status, skills bullets that link to artifacts.
2. **Flagship README** (`ratheshr8/reasoning-rag`) — problem, what works now, quickstart, retrieval mode, limitations.
3. **ADRs, product brief, evaluation reports** — decisions, protocol, and evidence.
4. **Website and LinkedIn** — same story, linking to GitHub as canonical.

Do not paste this master roadmap into the profile README. Link [`docs/ROADMAP.md`](docs/ROADMAP.md) for the public plan.

### Profile repository and README

1. Use the existing special public repository `ratheshr8/ratheshr8`. GitHub displays its README on the profile. It currently still describes Flutter interest; replace it with the reviewed AI Architecture README only after every statement is true.
2. Adapt [`docs/profile/GITHUB_PROFILE_README.md`](docs/profile/GITHUB_PROFILE_README.md). Do not replace an existing README in another repository without reviewing its current purpose.
3. Keep the profile README concise and scannable:
  - One-line role and focus (headline after the evidence gate in Section 2).
  - A short “what I build” paragraph.
  - A **Skills demonstrated** subsection: 4–6 bullets, each linking to a repo path, ADR, or labeled “planned until M*”.
  - Two or three featured projects with status and direct links. Do not feature empty shells.
  - Selected architecture, evaluation, and security topics with links.
  - Website and LinkedIn links.
  - Contact route only if intentionally public.
4. Use badges sparingly. Avoid contribution graphs, animated widgets, or technology lists that crowd out evidence.
5. Clearly mark projects as **prototype**, **experimental**, or **production** according to reality.

### Profile quality checklist

- Avatar, display name, bio, and location are accurate and professionally consistent.
- Website points to `ratheshworld.com` and LinkedIn points to the intended profile.
- Featured repositories have a clear README, license where appropriate, and a visible status.
- Pinned repositories tell a deliberate story; pin the flagship first once it meets the Section 5 release bar.
- Repository topics are specific and maintained; avoid keyword stuffing.
- Public contact information is intentional and does not expose private details.

## 5. Repository strategy

### Pin policy (no empty pins)

Pin only repositories that meet the release bar below.

1. **First pin:** `reasoning-rag`, after it is understandable without a personal walkthrough.
2. **Second pin:** one complementary repo, and only after flagship **M5** (measured system) and that repo has its own finished slice.
3. **Profile README** is the skills index; it is not a pin substitute for unfinished work.

Never pin a repository that is a stub, a renamed empty template, or a backlog idea. If a pin would require a verbal explanation to make sense, it is not ready.

### Repository sequence

Build in this order, based on readiness rather than a fixed calendar. Items 2–6 are **backlog until flagship M5+**. Do not create, announce, or pin them before then.

1. **`reasoning-rag` — flagship:** reasoning-first retrieval, evidence, evaluation, and an executable demo.
2. **AI Governance Reference Architecture (backlog):** model inventory, risk controls, evaluation gates, human oversight, and operational evidence.
3. **Agentic SDLC Playground (backlog):** practical design/build/review/evaluate workflow for an agentic feature, with boundaries and audit trail.
4. **Healthcare AI Reference Architecture (backlog):** privacy-conscious reference design with synthetic data only, explicit regulatory caveats, and the Section 2 headline evidence gate.
5. **Specification Engineering / Harness Engineering (backlog):** a compact example of specifications, quality gates, test fixtures, and feedback loops.
6. **AI Control Plane (backlog):** pursue only when there is a concrete scope that does not duplicate the governance and agent lifecycle repositories.

The prior conversation initially proposed a broader portfolio including an AI Control Plane. The revised strategy makes Reasoning RAG the first flagship; revisit the remaining ideas after the flagship has validated the profile narrative.

### Repository release bar

Before pinning a repository, require:

- A specific user problem and scope statement.
- A working quickstart tested from a clean environment.
- Architecture diagram and key design decisions.
- Meaningful examples or demo data that can be redistributed.
- Automated quality checks and a documented support status.
- Security and limitations sections.
- A license appropriate to the code and data.
- No credentials, private datasets, or unsupported production claims.

### Naming and consistency

Use descriptive repository names and consistent README structure. Each README should answer: What problem? Who is it for? What is implemented? How do I run it? How is it evaluated? What are its limitations? What is next?

## 6. Reasoning RAG product definition

### Problem statement

Long documents often contain evidence spread across sections, tables, appendices, and references. Flat chunk retrieval can miss relationships or return fragments without useful structural context. `reasoning-rag` investigates whether a hierarchy-aware planner can locate, verify, and cite evidence effectively for defined document question-answering tasks.

### Non-goals for the first release

- Reproducing another project's code, APIs, prompts, interface, or product identity.
- Claiming to outperform vector RAG before a fair evaluation.
- Supporting every file format, language, model provider, or deployment target.
- Autonomous actions that change external systems.
- Processing confidential or regulated real-world documents in the public demo.

### User-visible workflow

```text
Document(s)
   ↓
Parse and normalize with source locations
   ↓
Build a hierarchical document tree and concise node metadata
   ↓
Question → query analysis → retrieval plan
   ↓
Navigate tree → gather candidate passages and source coordinates
   ↓
Verify evidence coverage and citation support
   ↓
Answer with citations, or abstain / request clarification
```

### Initial use case

**Corpus (locked for v1):** a small, in-repo sample of public, redistributable technical specifications in Markdown, plus synthetic fixtures for unanswerable and conflicting-evidence cases. Start with one well-structured public spec (IETF RFC or similarly licensed document) converted or stored as Markdown, with a dataset card recording license and source.

**Format (locked for v1):** Markdown only. PDF is a later adapter, not a v1 requirement.

**Language/runtime (locked for v1):** Python 3.12+, typed models, CLI-first. Recorded in [`docs/adr/0001-project-scope.md`](docs/adr/0001-project-scope.md).

Do not use private employer or customer documents.

### Core behavior

- Ingest documents and preserve page, section, table, and character or token offsets where available.
- Build a tree of document nodes with stable IDs, parent/child relationships, source ranges, and summaries.
- Analyze each question into intent, entities, constraints, expected evidence type, and complexity.
- Produce an inspectable retrieval plan: target nodes, subquestions, and stopping criteria.
- Navigate and expand candidate nodes under configurable depth and token/call budgets.
- Return evidence records with exact source references and provenance.
- Generate an answer only from the selected evidence; cite claims at sentence or paragraph level where feasible.
- Detect insufficient, conflicting, or unsupported evidence and abstain or ask a follow-up question.
- Emit a trace that explains the retrieval path without exposing hidden chain-of-thought. Log concise decisions, selected node IDs, evidence IDs, scores, and tool actions instead.

## 7. Reference architecture

Keep the initial implementation a modular monolith. Split services only when deployment, scaling, or ownership needs justify it.

### Logical components

1. **Ingestion adapter:** accepts supported document formats and validates size/type limits.
2. **Parser/normalizer:** extracts text, tables, headings, page coordinates, and warnings.
3. **Tree builder:** creates stable hierarchical nodes and summaries; records the model and prompt version used.
4. **Document store:** persists source metadata, tree structure, and content. Start with a local format such as JSON/SQLite behind a repository interface.
5. **Query analyzer:** extracts intent, entities, constraints, and answer shape into a typed schema.
6. **Retrieval planner:** creates a bounded plan from the tree structure and query; supports deterministic rules before adding complex agent loops.
7. **Tree navigator:** scores or selects nodes using transparent metadata, lexical signals, and model-assisted relevance as configured; keeps a deterministic baseline.
8. **Evidence assembler:** deduplicates passages, preserves source coordinates, and detects coverage gaps/conflicts.
9. **Verifier:** checks that answer claims are entailed by supplied evidence, citations resolve, and required subquestions are covered.
10. **Answer renderer:** returns a structured answer, citations, confidence/coverage indicators, and abstention reason.
11. **Evaluation harness:** runs versioned datasets and baselines, captures quality, cost, latency, and failure categories.
12. **API/CLI/demo:** begins as a CLI and small local demo; add a service API only after core behavior is stable.

### Data contracts

Define typed, versioned schemas early for:

- `Document`: ID, source name, checksum, media type, ingestion time, parser version, access classification.
- `Node`: ID, parent ID, title, summary, level, source range, child IDs, metadata.
- `QueryAnalysis`: normalized query, intent, entities, constraints, subquestions, expected answer type.
- `RetrievalPlan`: steps, candidate node IDs, budgets, strategy, planner version.
- `Evidence`: ID, document/node IDs, exact text, page/section/offset range, provenance, relevance rationale.
- `Answer`: text, claim-to-evidence links, limitations, abstention status, trace ID.
- `EvaluationCase`: question, corpus/document references, expected evidence, expected answer properties, tags.

Validate model-produced structured output at boundaries. Reject malformed IDs and out-of-range citations rather than silently repairing them.

### Retrieval modes

Name and expose retrieval modes clearly:

- **Tree-first:** hierarchy navigation and node metadata are primary.
- **Tree + lexical:** adds BM25/keyword matching for node or passage discovery.
- **Hybrid comparison:** optionally adds vector retrieval as a comparator or candidate source.

No mode should be called “vectorless” if vector similarity is in its primary path. Record the mode in run metadata and benchmark reports.

### Model and provider boundaries

Use a small interface for structured generation, summarization, and (optionally) verification. Record provider, model identifier, temperature/decoding settings, prompt/template version, and relevant parameters in experiment metadata. Provide a deterministic mock or fixture mode so core tests and demos can run without paid API access.

## 8. Phased implementation plan for Cursor

Use one phase prompt at a time. Cursor should first inspect the repository, summarize its understanding, and propose a small file-level plan. Review the plan, then ask it to implement only that phase. Keep changes in reviewable commits and update documentation alongside behavior.

Phase 0–9 is the **build path**. Milestones M0–M8 in Section 16 are the **public skills narrative**. Do not wait for Phase 9 to show skill proofs; publish M2/M3/M5 artifacts as soon as they exist.

### Phase 0 — Repository discovery and product brief

**Build:** inspect current repo, preserve useful work, write `README.md`, `docs/PRODUCT_BRIEF.md`, `docs/ROADMAP.md`, and initial `docs/adr/0001-project-scope.md`.

**Acceptance:** problem, audience, non-goals, first corpus, supported formats, and success measures are explicit. No application code is needed yet.

**Cursor prompt:** “Inspect this repository and report its current structure and conventions. Do not modify files. Based on the attached roadmap, propose the smallest implementation plan for Phase 0, including files to add or change and open questions.”

### Phase 1 — Skeleton, contracts, and local developer experience

**Build:** package layout, typed domain models, configuration validation, structured logging, CLI skeleton, lint/format/type-check workflow, CI, license, contribution guidance.

**Acceptance:** clean setup instructions work; CLI reports help/version; configuration errors are actionable; no secrets are needed to run the skeleton.

### Phase 2 — Ingestion and provenance

**Build:** Markdown parser adapter, normalized sections, stable source coordinates, parser warnings, checksum and size/type validation. Do not add PDF in this phase.

**Acceptance:** sample documents produce inspectable normalized output; citations can point back to section/offset; malformed or unsupported files fail safely.

### Phase 3 — Knowledge tree construction

**Build:** deterministic heading-based tree baseline, typed node schema, stable IDs, summaries behind a model interface, tree serialization and visualization.

**Acceptance:** tree can be inspected and round-tripped; every node maps to a source range; summary generation is optional and records model/prompt version; large inputs respect budgets.

### Phase 4 — Baseline retrieval and answer path

**Build:** simple tree traversal and lexical baseline, evidence assembly, cited answers, “not enough evidence” response.

**Acceptance:** end-to-end CLI handles a small set of known questions, returns resolvable citations, and abstains on unsupported questions. Save example traces with synthetic or public data.

### Phase 5 — Query analysis and retrieval planning

**Build:** typed query analysis, subquestion decomposition, evidence plans, bounded planner, plan display in CLI.

**Acceptance:** planner output validates against schema, stays within call/token/depth budgets, and falls back safely when model output is malformed or unavailable.

### Phase 6 — Navigation, multi-hop retrieval, and verification

**Build:** hierarchical navigation strategies, explicit multi-hop evidence collection, conflict/coverage checks, citation verification, answer claim mapping.

**Acceptance:** each answer claim links to evidence; unresolved claims are removed or trigger abstention; conflicting source statements are surfaced rather than merged invisibly.

### Phase 7 — Evaluation and fair baselines

**Build:** versioned evaluation set, tree-first and lexical baselines, optional vector baseline with equal source corpus and comparable model settings, metrics and report generation.

**Acceptance:** evaluation is reproducible from documented commands; every metric has a definition; failures can be inspected case by case; report includes cost and latency alongside quality.

### Phase 8 — Usable demo and API boundary

**Build:** local demo for uploading/choosing sample documents and asking questions; optionally expose a small API with validated request/response schemas.

**Acceptance:** user can see answer citations and retrieval trace summary; upload limits and errors are clear; no sensitive document content is sent to an external provider without clear configuration and notice.

### Phase 9 — Hardening and first public release

**Build:** threat-model review, dependency and secret scanning, performance profiling, release notes, container or reproducible environment if useful, demo video/screenshots, project status.

**Acceptance:** clean-clone quickstart succeeds; public corpus licensing is checked; known limitations and supported configurations are documented; release is tagged and linked from the profile.

### Cursor operating rules

- Provide Cursor this internal roadmap and a phase-specific task, not a request to build the entire roadmap at once.
- Ask it to inspect existing code before changing structure or dependencies.
- Require a short proposed plan and acceptance criteria before implementation for each substantial phase.
- Keep diffs small; ask for explanations of new dependencies and abstractions.
- Review generated code, prompts, citations, and security-sensitive paths yourself.
- After implementation, inspect the diff and run only the relevant checks you have chosen for that phase.
- If a phase changes product scope or a key trade-off, record an ADR before or alongside implementation.

## 9. Engineering standards

### Code and design

- Use a typed language and formatter/linter appropriate to the selected stack; document the choice in an ADR.
- Keep domain logic separate from provider SDKs, parsing libraries, UI, and persistence.
- Prefer explicit schemas, small modules, dependency injection at boundaries, and predictable error types.
- Use stable IDs and deterministic serialization where possible.
- Track configuration centrally; validate it at startup; make defaults safe and visible.
- Avoid hidden model calls inside ordinary utility functions.
- Support cancellation, timeouts, bounded retries, and per-request budgets for external calls.

### Reliability and observability

- Use structured logs with trace/run IDs and component names.
- Record retrieval mode, document checksum, model/provider identifiers, prompt version, and evaluation version in experiment traces.
- Do not log full document contents or secrets by default.
- Track latency, token/call use, retrieval depth, selected evidence count, citation validity, abstention rate, and error categories.
- Treat external model, parser, and storage failures as expected states with clear recovery behavior.

### Quality workflow

- Add focused unit tests for schemas, tree construction, citation resolution, budget enforcement, and abstention logic as those features are implemented.
- Add integration tests for representative ingest-to-answer flows using fixtures or mocks.
- Keep a small smoke evaluation in normal development and a larger benchmark run separate from fast checks.
- Use pull requests or topic branches for meaningful changes; write commit messages that describe the change.
- Require CI for formatting/linting, type checks, tests, dependency checks, and secret scanning where tooling is available.

## 10. Evaluation and benchmarking

Do not use one leaderboard number as proof of quality. Publish the data, protocol, system configuration, and failure analysis that make results interpretable.

### Dataset design

Create a small, human-reviewed starter set, then expand it. Include:

- Direct lookup questions.
- Questions requiring navigation across sections.
- Multi-hop questions that need evidence from multiple locations.
- Table and appendix questions if supported by the parser.
- Ambiguous questions that should prompt clarification.
- Unanswerable questions that should lead to abstention.
- Conflicting or versioned-source questions where the system must report disagreement.

For each case, store document/corpus version, expected evidence spans or sections, expected answer properties, answerability, difficulty, and tags. Avoid hardcoding a single wording as the only acceptable answer.

### Baselines

Compare at least:

1. Simple keyword/lexical retrieval over the same source text.
2. Tree-first retrieval with the same answer model and answer prompt.
3. Optional vector retrieval baseline with equivalent documents, context limits, model settings, and evaluation cases.
4. Ablations that remove one feature at a time, such as summaries, query decomposition, or verifier.

Report model/provider, prompt version, parser version, retrieval mode, top-k/context budget, token/call budget, and date for every run. If baselines use different models or budgets, state that clearly and avoid direct performance claims.

### Metrics

- **Retrieval:** evidence recall/precision, section hit rate, evidence coverage, retrieval depth, and context tokens.
- **Answer:** correctness/faithfulness judged against references and evidence, citation precision/recall, unsupported-claim rate, and abstention quality.
- **Operations:** latency (median and tail), model calls, input/output tokens, estimated cost, parser failures, and timeout/error rates.
- **Human review:** a documented rubric for citation usefulness, completeness, and clarity; report sample size and reviewer process.

Use deterministic checks for citation resolution and schema validity. Treat LLM-as-judge scores as a noisy signal; calibrate them against human-reviewed examples and publish the judge/model/prompt.

### Benchmark reporting

Publish a report containing:

- Commit/tag, dataset version, and command to reproduce.
- Hardware/runtime and model configuration.
- Metric definitions and aggregation rules.
- Overall metrics plus slices by question type and difficulty.
- Cost/latency/quality trade-offs.
- Failures with representative examples and root-cause categories.
- Limits, such as corpus size, language, document formats, and sample count.

Do not label a result “state of the art” or “better than vector RAG” unless the comparison is broad, controlled, independently repeatable, and appropriately qualified.

## 11. Documentation and ADRs

### Public vs internal

| Surface | File | Role |
| --- | --- | --- |
| Public | `README.md` | Status, problem, what works now, links |
| Public | `docs/PRODUCT_BRIEF.md` | Problem, audience, non-goals, success measures |
| Public | `docs/ROADMAP.md` | Skills-first milestones and current slice |
| Public | `docs/adr/*.md` | Reversible-cost decisions |
| Internal | `AI-ARCHITECT-GITHUB-ROADMAP.md` | Full execution plan, Cursor phases, portfolio sequence |

Keep this master file in the repository for implementation context. Do not link it from the profile README. Visitors should not need it to understand the project.

### Suggested layout

```text
README.md
LICENSE
CONTRIBUTING.md
SECURITY.md
CHANGELOG.md
docs/
  PRODUCT_BRIEF.md
  ROADMAP.md
  ARCHITECTURE.md
  DATA_MODEL.md
  EVALUATION.md
  SECURITY_AND_PRIVACY.md
  LIMITATIONS.md
  profile/
    GITHUB_PROFILE_README.md
  adr/
    0001-project-scope.md
    0002-ingestion-and-provenance.md
    0003-tree-storage.md
    0004-retrieval-baselines.md
    0005-model-provider-boundary.md
    0006-evaluation-protocol.md
AI-ARCHITECT-GITHUB-ROADMAP.md   # internal master plan
```

### ADR template

Each ADR should include:

- Title, status, date, and decision owners.
- Context and the concrete decision to make.
- Options considered, including “do nothing” where relevant.
- Decision and reasons.
- Consequences, trade-offs, and risks.
- Revisit triggers and references.

Write ADRs for choices that are costly to reverse or materially affect trust, cost, privacy, or system behavior—not every code-level choice.

### README content

1. Name, one-sentence promise, and status.
2. Screenshot or short demo and architecture diagram.
3. What is implemented now, separated from planned work.
4. Quickstart and sample question.
5. How retrieval works and which mode is active.
6. Evaluation summary with links to methodology and raw outputs.
7. Security/privacy notes, limitations, and roadmap.
8. Contribution, license, and citation/attribution notes.

## 12. Security, privacy, and responsible use

### Threats to address

- Prompt injection embedded in source documents.
- Malicious or oversized files, parser exploits, decompression bombs, and malformed PDFs.
- Cross-document or cross-user leakage if a hosted version is added.
- Secrets or document content in logs, traces, crash reports, or benchmark artifacts.
- Model-generated fabricated citations or incorrect source coordinates.
- Dependency supply-chain risk and vulnerable parsers.
- Unbounded model calls, recursive planning, or denial-of-service through large inputs.
- Licensing and redistribution restrictions on documents and derived summaries.

### Baseline controls

- Treat retrieved content as data, never as trusted instructions. Separate system policy from document text and test prompt injection cases.
- Enforce upload size, page count, type, time, and recursion limits; isolate risky parsing where practical.
- Validate every citation against stored source ranges and reject unresolved citations.
- Require explicit configuration and notice before sending documents to external model providers.
- Keep credentials in environment or secret managers; include `.env.example`, never real keys.
- Redact document text and sensitive values from logs by default; define retention and deletion behavior.
- Pin and scan dependencies; review licenses; publish a security contact/process.
- Apply least privilege and tenant/document authorization before any multi-user deployment.
- Use only synthetic or redistributable public documents in examples and evaluation fixtures.
- Make limitations clear; the tool supports research and information retrieval, not professional advice or high-impact automated decisions.

## 13. Publication and GitHub contribution strategy

### Public development sequence

1. Create the repository with a truthful README status and product brief.
2. Publish architecture and initial ADRs before the codebase becomes hard to explain.
3. Build in visible vertical slices with issues or milestones.
4. Keep commits focused and write release notes that explain user-visible changes.
5. Share progress when there is evidence: a tree visualization, a reproducible retrieval trace, an evaluation result, or a documented design trade-off.
6. Tag a release only after the release bar in Section 5 is met.

### What to publish

- Architecture decisions and diagrams.
- Small sanitized traces that show retrieval and citations.
- Evaluation methodology, dataset cards, and failure analysis.
- Demonstrations with public or synthetic documents.
- Lessons learned when an approach failed, with measurable evidence.

### What not to publish

- Employer/customer documents, credentials, internal prompts, or proprietary code.
- Inflated claims, fabricated benchmark numbers, or unverified AI-generated results.
- Large numbers of low-value commits created only to make a contribution graph look active.
- Unlicensed datasets or copied PageIndex materials.

Consistency matters more than daily activity. A sustainable rhythm is one well-documented engineering update per week or two, adjusted to available time. Keep a short project log in GitHub issues/discussions or `CHANGELOG.md`, and close outdated tasks rather than leaving a misleading roadmap.

## 14. LinkedIn integration

### Profile alignment

- Match the name, headline, and focus areas used on GitHub, including the Section 2 evidence gate.
- Add `ratheshworld.com` and the flagship repository when there is a useful public landing page.
- Describe Reasoning RAG as an independent project inspired by research and public concepts; do not say it is PageIndex or affiliated with PageIndex.
- State its maturity accurately: prototype, research project, or release.

### Content sequence

Create posts around milestones, not generic AI announcements:

1. **Project thesis:** why hierarchy-aware, evidence-grounded retrieval is worth exploring.
2. **Architecture:** show the tree, planner, evidence, and verification boundaries.
3. **Engineering choice:** explain one ADR and trade-offs.
4. **Evaluation:** publish a small result with method, costs, and failure cases.
5. **Demo:** show a question, navigation trace, citations, and an abstention example.
6. **Retrospective:** explain what changed after evaluation and what remains limited.

Each post should link to a relevant artifact, invite technical discussion, and avoid claims beyond the evidence. Reuse a chart only when the underlying protocol and data are linked.

## 15. Website integration (`ratheshworld.com`)

Create a focused **AI Architecture** or **Projects** page that acts as the portfolio front door. It should include:

- A short professional introduction and the same positioning statement.
- Featured projects with status, role, architecture, and links to source code.
- A Reasoning RAG case study: problem, design, trade-offs, demo, evaluation, limitations, and next steps.
- Architecture diagrams with accessible text descriptions.
- A publications/notes section that can link to LinkedIn or longer technical articles.
- Contact and LinkedIn links.

Keep the website factual and maintainable. Link to the canonical GitHub README and benchmark report instead of duplicating details that will drift. Add no customer logos, confidential examples, or claims of deployment without permission and evidence.

## 16. Milestones and sequencing

Use milestone outcomes rather than hard deadlines; adjust dates to Rathesh's availability. This table is the public skills narrative. For website and profile copy, prefer short outcome bullets with links, not this table.

| Milestone | Outcome | Evidence | Skill signal |
| --- | --- | --- | --- |
| M0 — Identity ready | GitHub profile repository and consistent `ratheshr8` positioning | Profile README reviewed and links verified | Communication |
| M1 — Scope approved | Problem, corpus, non-goals, and success criteria fixed | Product brief and scope ADR | Spec / design |
| M2 — Inspectable documents | Markdown produces a normalized source-aware tree | Sample outputs and tree visualization | AI system design |
| M3 — Grounded baseline | End-to-end answer with resolvable citations and abstention | Demo traces and focused cases | Retrieval + trust |
| M4 — Planned retrieval | Query analysis and bounded tree navigation work | Inspectable plans and budget behavior | Agentic / planning |
| M5 — Measured system | Baselines and evaluation harness produce reproducible reports | Versioned dataset and benchmark report | Evaluation |
| M6 — Public beta | Demo, security notes, limitations, and release process are ready | Clean-clone quickstart and tagged release | Security + ops |
| M7 — Portfolio integrated | GitHub, LinkedIn, and website tell the same story | Links, case study, and evidence aligned | Communication |
| M8 — Next portfolio work | One complementary repository has a useful released slice | Maintained project that meets the pin policy | Second skill cluster |

```text
M0 Identity → M1 Scope → M2 Tree → M3 Cited baseline
    → M5 Eval report → M6 Tagged release → M7 Aligned surfaces
```

M4 (planned retrieval) sits between M3 and M5 in the build path. Public showcase can skip advertising M4 until traces exist.

### Suggested first 30 days

- **Week 1:** profile positioning on `ratheshr8`, flagship repository, scope brief, first ADR.
- **Week 2:** lock corpus files into the repo; define data contracts and tree visualization; set up CI and local quickstart.
- **Week 3:** implement parsing, provenance, and deterministic hierarchy baseline (M2 proof).
- **Week 4:** deliver the first cited retrieval path and abstention example (M3 proof); draft initial evaluation cases.

The schedule is a planning aid, not a promise. Reduce scope rather than weakening evaluation or safety requirements.

## 17. Definition of done

### Flagship v1 is done when

- A clean checkout can be installed and run using documented steps.
- The supported document format(s) are explicit and work on the public sample corpus.
- Every retrieved evidence item resolves to its source location.
- The system can answer supported questions and abstain on unsupported ones.
- Retrieval mode and model configuration are explicit and recorded.
- A versioned evaluation set and at least one fair baseline can be run reproducibly.
- Quality, citation, latency, and cost results are reported with method and limitations.
- Security, privacy, licensing, and threat assumptions are documented.
- The README distinguishes implemented features from future work.
- CI and release checks pass; no secrets or private data are committed.
- A tagged release, concise demo, and portfolio links are published.

### AI Architect profile is ready when

- GitHub identity (`ratheshr8`), LinkedIn, and website share a consistent, accurate narrative.
- The profile README features evidence-backed projects, not a wish list.
- The flagship repository is pinned and understandable without a personal explanation.
- At least one supporting project demonstrates a different architecture competency, is maintained, and was started only after flagship M5.
- Public claims can be traced to code, ADRs, evaluation, or a clearly labeled design proposal.
- Healthcare and FinTech wording appears only if the Section 2 evidence gate is met.

## 18. Practical checklist

### Before implementation

- Confirm GitHub handle `ratheshr8`, repository access, and the current profile README draft.
- Verify the special public repository `ratheshr8/ratheshr8` (exists; README still reflects an old Flutter bio and must be replaced with the draft in `docs/profile/GITHUB_PROFILE_README.md` after review).
- Create `ratheshr8/reasoning-rag` with license and a truthful prototype status when GitHub credentials are available. This local workspace is not yet a git remote.
- Select one legal, public corpus and one initial document format (Markdown + public spec samples; see ADR 0001).
- Write the product brief, non-goals, success measures, and scope ADR.
- Decide the initial language/runtime and record the rationale (Python 3.12+ in ADR 0001).

### During each Cursor phase

- Ask Cursor to inspect before editing and provide a focused plan.
- Review files and dependencies it proposes to change.
- Check that implementation matches acceptance criteria and does not expand scope silently.
- Review prompts, schemas, citations, logs, and failure handling.
- Update README/docs/ADR when behavior or trade-offs change.
- Run the phase's chosen checks and record results honestly.
- Commit a coherent slice and note follow-up work.

### Before public release

- Verify quickstart from a clean environment.
- Reproduce benchmark commands and inspect raw failures.
- Confirm all sample documents and derived artifacts can be redistributed.
- Scan for secrets and sensitive data; check dependency and license status.
- Review prompt-injection, malformed input, upload limits, and citation validation.
- Check every README/profile/website/LinkedIn statement for accuracy.
- Add demo, release notes, limitations, security reporting route, and support status.
- Pin the repository only if the Section 5 pin policy is met, then publish a focused technical explanation.

## 19. Working master prompt for Cursor

Use this prompt as the standing project context, then append one phase-specific task:

> You are helping implement `reasoning-rag`, an independently designed, reasoning-first document retrieval project. It explores hierarchical document trees, bounded query planning, evidence-grounded answers, citations, and abstention. It may be informed by public concepts including PageIndex, but it must not copy another project's code, branding, prompts, or documentation or imply affiliation. Treat the internal file `AI-ARCHITECT-GITHUB-ROADMAP.md` and the repository's current ADRs as project context. Prefer public docs (`README.md`, `docs/PRODUCT_BRIEF.md`, `docs/ROADMAP.md`) for visitor-facing text. Before substantial changes, inspect the existing code and conventions, summarize your understanding, propose a small plan, and identify risks. Implement only the requested phase. Preserve provenance, validate model output, bound file/model work, treat document text as untrusted, and never commit secrets or private data. Keep documentation and acceptance criteria current. At the end, summarize files changed, design choices, checks run, results, limitations, and remaining work. Do not claim tests or benchmarks passed unless you actually ran them.

## 20. Immediate next actions

1. ~~Publish profile README to `ratheshr8/ratheshr8`~~ — done (replaces the stale Flutter bio; draft remains in [`docs/profile/GITHUB_PROFILE_README.md`](docs/profile/GITHUB_PROFILE_README.md)).
2. **Manual (GitHub UI):** pin `ratheshr8/reasoning-rag` on the profile (API cannot set pins).
3. Align LinkedIn/website copy with shipped `v0.1.0` artifacts only (demo, eval, threat model).
4. Do not pin empty complementary repositories; M8 requires its own release bar.

---

**Maintenance note:** Update this roadmap when scope, evaluation protocol, repository sequence, or release status changes. Keep completed work evidence-linked and remove stale dates or claims.
