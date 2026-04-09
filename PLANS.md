# Plan

## Goal

Upgrade the bootstrap script to infer project profile, repo structure, and workflow suggestions from a Documentation Pack, while staying language- and architecture-agnostic.

## Scope

- Add project profile parsing to the Documentation Pack contract.
- Generate profile-specific bootstrap guidance for common project kinds.
- Keep PRD and TAD mandatory, with optional profile metadata.
- Keep the script usable for full stack, mobile, web app, web game, and iOS game repos.

## Files to Modify

- `PLANS.md`
- `scripts/bootstrap_project_guide.py`
- `docs/project_bootstrap_guide.md`
- `docs/documentation_pack_example.md`

## Steps

1. Extend the pack contract with a project profile section.
2. Add profile classification and repo-structure suggestions to the generator.
3. Regenerate the guide from the example pack.
4. Validate the generator against the example pack.

## Validation

- Run `python3 scripts/bootstrap_project_guide.py --pack docs/documentation_pack_example.md --output docs/project_bootstrap_guide.md --check`.

## Risks

- Overfitting the profile catalog to one stack family would reduce reuse.

## Rollback

- Restore the files listed in `Files to Modify`.
