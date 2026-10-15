#!/usr/bin/env python3

import re
import sys
from pathlib import Path

TABLE_HEADER_RE = re.compile(
    r"^\s*\|\s*Original file line number\s*\|.*$",
    re.MULTILINE,
)

TABLE_ROW_RE = re.compile(
    r"^\s*\|(?P<cells>.*?)\|\s*$",
    re.MULTILINE,
)

CODE_CELL_RE = re.compile(
    r"`(?P<content>[^`]+)`"
)


def extract_workflow(diff: str) -> str:
    header = TABLE_HEADER_RE.search(diff)
    if not header:
        raise ValueError("No se ha encontrado la tabla del diff.")

    workflow_lines = []

    for row in TABLE_ROW_RE.finditer(diff[header.end():]):
        code_cells = CODE_CELL_RE.findall(row.group("cells"))
        if code_cells:
            workflow_lines.append(code_cells[-1])

    if not workflow_lines:
        raise ValueError("No se ha encontrado código en la tabla.")

    return "\n".join(workflow_lines) + "\n"


def main() -> None:
    diff = sys.stdin.read()
    workflow = extract_workflow(diff)

    output = Path(".github/workflows/jekyll-gh-pages.yml")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(workflow, encoding="utf-8")

    print(f"Workflow extraído en {output}")


if __name__ == "__main__":
    main()
