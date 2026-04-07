import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.services.workspace.insights import WorkspaceInsights


class WorkspaceInsightsTests(unittest.TestCase):
    def test_workspace_insights_build(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src").mkdir()
            (root / "src" / "main.py").write_text("print('ok')", encoding="utf-8")
            (root / "src" / "api.py").write_text("x = 1", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "guide.md").write_text("hello", encoding="utf-8")

            result = WorkspaceInsights(root).build(depth=4)

            self.assertTrue(result.ok)
            payload = json.loads(result.output)
            self.assertEqual(payload["files"], 3)
            self.assertEqual(payload["dominant_extension"], ".py")
            self.assertEqual(payload["dominant_folder"], "src")


if __name__ == "__main__":
    unittest.main()
