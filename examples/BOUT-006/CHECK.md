# BOUT-006 · Config Clash check

## Round 1
- Corners: Agentic Strava vs Strava Live Review (Iron/Ink rejected: rename theater)
- Pre-kickoff hashes required; gate: `python3 scripts/config_clash_gate.py examples/BOUT-006/pre-kickoff-seal.json`
- Judge: `python3 scripts/judge examples/BOUT-006/bout.json`
- Card: `python3 scripts/render_card.py examples/BOUT-006/bout.json`

## Day-two rematch
- Exactly one losing config item: `skills [] → [post-agentic-strava-run]`
- Tree: `examples/BOUT-006/rematch-day2/`
