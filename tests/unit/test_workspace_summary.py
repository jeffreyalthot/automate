import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.services.workspace.summary import WorkspaceSummary


class WorkspaceSummaryTests(unittest.TestCase):
    def test_workspace_summary_build(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.py").write_text("print('ok')", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "note.md").write_text("hello", encoding="utf-8")

            summary = WorkspaceSummary(root).build(depth=3)

            self.assertTrue(summary.ok)
            payload = json.loads(summary.output)
            self.assertEqual(payload["files"], 2)
            self.assertGreaterEqual(payload["directories"], 1)
            self.assertTrue(any(item["extension"] == ".py" for item in payload["top_extensions"]))


if __name__ == "__main__":
    unittest.main()
