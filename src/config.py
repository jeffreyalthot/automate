from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeConfig:
    """Configuration runtime du CLI local."""

    max_command_length: int = int(os.getenv("AGENT_MAX_COMMAND_LENGTH", "8000"))
    max_file_write_chars: int = int(os.getenv("AGENT_MAX_FILE_WRITE_CHARS", "50000"))
    workspace_root: str = os.getenv("AGENT_WORKSPACE_ROOT", ".")


DEFAULT_RUNTIME_CONFIG = RuntimeConfig()
