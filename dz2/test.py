import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from main import get_git_commits, create_mermaid_graph

class TestGitVisualizer(unittest.TestCase):

    @patch("subprocess.run")
    def test_get_git_commits(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="abc123 def456\nghi789 jkl012".encode())
        commits = get_git_commits("/path/to/repo", datetime(2024, 11, 1))
        self.assertEqual(commits, [["abc123", "def456"], ["ghi789", "jkl012"]])

    def test_create_mermaid_graph(self):
        commits = [["abc123", "def456"], ["ghi789", "jkl012"]]
        graph = create_mermaid_graph(commits)
        expected_graph = "graph TD\n  abc123[abc123] --> def456[def456]\n  ghi789[ghi789] --> jkl012[jkl012]\n"
        self.assertEqual(graph, expected_graph)

if __name__ == "__main__":
    unittest.main()