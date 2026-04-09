# bootstrap-doc-pack

Bootstrap a new repository from a mandatory Documentation Pack.

Generate a repo-ready bootstrap guide and baseline scaffold from a small, structured documentation pack.

## What it does

- Validates a Documentation Pack with required `PRD` - Product Requirement Document and `TAD` - Technical Architecture Document
- Infers a project profile when one is provided
- Generates repo-agnostic bootstrap guidance
- Suggests workflow, structure, and deliverables by project kind
- Can create a starter scaffold for the target repository

## Supported repository kinds

- Full-stack application repository
- Native mobile application repository
- Browser-based web application repository
- Browser-based game repository
- Native iOS game repository
- General repository fallback

## Input contract

The script expects a Documentation Pack with:

- `PRD` - Product Requirement Document
- `TAD` - Technical Architecture Document
- optional `Project Profile` with `Repository Kind` or `Project Kind`

## Generated output

- [`docs/project_bootstrap_guide.md`](docs/project_bootstrap_guide.md)
- optional scaffold files under a target repository root
- a normalized bootstrap workflow
- recommended repo structure by project kind
- profile-specific deliverables

## Files

- [`AGENTS.md`](AGENTS.md) - agent entrypoint and reading order
- [`scripts/bootstrap_project_guide.py`](scripts/bootstrap_project_guide.py) - validate the pack and generate the guide
- [`docs/documentation_pack_example.md`](docs/documentation_pack_example.md) - example input pack
- [`docs/project_bootstrap_guide.md`](docs/project_bootstrap_guide.md) - generated guide
- [`docs/README.md`](docs/README.md) - documentation entrypoint
- [`docs/governance/README.md`](docs/governance/README.md) - governance entrypoint

## Usage

```bash
python3 scripts/bootstrap_project_guide.py --pack docs/documentation_pack_example.md --output docs/project_bootstrap_guide.md
python3 scripts/bootstrap_project_guide.py --pack docs/documentation_pack_example.md --output docs/project_bootstrap_guide.md --check
python3 scripts/bootstrap_project_guide.py --pack docs/documentation_pack_example.md --output docs/project_bootstrap_guide.md --scaffold --scaffold-root /path/to/new-repo
```

## Output model

The guide is designed to work across:

- full-stack application repositories
- native mobile application repositories
- browser-based web application repositories
- browser-based game repositories
- native iOS game repositories

## Design

- Rules are intentionally profile-driven, not stack-specific.
- PRD and TAD stay mandatory.
- The pack remains the source of truth.
- Governance entrypoints live under `docs/` so agents do not need to crawl the tree.
