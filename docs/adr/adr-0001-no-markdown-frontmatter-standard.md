---
schema_version: '1.1'
id: 'adr-0001-docmend-do-not-adopt-markdown-frontmatter-standard'
title: 'ADR 0001: Do not adopt the Markdown Frontmatter Standard'
description: "docmend adopts five Project Standards but deliberately excludes the Markdown Frontmatter Standard, whose canonical schema conflicts with docmend's own frontmatter contracts."
doc_type: 'adr'
status: 'accepted'
created: '2026-07-05'
updated: '2026-07-29'
reviewed: null
owner: 'chrisdpurcell'
consumer: 'agent'
tags:
  - 'standards'
  - 'frontmatter'
  - 'markdown'
  - 'deviation'
aliases: []
related:
  - '.standards/config.toml'
  - 'docs/specs/docmend.md'
supersedes: []
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

# Do not adopt the Markdown Frontmatter Standard

## Context and Problem Statement

docmend adopts five standards from [Project Standards](https://github.com/L3DigitalNet/project-standards): Python Tooling SSOT, Markdown Tooling, Project Specification, ADR, and Agent Handoff. The Markdown Frontmatter Standard remains independently selectable; the ADR and Project Specification packages support this repository's deliberately unvalidated documentation-frontmatter policy.

Should docmend also adopt the Markdown Frontmatter Standard so that ADR and other managed Markdown carry CI-validated canonical frontmatter?

## Decision Drivers

- docmend's **product output** is Markdown files whose YAML frontmatter follows a **Pandoc-flavored, purpose-built schema** (title, author, date, tags, source provenance, generated fields such as word/chapter count and checksum) validated against docmend's _own_ schema — see [`docs/specs/docmend.md`](../specs/docmend.md) (§9 Data Model / DR-005). This is the tool's core contract, not a docs concern.
- The repository's spec uses **Pandoc-style metadata blocks**, again distinct from the canonical schema.
- The canonical Markdown Frontmatter Standard defines one repo-wide frontmatter schema and a validator that would compete with both of the above over the same file surface.
- Adopting a standard must not force fighting a validator against docmend's primary output format, and the two other Markdown-frontmatter-adjacent standards we _do_ want (ADR, Project Spec) can function without it.

## Considered Options

- **Adopt the Markdown Frontmatter Standard** alongside the other four, scoping its globs to avoid product output.
- **Do not adopt the Markdown Frontmatter Standard**; take ADR and Project Spec in their non-frontmatter-validated forms.

## Decision Outcome

Chosen option: **"Do not adopt the Markdown Frontmatter Standard"**, because docmend already owns two conflicting frontmatter contracts (its Pandoc-flavored product output and the Pandoc-style spec metadata), and a repo-wide canonical frontmatter validator would either fight those contracts or require fragile glob carve-outs that grow with every new document type. The ADR and Project Specification standards are adopted in the forms that do not depend on the frontmatter validator.

### Consequences

- Good, because docmend's product frontmatter schema and the Pandoc spec metadata remain the uncontested authority over their files — no second validator competes for them.
- Good, because glob-partitioning fragility (canonical vs. spec vs. product frontmatter) is avoided entirely.
- Bad, because **ADR frontmatter is not CI-validated** in this repo. ADR section enforcement is also deliberately disabled with `require_sections = false`. ADRs are authored from `docs/adr/adr.template.md` and kept consistent **by convention**.
- Bad, because other managed Markdown (docs/) likewise gets no canonical frontmatter validation. Markdown **body** linting/formatting is unaffected — the Markdown Tooling Standard (markdownlint + Prettier) is fully adopted and does cover these files.

### Confirmation

Compliance is confirmed by inspection of `.standards/config.toml`: it enables the five selected packages and carries no `[standards.markdown-frontmatter]` block. The ADR package sets `require_sections = false`. This ADR records the repository's deliberate non-adoption.

## More Information

- Adopted standards and their wiring: [`.standards/config.toml`](../../.standards/config.toml).
- Current package guidance: the [ADR 1.3 adoption guide](https://github.com/L3DigitalNet/project-standards/blob/v5.11.0/standards/adr/versions/1.3/adopt.md) and [Project Specification 1.5 adoption guide](https://github.com/L3DigitalNet/project-standards/blob/v5.11.0/standards/project-spec/versions/1.5/adopt.md).
- Revisit this decision if docmend's product frontmatter and the canonical schema converge, or if a per-directory frontmatter-schema selection mechanism is added to the standard.
