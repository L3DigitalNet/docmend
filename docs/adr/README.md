# Architecture Decision Records

This directory holds docmend's Architecture Decision Records (ADRs): short documents that each capture a single architecturally-significant decision — its context, the options weighed, the choice made, and the consequences.

## Contents

- **[index.md](index.md)** — the full ADR index (status table with links to every record).
- **[adr-backlog.md](adr-backlog.md)** — the prioritized backlog of ADR _candidates_ (decisions worth recording that are not yet written up), with per-candidate scoring and an explicit list of what was deliberately skipped.
- **[adr.template.md](adr.template.md)** — the MADR-shaped template new ADRs are authored from.

## Conventions

- **Format:** [MADR](https://adr.github.io/madr/) (Markdown Any Decision Records) — one decision per file.
- **Filenames:** `adr-NNNN-short-title.md`; the `id` frontmatter embeds the repo name (`adr-NNNN-docmend-short-title`). Numbering is sequential and never reused.
- **Status lifecycle:** frontmatter uses `draft` → `active` → (eventually) `superseded`; `active` is the package's canonical mapping for MADR's accepted state. A superseded ADR stays in place with `superseded_by` set — ADRs are immutable historical records, not living documents; a changed decision gets a new ADR that supersedes the old one.
- **Validation:** ADR frontmatter is validated by the narrowly scoped Markdown Frontmatter package (see [ADR-0023](adr-0023-adopt-markdown-frontmatter-for-adrs.md)); the create-only template is excluded. Markdown body linting (markdownlint + Prettier) also applies.

## Relationship to the decision backlog

Settled decisions are first recorded as resolved questions (`RQ-###`) in [`../resolved-questions.md`](../resolved-questions.md). The architecturally-significant ones graduate into ADRs here; the [backlog](adr-backlog.md) tracks which resolved questions and spec design-decisions (`D-###`) are ADR candidates and at what priority. Once an ADR is the canonical record for a decision, that decision's `RQ-###` entry may be condensed to an ADR pointer.
