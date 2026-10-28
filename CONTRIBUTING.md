# Contributing

Thank you for contributing. Keep changes small, sourced, and checkable.

## Running tests

```bash
python -m pytest tests/ -q
```

All tests must pass before submitting.

## Proposing a Markdown change

1. Open an issue first for anything bigger than a typo, or comment on
   an existing issue asking to be picked up.
2. Fork, branch `docs/issue-<number>-<slug>` for docs or
   `fix/issue-<number>-<slug>` for a fix, and make the smallest change
   that does the job.
3. For a new template or checklist item, follow the format of the
   existing templates in the repo and keep the standard sections intact
   — if a section does not apply, write why, rather than deleting it.
4. Cite a source for every new number, with its period, on the same page.
   Unsourced numbers will not be merged, however plausible they look.

## Proposing a code change

Every new function needs a docstring stating its definition and its
edge-case behaviour, and at least one edge-case test. Run the suite
above before submitting.

## House rules (all contributions)

- Research and education only: never investment advice, never a buy/sell/
  hold recommendation, never guaranteed returns.
- Every number sourced with its period, or labelled UNKNOWN / TO VERIFY.
- No fake metrics, no invented features, no live NEPSE feed claim.
- No credentials anywhere. No paywalled scraping.
