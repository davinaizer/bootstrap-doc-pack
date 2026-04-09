# bootstrap-doc-pack

Bootstrap a new repository from a mandatory Documentation Pack.

Generate a repo-ready bootstrap guide from a small, structured documentation pack.

## What it does

- Validates a Documentation Pack with required `PRD` and `TAD`
- Infers a project profile when one is provided
- Generates repo-agnostic bootstrap guidance
- Suggests workflow, structure, and deliverables by project kind

## Supported project kinds

- Full stack
- Mobile
- Web app
- Web game
- iOS game
- General fallback

## Input contract

The script expects a Documentation Pack with:

- `PRD`
- `TAD`
- optional `Project Profile`

## Generated output

- [`docs/project_bootstrap_guide.md`](docs/project_bootstrap_guide.md)
- a normalized bootstrap workflow
- recommended repo structure by project kind
- profile-specific deliverables

## Files

- [`scripts/bootstrap_project_guide.py`](scripts/bootstrap_project_guide.py) - validate the pack and generate the guide
- [`docs/documentation_pack_example.md`](docs/documentation_pack_example.md) - example input pack
- [`docs/project_bootstrap_guide.md`](docs/project_bootstrap_guide.md) - generated guide

## Usage

```bash
python3 scripts/bootstrap_project_guide.py --pack docs/documentation_pack_example.md --output docs/project_bootstrap_guide.md
python3 scripts/bootstrap_project_guide.py --pack docs/documentation_pack_example.md --output docs/project_bootstrap_guide.md --check
```

## Output model

The guide is designed to work across:

- full stack repos
- mobile repos
- web app repos
- web game repos
- iOS game repos

## Design

- Rules are intentionally profile-driven, not stack-specific.
- PRD and TAD stay mandatory.
- The pack remains the source of truth.
