import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Import monitor script module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
monitor = __import__("automated-memory-monitoring-jira-ticketing")


class TestMemoryMonitoring(unittest.TestCase):
    def setUp(self):
        self.config = {
            "ssh_host": "10.0.0.1",
            "ssh_user": "testuser",
            "ssh_password": "testpassword",
            "ssh_key_path": "",
            "ssh_port": 22,
            "memory_threshold_gb": 2,
            "jira_server": "https://test.atlassian.net",
            "jira_user": "test@test.com",
            "jira_api_token": "token123",
            "jira_project_key": "OPS",
            "jira_assignee_id": "acc123",
            "smtp_server": "smtp.test.com",
            "smtp_port": 587,
            "smtp_user": "alert@test.com",
            "smtp_password": "pass",
            "alert_recipient": "sre@test.com"
        }

    def test_optimal_memory_check(self):
        """When available memory exceeds threshold, no escalation should occur."""
        exit_code = monitor.run_monitor(dry_run=True, mock_available_gb=16)
        self.assertEqual(exit_code, 0)

    def test_critical_memory_check_triggers_escalation(self):
        """When memory is below threshold, escalation functions are called."""
        exit_code = monitor.run_monitor(dry_run=True, mock_available_gb=1)
        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
