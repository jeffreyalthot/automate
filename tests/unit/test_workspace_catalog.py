import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.services.workspace.catalog import WorkspaceCatalog


class WorkspaceCatalogTests(unittest.TestCase):
    def test_workspace_catalog_build(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src").mkdir()
            (root / "src" / "main.py").write_text("print('ok')", encoding="utf-8")
            (root / "src" / "util.py").write_text("x = 1", encoding="utf-8")
            (root / "README.md").write_text("desc", encoding="utf-8")

            result = WorkspaceCatalog(root).build(depth=4)

            self.assertTrue(result.ok)
            payload = json.loads(result.output)
            self.assertEqual(payload["total_files"], 3)
            self.assertTrue(any(item["extension"] == ".py" for item in payload["top_extensions"]))
            self.assertTrue(any(item["path"] == "src" for item in payload["top_directories"]))


if __name__ == "__main__":
    unittest.main()
