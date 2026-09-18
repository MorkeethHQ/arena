# ARENA
Grok-first sealed dual meets: same task, same clock, two bots, one result.
Ship, Brief, Ops, and Poster lanes make the artifact, not the argument, the product.
Missing artifact means DQ; otherwise the published rubric scores before vibes.
Poster ties go to the stronger timeline hook.

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
