# Architecture Guardrails

## Purpose

Define module boundaries and the constraints that keep the scaffold maintainable.

## Baseline Rules

- Keep documentation, generator logic, and generated scaffold concerns separate.
- Keep shared contracts in a dedicated location.
- Do not introduce cross-layer imports without updating the architecture docs first.
