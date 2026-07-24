import os
import tempfile
import unittest
from unittest.mock import patch

import database as db_module
from services.notifications import should_trigger_alert


class NotificationTests(unittest.TestCase):
    def test_above_condition_triggers_when_rate_reaches_target(self) -> None:
        self.assertTrue(should_trigger_alert(100, 100, "above"))
        self.assertTrue(should_trigger_alert(110, 100, "above"))
        self.assertFalse(should_trigger_alert(90, 100, "above"))

    def test_below_condition_triggers_when_rate_falls_to_target(self) -> None:
        self.assertTrue(should_trigger_alert(90, 100, "below"))
        self.assertTrue(should_trigger_alert(100, 100, "below"))
        self.assertFalse(should_trigger_alert(110, 100, "below"))

    async def _test_list_active_rate_alerts_returns_active_records(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_db_path = os.path.join(temp_dir, "test.db")
            with patch.object(db_module, "DB_PATH", temp_db_path):
                await db_module.init_db()
                await db_module.add_rate_alert(7, "branch-1", "USD", "buy", "above", "400",)
                await db_module.add_rate_alert(8, "branch-2", "EUR", "sell", "below", "500")
                alerts = await db_module.list_active_rate_alerts()
                self.assertEqual(len(alerts), 2)
                self.assertTrue(all(alert["is_active"] for alert in alerts))


if __name__ == "__main__":
    unittest.main()
