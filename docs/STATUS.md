# Project Status

## Current snapshot

- docmend v2.0.2 is released with the complete scan, plan, apply, restore, resume, and verify pipeline; 2.0.2 is a maintenance release (Project Standards v5.3.1 tooling migration plus the 2026-07-21 simplification refactors) on top of 2.0.1's 2026-07-19 comprehensive-review remediation (26 findings, none Critical/High — `docs/fable-review/2026-07-19-docmend-review.md`).
- SPEC-VHHB revision 0.45 and ADRs 0001-0024 govern landed post-v1 changes.
- ADR-0024 establishes a neutral Go tooling lane alongside Python; it does not authorize a migration or language preference.
- ADR-0023 supersedes ADR-0001 and adopts Markdown Frontmatter validation for ADR metadata only.
- Product-output and Project Spec frontmatter remain under their independent schemas.
- The current `dev` baseline is 1,728 passing tests with no skips on a non-root runner (four permission-bit tests skip only when run as root), 89% branch coverage, and no known dependency vulnerabilities.
- Review at `834f075` covered all 40 `src/` Python files: 8 actionable, 7 retained, and 3 manual. All 8 actionable findings (S-001..S-008) were applied and shipped in v2.0.2. Reports: `docs/reviews/`.
- The repository workflow is `dev` to pull request to protected `main`; releases are signed `vX.Y.Z` tags with sdist and wheel artifacts. The v2.0.0 safety-core release ships all four remediation plans.
- Safety-core Plans A-D are implemented: output/backup ownership and artifact guards (DMR-01/02); manifest/report 2.0 lineage, journaled recovery, and shared lifecycle adjudication (DMR-03/04); descriptor-bound commit authority and action-time overwrite preservation (DMR-06/07); and plan-aware verification with complete false-clean findings, guarded verify reports, and same-root read locking (DMR-05).
- Plan D was implemented as eight green commits (`39784b0..f906e9e`) after three audit rounds approved the [plan](superpowers/plans/2026-07-11-safety-core-d-verify-redesign.md), then fast-forward merged into `dev` and pushed to `origin/dev`. `verify --plan` now certifies repeatable attempt lineage and exactly-once outcomes; restore evidence is lifecycle-only and never requires an apply report.
- NFR-001 is Complete. Accepted [million-file evidence](scale-evidence/accepted/ae3a28677390da7c823846c32af2c84b746ae861-release-1000000.json) for clean candidate `ae3a286` records 1,000,000 scanned, 875,000 applied, and the exact 25,000 expected/observed findings; all four artifacts validated, child swap stayed zero, the maximum stage RSS was 20,825,497,600 bytes, and the 25,902,581,760-byte absolute, 25,804-byte/file slope, 20% linearity, reference, and 43,200-second runtime limits passed. The workflow completed in 25,629.225 seconds. Evidence SHA-256: `c5253a874159e938768d0d7cd42e8742cc8464b0044888997cf61bfca13fb7e6`.
- The owner's staged real-library write rollout is the next project task under the spec section 18.4 safeguards.
- Project Standards is current at v5.14.0 with ADR 1.3, Agent Handoff 1.8, and CLI Documentation 1.5.
- The remaining packages are Markdown Frontmatter 1.8, Markdown Tooling 1.12, Project Specification 1.6, and Python Tooling 1.10.
- The V5 control plane preserves dual Claude/Codex automatic handoff and consumer-owned project knowledge.
- Agent Handoff 1.8 restores automatic startup with the `uv-strict-python` shim through its bounded launcher ([project-standards#80][ps-80]).
- Codex and Claude Code both emit one bounded SessionStart context through the managed launcher.

[ps-80]: https://github.com/L3DigitalNet/project-standards/issues/80
