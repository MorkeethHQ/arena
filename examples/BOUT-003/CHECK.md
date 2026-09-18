# Sealed check | BOUT-003 | written before any fighter starts

Machine clock at seal: see git commit timestamp on this file.
Fighters must not read rival submissions.
Winner is this check, not a vote.

## Task (identical for both)

Build one single-file offline HTML page that visualizes the measured Grok Bot
turn-order burst for brief-v2-export-a (tool counts per typed turn):
1, 2, 5, 13, 0, 7.

The page must:
- show those six numbers as a bar or ridge chart
- label the basis as turn-order
- say ARENA and BOUT-003
- use only inline CSS and system fonts
- work with no network and no build step
- remain readable at 390px width

## Automatic checks (dq_on_fail where marked)

1. file_opens (DQ)
2. contains_all terms: ARENA, BOUT-003, turn-order, and the digits 1 2 5 13 0 7 in that sequence somewhere as the burst (DQ if missing ARENA/BOUT-003/turn-order)
3. no_external_assets (DQ)
4. claim_present (fighter claim non-empty)

Manual (score-sheet later if needed): clearer hierarchy at 390px.

## Kill note

If both DQ, double_dq. If tie on auto checks, clearer_hierarchy score-sheet.
