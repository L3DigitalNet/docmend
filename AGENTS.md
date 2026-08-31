# Agents

**Session state:** Agent Handoff SessionStart injects `docs/handoff/state.md`; do not reread it when injected. Then use this file and `docs/handoff/conventions.md`.

**Full conventions reference:** [`docs/handoff/conventions.md`](docs/handoff/conventions.md) - LLM-targeted pattern library. Check it before adding persistent patterns.

**Detailed review workflows:** not configured for this repo.

## Project

`docmend` is a Python CLI tool (v2.0.2 released 2026-07-22 — the full scan/plan/apply/restore/verify pipeline is live) for normalizing, repairing, and converting a large library (>100k files) of legacy `.txt`/`.html` documents into clean, well-structured Markdown.

Read [`docs/specs/docmend.md`](docs/specs/docmend.md) (SPEC-VHHB, `full` profile, binding Agent Implementation Contract in Appendix B) before proposing any implementation.

## Task Tracking

- [`docs/TODO.md`](docs/TODO.md) — user tasks above agent tasks; don't complete a user task unless asked.
- [`docs/repo-hygiene.md`](docs/workflows/repo-hygiene.md) — periodic repository hygiene checklist for cleanup and maintenance passes.
- [`docs/open-questions.md`](docs/open-questions.md) / [`docs/resolved-questions.md`](docs/resolved-questions.md) — the spec's `OQ-`/`RQ-` decision backlog.

## Non-Negotiables

- This repo is public — see conventions #6 before adding any file, fixture, or doc: never real library documents, paths, or personal content.
- Seven Project Standards packages are adopted (adr, agent-handoff, cli-documentation, markdown-frontmatter, markdown-tooling, project-spec, and python-tooling), managed via the V5 control plane (`.standards/`) — conventions #1-#5 and #8 are their operational how-to. Markdown Frontmatter is scoped only to ADRs (ADR-0023); see conventions #7 for the product, specification, and ADR frontmatter boundaries.
- Never hand-edit a standard-owned file to bypass a check (conventions #8).

## Review Orchestrator Note

- Full `review-orchestrator` sweeps now run selected child reviews with bounded parallelism by default, currently up to `8` in parallel after planning, preflight, and shared research complete.
- The shared-research phase can legitimately take around `10` minutes on larger or research-heavy repos before child reviews start, so treat that as normal unless heartbeats stop or no artifact activity appears beyond that window.
- Expect the sweep index, child review reports, and `*-execution.json` manifests under `docs/reviews/` while the sweep is running.
- Do not describe sweep child reviews as running “one at a time” unless the sweep was explicitly configured down to serial execution.

Go work uses the module and toolchain declared in `go.mod`. Install pinned tools with `make go-tools`, use `make go-format` for fixes, and run `make go-check` before reporting Go changes complete.

<!-- prettier-ignore-start -->

<!-- BEGIN project-standards:agent-handoff -->
<!-- markdownlint-disable MD025 -->
# Agent Handoff

Use the repo-local `agent-handoff` skill at session startup and closeout. Do not reread state already injected by SessionStart. Keep project knowledge inside this repository and store credential references only, never values.
<!-- markdownlint-enable MD025 -->
<!-- END project-standards:agent-handoff -->

<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->

<!-- BEGIN project-standards:markdown-tooling -->
<!-- markdownlint-disable MD025 -->
# Markdown and structured-text tooling

Prettier owns physical formatting and markdownlint owns Markdown structure. Do not add overlapping tools.

Enabled checks: format, lint.
Markdown scope: `**/*.md`.
Structured-config scope: `**/*.json`, `**/*.jsonc`, `**/*.yml`, `**/*.yaml`.
Lint additionally skips generated directories: `.pytest_cache/**`, `.ruff_cache/**`, `.venv/**`, `node_modules/**`.

Check formatting over exactly that scope, with Git as the corpus authority:

```bash
git ls-files -z -- ':(glob)**/*.md' ':(glob)**/*.json' ':(glob)**/*.jsonc' ':(glob)**/*.yml' ':(glob)**/*.yaml' | xargs -0 -r npx prettier --check --
```

Without Git, bound the same scope by glob instead:

```bash
npx prettier --check --no-error-on-unmatched-pattern -- '**/*.md' '**/*.json' '**/*.jsonc' '**/*.yml' '**/*.yaml'
```

Never check or write with a bare `.`: it reaches undeclared languages and Git-excluded scratch.

Lint Markdown structure over the same Git-tracked scope:

```bash
git ls-files -z -- ':(glob)**/*.md' ':(glob,exclude).pytest_cache/**' ':(glob,exclude).ruff_cache/**' ':(glob,exclude).venv/**' ':(glob,exclude)node_modules/**' | sed -z 's|^|:|' | xargs -0 -r npx markdownlint-cli2 --no-globs
```

Never lint a bare recursive glob: it descends into any independent Git repository checked out below this one.

Run the enabled checks before claiming completion.
<!-- markdownlint-enable MD025 -->
<!-- END project-standards:markdown-tooling -->

<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->

<!-- BEGIN project-standards:python-tooling -->
<!-- markdownlint-disable MD025 -->
# Python tooling

Use uv for environments and dependency changes. Ruff owns formatting, linting, and imports.
Use basedpyright in strict mode for type checking. Do not add a competing Python gate.

Run before claiming completion:

```bash
uv run ruff format --check src tests
uv run ruff check src tests
uv run basedpyright
uv run coverage run -m pytest
uv run coverage report
uv run pip-audit
```

When the gate reports formatting or lint findings, run:

```bash
uv run ruff format src tests
uv run ruff check src tests --fix
```
<!-- markdownlint-enable MD025 -->
<!-- END project-standards:python-tooling -->

<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->

<!-- BEGIN project-standards:markdown-frontmatter -->
<!-- markdownlint-disable MD025 -->
# Markdown Frontmatter

Managed Markdown in this repository carries YAML frontmatter under the Markdown Frontmatter Standard: the eleven required fields in canonical order, every scalar quoted, and an id of the form `{doc_type}-{6-char base36 token}-{slug}`.

Create a new managed document with `scripts/new-doc-id --scaffold --doc-type <type> <name>` from the repo-local skill at `.agents/skills/markdown-frontmatter/`. Read that skill's `SKILL.md` before hand-authoring or repairing a frontmatter block.

The gate is `project-standards validate`.

`AGENTS.md`, `CLAUDE.md`, and anything under `.agents/**`, `.claude/**`, or `.codex/**` never carry frontmatter.
<!-- markdownlint-enable MD025 -->
<!-- END project-standards:markdown-frontmatter -->

<!-- prettier-ignore-end -->
