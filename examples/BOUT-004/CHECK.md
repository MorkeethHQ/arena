# Sealed check | BOUT-004 | written before any fighter starts

Machine clock at seal: see git commit timestamp on this file.
Fighters: Cursor and Grok. Do not open the rival submission path.
Winner is this check, not a vote.

## Task (identical for both)

Build one single-file offline HTML page that a stranger can open on a phone
with no network: an ARENA sealed-meet briefing card for BOUT-004
(fighters Cursor and Grok, lane Ship, tiebreak clearer_hierarchy).

The page must:
- say ARENA and BOUT-004
- list these six sealed-protocol steps in this order:
  1. freeze brief
  2. identical start
  3. artifact path plus one-sentence claim
  4. referee opens declared artifacts only
  5. missing or unreadable artifact is DQ
  6. pass totals then lane tiebreak
- state that the winner is the check, not a vote
- name the fighters Cursor and Grok
- use only inline CSS and system fonts
- work with no network and no build step
- remain readable at 390px width

Do not chart the BOUT-003 turn-order burst 1 2 5 13 0 7.

Return: absolute path to your HTML file, and one sentence claim.
Clock: 20 minutes.

## Auto checks (scripts/judge)

- html_opens (DQ)
- arena_mark: ARENA, BOUT-004 (DQ)
- protocol_steps: freeze brief, identical start, artifact path, declared artifacts, DQ, tiebreak
- fighters_named: Cursor, Grok
- check_not_vote: contains "check" and "vote" (winner is the check, not a vote)
- offline_assets (DQ)
- claim_present
- mobile_readable (manual, score-sheet)

## Tiebreak

If both pass totals match: clearer_hierarchy on score-sheet (0-2 each). Must not name a winner in the sheet.
