# ARENA
**ARENA runs sealed head-to-head bouts between two bots on the same task and the same clock, and the artifact they ship decides the result, not the argument.**

Comparing agents by vibes is unfair: briefs drift, one side sees the other's work, and a missing deliverable gets talked around.
For anyone who wants to compare two coding agents or models on a real task and defend the result.
A referee freezes the brief, rubric, DQ rules and tiebreak before either fighter sees it; both get identical text at the same start; the judge opens only the declared artifacts, DQs a missing one and scores the published rubric in order, across Ship, Brief, Ops and Poster lanes.
Grok-first, offline, no network or build step: `python3 scripts/judge examples/BOUT-001/bout.json`.

A **bout** is one sealed meet. **ARENA** is the product.

Run a fixture: `python3 scripts/judge examples/BOUT-001/bout.json`
Run both smoke bouts: `python3 -m unittest discover -s tests -v`
Results are written beside each brief under `generated/`; no network or build step is required.
Protocol: [SPEC.md](SPEC.md) · machine contract: [spec/bout.schema.json](spec/bout.schema.json)

## Produce the public kit

Run `make card BOUT=examples/BOUT-002/bout.json`. The command judges the bout,
screenshots each HTML fighter artifact when applicable, and writes fixed
1200×630 side-by-side and result HTML/PNG cards under the example’s `cards/`
directory. Set `BOUT_CHROME` if Chrome/Chromium is not on `PATH`; use
`python3 scripts/render_card.py examples/BOUT-002/bout.json --dry-run` to
validate the plan without a browser. X sharing is always draft-only and requires
explicit human approval. This repository never posts automatically.
