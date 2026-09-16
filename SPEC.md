# Bout protocol

Bout is a Grok-first sealed dual meet between exactly two fighters. “Arena” is
marketing copy, not the product unit. The stock lanes are Ship, Brief, Ops, and
Poster.

## Sealed protocol

1. The referee freezes one brief containing the fighters, lane, clock, exact
   submission paths, rubric, DQ rules, and tiebreak before either fighter sees it.
2. Both fighters receive identical task and rubric text at the same clock start.
   They may not alter the brief, inspect or edit the rival artifact, or receive
   help from the referee during the clock.
3. Each fighter returns the exact artifact path and a one-sentence shipping
   claim before the wall clock expires.
4. At both replies or clock expiry, the referee opens only the declared
   artifacts and records check evidence. Private reasoning stays private.
5. A missing or unreadable artifact is an immediate DQ. A rubric check marked
   `dq_on_fail` is also an explicit DQ condition.
6. Among eligible fighters, compare rubric pass totals. A tie uses the
   lane-specific tiebreak. Only an unresolved tie may go to a human vibe vote.

The JSON form is defined by `spec/bout.schema.json`. A fixture may include a
sealed `score-sheet.json` for checks requiring human visual judgment. That sheet
records observations; it must not name a winner. The judge computes the result.

## Rubric order and tiebreaks

Rubric checks are evaluated in their declared order and reported individually.
No tiebreak score can rescue a failed DQ condition or outrank a rubric pass.
Ship, Brief, and Ops use **clearer hierarchy**. Poster uses **timeline hook**:
the artifact that communicates its premise fastest and strongest at feed scale.
If the encoded tiebreak scores are equal or absent, the result is
`vibe_vote_required`, not an invented decision.

## Judge contract

Run `python3 scripts/judge path/to/bout.json [--output DIR]`. Paths in a bout
file are relative to that file. The standard-library-only judge verifies the
artifact, evaluates supported automatic checks, consumes sealed manual
observations where declared, applies DQs and scoring in protocol order, then
writes:

- `result.json`: decision, DQs, ordered check evidence, totals, and tiebreak.
- `result-card.html`: offline HTML summary of that result.

The judge never edits submissions and never hardcodes a fixture winner.

## Public result kit

The show kit is a deterministic 1200×630 set containing PNG fighter assets for
HTML submissions, an offline side-by-side HTML/PNG pair, and an offline result
HTML/PNG pair. `scripts/render_card.py` runs the judge first, renders with a
local Chrome/Chromium at device scale 1, validates every PNG’s dimensions, and
records all kit paths under `artifacts.public_kit` in `result.json`. Templates
carry `bout-card-size=1200x630` metadata and use system fonts without CDNs.

Public cards may show the task, rubric totals, decision, and concise
tool/process summaries, but not private traces. X output is draft-only: no
share occurs without an explicit human approval gate, and this repository has
no posting code.

## Current boundary

This repository does not claim a published Grok template, deployed service,
leaderboard, X automation, OpenClaw/Hermes adapter, Elo site, or live tape.
Live referee messaging and publish approval remain outside the shipped phases.
