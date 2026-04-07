from __future__ import annotations

import ast
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from src.models import ToolResult


@dataclass
class WorkspacePythonOverview:
    """Analyse ciblée des fichiers Python du workspace."""

    root: Path

    def build(self, depth: int = 3, max_files: int = 400) -> ToolResult:
        safe_depth = max(1, min(depth, 12))
        safe_max_files = max(20, min(max_files, 2000))

        files_scanned = 0
        total_functions = 0
        total_classes = 0
        total_imports = 0
        syntax_errors = 0
        truncated = False

        folders_counter: Counter[str] = Counter()
        complexity_by_file: list[dict[str, int | str]] = []

        try:
            for entry in _iter_entries(self.root, max_depth=safe_depth):
                if not entry.is_file() or entry.suffix.lower() != ".py":
                    continue

                files_scanned += 1
                if files_scanned > safe_max_files:
                    truncated = True
                    break

                rel_path = str(entry.relative_to(self.root))
                folder = entry.parent.relative_to(self.root)
                top_folder = folder.parts[0] if folder.parts else "."
                folders_counter[top_folder] += 1

                source = entry.read_text(encoding="utf-8")
                try:
                    node = ast.parse(source)
                except SyntaxError:
                    syntax_errors += 1
                    continue

                metrics = _extract_metrics(node)
                total_functions += metrics["functions"]
                total_classes += metrics["classes"]
                total_imports += metrics["imports"]

                complexity_by_file.append(
                    {
                        "path": rel_path,
                        "functions": metrics["functions"],
                        "classes": metrics["classes"],
                        "imports": metrics["imports"],
                    }
                )

            payload = {
                "root": str(self.root),
                "depth": safe_depth,
                "files_scanned": files_scanned,
                "truncated": truncated,
                "python_files": files_scanned,
                "total_functions": total_functions,
                "total_classes": total_classes,
                "total_imports": total_imports,
                "syntax_errors": syntax_errors,
                "top_python_folders": [
                    {"folder": folder, "files": count}
                    for folder, count in folders_counter.most_common(8)
                ],
                "top_python_files": sorted(
                    complexity_by_file,
                    key=lambda item: (
                        -int(item["functions"]) - int(item["classes"]),
                        str(item["path"]),
                    ),
                )[:10],
            }
            return ToolResult(ok=True, output=json.dumps(payload, ensure_ascii=False, indent=2))
        except Exception as exc:
            return ToolResult(ok=False, output=f"Erreur analyse Python workspace: {exc}")


def _extract_metrics(node: ast.AST) -> dict[str, int]:
    functions = 0
    classes = 0
    imports = 0

    for child in ast.walk(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions += 1
        elif isinstance(child, ast.ClassDef):
            classes += 1
        elif isinstance(child, (ast.Import, ast.ImportFrom)):
            imports += 1

    return {"functions": functions, "classes": classes, "imports": imports}


def _iter_entries(root: Path, max_depth: int) -> list[Path]:
    entries: list[Path] = []

    def walk(path: Path, depth: int) -> None:
        if depth > max_depth:
            return

        children = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        for child in children:
            entries.append(child)
            if child.is_dir():
                walk(child, depth + 1)

    walk(root, 1)
    return entries
