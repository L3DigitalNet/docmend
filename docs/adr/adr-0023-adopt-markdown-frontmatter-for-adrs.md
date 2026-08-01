---
schema_version: '1.1'
id: 'adr-0023-docmend-adopt-markdown-frontmatter-for-adrs'
title: 'ADR 0023: Adopt Markdown Frontmatter for ADRs'
description: 'docmend adopts the Project Standards Markdown Frontmatter package for ADR documents only, while keeping project specifications and product-output frontmatter under their existing independent schemas.'
doc_type: 'adr'
status: 'active'
created: '2026-08-01'
updated: '2026-08-01'
reviewed: '2026-08-01'
owner: 'chrisdpurcell'
consumer: 'agent'
tags:
  - 'standards'
  - 'frontmatter'
  - 'adr'
  - 'validation'
aliases: []
related:
  - '.standards/config.toml'
  - 'docs/specs/docmend.md'
  - 'docs/adr/adr-0001-no-markdown-frontmatter-standard.md'
  - 'docs/adr/adr-0011-frontmatter-optional-minimal-split.md'
supersedes:
  - 'docs/adr/adr-0001-no-markdown-frontmatter-standard.md'
superseded_by: null
source: []
confidence: 'high'
visibility: 'public'
license: null
project:
  decision_makers:
    - 'chrisdpurcell'
  consulted: []
  informed: []
---

# Adopt Markdown Frontmatter for ADRs

## Context and Problem Statement

ADR-0001 rejected the Markdown Frontmatter package because a repository-wide schema would compete with docmend's Project Specification metadata and with the Pandoc-oriented frontmatter that docmend emits into product documents. The package now supports an explicit include/exclude corpus, and the owner has selected it as part of the repository's Catalog 5 package set. How can docmend gain schema validation for ADR metadata without creating a second authority over specifications or product output?

## Decision Drivers

- The requested Project Standards package set explicitly includes `markdown-frontmatter`.
- Product-output frontmatter remains governed exclusively by SPEC-VHHB and `src/docmend/schemas/frontmatter.schema.json`.
- Project specifications remain governed exclusively by the `project-spec` package and must not enter the generic Frontmatter corpus.
- The existing ADRs already use the compatible Project Standards metadata shape and benefit from automated schema and ID validation.
- Package corpora must be easy to inspect and remain disjoint by construction.

## Considered Options

- Adopt Markdown Frontmatter for ADR documents only.
- Adopt it for all repository documentation and carve out conflicting files individually.
- Continue the ADR-0001 non-adoption decision.

## Decision Outcome

Chosen option: **adopt Markdown Frontmatter for ADR documents only**, because a single positive include (`docs/adr/**/*.md`) plus the ADR-template exclusion creates a stable, reviewable boundary. The Project Spec corpus, Agent Handoff knowledge, harness assets, README, and docmend's product documents remain outside the package.

The package uses contract 1.1, the bundled schema, required frontmatter, the caller workflow, and reference validation disabled. ADR body-section enforcement remains a separate option and stays disabled; this decision validates ADR metadata without changing the repository's existing body convention.

### Consequences

- Good, because ADR metadata and IDs now have local and CI validation.
- Good, because the product and Project Spec frontmatter contracts remain uncontested.
- Good, because the selected corpus is defined positively rather than through a growing repository-wide exclusion list.
- Bad, because a new Markdown document type under `docs/adr/` must either conform or be explicitly excluded.
- Bad, because cross-document reference validation remains unavailable until the repository deliberately enables and repairs that optional stricter check.

### Confirmation

Compliance is confirmed when `.standards/config.toml` selects only `docs/adr/**/*.md`, excludes `docs/adr/adr.template.md`, `project-standards validate` succeeds, and Project Spec validation continues to govern `docs/specs/**/*.md` independently.

## More Information

- Supersedes [ADR-0001](adr-0001-no-markdown-frontmatter-standard.md).
- The product frontmatter decision remains [ADR-0011](adr-0011-frontmatter-optional-minimal-split.md); this ADR does not change docmend output.
- The selected package and corpus are recorded in [`.standards/config.toml`](../../.standards/config.toml).
