from __future__ import annotations

import json
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from src.security import PathGuard


@dataclass
class ToolResult:
    ok: bool
    output: str


class Toolkit:
    def __init__(self, path_guard: PathGuard) -> None:
        self.path_guard = path_guard

    def fetch_webpage_text(self, url: str, timeout: int = 20) -> ToolResult:
        try:
            r = requests.get(url, timeout=timeout)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            text = " ".join(soup.get_text(separator=" ").split())
            return ToolResult(True, text[:5000])
        except Exception as exc:
            return ToolResult(False, f"Erreur web: {exc}")

    def web_search(self, query: str, timeout: int = 20) -> ToolResult:
        try:
            endpoint = "https://duckduckgo.com/html/"
            r = requests.get(endpoint, params={"q": query}, timeout=timeout)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            results = []
            for a in soup.select("a.result__a")[:5]:
                results.append({"title": a.get_text(strip=True), "url": a.get("href", "")})
            return ToolResult(True, json.dumps(results, ensure_ascii=False, indent=2))
        except Exception as exc:
            return ToolResult(False, f"Erreur search: {exc}")

    def fill_form(self, url: str, fields: dict[str, str], submit_selector: str | None = None) -> ToolResult:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=30000)

                for selector, value in fields.items():
                    page.fill(selector, value)

                if submit_selector:
                    page.click(submit_selector)
                    page.wait_for_timeout(1000)

                final_url = page.url
                browser.close()
                return ToolResult(True, f"Formulaire rempli. URL finale: {final_url}")
        except Exception as exc:
            return ToolResult(False, f"Erreur formulaire: {exc}")

    def write_file(self, path: str, content: str) -> ToolResult:
        try:
            target = self.path_guard.resolve(path)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            return ToolResult(True, f"Fichier écrit: {target}")
        except Exception as exc:
            return ToolResult(False, f"Erreur écriture: {exc}")

    def read_file(self, path: str) -> ToolResult:
        try:
            target = self.path_guard.resolve(path)
            content = target.read_text(encoding="utf-8")
            return ToolResult(True, content)
        except Exception as exc:
            return ToolResult(False, f"Erreur lecture: {exc}")
