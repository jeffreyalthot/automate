from __future__ import annotations

from dataclasses import dataclass

from src.commands import ParsedCommand
from src.config import RuntimeConfig
from src.model_loader import ModelConfig, generate, load_model
from src.secure_store import SecureStore
from src.toolkit import Toolkit


HELP_TEXT = """Commandes disponibles:
- help
- web:<url>
- search:<requête>
- form:fill:<url>:<selecteur>=<valeur>,<selecteur>=<valeur>
- secret:set:<clé>:<valeur>
- secret:get:<clé>
- secret:list
- file:read:<chemin_relatif>
- file:write:<chemin_relatif>:<contenu>
- Toute autre entrée est envoyée au modèle local.
"""


@dataclass
class CommandExecutor:
    toolkit: Toolkit
    store: SecureStore
    runtime_config: RuntimeConfig
    _llm: object | None = None

    def _get_llm(self) -> object:
        if self._llm is None:
            self._llm = load_model(ModelConfig())
        return self._llm

    def execute(self, parsed: ParsedCommand) -> str:
        if parsed.name == "empty":
            return "Commande vide."

        if parsed.name == "help":
            return HELP_TEXT

        if parsed.name == "invalid":
            return parsed.args[0]

        if parsed.name == "web":
            return self.toolkit.fetch_webpage_text(parsed.args[0]).output

        if parsed.name == "search":
            return self.toolkit.web_search(parsed.args[0]).output

        if parsed.name == "form_fill":
            url, serialized_fields = parsed.args
            fields = self._parse_form_fields(serialized_fields)
            if isinstance(fields, str):
                return fields
            return self.toolkit.fill_form(url=url, fields=fields).output

        if parsed.name == "secret_set":
            key, value = parsed.args
            self.store.set_secret(key, value)
            return f"Secret enregistré: {key}"

        if parsed.name == "secret_get":
            key = parsed.args[0]
            value = self.store.get_secret(key)
            return f"{key}={value}" if value is not None else "Secret introuvable"

        if parsed.name == "secret_list":
            return ", ".join(self.store.list_keys()) or "Aucun secret"

        if parsed.name == "file_read":
            return self.toolkit.read_file(parsed.args[0]).output

        if parsed.name == "file_write":
            path, content = parsed.args
            if len(content) > self.runtime_config.max_file_write_chars:
                return "Contenu trop volumineux pour file:write."
            return self.toolkit.write_file(path, content).output

        llm_prompt = parsed.args[0]
        return generate(self._get_llm(), llm_prompt)

    @staticmethod
    def _parse_form_fields(serialized: str) -> dict[str, str] | str:
        fields: dict[str, str] = {}
        for entry in [chunk.strip() for chunk in serialized.split(",") if chunk.strip()]:
            if "=" not in entry:
                return "Format invalide. Utilisez: selector=valeur,selector=valeur"
            selector, value = entry.split("=", 1)
            selector = selector.strip()
            if not selector:
                return "Format invalide: selecteur vide."
            fields[selector] = value.strip()

        if not fields:
            return "Aucun champ de formulaire fourni."

        return fields
