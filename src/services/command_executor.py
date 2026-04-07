from __future__ import annotations

from dataclasses import dataclass, field

from src.commands import ParsedCommand, parse_form_fields
from src.config import RuntimeConfig
from src.model_loader import ModelConfig, generate, load_model
from src.reporting import SessionReport
from src.secure_store import SecureStore
from src.toolkit import Toolkit


HELP_TEXT = """Commandes disponibles:
- help
- web:<url>
- search:<requête>
- workspace:tree[:profondeur]
- workspace:summary[:profondeur]
- workspace:catalog[:profondeur]
- form:fill:<url>:<selecteur>=<valeur>,<selecteur>=<valeur>
- form:analyze:<url>
- form:dryrun:<url>:<selecteur>=<valeur>,<selecteur>=<valeur>
- secret:set:<clé>:<valeur>
- secret:get:<clé>
- secret:list
- file:read:<chemin_relatif>
- file:write:<chemin_relatif>:<contenu>
- report:markdown
- report:write:<chemin_relatif>
- Toute autre entrée est envoyée au modèle local.
"""


@dataclass
class CommandExecutor:
    toolkit: Toolkit
    store: SecureStore
    runtime_config: RuntimeConfig
    _llm: object | None = None
    _session_report: SessionReport = field(default_factory=SessionReport)

    def _get_llm(self) -> object:
        if self._llm is None:
            self._llm = load_model(ModelConfig())
        return self._llm

    def execute(self, parsed: ParsedCommand) -> str:
        response: str
        if parsed.name == "empty":
            response = "Commande vide."
            self._track(parsed, response, success=False)
            return response

        if parsed.name == "help":
            self._track(parsed, HELP_TEXT, success=True)
            return HELP_TEXT

        if parsed.name == "invalid":
            self._track(parsed, parsed.args[0], success=False)
            return parsed.args[0]

        if parsed.name == "web":
            result = self.toolkit.fetch_webpage_text(parsed.args[0])
            self._track(parsed, result.output, success=result.ok)
            return result.output

        if parsed.name == "search":
            result = self.toolkit.web_search(parsed.args[0])
            self._track(parsed, result.output, success=result.ok)
            return result.output

        if parsed.name == "workspace_tree":
            raw_depth = parsed.args[0]
            try:
                depth = int(raw_depth)
            except ValueError:
                response = "Profondeur invalide. Utilisez un entier entre 1 et 6."
                self._track(parsed, response, success=False)
                return response
            result = self.toolkit.workspace_tree(depth=depth)
            self._track(parsed, result.output, success=result.ok)
            return result.output

        if parsed.name == "workspace_summary":
            raw_depth = parsed.args[0]
            try:
                depth = int(raw_depth)
            except ValueError:
                response = "Profondeur invalide. Utilisez un entier entre 1 et 8."
                self._track(parsed, response, success=False)
                return response
            result = self.toolkit.workspace_summary_report(depth=depth)
            self._track(parsed, result.output, success=result.ok)
            return result.output

        if parsed.name == "workspace_catalog":
            raw_depth = parsed.args[0]
            try:
                depth = int(raw_depth)
            except ValueError:
                response = "Profondeur invalide. Utilisez un entier entre 1 et 8."
                self._track(parsed, response, success=False)
                return response
            result = self.toolkit.workspace_catalog_report(depth=depth)
            self._track(parsed, result.output, success=result.ok)
            return result.output

        if parsed.name == "form_fill":
            url, serialized_fields = parsed.args
            fields = parse_form_fields(serialized_fields)
            if isinstance(fields, str):
                self._track(parsed, fields, success=False)
                return fields
            result = self.toolkit.fill_form(url=url, fields=fields)
            self._track(parsed, result.output, success=result.ok)
            return result.output

        if parsed.name == "form_analyze":
            result = self.toolkit.analyze_form(parsed.args[0])
            self._track(parsed, result.output, success=result.ok)
            return result.output

        if parsed.name == "form_dryrun":
            url, serialized_fields = parsed.args
            fields = parse_form_fields(serialized_fields)
            if isinstance(fields, str):
                self._track(parsed, fields, success=False)
                return fields
            formatted = "\n".join([f"- {selector} => {value}" for selector, value in fields.items()])
            response = f"Dry-run formulaire pour {url}\n{formatted}"
            self._track(parsed, response, success=True)
            return response

        if parsed.name == "secret_set":
            key, value = parsed.args
            self.store.set_secret(key, value)
            response = f"Secret enregistré: {key}"
            self._track(parsed, response, success=True)
            return response

        if parsed.name == "secret_get":
            key = parsed.args[0]
            value = self.store.get_secret(key)
            response = f"{key}={value}" if value is not None else "Secret introuvable"
            self._track(parsed, response, success=value is not None)
            return response

        if parsed.name == "secret_list":
            response = ", ".join(self.store.list_keys()) or "Aucun secret"
            self._track(parsed, response, success=True)
            return response

        if parsed.name == "file_read":
            result = self.toolkit.read_file(parsed.args[0])
            self._track(parsed, result.output, success=result.ok)
            return result.output

        if parsed.name == "file_write":
            path, content = parsed.args
            if len(content) > self.runtime_config.max_file_write_chars:
                response = "Contenu trop volumineux pour file:write."
                self._track(parsed, response, success=False)
                return response
            result = self.toolkit.write_file(path, content)
            self._track(parsed, result.output, success=result.ok)
            return result.output

        if parsed.name == "report_markdown":
            response = self._session_report.to_markdown()
            self._track(parsed, "Rapport markdown généré.", success=True)
            return response

        if parsed.name == "report_write":
            path = parsed.args[0]
            result = self.toolkit.write_file(path, self._session_report.to_markdown())
            self._track(parsed, result.output, success=result.ok)
            return result.output

        llm_prompt = parsed.args[0]
        response = generate(self._get_llm(), llm_prompt)
        self._track(parsed, response, success=True)
        return response

    def _track(self, parsed: ParsedCommand, output: str, success: bool) -> None:
        joined_args = ":".join(parsed.args)
        command_repr = parsed.name if not joined_args else f"{parsed.name}:{joined_args}"
        self._session_report.add_entry(command=command_repr, output=output, success=success)
