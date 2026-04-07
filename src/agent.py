from __future__ import annotations

from dataclasses import dataclass

from src.model_loader import ModelConfig, generate, load_model
from src.secure_store import SecureStore
from src.toolkit import Toolkit


@dataclass
class Agent:
    toolkit: Toolkit
    store: SecureStore

    @classmethod
    def create(cls) -> "Agent":
        return cls(toolkit=Toolkit(), store=SecureStore())

    def run(self, command: str) -> str:
        if command.startswith("web:"):
            return self.toolkit.fetch_webpage_text(command.replace("web:", "", 1)).output

        if command.startswith("search:"):
            return self.toolkit.web_search(command.replace("search:", "", 1)).output

        if command.startswith("secret:set:"):
            _, _, key, value = command.split(":", 3)
            self.store.set_secret(key, value)
            return f"Secret enregistré: {key}"

        if command.startswith("secret:get:"):
            key = command.replace("secret:get:", "", 1)
            value = self.store.get_secret(key)
            return f"{key}={value}" if value is not None else "Secret introuvable"

        if command.strip() == "secret:list":
            return ", ".join(self.store.list_keys()) or "Aucun secret"

        llm = load_model(ModelConfig())
        return generate(llm, command)
