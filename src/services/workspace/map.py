from __future__ import annotations

import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from src.models import ToolResult


@dataclass
class WorkspaceMap:
    """Produit une cartographie exploitable de l'arborescence du projet."""

    root: Path

    def build(self, depth: int = 3, max_entries: int = 2000) -> ToolResult:
        safe_depth = max(1, min(depth, 8))
        safe_max_entries = max(200, min(max_entries, 5000))

        scanned_entries = 0
        truncated = False

        nodes_by_depth: defaultdict[int, dict[str, int]] = defaultdict(
            lambda: {"directories": 0, "files": 0}
        )
        file_count_by_extension: Counter[str] = Counter()
        size_by_extension: Counter[str] = Counter()
        leaf_directories: set[str] = set()

        try:
            for entry in _iter_entries(self.root, max_depth=safe_depth):
                scanned_entries += 1
                if scanned_entries > safe_max_entries:
                    truncated = True
                    break

                relative = entry.relative_to(self.root)
                depth_index = len(relative.parts)

                if entry.is_dir():
                    nodes_by_depth[depth_index]["directories"] += 1
                    leaf_directories.add(str(relative))
                    continue

                if entry.is_file():
                    nodes_by_depth[depth_index]["files"] += 1
                    extension = entry.suffix.lower() or "<none>"
                    size_bytes = entry.stat().st_size
                    file_count_by_extension[extension] += 1
                    size_by_extension[extension] += size_bytes

                    parent_relative = str(entry.parent.relative_to(self.root))
                    leaf_directories.discard(parent_relative)

            level_breakdown = [
                {
                    "depth": depth,
                    "directories": values["directories"],
                    "files": values["files"],
                }
                for depth, values in sorted(nodes_by_depth.items(), key=lambda item: item[0])
            ]

            extension_matrix = [
                {
                    "extension": ext,
                    "files": file_count_by_extension[ext],
                    "size_bytes": size_by_extension[ext],
                }
                for ext, _ in file_count_by_extension.most_common(12)
            ]

            payload = {
                "root": str(self.root),
                "depth": safe_depth,
                "scanned_entries": scanned_entries,
                "truncated": truncated,
                "levels": level_breakdown,
                "extension_matrix": extension_matrix,
                "leaf_directories": sorted([leaf for leaf in leaf_directories if leaf != "."])[:20],
            }
            return ToolResult(ok=True, output=json.dumps(payload, ensure_ascii=False, indent=2))
        except Exception as exc:
            return ToolResult(ok=False, output=f"Erreur map workspace: {exc}")


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
