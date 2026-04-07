import unittest

from src.commands import parse_command


class ParserWorkspaceSummaryTests(unittest.TestCase):
    def test_workspace_summary_default(self) -> None:
        parsed = parse_command("workspace:summary")
        self.assertEqual(parsed.name, "workspace_summary")
        self.assertEqual(parsed.args, ("3",))

    def test_workspace_summary_custom_depth(self) -> None:
        parsed = parse_command("workspace:summary:5")
        self.assertEqual(parsed.name, "workspace_summary")
        self.assertEqual(parsed.args, ("5",))


if __name__ == "__main__":
    unittest.main()
