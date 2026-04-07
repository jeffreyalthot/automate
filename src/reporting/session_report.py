from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class SessionReportEntry:
    command: str
    success: bool
    output_preview: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class SessionReport:
    entries: list[SessionReportEntry] = field(default_factory=list)

    def add_entry(self, command: str, output: str, success: bool) -> None:
        preview = output.strip().replace("\n", " ")
        self.entries.append(
            SessionReportEntry(
                command=command,
                success=success,
                output_preview=preview[:180] if preview else "(vide)",
            )
        )

    def to_markdown(self) -> str:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        lines = [
            "# Rapport de session automate",
            "",
            f"Généré le: {now}",
            "",
            "| # | Date (UTC) | Commande | Statut | Aperçu |",
            "|---|------------|----------|--------|--------|",
        ]

        if not self.entries:
            lines.append("| 1 | - | - | - | Aucune action enregistrée |")
            return "\n".join(lines)

        for i, entry in enumerate(self.entries, start=1):
            status = "OK" if entry.success else "ERREUR"
            created_at = entry.created_at.strftime("%Y-%m-%d %H:%M:%S")
            command = entry.command.replace("|", "\\|")
            preview = entry.output_preview.replace("|", "\\|")
            lines.append(f"| {i} | {created_at} | `{command}` | {status} | {preview} |")

        return "\n".join(lines)
