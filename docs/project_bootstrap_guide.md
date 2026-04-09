---
createdAt: "2026-04-09T10:43:04-0300"
lastModifiedAt: "2026-04-09T12:11:00-0300"
---

# Repository Bootstrap Guide

## Purpose

Use this guide to start a new repository from a Documentation Pack without inventing scope, rules, or work order.

## Pack Contract

- Pack title: Documentation Pack
- Mandatory inputs: PRD, TAD
- Optional but recommended: Project Profile
- Recommended taxonomy: PRD, TAD, API Contract and Data Model, UX/UI Specification, Implementation Backlog, QA and Acceptance Test Plan, Build and Deployment Runbook, Governance, Handoff

## Detected Profile

- Project kind: Full stack
- Profile summary: Use when the repo includes backend plus at least one client surface.
- Project Kind: full-stack
- Primary Platforms: web app, iOS app
- Primary Stack: backend + client apps
- Architecture Style: service + client
- Repo Model: monorepo

## Documentation Order

| Order | Document |
| --- | --- |
| 1 | Product Requirements Document (PRD) |
| 2 | Technical Architecture Document (TAD) |
| 3 | API Contract and Data Model |
| 4 | UX/UI Specification |
| 5 | Implementation Backlog |
| 6 | QA and Acceptance Test Plan |
| 7 | Build and Deployment Runbook |
| 8 | Governance |
| 9 | Handoff |

## Suggested Deliverables

- API contract and boundary document
- Data model and storage rules
- Client app guidance for each surfaced client
- Deployment and environment runbook
- Cross-platform validation checklist

## Suggested Repo Structure

| Path | Purpose |
| --- | --- |
| docs/ | product, architecture, governance, and runbooks |
| services/api/ | backend service or API |
| apps/web/ | web client |
| apps/mobile/ | mobile client, if applicable |
| packages/shared/ | contracts, utilities, and shared models |
| infra/ | deployment, environment, and delivery assets |
| tests/ | contract, integration, and end-to-end tests |

## Bootstrap Sequence

1. Validate the Documentation Pack before writing anything.
2. Lock product intent in PRD.
3. Lock system boundaries in TAD.
4. Add the remaining source-of-truth documents in pack order.
5. Add governance rules before implementation starts.
6. Define any team or agent routing if the project uses delegation.
7. Build backlog, QA, and handoff artifacts from the authoritative docs.
8. Start implementation only after the guide, governance, and validation rules exist.

## Suggested Workflow

1. Define the API and data boundaries before client implementation.
2. Separate shared contracts from client-specific views.
3. Treat deployment, auth, and data ownership as first-class governance topics.
4. Validate backend, client, and integration paths independently.

## Governance Baseline

- Keep a single source of truth per decision.
- Put scope rules in PRD or the project rules doc, not in task chatter.
- Put architecture boundaries in TAD or architecture governance, not in implementation notes.
- Put content, data, or domain rules in the relevant source-of-truth doc or governance file.
- Put workflow, planning, and validation rules in governance docs before coding.
- Record exceptions explicitly, with a removal plan and expiry if applicable.

## Work Organization

- Use one entry point for ambiguous requests.
- Route each request to exactly one owner or workstream.
- Keep planning in architecture and implementation in the owning workstream.
- Keep validation in a dedicated validation phase or quality gate.
- Keep handoff artifacts short, explicit, and generated from the current state.

## Validation Gate

- Do not begin implementation if PRD or TAD is missing.
- Do not bypass governance, architecture, or domain rules silently.
- Validate the first implementation slice before expanding scope.
- Update the active task or handoff artifact whenever work changes hands.

## Script Usage

```bash
python3 scripts/bootstrap_project_guide.py --pack path/to/documentation-pack.md --output docs/project_bootstrap_guide.md
python3 scripts/bootstrap_project_guide.py --pack path/to/documentation-pack.md --output docs/project_bootstrap_guide.md --check
```