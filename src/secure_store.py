from __future__ import annotations

import json
import os
from pathlib import Path

from cryptography.fernet import Fernet


class SecureStore:
    def __init__(self, data_dir: str | None = None) -> None:
        self.data_dir = Path(data_dir or os.getenv("AGENT_DATA_DIR", ".agent_data"))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.key_file = self.data_dir / "master.key"
        self.db_file = self.data_dir / "secrets.enc"
        self._fernet = Fernet(self._load_or_create_key())

    def _load_or_create_key(self) -> bytes:
        if self.key_file.exists():
            return self.key_file.read_bytes()
        key = Fernet.generate_key()
        self.key_file.write_bytes(key)
        return key

    def _load(self) -> dict[str, str]:
        if not self.db_file.exists():
            return {}
        encrypted = self.db_file.read_bytes()
        raw = self._fernet.decrypt(encrypted)
        return json.loads(raw.decode("utf-8"))

    def _save(self, payload: dict[str, str]) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        encrypted = self._fernet.encrypt(raw)
        self.db_file.write_bytes(encrypted)

    def set_secret(self, key: str, value: str) -> None:
        payload = self._load()
        payload[key] = value
        self._save(payload)

    def get_secret(self, key: str) -> str | None:
        return self._load().get(key)

    def list_keys(self) -> list[str]:
        return sorted(self._load().keys())
