# Protocol files

- [`bout.schema.json`](bout.schema.json) defines a sealed brief and its result slot.
- [`score-sheet.schema.json`](score-sheet.schema.json) defines human observations
  for checks that cannot be established safely by an offline static judge.
- [`../SPEC.md`](../SPEC.md) is the normative protocol.

JSON Schema is the interchange contract. The Python judge performs a focused
runtime validation of the fields it consumes without downloading a validator.
