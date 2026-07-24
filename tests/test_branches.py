import unittest

from services.branches import get_branch_display, get_branch_info, load_branches


class BranchesServiceTests(unittest.TestCase):
    def test_load_branches_reads_json_data(self) -> None:
        data = load_branches()
        self.assertIn("aktobe", data)
        self.assertIn("aktobe_ecash", data["aktobe"]["branches"])

    def test_get_branch_info_returns_branch_details(self) -> None:
        branch = get_branch_info("aktobe_ecash")
        self.assertIsNotNone(branch)
        self.assertEqual(branch["name"], "Актобе Ecash")
        self.assertIn("Алии Молдагуловой", branch["address"])

    def test_get_branch_display_uses_human_readable_label(self) -> None:
        self.assertEqual(get_branch_display("aktobe_ecash"), "Актобе · Актобе Ecash")


if __name__ == "__main__":
    unittest.main()
