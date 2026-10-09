# Evaluation protocol

**Dataset:** [`data/eval/v0/dataset.json`](../data/eval/v0/dataset.json) (`eval-v0`)  
**Corpus:** [`data/corpus/v0/`](../data/corpus/v0/) (`v0`, synthetic / CC0-1.0)

## Reproduce

```bash
pip install -e ".[dev]"
reasoning-rag eval \
  --dataset data/eval/v0/dataset.json \
  --modes tree-first,tree-lexical \
  --output reports/eval-v0
```

Reports write:

- `report.json` — machine-readable metrics, per-case results, config
- `report.md` — human-readable summary and failures
- `cases/<mode>/<case_id>.json` — full `AskResult` for inspection

## Fair comparison rules

- Same dataset version, document path, and case IDs for every mode
- Same `Settings` budgets (top-k, plan, navigation) unless a report field says otherwise
- Same answer composer and fixture model provider (`fixture` / `fixture-v0`)
- Record commit/tag, dataset version, modes, and command in the report
- Do **not** claim “better than vector RAG” unless a vector baseline ran under these rules

## Metric definitions

| Metric | Definition |
| --- | --- |
| `abstention_accuracy` | Fraction of cases where `answer.abstained == expect_abstain` (from `answerable` / `expected_answer_properties.expect_abstain`) |
| `answerable_success_rate` | Among answerable cases, fraction that did not abstain and satisfied `must_contain_any` when provided |
| `section_hit_rate` | Among cases with `expected_evidence_sections`, fraction where at least one expected section title appears in retrieved evidence `section_path`/text |
| `citation_resolution_rate` | Across cases, fraction of assembled evidence items with resolvable source ranges (after verification kept set) |
| `conflict_detection_rate` | Among cases with `expect_conflict=true`, fraction where `verification.conflicts` is non-empty |
| `unsupported_claim_rate` | Fraction of non-abstaining answers that have zero claim links (should be ~0 after Phase 6) |
| `latency_ms_median` / `latency_ms_p95` | Wall-clock ask latency per case |
| `estimated_cost_usd` | Always `0.0` for fixture provider; non-zero only when a paid model is configured and metered |

## Vector baseline

`hybrid-comparison` / vector mode is listed in reports as **not implemented** for `eval-v0` when requested. The harness records the intended equal-corpus protocol but does not invent scores.

## Failure analysis

Inspect `report.md` failure tables and per-case JSON under `cases/`. Root-cause tags include `false_abstain`, `missed_abstain`, `missing_section`, `missing_answer_span`, `missed_conflict`, `unsupported_claims`.
