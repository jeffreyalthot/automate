from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from src.models import ToolResult


@dataclass
class WorkspaceSummary:
    root: Path

    def build(self, depth: int = 3, max_entries: int = 500) -> ToolResult:
        """Construit un résumé JSON de l'espace de travail."""
        safe_depth = max(1, min(depth, 12))
        safe_max_entries = max(50, min(max_entries, 2000))

        counters = Counter()
        extension_counter: Counter[str] = Counter()
        largest_files: list[tuple[int, str]] = []

        try:
            for entry in _iter_entries(self.root, max_depth=safe_depth):
                counters["entries"] += 1
                if counters["entries"] > safe_max_entries:
                    counters["truncated"] = 1
                    break

                if entry.is_dir():
                    counters["directories"] += 1
                    continue

                if entry.is_file():
                    counters["files"] += 1
                    ext = entry.suffix.lower() or "<none>"
                    extension_counter[ext] += 1

                    size = entry.stat().st_size
                    rel_path = str(entry.relative_to(self.root))
                    largest_files.append((size, rel_path))

            top_extensions = [
                {"extension": ext, "count": count}
                for ext, count in extension_counter.most_common(8)
            ]
            top_largest = [
                {"path": path, "size_bytes": size}
                for size, path in sorted(largest_files, reverse=True)[:5]
            ]

            payload = {
                "root": str(self.root),
                "depth": safe_depth,
                "total_entries": counters["entries"],
                "directories": counters["directories"],
                "files": counters["files"],
                "truncated": bool(counters["truncated"]),
                "top_extensions": top_extensions,
                "largest_files": top_largest,
            }
            return ToolResult(ok=True, output=json.dumps(payload, ensure_ascii=False, indent=2))
        except Exception as exc:
            return ToolResult(ok=False, output=f"Erreur résumé workspace: {exc}")


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
