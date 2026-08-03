# /// script
# requires-python = ">=3.14"
# ///
"""CI gate: the spec's ID registries must not drift (gap-analysis GAP-53).

The spec (docs/specs/docmend.md) mints IDs in one table that a companion
table or file is required to enumerate; drift between the two is invisible
to a human skim because each table looks complete on its own. This script
cross-checks the registries mechanically:

  A. Every FR-/NFR-/IR-/DR- requirement defined in spec §7 has a row in the
     §17.3 traceability matrix, and every §17.3 row names a real §7
     requirement.
  B. Every OQ- row in spec §21 has a settled RQ- record in
     docs/resolved-questions.md or an open OQ- heading in
     docs/open-questions.md, and every settled RQ- record has a §21 row.
     (OQ-N and RQ-N share the number N by convention.)
  C. Once a §17.3 row's status leaves "Not Started", its evidence must name
     at least one existing ``tests/**/*.py`` file and one named file must
     mention the requirement ID (convention per Appendix B: a `# spec:
     FR-001` comment or the bare ID in a test name/docstring). This prevents
     a stale matrix path or an unrelated test mention from supporting a
     completion claim.

Exit codes: 0 clean · 1 drift found · 2 document layout changed under the
script (a required heading is missing — fix the script, not the spec).

Run from CI as `uv run python scripts/check_traceability.py`; an optional
argument overrides the repo root (used by the tests to point at fixtures).
"""

import ast
import re
import sys
from pathlib import Path

REQ_ROW = re.compile(r"^\| ((?:FR|NFR|IR|DR)-\d{3}) \|", re.MULTILINE)
OQ_ROW = re.compile(r"^\| (OQ-\d{3}) \|", re.MULTILINE)
RQ_ID = re.compile(r"\bRQ-(\d{3})\b")
OQ_HEADING = re.compile(r"^#{2,4} .*\b(OQ-\d{3})\b", re.MULTILINE)
TEST_FILE = re.compile(r"\b(tests/[A-Za-z0-9_./-]+\.py)\b")
TEST_SELECTOR = re.compile(
    r"\b(tests/[A-Za-z0-9_./-]+\.py)::([A-Za-z_][A-Za-z0-9_]*(?:::[A-Za-z_][A-Za-z0-9_]*)*)"
)


def section(text: str, start: str, end: str, path: Path) -> str:
    """Slice text between two unique heading strings.

    The spec's headings are unique literals, so no Markdown AST is needed;
    a missing heading means the document layout changed and this script's
    anchors must be updated with it.
    """
    try:
        lo = text.index(start)
        hi = text.index(end, lo)
    except ValueError as exc:
        print(f"layout: heading {exc.args[0]!r} not found in {path}", file=sys.stderr)
        raise SystemExit(2) from exc
    return text[lo:hi]


def trace_rows(sec: str) -> dict[str, tuple[str, str]]:
    """§17.3 rows as {requirement ID: (evidence, status)}.

    Cells are split on bare '|'; §17.3 cells never contain escaped pipes
    (unlike §7.3 contract cells).
    """
    rows: dict[str, tuple[str, str]] = {}
    for line in sec.splitlines():
        m = REQ_ROW.match(line)
        if m:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows[m.group(1)] = (cells[1], cells[-1])
    return rows


def selector_exists(path: Path, selector: str) -> bool:
    """Return whether a simple pytest node selector resolves in one test module.

    Matrix prose sometimes abbreviates parametrized selectors with braces. The
    regex therefore extracts only the explicit ``Class`` or ``Class::method``
    prefix, while bare file references remain valid evidence.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    nodes: list[ast.stmt] = tree.body
    for name in selector.split("::"):
        node = next(
            (
                candidate
                for candidate in nodes
                if isinstance(candidate, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
                and candidate.name == name
            ),
            None,
        )
        if node is None:
            return False
        nodes = node.body if isinstance(node, ast.ClassDef) else []
    return True


def main(root: Path) -> int:
    spec_path = root / "docs" / "specs" / "docmend.md"
    spec = spec_path.read_text(encoding="utf-8")
    resolved = (root / "docs" / "resolved-questions.md").read_text(encoding="utf-8")
    open_qs = (root / "docs" / "open-questions.md").read_text(encoding="utf-8")

    drifts: list[str] = []

    # --- A: §7 requirement table <-> §17.3 traceability matrix ---
    sec7 = section(spec, "## 7. Requirements", "## 8. Architecture and Design", spec_path)
    sec173 = section(
        spec, "### 17.3 Requirement-to-Test Traceability", "## 18. Deployment", spec_path
    )
    defined = set(REQ_ROW.findall(sec7))
    traced = trace_rows(sec173)
    if missing := defined - traced.keys():
        drifts.append(f"requirement IDs defined in §7 but missing from §17.3: {sorted(missing)}")
    if unknown := traced.keys() - defined:
        drifts.append(f"§17.3 rows reference IDs not defined in §7: {sorted(unknown)}")

    # --- B: spec §21 OQ registry <-> resolved/open question records ---
    sec21 = section(spec, "## 21. Open Questions and Decisions", "## Deviations Log", spec_path)
    oq_nums = {i.removeprefix("OQ-") for i in OQ_ROW.findall(sec21)}
    settled_nums = set(RQ_ID.findall(resolved))
    open_nums = {i.removeprefix("OQ-") for i in OQ_HEADING.findall(open_qs)}
    if unrecorded := oq_nums - settled_nums - open_nums:
        drifts.append(
            "spec §21 OQ rows with neither an RQ record nor an open-question heading: "
            f"{sorted('OQ-' + n for n in unrecorded)}"
        )
    if unlisted := (settled_nums | open_nums) - oq_nums:
        drifts.append(
            f"question records with no spec §21 row: {sorted('OQ-/RQ-' + n for n in unlisted)}"
        )

    # --- C: §17.3 progress claims <-> their named test evidence ---
    for rid, (evidence, status) in traced.items():
        if status == "Not Started":
            continue
        paths = sorted(set(TEST_FILE.findall(evidence)))
        if not paths:
            drifts.append(f"§17.3 {rid} claims progress but names no tests/*.py evidence")
            continue
        missing = [path for path in paths if not (root / path).is_file()]
        if missing:
            drifts.append(f"§17.3 {rid} names missing test evidence: {missing}")
            continue
        requirement_id = re.compile(rf"\b{re.escape(rid)}\b")
        if not any(
            requirement_id.search((root / path).read_text(encoding="utf-8")) for path in paths
        ):
            drifts.append(f"§17.3 {rid} evidence files do not mention the requirement ID: {paths}")
        for path, selector in TEST_SELECTOR.findall(evidence):
            if not selector_exists(root / path, selector):
                drifts.append(f"§17.3 {rid} names missing test selector: {path}::{selector}")

    for d in drifts:
        print(f"DRIFT: {d}")
    if not drifts:
        print("ok: no traceability drift detected")
    return 1 if drifts else 0


if __name__ == "__main__":
    repo_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    raise SystemExit(main(repo_root))
