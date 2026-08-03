---
schema_version: '1.1'
id: 'adr-0024-docmend-adopt-go-alongside-python-with-neutral-tooling'
title: 'ADR 0024: Adopt Go Alongside Python with Neutral Tooling'
description: 'Adopt Go as a supported repository language with a canonical tooling lane while deferring language-selection policy.'
doc_type: 'adr'
status: 'active'
created: '2026-08-02'
updated: '2026-08-02'
reviewed: '2026-08-02'
owner: 'chrisdpurcell'
consumer: 'agent'
tags:
  - 'adr'
  - 'architecture'
  - 'go'
  - 'python'
  - 'tooling'
aliases:
  - 'go adoption'
  - 'go python coexistence'
  - 'neutral language policy'
related:
  - 'AGENTS.md'
  - 'README.md'
  - 'docs/adr/README.md'
  - 'docs/handoff/conventions.md'
supersedes: []
superseded_by: null
source:
  - 'Owner decision, 2026-08-02'
  - 'go.mod'
  - 'Makefile'
  - '.golangci.yml'
  - '.github/workflows/go.yml'
  - '.vscode/tasks.json'
confidence: 'high'
visibility: 'public'
license: null
project:
  decision_makers:
    - 'chrisdpurcell'
  consulted:
    - 'Codex'
  informed: []
---

# Adopt Go alongside Python with neutral tooling

_MADR status: accepted._

## Context and Problem Statement

This repository has established a Go development and automation lane before adding its first repository-owned Go package. Python remains the implementation language for current repository tooling, managed hooks, tests, and other active surfaces.

Adopting a second implementation language changes the repository's module, dependency, editor, verification, and CI architecture. Those boundaries should be deliberate even though the repository has not yet decided which language is appropriate for each kind of work.

The decision must therefore answer two separate questions: whether Go is supported alongside Python, and how Go changes are verified. It must not turn tooling adoption into a default language preference, migration mandate, or permission to retire Python.

## Decision Drivers

- Make Go work reproducible and independently verifiable before production Go code is introduced.
- Preserve the existing Python implementation and its Project Standards-managed tooling without weakening either lane.
- Keep local, editor, and CI commands aligned behind one canonical owner.
- Pin executable tools and toolchains through reviewable repository authorities.
- Avoid selecting a preferred language before the repository has approved guidance for choosing between Go and Python.
- Preserve separate ownership boundaries for repository tooling, skills, plugins, hooks, and standards-managed files.

## Considered Options

- Adopt Go alongside Python with a neutral, canonical tooling lane.
- Defer Go adoption until language-selection guidance and the first migration are approved together.
- Adopt Go as the preferred language for new repository-owned tooling.

## Decision Outcome

Chosen option: "Adopt Go alongside Python with a neutral, canonical tooling lane." This makes Go an approved repository language and defines how Go work is built and verified without assigning either Go or Python to a category of future work.

The following invariants apply:

- Go and Python coexist as supported repository languages. Neither language is the repository-wide default or preferred choice.
- This decision does not authorize a Python-to-Go migration, production cutover, Python freeze, dependency removal, test retirement, or standards-package change.
- Language selection for new work or migration requires case-specific requirements or later approved guidance. Existing architecture and ownership boundaries take precedence.
- The repository has one root Go module, `github.com/chrisdpurcell/docmend`. Additional modules or a Go workspace require an independently justified ownership or distribution boundary.
- `go.mod` owns the minimum Go version, preferred toolchain, module dependencies, and module-tracked executable tools. `go.sum` owns module checksums.
- The root `Makefile` owns the canonical Go commands. Local users, editor tasks, and CI invoke its targets instead of maintaining independent command lists.
- The canonical Go gate checks repository-scoped formatting, module tidiness and integrity, `go vet`, configured `golangci-lint` analysis, race-enabled tests with coverage, builds, and `govulncheck` when Go packages exist.
- `golangci-lint` is version-pinned and installed under the ignored repository-local `.tools/` directory. Its configuration uses a reviewed linter set; exclusions and disabled analyzers require a documented ownership or correctness reason.
- `govulncheck` is pinned as a module tool and invoked with `go tool`. `go vet` remains a first-party gate and is disabled inside `golangci-lint` to prevent duplicate ownership.
- The Go CI workflow installs the exact preferred toolchain and pinned tools, then invokes the canonical gate. VS Code recommends the Go extension and delegates repository operations to Make targets.
- Go tooling does not own Python, Markdown, shell, standards, handoff, skill, plugin, or harness validation. Those gates remain independent and applicable according to their existing scopes.
- Repository-owned Go source may use the root module. A skill, plugin, generated fixture, or externally distributed component does not join that module merely because it is stored in this repository.

Exact Go and tool versions are ordinary reviewed configuration owned by their declared files. Compatible upgrades do not require an ADR amendment. Changing the module boundary, canonical command owner, verification categories, coexistence policy, or language-neutral posture does.

### Consequences

- Good, because Go code can be introduced through a reproducible local and CI lane without waiting for a migration decision.
- Good, because one command owner prevents VS Code, CI, and local verification from drifting apart.
- Good, because Python remains supported and no migration authority is inferred from the presence of Go tooling.
- Good, because future language guidance can be evaluated independently from the mechanical readiness of the Go lane.
- Bad, because the repository must maintain two language toolchains and their independent supply-chain checks while both remain active.
- Bad, because neutrality leaves language choice unresolved for each new component until later guidance or case-specific evidence settles it.
- Neutral, because package-specific Go checks report an explicit skip until the first Go package exists; module and configuration checks remain active immediately.

### Confirmation

Conformance is confirmed when `make go-check` is the canonical local and CI entry point, pinned tool versions are provable, editor tasks delegate to Make targets, and Go changes do not remove or weaken applicable non-Go gates.

While no Go packages exist, vet, lint, test, build, and vulnerability-package scans must report an explicit skip rather than imply package-level verification. Once a package is added, those same targets must execute against it without requiring a second gate definition.

## Pros and Cons of the Options

### Neutral Go and Python coexistence

- Good, because tooling readiness and language policy remain separate decisions.
- Good, because it preserves current Python authority while allowing bounded Go work.
- Bad, because each future language choice may require additional analysis until general guidance exists.

### Defer Go adoption

- Good, because the repository would maintain only one active implementation-language toolchain until the first approved Go project.
- Bad, because the first Go implementation would also need to design and prove the tooling lane, increasing its scope and coupling infrastructure decisions to product behavior.

### Prefer Go for new repository tooling

- Good, because new work would have an immediate language-selection rule.
- Bad, because no approved evidence or policy currently establishes that Go is the better choice for every repository-owned tool.
- Bad, because a preference could cause opportunistic migration or inappropriate language choices across distinct ownership and distribution boundaries.

## More Information

The current tooling implementation is defined by [`go.mod`](../../go.mod), [`Makefile`](../../Makefile), [`.golangci.yml`](../../.golangci.yml), the [Go CI workflow](../../.github/workflows/go.yml), and the [VS Code tasks](../../.vscode/tasks.json). The commands and versions in those files are implementation authorities, not prose duplicated by this ADR.

Revisit this decision when the repository is ready to define language-selection guidance, when the first Go package exposes a missing verification category, or when a component needs a module, distribution, or tooling boundary that the root lane cannot represent cleanly.
