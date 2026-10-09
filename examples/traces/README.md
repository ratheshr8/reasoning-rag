# Example traces

This directory holds sanitized AskResult JSON from the Phase 4 baseline.

Regenerate (after install):

```bash
reasoning-rag ask data/corpus/v0/acme-widget-spec.md \
  -q "What supply voltage does the Acme Widget require?" \
  --synthetic \
  -o examples/traces/case-power-voltage.json

reasoning-rag ask data/corpus/v0/acme-widget-spec.md \
  -q "How do I perform firmware updates on the Acme Widget?" \
  --synthetic \
  -o examples/traces/case-firmware-absent.json
```

Traces include retrieval mode, evidence with source ranges, answer/abstention, and event steps — not hidden chain-of-thought.
