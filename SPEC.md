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

The default show kit targets 1200×630 and contains fighter assets, a
side-by-side comparison, and a result card. Phase 1 ships offline HTML templates
and fixture cards only; PNG rendering is deliberately deferred. Public cards
may show the task, rubric totals, decision, and concise tool/process summaries,
but not private traces.

## Current boundary

This repository does not claim a published Grok template, deployed service,
leaderboard, X automation, OpenClaw/Hermes adapter, or PNG pipeline. Live
referee messaging and publish approval remain outside Phase 0/1.
