---
schema_version: '1.1'
id: 'reference-000001-docmend-cli-usage'
title: 'docmend CLI Usage'
description: 'Canonical command, option, artifact, safety, and exit-status reference for the docmend CLI.'
doc_type: 'reference'
status: 'active'
created: '2026-08-01'
updated: '2026-08-01'
tags:
  - 'cli'
  - 'reference'
  - 'documents'
aliases: []
related:
  - 'README.md'
  - 'docs/specs/docmend.md'
  - 'docs/runbooks/restore-from-manifest.md'
  - 'docs/runbooks/resume-after-interruption.md'
---

# docmend

## NAME

`docmend` — normalize, repair, and convert text and HTML documents into clean, well-structured Markdown.

## SYNOPSIS

```text
docmend [GLOBAL OPTIONS] COMMAND [COMMAND OPTIONS] [ARGS]...
docmend {--help | --version}
```

Commands:

```text
docmend scan [OPTIONS] PATH
docmend plan [OPTIONS] [PATH]
docmend apply [OPTIONS] PLAN
docmend restore [OPTIONS]
docmend verify [OPTIONS] PATH
```

## DESCRIPTION

`docmend` processes one file or a directory tree through an explicit scan, plan, apply, and verify pipeline. `scan`, `plan`, and `verify` are read-only. `apply` and `restore` preview by default and write only with `--write`.

Run artifacts default to `.docmend/` in the invocation directory. Each writing operation is safety-gated, uses atomic publication, and records an append-only manifest. Risky or ambiguous files are skipped with a reason instead of being guessed at.

Configuration precedence is CLI options, then `docmend.toml`, then built-in defaults. List-valued `--include` and `--exclude` options replace their configured lists; they do not append.

## GLOBAL OPTIONS

### `--version`, `-V`

Print the package version and exit.

### `--verbose`, `-v`

Raise console detail. Level `1` shows per-file outcomes and level `2` shows debug output. The file log level is unaffected.

Default: `0`.

### `--quiet`, `-q`

Limit console output to errors and critical messages. Mutually exclusive with nonzero `--verbose`.

### `--dry-run`, `-n`

Preview without writing. This is already the default posture for `apply` and `restore`.

### `--help`, `-h`

Show help and exit.

## COMMANDS

### `scan`

Scan one file or directory tree read-only and write a structured inventory.

```text
docmend scan [OPTIONS] PATH
```

Options:

- `--report PATH` — write the inventory to the selected path. Default: `.docmend/docmend-<run-id>-inventory.json`.
- `--config PATH` — read configuration from the selected TOML file. Default: `./docmend.toml` when present.
- `--include TEXT` — replace `paths.include`; repeatable.
- `--exclude TEXT` — replace `paths.exclude`; repeatable.

Exit status: `0` clean; `1` unreadable files or directories were skipped; `2` invalid input or configuration; `3` concurrent-run safety refusal.

### `plan`

Create a reviewable plan from an existing inventory or from a path scanned by the command.

```text
docmend plan [OPTIONS] [PATH]
docmend plan --inventory INVENTORY [OPTIONS]
```

Exactly one of `PATH` or `--inventory` supplies the input.

Options:

- `--inventory PATH` — consume an existing inventory artifact.
- `--out PATH` — write the plan to the selected path. Default: `.docmend/docmend-<run-id>-plan.json`.
- `--config PATH` — read configuration from the selected TOML file. Default: `./docmend.toml` when present.
- `--include TEXT` — replace `paths.include`; repeatable.
- `--exclude TEXT` — replace `paths.exclude`; repeatable.
- `--fail-on-low-confidence-encoding` — exit `1` when any file is skipped by an encoding-confidence gate.

Exit status: `0` clean; `1` planning findings, including configured collision failures and qualifying skips; `2` invalid input or configuration; `3` concurrent-run safety refusal.

### `apply`

Execute the actions in a reviewed plan. Without `--write`, the command only previews outcomes.

```text
docmend apply [OPTIONS] PLAN
```

Options:

- `--write` — opt into filesystem mutation.
- `--dry-run` — preview without writing; this is the default.
- `--backup-dir PATH` — store verified source and overwritten-target backups under this root; overrides `write.backup_dir`.
- `--preserved-by git|external` — declare an external byte-preserving strategy that satisfies the write gate.
- `--allow-no-backup` — accept reduced rollback for a single-action plan only.
- `--report PATH` — write the apply report to the selected path. Default: `.docmend/docmend-<run-id>-report.json`.
- `--resume-manifest PATH` — reconcile against a prior apply manifest; repeat for every manifest in a multiply interrupted chain.
- `--resume-run-id TEXT` — resolve both default manifest and report sidecars for a prior run ID; repeatable and combinable with explicit evidence.
- `--prior-report PATH` — supply a relocated or report-only predecessor attempt report; repeatable.

A content-changing write requires `--backup-dir`, `--preserved-by`, or the restricted `--allow-no-backup` opt-in. Only tool-written backups contain the bytes needed for full `restore`; external preservation and no-backup runs may be renames-only from the manifest.

Exit status: `0` clean; `1` skips or failures other than `already-applied`; `2` invalid plan, evidence, or option combination; `3` safety-gate or run-lock refusal.

### `restore`

Undo one apply attempt chain in last-in, first-out order. Without `--write`, the command previews the restore.

```text
docmend restore [OPTIONS]
```

Options:

- `--manifest PATH` — supply a manifest in the attempt chain; repeatable.
- `--run-id TEXT` — resolve `.docmend/docmend-<ID>-manifest.jsonl`; repeatable and combinable with `--manifest`.
- `--id TEXT` — restore only the selected `docmend.id`; repeatable.
- `--write` — perform the restore.
- `--dry-run` — preview the restore; this is the default.

Supply the complete manifest chain for a multiply resumed run. A changed live output is skipped rather than overwritten. A manifest without tool-written backup bytes supports pure-rename restoration only.

Exit status: `0` clean; `1` skips, failures, or an `--id` selection matching nothing; `2` invalid manifest input; `3` lock or containment refusal.

### `verify`

Check converted output read-only. Content checks always run; optional plan, report, and manifest evidence enables lifecycle, recovery, and exactly-once coverage checks.

```text
docmend verify [OPTIONS] PATH
```

Options:

- `--manifest PATH` — supply a manifest artifact; repeatable.
- `--run-id TEXT` — resolve default manifest and report sidecars for a run ID; repeatable.
- `--report PATH` — supply an apply-report artifact; repeatable.
- `--plan PATH` — certify complete, exactly-once coverage of the selected plan.
- `--out PATH` — write a durable verify-report artifact.
- `--config PATH` — read configuration from the selected TOML file. Default: `./docmend.toml` when present.

The command checks UTF-8 decodability, LF line endings, frontmatter validity where present, live hashes against supplied manifests, report/manifest accounting, and plan coverage when those evidence artifacts are supplied. It does not mutate the corpus or write a manifest.

Exit status: `0` clean; `1` findings; `2` invalid invocation or structural evidence; `3` safety refusal.

## EXIT STATUS

The command-specific sections identify refinements. The shared taxonomy is:

| Code | Meaning                                                         |
| ---- | --------------------------------------------------------------- |
| `0`  | Clean completion.                                               |
| `1`  | Findings, skips, or operational failures.                       |
| `2`  | Invalid invocation, configuration, or artifact input.           |
| `3`  | Safety refusal, including a gate, lock, or containment refusal. |

## ENVIRONMENT

`docmend` has no application-specific environment variables. Runtime and terminal libraries may honor their own conventional environment settings, but they do not replace `docmend.toml` or CLI options.

## FILES

- `./docmend.toml` — optional repository or working-directory configuration, auto-discovered when `--config` is omitted.
- `./.docmend/` — default run-artifact and log directory.
- `.docmend/docmend-<run-id>-inventory.json` — default scan artifact.
- `.docmend/docmend-<run-id>-plan.json` — default plan artifact.
- `.docmend/docmend-<run-id>-report.json` — default apply report.
- `.docmend/docmend-<run-id>-manifest.jsonl` — append-only apply or restore manifest.
- `.docmend/docmend-<run-id>-verify-report.json` — verify report when requested at the default convention.

Artifacts and backups are retained until the operator removes them; `docmend` does not purge them automatically.

## EXAMPLES

### Scan and plan one directory

```bash
docmend scan ./documents --report ./inventory.json
docmend plan --inventory ./inventory.json --out ./plan.json
```

### Preview and then apply with tool-written backups

```bash
docmend apply ./plan.json
docmend apply ./plan.json --write --backup-dir ../docmend-backups
```

### Resume an interrupted attempt

```bash
docmend apply ./plan.json --write --backup-dir ../docmend-backups \
  --resume-run-id run_20260706T000000Z_000001
```

### Preview and perform a restore

```bash
docmend restore --run-id run_20260706T000000Z_000001
docmend restore --run-id run_20260706T000000Z_000001 --write
```

### Certify plan coverage after apply

```bash
docmend verify ./documents --plan ./plan.json \
  --run-id run_20260706T000000Z_000001 --out ./verify-report.json
```

## NOTES

- Paths are interpreted relative to the current working directory unless absolute.
- `apply` and `restore` never infer authorization to write from configuration alone; `--write` is required for each invocation.
- `--include` and `--exclude` replace configured lists rather than extending them.
- Plan schema 1.x and the removed `parallel.*` configuration namespace are rejected by docmend 2.x with regeneration or migration guidance.

## SEE ALSO

- [README](../README.md) — task-oriented overview and configuration defaults.
- [Project specification](specs/docmend.md) — normative behavior and safety contracts.
- [Restore from a manifest](runbooks/restore-from-manifest.md).
- [Resume after an interruption](runbooks/resume-after-interruption.md).
