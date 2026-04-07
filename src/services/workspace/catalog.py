from __future__ import annotations

import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from src.models import ToolResult


@dataclass
class WorkspaceCatalog:
    root: Path

    def build(self, depth: int = 3, max_entries: int = 1200) -> ToolResult:
        safe_depth = max(1, min(depth, 12))
        safe_max_entries = max(100, min(max_entries, 3000))

        extension_counter: Counter[str] = Counter()
        directory_stats: defaultdict[str, dict[str, int]] = defaultdict(
            lambda: {"files": 0, "size_bytes": 0}
        )

        scanned_entries = 0
        truncated = False

        try:
            for entry in _iter_entries(self.root, max_depth=safe_depth):
                scanned_entries += 1
                if scanned_entries > safe_max_entries:
                    truncated = True
                    break

                if not entry.is_file():
                    continue

                relative_parent = str(entry.parent.relative_to(self.root))
                directory_key = "." if relative_parent == "." else relative_parent
                size_bytes = entry.stat().st_size

                directory_stats[directory_key]["files"] += 1
                directory_stats[directory_key]["size_bytes"] += size_bytes

                ext = entry.suffix.lower() or "<none>"
                extension_counter[ext] += 1

            directories = [
                {
                    "path": path,
                    "files": stats["files"],
                    "size_bytes": stats["size_bytes"],
                }
                for path, stats in sorted(
                    directory_stats.items(), key=lambda item: (-item[1]["size_bytes"], item[0])
                )[:12]
            ]

            payload = {
                "root": str(self.root),
                "depth": safe_depth,
                "scanned_entries": scanned_entries,
                "truncated": truncated,
                "total_files": sum(stats["files"] for stats in directory_stats.values()),
                "top_extensions": [
                    {"extension": ext, "count": count}
                    for ext, count in extension_counter.most_common(10)
                ],
                "top_directories": directories,
            }
            return ToolResult(ok=True, output=json.dumps(payload, ensure_ascii=False, indent=2))
        except Exception as exc:
            return ToolResult(ok=False, output=f"Erreur catalog workspace: {exc}")


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
