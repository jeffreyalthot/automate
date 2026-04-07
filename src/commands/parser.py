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

    if command.startswith("form:fill:"):
        parts = command.split(":", 3)
        if len(parts) != 4:
            return ParsedCommand(
                name="invalid",
                args=("Format attendu: form:fill:<url>:<selecteur>=<valeur>,...",),
            )
        _, _, url, fields = parts
        return ParsedCommand(name="form_fill", args=(url, fields))

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

    return ParsedCommand(name="llm", args=(command,))
