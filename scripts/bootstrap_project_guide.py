#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs/project_bootstrap_guide.md"

PROFILE_CATALOG = {
    "general": {
        "label": "General repository",
        "summary": "Use when the pack does not identify a narrower delivery shape.",
        "recommended_taxonomy": [
            "PRD",
            "TAD",
            "Domain Specification",
            "Data Model",
            "UX/UI Specification",
            "Backlog",
            "QA",
            "Build",
            "Governance",
            "Handoff",
        ],
        "repo_structure": [
            ("AGENTS.md", "agent entrypoint and reading order"),
            ("README.md", "project overview and bootstrap usage"),
            ("docs/README.md", "documentation entrypoint"),
            ("docs/governance/", "governance rules and guardrails"),
            ("docs/product/", "product and source-of-truth docs"),
            ("src/", "implementation code"),
            ("tests/", "unit, integration, and acceptance tests"),
        ],
        "deliverables": [
            "Core domain docs: PRD, TAD, and the remaining pack documents",
            "Governance rules for scope, architecture, workflow, and validation",
            "Implementation backlog with clear dependency order",
            "Release and QA criteria for the chosen stack",
        ],
        "workflow": [
            "Write PRD and TAD first.",
            "Add the remaining source-of-truth docs only after the boundaries are stable.",
            "Define the smallest implementation slice that can be verified independently.",
            "Keep one owner per workstream and one handoff artifact per completed slice.",
        ],
    },
    "full-stack": {
        "label": "Full-stack application repository",
        "summary": "Use when the repository includes backend plus at least one client surface.",
        "recommended_taxonomy": [
            "PRD",
            "TAD",
            "API Contract and Data Model",
            "UX/UI Specification",
            "Implementation Backlog",
            "QA and Acceptance Test Plan",
            "Build and Deployment Runbook",
            "Governance",
            "Handoff",
        ],
        "repo_structure": [
            ("AGENTS.md", "agent entrypoint and reading order"),
            ("README.md", "project overview and bootstrap usage"),
            ("docs/README.md", "documentation entrypoint"),
            ("docs/governance/", "governance rules and guardrails"),
            ("docs/product/", "product and source-of-truth docs"),
            ("services/api/", "backend service or API"),
            ("apps/web/", "web client"),
            ("apps/mobile/", "mobile client, if applicable"),
            ("packages/shared/", "contracts, utilities, and shared models"),
            ("infra/", "deployment, environment, and delivery assets"),
            ("tests/", "contract, integration, and end-to-end tests"),
        ],
        "deliverables": [
            "API contract and boundary document",
            "Data model and storage rules",
            "Client app guidance for each surfaced client",
            "Deployment and environment runbook",
            "Cross-platform validation checklist",
        ],
        "workflow": [
            "Define the API and data boundaries before client implementation.",
            "Separate shared contracts from client-specific views.",
            "Treat deployment, auth, and data ownership as first-class governance topics.",
            "Validate backend, client, and integration paths independently.",
        ],
    },
    "mobile": {
        "label": "Native mobile application repository",
        "summary": "Use when the primary deliverable is an iOS or Android app without a web client focus.",
        "recommended_taxonomy": [
            "PRD",
            "TAD",
            "App Shell and Navigation",
            "Platform Constraints",
            "Implementation Backlog",
            "QA and Device Test Plan",
            "Release and Signing Runbook",
            "Governance",
            "Handoff",
        ],
        "repo_structure": [
            ("AGENTS.md", "agent entrypoint and reading order"),
            ("README.md", "project overview and bootstrap usage"),
            ("docs/README.md", "documentation entrypoint"),
            ("docs/governance/", "governance rules and guardrails"),
            ("docs/product/", "product and source-of-truth docs"),
            ("apps/mobile/", "mobile application"),
            ("packages/shared/", "shared domain models and utilities"),
            ("tests/", "unit, device, and integration tests"),
        ],
        "deliverables": [
            "Navigation and screen flow specification",
            "Platform permissions and offline behavior",
            "Release, signing, and store-readiness notes",
            "Device testing and accessibility criteria",
        ],
        "workflow": [
            "Define app shell, navigation, and state boundaries early.",
            "Capture platform-specific constraints before implementation.",
            "Keep release/signing work visible in the planning sequence.",
            "Validate on real device targets before release.",
        ],
    },
    "web-app": {
        "label": "Browser-based web application repository",
        "summary": "Use when the primary deliverable is a browser application.",
        "recommended_taxonomy": [
            "PRD",
            "TAD",
            "Routing and State Specification",
            "UX/UI Specification",
            "Implementation Backlog",
            "QA and Browser Test Plan",
            "Build and Deployment Runbook",
            "Governance",
            "Handoff",
        ],
        "repo_structure": [
            ("AGENTS.md", "agent entrypoint and reading order"),
            ("README.md", "project overview and bootstrap usage"),
            ("docs/README.md", "documentation entrypoint"),
            ("docs/governance/", "governance rules and guardrails"),
            ("docs/product/", "product and source-of-truth docs"),
            ("apps/web/", "browser application"),
            ("packages/shared/", "shared UI, domain, or contract code"),
            ("tests/", "unit, integration, and browser tests"),
        ],
        "deliverables": [
            "Routing and navigation model",
            "State, accessibility, and responsive layout rules",
            "Build, deploy, and preview workflow",
            "Browser compatibility and performance checks",
        ],
        "workflow": [
            "Define route structure and layout boundaries before feature work.",
            "Separate view state, domain state, and persistence concerns.",
            "Make accessibility and responsive behavior part of the acceptance criteria.",
            "Validate build, preview, and browser behavior before handoff.",
        ],
    },
    "web-game": {
        "label": "Browser-based game repository",
        "summary": "Use when the primary deliverable is a browser game.",
        "recommended_taxonomy": [
            "PRD",
            "TAD",
            "Game Loop and Rules",
            "Content Specification",
            "Implementation Backlog",
            "QA and Gameplay Test Plan",
            "Build and Deployment Runbook",
            "Governance",
            "Handoff",
        ],
        "repo_structure": [
            ("AGENTS.md", "agent entrypoint and reading order"),
            ("README.md", "project overview and bootstrap usage"),
            ("docs/README.md", "documentation entrypoint"),
            ("docs/governance/", "governance rules and guardrails"),
            ("docs/product/", "product and source-of-truth docs"),
            ("apps/web/", "browser shell and hosting entry point"),
            ("packages/game/", "game loop, rules, and state"),
            ("packages/content/", "content and authored data"),
            ("assets/", "sprites, audio, and media"),
            ("tests/", "unit, integration, and gameplay verification"),
        ],
        "deliverables": [
            "Game loop and interaction model",
            "Content pipeline and authored-data rules",
            "Render/input separation boundaries",
            "Gameplay QA and content validation criteria",
        ],
        "workflow": [
            "Define the game loop and rule boundaries before rendering code.",
            "Keep content, state, and rendering separate.",
            "Make authored data validation part of the build or QA path.",
            "Validate gameplay flow and content integrity before release.",
        ],
    },
    "ios-game": {
        "label": "Native iOS game repository",
        "summary": "Use when the primary deliverable is a native iOS game.",
        "recommended_taxonomy": [
            "PRD",
            "TAD",
            "Game Loop and Rules",
            "Native App Shell",
            "Implementation Backlog",
            "QA and Device Test Plan",
            "Release and Signing Runbook",
            "Governance",
            "Handoff",
        ],
        "repo_structure": [
            ("AGENTS.md", "agent entrypoint and reading order"),
            ("README.md", "project overview and bootstrap usage"),
            ("docs/README.md", "documentation entrypoint"),
            ("docs/governance/", "governance rules and guardrails"),
            ("docs/product/", "product and source-of-truth docs"),
            ("apps/ios/", "native iOS shell and platform integration"),
            ("packages/game/", "game loop, rules, and state"),
            ("packages/content/", "content and authored data"),
            ("assets/", "art, audio, and media"),
            ("tests/", "unit, integration, and device verification"),
        ],
        "deliverables": [
            "Native app shell and platform integration notes",
            "Game loop and content pipeline boundary",
            "Device testing and performance criteria",
            "Release/signing and store-readiness workflow",
        ],
        "workflow": [
            "Define the native shell and game boundary before implementation.",
            "Keep platform integration separate from game rules.",
            "Treat device performance and release signing as explicit workstreams.",
            "Validate on device targets before release handoff.",
        ],
    },
}

PROFILE_ALIASES = {
    "full stack": "full-stack",
    "full-stack": "full-stack",
    "backend + client": "full-stack",
    "mobile": "mobile",
    "mobile only": "mobile",
    "webapp": "web-app",
    "web app": "web-app",
    "web-app": "web-app",
    "browser app": "web-app",
    "web game": "web-game",
    "browser game": "web-game",
    "ios game": "ios-game",
    "iOS game": "ios-game",
    "native game": "ios-game",
}


def now_stamp() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"missing file: {path}")
    return path.read_text()


def parse_markdown_sections(text: str) -> tuple[str, dict[str, list[str]]]:
    title = "Documentation Pack"
    sections: dict[str, list[str]] = {}
    current: str | None = None

    for line in text.splitlines():
        if line.startswith("# ") and title == "Documentation Pack":
            title = line[2:].strip()
            continue
        match = re.match(r"^##\s+(.*\S)\s*$", line)
        if match:
            current = match.group(1)
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)

    return title, sections


def collect_order_items(lines: list[str]) -> list[str]:
    items: list[str] = []
    for line in lines:
        match = re.match(r"^\s*\d+\.\s+(.*\S)\s*$", line)
        if match:
            items.append(match.group(1))
    return items


def collect_bullet_pairs(lines: list[str]) -> dict[str, str]:
    pairs: dict[str, str] = {}
    for line in lines:
        match = re.match(r"^\s*-\s*(.+?):\s*(.+\S)\s*$", line)
        if match:
            pairs[match.group(1).strip().lower()] = match.group(2).strip()
    return pairs


def has_token(items: list[str], token: str, alt: str) -> bool:
    pattern = re.compile(rf"\b{re.escape(token)}\b", re.IGNORECASE)
    return any(pattern.search(item) or alt.lower() in item.lower() for item in items)


def normalize_kind(value: str) -> str:
    key = re.sub(r"\s+", " ", value.strip().lower())
    return PROFILE_ALIASES.get(key, PROFILE_ALIASES.get(key.replace("_", " "), key))


def normalize_key(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def parse_project_profile(lines: list[str]) -> dict[str, str]:
    profile: dict[str, str] = {}
    for key, value in collect_bullet_pairs(lines).items():
        profile[normalize_key(key)] = value
    return profile


def infer_project_kind(title: str, profile: dict[str, str], order_items: list[str]) -> str:
    explicit = (
        profile.get("repository kind")
        or profile.get("project kind")
        or profile.get("project type")
        or profile.get("kind")
        or profile.get("delivery model")
    )
    if explicit:
        normalized = normalize_kind(explicit)
        if normalized in PROFILE_CATALOG:
            return normalized

    corpus = " ".join([title, " ".join(order_items), " ".join(profile.values())]).lower()
    if ("ios" in corpus or "iphone" in corpus or "ipad" in corpus) and "game" in corpus:
        return "ios-game"
    if "web game" in corpus or "browser game" in corpus or ("game" in corpus and "web" in corpus):
        return "web-game"
    if "full stack" in corpus or "backend" in corpus or "api" in corpus or "service" in corpus:
        if "mobile" in corpus or "web" in corpus:
            return "full-stack"
    if "mobile" in corpus or "android" in corpus:
        return "mobile"
    if "web app" in corpus or "webapp" in corpus or "browser app" in corpus:
        return "web-app"
    return "general"


def validate_pack(pack_path: Path) -> tuple[str, list[str], dict[str, str], str]:
    title, sections = parse_markdown_sections(read_text(pack_path))

    if "Documentation Order" not in sections:
        raise ValueError("Documentation Pack must include a 'Documentation Order' section")

    order_items = collect_order_items(sections["Documentation Order"])
    if not order_items:
        raise ValueError("Documentation Order must contain at least one numbered item")

    if not has_token(order_items, "PRD", "product requirements document"):
        raise ValueError("Documentation Order must include PRD")

    if not has_token(order_items, "TAD", "technical architecture document"):
        raise ValueError("Documentation Order must include TAD")

    profile = parse_project_profile(sections.get("Project Profile", []))
    kind = infer_project_kind(title, profile, order_items)
    return title, order_items, profile, kind


def slugify_title(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "document"


def make_readme_index(title: str, section_title: str, entries: list[tuple[str, str]]) -> str:
    lines = [
        f"# {title}",
        "",
        f"## {section_title}",
        "",
    ]
    for label, path in entries:
        lines.append(f"- [{label}]({path})")
    lines.append("")
    return "\n".join(lines)


def build_scaffold_files(title: str, profile: dict[str, str], kind: str, order_items: list[str]) -> dict[Path, str]:
    catalog = PROFILE_CATALOG[kind]
    docs_root = Path("docs")
    governance_root = docs_root / "governance"
    product_root = docs_root / "product"

    project_name = title if title else "Bootstrap Scaffold"
    readme_lines = [
        f"# {project_name}",
        "",
        "This repository was scaffolded from a Documentation Pack.",
        "",
        "## Entry Points",
        "",
        "- [Documentation](docs/README.md)",
        "- [Governance](docs/governance/README.md)",
        "- [Bootstrap Guide](docs/project_bootstrap_guide.md)",
        "",
    ]

    docs_index_entries = [("Governance", "governance/README.md"), ("Project Docs", "product/README.md")]
    product_entries: list[tuple[str, str]] = []
    for item in order_items:
        if item.strip().lower() == "governance":
            continue
        filename = f"{slugify_title(item)}.md"
        product_entries.append((item, f"{filename}"))

    files: dict[Path, str] = {
        Path("README.md"): "\n".join(readme_lines),
        Path("AGENTS.md"): "\n".join(
            [
                f"# AGENTS.md — {project_name}",
                "",
                "- Start at `docs/README.md`.",
                "- `docs/governance/README.md` is the authoritative governance entrypoint.",
                "- Read docs on demand; do not crawl the repository unnecessarily.",
                "- Use repo entrypoints and existing scripts only.",
                "- Create or update `PLANS.md` before non-trivial multi-file work.",
                "- If something is undefined, resolve it in the governing docs first.",
                "",
            ]
        ),
        docs_root / "README.md": make_readme_index(f"{project_name} Documentation", "Navigation", docs_index_entries),
        governance_root / "README.md": make_readme_index(
            "Governance Index",
            "Read On Demand",
            [
                ("PROJECT_RULES.md", "PROJECT_RULES.md"),
                ("ARCHITECTURE_GUARDRAILS.md", "ARCHITECTURE_GUARDRAILS.md"),
                ("CONTENT_GOVERNANCE.md", "CONTENT_GOVERNANCE.md"),
                ("QUALITY_GATES.md", "QUALITY_GATES.md"),
                ("WORKFLOW_RULES.md", "WORKFLOW_RULES.md"),
            ],
        ),
        governance_root / "PROJECT_RULES.md": "\n".join(
            [
                "# Project Rules",
                "",
                "## Purpose",
                "",
                "Define the immutable product rules that constrain implementation and content decisions.",
                "",
                "## Scope Boundaries",
                "",
                f"- Repository kind: {catalog['label']}",
                f"- Project profile: {profile or 'Insufficient data'}",
                "",
                "## Change Rule",
                "",
                "- Any new product rule must be captured in the relevant source-of-truth doc before implementation.",
                "",
            ]
        ),
        governance_root / "ARCHITECTURE_GUARDRAILS.md": "\n".join(
            [
                "# Architecture Guardrails",
                "",
                "## Purpose",
                "",
                "Define module boundaries and the constraints that keep the scaffold maintainable.",
                "",
                "## Baseline Rules",
                "",
                "- Keep presentation, domain logic, and persistence separate.",
                "- Keep shared contracts in a dedicated shared layer.",
                "- Do not introduce cross-layer imports without updating the architecture doc first.",
                "",
            ]
        ),
        governance_root / "CONTENT_GOVERNANCE.md": "\n".join(
            [
                "# Content Governance",
                "",
                "## Purpose",
                "",
                "Define content ownership, naming, and validation rules for authored files.",
                "",
                "## Baseline Rules",
                "",
                "- Use stable, semantic names for files and document ids.",
                "- Keep locale-specific or domain-specific content scoped explicitly.",
                "- Validate authored content before runtime use.",
                "",
            ]
        ),
        governance_root / "QUALITY_GATES.md": "\n".join(
            [
                "# Quality Gates",
                "",
                "## Purpose",
                "",
                "Define the minimum checks required before implementation or release.",
                "",
                "## Baseline Rules",
                "",
                "- Do not bypass validation silently.",
                "- Require the first implementation slice to pass review and test gates before expansion.",
                "- Treat unresolved exceptions as release blockers unless explicitly documented.",
                "",
            ]
        ),
        governance_root / "WORKFLOW_RULES.md": "\n".join(
            [
                "# Workflow Rules",
                "",
                "## Purpose",
                "",
                "Define how planning, editing, and validation should proceed in the scaffolded repository.",
                "",
                "## Baseline Rules",
                "",
                "- Keep one owner per workstream.",
                "- Record the active task state in a dedicated handoff or backlog document.",
                "- Use small, reversible changes.",
                "",
            ]
        ),
        product_root / "README.md": make_readme_index(
            "Product Documentation Index",
            "Documents",
            product_entries,
        ),
    }

    for item in order_items:
        if item.strip().lower() == "governance":
            continue
        filename = slugify_title(item)
        files[product_root / filename] = "\n".join(
            [
                f"# {item}",
                "",
                "## Purpose",
                "",
                "Source-of-truth document scaffolded from the Documentation Pack.",
                "",
                "## Notes",
                "",
                "- Fill this document from the Documentation Pack before implementation starts.",
                "",
            ]
        )

    return files


def write_scaffold(root: Path, files: dict[Path, str]) -> list[Path]:
    created: list[Path] = []
    for relative_path, content in files.items():
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            continue
        target.write_text(content.rstrip() + "\n")
        created.append(target)
    return created


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fm: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fm[key.strip()] = value.strip().strip('"')
    return fm


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break
    if end_index is None:
        return {}, text
    fm_text = "\n".join(lines[1:end_index])
    body = "\n".join(lines[end_index + 1 :]).lstrip("\n")
    return parse_frontmatter("---\n" + fm_text + "\n---\n"), body


def format_table_rows(rows: list[tuple[str, str]]) -> list[str]:
    formatted = []
    for left, right in rows:
        formatted.append(f"| {left} | {right} |")
    return formatted


def render_guide_body(title: str, profile: dict[str, str], kind: str, order_items: list[str]) -> str:
    catalog = PROFILE_CATALOG[kind]
    profile_lines = []
    if profile:
        for key, value in profile.items():
            profile_lines.append(f"- {key.title()}: {value}")
    else:
        profile_lines.append("- Not specified")

    rows = [f"| {index} | {item} |" for index, item in enumerate(order_items, start=1)]
    taxonomy = catalog["recommended_taxonomy"]
    deliverables = [f"- {item}" for item in catalog["deliverables"]]
    workflow = [f"{index}. {item}" for index, item in enumerate(catalog["workflow"], start=1)]
    structure_rows = format_table_rows(catalog["repo_structure"])

    lines = [
        "# Repository Bootstrap Guide",
        "",
        "## Purpose",
        "",
        "Use this guide to start a new repository from a Documentation Pack without inventing scope, rules, or work order.",
        "",
        "## Pack Contract",
        "",
        f"- Pack title: {title}",
        "- Mandatory inputs: PRD, TAD",
        "- Optional but recommended: Project Profile",
        f"- Recommended taxonomy: {', '.join(taxonomy)}",
        "",
        "## Detected Repository Profile",
        "",
        f"- Repository kind: {catalog['label']}",
        f"- Profile summary: {catalog['summary']}",
        *profile_lines,
        "",
        "## Documentation Order",
        "",
        "| Order | Document |",
        "| --- | --- |",
        *rows,
        "",
        "## Suggested Deliverables",
        "",
        *deliverables,
        "",
        "## Suggested Repo Structure",
        "",
        "| Path | Purpose |",
        "| --- | --- |",
        *structure_rows,
        "",
        "## Bootstrap Sequence",
        "",
        "1. Validate the Documentation Pack before writing anything.",
        "2. Lock product intent in PRD.",
        "3. Lock system boundaries in TAD.",
        "4. Add the remaining source-of-truth documents in pack order.",
        "5. Add governance rules before implementation starts.",
        "6. Define any team or agent routing if the project uses delegation.",
        "7. Build backlog, QA, and handoff artifacts from the authoritative docs.",
        "8. Start implementation only after the guide, governance, and validation rules exist.",
        "",
        "## Suggested Workflow",
        "",
        *workflow,
        "",
        "## Governance Baseline",
        "",
        "- Keep a single source of truth per decision.",
        "- Put scope rules in PRD or the project rules doc, not in task chatter.",
        "- Put architecture boundaries in TAD or architecture governance, not in implementation notes.",
        "- Put content, data, or domain rules in the relevant source-of-truth doc or governance file.",
        "- Put workflow, planning, and validation rules in governance docs before coding.",
        "- Record exceptions explicitly, with a removal plan and expiry if applicable.",
        "",
        "## Work Organization",
        "",
        "- Use one entry point for ambiguous requests.",
        "- Route each request to exactly one owner or workstream.",
        "- Keep planning in architecture and implementation in the owning workstream.",
        "- Keep validation in a dedicated validation phase or quality gate.",
        "- Keep handoff artifacts short, explicit, and generated from the current state.",
        "",
        "## Validation Gate",
        "",
        "- Do not begin implementation if PRD or TAD is missing.",
        "- Do not bypass governance, architecture, or domain rules silently.",
        "- Validate the first implementation slice before expanding scope.",
        "- Update the active task or handoff artifact whenever work changes hands.",
        "",
        "## Script Usage",
        "",
        "```bash",
        "python3 scripts/bootstrap_project_guide.py --pack path/to/documentation-pack.md --output docs/project_bootstrap_guide.md",
        "python3 scripts/bootstrap_project_guide.py --pack path/to/documentation-pack.md --output docs/project_bootstrap_guide.md --check",
        "python3 scripts/bootstrap_project_guide.py --pack path/to/documentation-pack.md --output docs/project_bootstrap_guide.md --scaffold --scaffold-root /path/to/new-repo",
        "```",
        "",
    ]
    return "\n".join(lines).rstrip()


def render_guide(title: str, profile: dict[str, str], kind: str, order_items: list[str], created_at: str, last_modified_at: str) -> str:
    body = render_guide_body(title, profile, kind, order_items)
    return "\n".join(
        [
            "---",
            f'createdAt: "{created_at}"',
            f'lastModifiedAt: "{last_modified_at}"',
            "---",
            "",
            body,
        ]
    )


def resolve_created_at(output_path: Path) -> str:
    existing = parse_frontmatter(read_text(output_path)) if output_path.exists() else {}
    return existing.get("createdAt", now_stamp())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a Documentation Pack and generate a bootstrap guide.")
    parser.add_argument("--pack", required=True, help="Path to the markdown Documentation Pack.")
    parser.add_argument(
        "--output",
        default=None,
        help="Path to the generated markdown guide.",
    )
    parser.add_argument(
        "--scaffold",
        action="store_true",
        help="Create a baseline repository scaffold from the Documentation Pack.",
    )
    parser.add_argument(
        "--scaffold-root",
        default=".",
        help="Target root directory for scaffold creation.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compare the generated output with the existing file instead of writing it.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pack_path = Path(args.pack)
    scaffold_root = Path(args.scaffold_root)
    if args.output is None:
        output_path = scaffold_root / "docs/project_bootstrap_guide.md" if args.scaffold else DEFAULT_OUTPUT
    else:
        output_path = Path(args.output)
        if args.scaffold and not output_path.is_absolute():
            output_path = scaffold_root / output_path

    try:
        title, order_items, profile, kind = validate_pack(pack_path)
        if args.check:
            if not output_path.exists():
                print(f"Missing output file: {output_path}")
                return 1
            existing_text = output_path.read_text()
            existing_frontmatter, existing_body = split_frontmatter(existing_text)
            if not existing_frontmatter.get("createdAt") or not existing_frontmatter.get("lastModifiedAt"):
                print(f"Output is missing freshness metadata: {output_path}")
                return 1
            generated_body = render_guide_body(title, profile, kind, order_items)
            if existing_body != generated_body:
                print(f"Output is out of date: {output_path}")
                return 1
            print("Bootstrap guide is up to date.")
            return 0

        created_at = resolve_created_at(output_path)
        last_modified_at = now_stamp()
        generated = render_guide(title, profile, kind, order_items, created_at, last_modified_at)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(generated)
        if args.scaffold:
            files = build_scaffold_files(title, profile, kind, order_items)
            created = write_scaffold(scaffold_root, files)
            print(f"Created {len(created)} scaffold file(s) under {scaffold_root}")
        print(f"Generated bootstrap guide at {output_path}")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
