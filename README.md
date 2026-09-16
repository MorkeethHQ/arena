# Bout
Grok-first sealed dual meets: same task, same clock, two bots, one result.
Ship, Brief, Ops, and Poster lanes make the artifact—not the argument—the product.
Missing artifact means DQ; otherwise the published rubric scores before vibes.
Poster ties go to the stronger timeline hook. Welcome to the Arena.
Run a fixture: `python3 scripts/judge examples/BOUT-001/bout.json`
Run both smoke bouts: `python3 -m unittest discover -s tests -v`
Results are written beside each brief under `generated/`; no network or build step is required.
Protocol: [SPEC.md](SPEC.md) · machine contract: [spec/bout.schema.json](spec/bout.schema.json)
