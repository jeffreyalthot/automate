import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.services.workspace.python_overview import WorkspacePythonOverview


class WorkspacePythonOverviewTests(unittest.TestCase):
    def test_workspace_python_overview_build(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src").mkdir()
            (root / "src" / "main.py").write_text(
                "import os\n\nclass Worker:\n    pass\n\ndef run():\n    return os.getcwd()\n",
                encoding="utf-8",
            )
            (root / "src" / "helper.py").write_text("def util():\n    return 1\n", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "guide.md").write_text("hello", encoding="utf-8")

            result = WorkspacePythonOverview(root).build(depth=4)

            self.assertTrue(result.ok)
            payload = json.loads(result.output)
            self.assertEqual(payload["python_files"], 2)
            self.assertEqual(payload["total_classes"], 1)
            self.assertEqual(payload["total_functions"], 2)
            self.assertEqual(payload["total_imports"], 1)
            self.assertTrue(any(item["path"] == "src/main.py" for item in payload["top_python_files"]))


if __name__ == "__main__":
    unittest.main()
