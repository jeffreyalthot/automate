import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.services.workspace.map import WorkspaceMap


class WorkspaceMapTests(unittest.TestCase):
    def test_workspace_map_build(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src").mkdir()
            (root / "src" / "main.py").write_text("print('ok')", encoding="utf-8")
            (root / "src" / "pkg").mkdir()
            (root / "src" / "pkg" / "module.py").write_text("x = 1", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "guide.md").write_text("hello", encoding="utf-8")

            result = WorkspaceMap(root).build(depth=5)

            self.assertTrue(result.ok)
            payload = json.loads(result.output)
            self.assertGreaterEqual(payload["scanned_entries"], 6)
            self.assertTrue(any(item["extension"] == ".py" for item in payload["extension_matrix"]))
            self.assertTrue(any(level["depth"] == 2 for level in payload["levels"]))


if __name__ == "__main__":
    unittest.main()
