from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from src.models import ToolResult


@dataclass
class WorkspaceInsights:
    root: Path

    def build(self, depth: int = 3, max_entries: int = 1500) -> ToolResult:
        safe_depth = max(1, min(depth, 12))
        safe_max_entries = max(100, min(max_entries, 4000))

        entries_seen = 0
        file_count = 0
        directory_count = 0
        total_size = 0
        truncated = False

        extension_counter: Counter[str] = Counter()
        folder_counter: Counter[str] = Counter()

        try:
            for entry in _iter_entries(self.root, max_depth=safe_depth):
                entries_seen += 1
                if entries_seen > safe_max_entries:
                    truncated = True
                    break

                if entry.is_dir():
                    directory_count += 1
                    continue

                if not entry.is_file():
                    continue

                file_count += 1
                rel_path = entry.relative_to(self.root)
                total_size += entry.stat().st_size

                extension = entry.suffix.lower() or "<none>"
                extension_counter[extension] += 1

                if rel_path.parts:
                    root_folder = rel_path.parts[0]
                    folder_counter[root_folder] += 1

            average_size = int(total_size / file_count) if file_count else 0
            dominant_extension = extension_counter.most_common(1)[0][0] if extension_counter else "<none>"
            dominant_folder = folder_counter.most_common(1)[0][0] if folder_counter else "."

            payload = {
                "root": str(self.root),
                "depth": safe_depth,
                "entries_seen": entries_seen,
                "truncated": truncated,
                "directories": directory_count,
                "files": file_count,
                "total_size_bytes": total_size,
                "average_file_size_bytes": average_size,
                "dominant_extension": dominant_extension,
                "dominant_folder": dominant_folder,
                "top_extensions": [
                    {"extension": ext, "count": count}
                    for ext, count in extension_counter.most_common(8)
                ],
                "top_folders": [
                    {"folder": folder, "files": count}
                    for folder, count in folder_counter.most_common(8)
                ],
            }
            return ToolResult(ok=True, output=json.dumps(payload, ensure_ascii=False, indent=2))
        except Exception as exc:
            return ToolResult(ok=False, output=f"Erreur insights workspace: {exc}")


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
