from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedCommand:
    name: str
    args: tuple[str, ...]


def parse_command(raw_command: str) -> ParsedCommand:
    command = raw_command.strip()
    if not command:
        return ParsedCommand(name="empty", args=())

    if command == "help":
        return ParsedCommand(name="help", args=())

    if command == "secret:list":
        return ParsedCommand(name="secret_list", args=())

    if command.startswith("web:"):
        return ParsedCommand(name="web", args=(command.removeprefix("web:"),))

    if command.startswith("search:"):
        return ParsedCommand(name="search", args=(command.removeprefix("search:"),))

    if command == "workspace:tree":
        return ParsedCommand(name="workspace_tree", args=("3",))

    if command.startswith("workspace:tree:"):
        return ParsedCommand(name="workspace_tree", args=(command.removeprefix("workspace:tree:"),))

    if command == "workspace:catalog":
        return ParsedCommand(name="workspace_catalog", args=("3",))

    if command.startswith("workspace:catalog:"):
        return ParsedCommand(name="workspace_catalog", args=(command.removeprefix("workspace:catalog:"),))

    if command == "workspace:summary":
        return ParsedCommand(name="workspace_summary", args=("3",))

    if command == "workspace:insights":
        return ParsedCommand(name="workspace_insights", args=("3",))

    if command.startswith("workspace:insights:"):
        return ParsedCommand(name="workspace_insights", args=(command.removeprefix("workspace:insights:"),))

    if command == "workspace:map":
        return ParsedCommand(name="workspace_map", args=("3",))

    if command.startswith("workspace:map:"):
        return ParsedCommand(name="workspace_map", args=(command.removeprefix("workspace:map:"),))

    if command.startswith("workspace:summary:"):
        return ParsedCommand(name="workspace_summary", args=(command.removeprefix("workspace:summary:"),))

    if command.startswith("form:fill:"):
        payload = command.removeprefix("form:fill:")
        url, separator, fields = payload.rpartition(":")
        if not separator or not url.strip() or not fields.strip():
            return ParsedCommand(
                name="invalid",
                args=("Format attendu: form:fill:<url>:<selecteur>=<valeur>,...",),
            )
        return ParsedCommand(name="form_fill", args=(url, fields))

    if command.startswith("form:analyze:"):
        return ParsedCommand(name="form_analyze", args=(command.removeprefix("form:analyze:"),))

    if command.startswith("form:dryrun:"):
        payload = command.removeprefix("form:dryrun:")
        url, separator, fields = payload.rpartition(":")
        if not separator or not url.strip() or not fields.strip():
            return ParsedCommand(
                name="invalid",
                args=("Format attendu: form:dryrun:<url>:<selecteur>=<valeur>,...",),
            )
        return ParsedCommand(name="form_dryrun", args=(url, fields))

    if command.startswith("secret:get:"):
        return ParsedCommand(name="secret_get", args=(command.removeprefix("secret:get:"),))

    if command.startswith("secret:set:"):
        parts = command.split(":", 3)
        if len(parts) != 4:
            return ParsedCommand(name="invalid", args=("Format attendu: secret:set:<clé>:<valeur>",))
        _, _, key, value = parts
        return ParsedCommand(name="secret_set", args=(key, value))

    if command.startswith("file:read:"):
        return ParsedCommand(name="file_read", args=(command.removeprefix("file:read:"),))

    if command.startswith("file:write:"):
        parts = command.split(":", 3)
        if len(parts) != 4:
            return ParsedCommand(name="invalid", args=("Format attendu: file:write:<chemin>:<contenu>",))
        _, _, path, content = parts
        return ParsedCommand(name="file_write", args=(path, content))

    if command == "report:markdown":
        return ParsedCommand(name="report_markdown", args=())

    if command.startswith("report:write:"):
        return ParsedCommand(name="report_write", args=(command.removeprefix("report:write:"),))

    return ParsedCommand(name="llm", args=(command,))
