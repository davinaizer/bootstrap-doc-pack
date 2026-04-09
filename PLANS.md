# Plan

## Goal

Keep the bootstrap generator aligned with the Documentation Pack contract and the scaffolded repository structure.

## Scope

- Keep the guide generator profile-aware and repo-agnostic.
- Keep scaffold output aligned with the documented governance and docs entrypoints.
- Keep PRD and TAD mandatory, with optional profile metadata.
- Keep the script usable for full stack, mobile, web app, web game, and iOS game repos.

## Files to Modify

- `PLANS.md`
- `scripts/bootstrap_project_guide.py`
- `docs/project_bootstrap_guide.md`
- `docs/documentation_pack_example.md`
- `README.md`
- `AGENTS.md`
- `docs/README.md`
- `docs/governance/*`

## Steps

1. Keep the Documentation Pack profile keys aligned with generator parsing.
2. Generate the bootstrap guide from the example pack.
3. Validate the generator against the example pack.
4. Expand scaffold output only if a target repository requires additional baseline files.

## Validation

- Run `python3 scripts/bootstrap_project_guide.py --pack docs/documentation_pack_example.md --output docs/project_bootstrap_guide.md --check`.

## Risks

- Overfitting the profile catalog to one stack family would reduce reuse.
- Generating too many repository-specific files in the scaffold would make the tool harder to maintain.

## Rollback

- Restore the files listed in `Files to Modify`.
