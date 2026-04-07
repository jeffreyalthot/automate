from __future__ import annotations

from pathlib import Path


def format_tree(root: Path, depth: int = 2, max_entries: int = 200) -> str:
    """Retourne une vue arborescente simple d'un répertoire."""
    if depth < 1:
        return "."

    lines = [root.name or "."]
    emitted = 0

    def walk(directory: Path, prefix: str, level: int) -> None:
        nonlocal emitted
        if emitted >= max_entries or level >= depth:
            return

        children = sorted(directory.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        for index, child in enumerate(children):
            if emitted >= max_entries:
                break
            connector = "└── " if index == len(children) - 1 else "├── "
            lines.append(f"{prefix}{connector}{child.name}")
            emitted += 1
            if child.is_dir():
                extension = "    " if index == len(children) - 1 else "│   "
                walk(child, prefix + extension, level + 1)

    walk(root, "", 0)

    if emitted >= max_entries:
        lines.append("… (sortie tronquée)")

    return "\n".join(lines)
