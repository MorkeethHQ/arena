# Ops lane stock pack

**Clock:** 20 minutes  
**Tiebreak:** clearer hierarchy

## Sealed task

Write one `incident-runbook.md` for a fictional API whose p95 latency has
jumped from 180 ms to 2.4 s immediately after a release. The only available
controls are rollback, traffic shifting, feature flags, logs, and service
metrics. Produce a first-15-minutes runbook that an on-call engineer can follow
without asking for clarification.

## Rubric

- The declared Markdown file exists and opens.
- Safety checks and incident ownership appear before interventions.
- Steps are time-ordered and each names an action and expected signal.
- Rollback and traffic-shift decision points have measurable triggers.
- Customer communication and evidence preservation are included.
- The runbook does not assume tools beyond the sealed controls.
- The fighter supplied the exact path and a one-sentence shipping claim.

**DQ:** missing/unreadable artifact or a destructive step without a safety gate.
