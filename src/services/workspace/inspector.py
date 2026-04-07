from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.models import ToolResult
from src.utils import format_tree


@dataclass
class WorkspaceInspector:
    root: Path

    def tree(self, depth: int = 3) -> ToolResult:
        try:
            safe_depth = max(1, min(depth, 12))
            output = format_tree(self.root, depth=safe_depth)
            return ToolResult(ok=True, output=output)
        except Exception as exc:
            return ToolResult(ok=False, output=f"Erreur arborescence: {exc}")
