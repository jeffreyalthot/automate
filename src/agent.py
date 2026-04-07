from __future__ import annotations

from dataclasses import dataclass, field

from src.commands import parse_command
from src.config import DEFAULT_RUNTIME_CONFIG, RuntimeConfig
from src.model_loader import ModelConfig, generate, load_model
from src.secure_store import SecureStore
from src.toolkit import Toolkit


HELP_TEXT = """Commandes disponibles:
- help
- web:<url>
- search:<requête>
- secret:set:<clé>:<valeur>
- secret:get:<clé>
- secret:list
- file:read:<chemin>
- file:write:<chemin>:<contenu>
- Toute autre entrée est envoyée au modèle local.
"""


@dataclass
class Agent:
    toolkit: Toolkit
    store: SecureStore
    runtime_config: RuntimeConfig = field(default_factory=lambda: DEFAULT_RUNTIME_CONFIG)
    _llm: object | None = field(default=None, init=False, repr=False)

    @classmethod
    def create(cls) -> "Agent":
        return cls(toolkit=Toolkit(), store=SecureStore())

    def _get_llm(self) -> object:
        if self._llm is None:
            self._llm = load_model(ModelConfig())
        return self._llm

    def run(self, command: str) -> str:
        if len(command) > self.runtime_config.max_command_length:
            return "Commande trop longue."

        parsed = parse_command(command)

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
