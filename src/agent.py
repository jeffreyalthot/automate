from __future__ import annotations

from dataclasses import dataclass, field

from src.commands import parse_command
from src.config import DEFAULT_RUNTIME_CONFIG, RuntimeConfig
from src.secure_store import SecureStore
from src.security import PathGuard
from src.services import CommandExecutor
from src.toolkit import Toolkit


@dataclass
class Agent:
    toolkit: Toolkit
    store: SecureStore
    runtime_config: RuntimeConfig = field(default_factory=lambda: DEFAULT_RUNTIME_CONFIG)
    executor: CommandExecutor = field(init=False)

    def __post_init__(self) -> None:
        self.executor = CommandExecutor(
            toolkit=self.toolkit,
            store=self.store,
            runtime_config=self.runtime_config,
        )

    @classmethod
    def create(cls) -> "Agent":
        runtime_config = DEFAULT_RUNTIME_CONFIG
        path_guard = PathGuard(runtime_config.workspace_root)
        return cls(toolkit=Toolkit(path_guard=path_guard), store=SecureStore(), runtime_config=runtime_config)

    def run(self, command: str) -> str:
        if len(command) > self.runtime_config.max_command_length:
            return "Commande trop longue."

        parsed = parse_command(command)
        return self.executor.execute(parsed)
