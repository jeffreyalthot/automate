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


class ParserWorkspaceCatalogTests(unittest.TestCase):
    def test_workspace_catalog_default(self) -> None:
        parsed = parse_command("workspace:catalog")
        self.assertEqual(parsed.name, "workspace_catalog")
        self.assertEqual(parsed.args, ("3",))

    def test_workspace_catalog_custom_depth(self) -> None:
        parsed = parse_command("workspace:catalog:6")
        self.assertEqual(parsed.name, "workspace_catalog")
        self.assertEqual(parsed.args, ("6",))


class ParserWorkspaceInsightsTests(unittest.TestCase):
    def test_workspace_insights_default(self) -> None:
        parsed = parse_command("workspace:insights")
        self.assertEqual(parsed.name, "workspace_insights")
        self.assertEqual(parsed.args, ("3",))

    def test_workspace_insights_custom_depth(self) -> None:
        parsed = parse_command("workspace:insights:7")
        self.assertEqual(parsed.name, "workspace_insights")
        self.assertEqual(parsed.args, ("7",))


if __name__ == "__main__":
    unittest.main()
