from __future__ import annotations

from pathlib import Path


class PathGuard:
    """Valide les chemins pour éviter les écritures/lectures hors périmètre."""

    def __init__(self, base_dir: str) -> None:
        self.base_dir = Path(base_dir).expanduser().resolve()

    def resolve(self, target_path: str) -> Path:
        target = Path(target_path).expanduser()
        if not target.is_absolute():
            target = self.base_dir / target

        resolved = target.resolve()
        if self.base_dir not in resolved.parents and resolved != self.base_dir:
            raise ValueError(f"Chemin interdit en dehors du workspace: {target_path}")

        return resolved
