import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.services.workspace.inspector import WorkspaceInspector


class WorkspaceInspectorTests(unittest.TestCase):
    def test_workspace_tree_allows_deeper_views(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            nested = root / "a" / "b" / "c" / "d" / "e" / "f" / "g"
            nested.mkdir(parents=True)
            (nested / "target.txt").write_text("ok", encoding="utf-8")

            result = WorkspaceInspector(root).tree(depth=20)

            self.assertTrue(result.ok)
            self.assertIn("target.txt", result.output)


if __name__ == "__main__":
    unittest.main()
