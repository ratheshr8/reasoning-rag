# Product brief — reasoning-rag

**Status:** prototype (Phase 5 — query analysis / planning)  
**Owner:** Rathesh R (`ratheshr8`)  
**Audience:** hiring managers, AI engineers, and peers evaluating architecture judgment

## Problem

Long documents bury answers across sections, tables, appendices, and references. Flat chunk retrieval often returns fragments without structural context and makes weak or missing evidence hard to see. This project asks whether a hierarchy-aware planner can locate, verify, and cite evidence for a defined document QA task.

## Who it is for

People who need inspectable answers from structured technical documents: section-level lookups, multi-section questions, and explicit abstention when the document does not support an answer.

It is not a hosted enterprise product and not a substitute for professional, legal, or clinical advice.

## What v1 will do

- Ingest **Markdown** documents and preserve section/offset provenance
- Build a hierarchical node tree with stable IDs and summaries
- Answer from selected evidence with resolvable citations, or abstain
- Record retrieval mode, model identity, and prompt version on every run
- Compare tree-first retrieval against a lexical baseline on a versioned eval set

## Non-goals (v1)

- Copying another project's code, APIs, prompts, UI, or branding
- Claiming to beat vector RAG before a fair, documented comparison
- PDF, multilingual corpora, every model provider, or cloud multi-tenancy
- Autonomous actions against external systems
- Confidential, employer, customer, or regulated real-world documents in the public demo

## First corpus and format

| Choice | Decision |
| --- | --- |
| Format | Markdown only |
| Corpus | `data/corpus/v0/acme-widget-spec.md` (synthetic technical spec) with unanswerable and conflicting-evidence content |
| License bar | CC0-1.0; see [`data/corpus/v0/DATASET_CARD.md`](../data/corpus/v0/DATASET_CARD.md) |
| Out of scope | Private employer/customer files; unlabeled Healthcare/FinTech production claims |

## Success measures

v1 is successful when a clean checkout can ingest the sample corpus, return answers whose citations resolve to source ranges, abstain on unsupported questions, and reproduce an evaluation report that includes quality, citation validity, latency, and cost, with method and limitations stated.

## Constraints

- Independent design; PageIndex is prior art, not a template
- Document text is untrusted input (prompt-injection risk)
- Provider-neutral model interface; fixture/mock mode for tests without paid APIs
- Modular monolith until deployment needs justify a split
