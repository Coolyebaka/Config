import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

from main import get_commits, build_dependency_graph, generate_mermaid_graph, generate_svg_from_mermaid

class TestGitVisualize(unittest.TestCase):

    @patch('pygit2.init_repository')
    def test_get_commits(self, mock_init_repo):
        # Создаем фальшивый репозиторий
        mock_repo = MagicMock()
        mock_init_repo.return_value = mock_repo

        # Мокируем коммиты
        mock_commit_1 = MagicMock()
        mock_commit_1.commit_time = datetime(2024, 1, 1).timestamp()
        mock_commit_1.id = "commit1"
        mock_commit_2 = MagicMock()
        mock_commit_2.commit_time = datetime(2024, 2, 1).timestamp()
        mock_commit_2.id = "commit2"
        mock_repo.walk.return_value = [mock_commit_1, mock_commit_2]

        before_date = datetime(2024, 2, 1)
        commits = get_commits('/fake/repo', before_date)

        # Проверяем, что возвращаются только коммиты до указанной даты
        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0].id, "commit1")

    def test_build_dependency_graph(self):
        # Создаем фальшивые коммиты
        mock_commit_1 = MagicMock()
        mock_commit_1.id = "commit1"
        mock_commit_2 = MagicMock()
        mock_commit_2.id = "commit2"
        mock_commit_2.parents = [mock_commit_1]

        graph = build_dependency_graph([mock_commit_1, mock_commit_2])

        # Проверяем, что граф зависит от коммитов
        self.assertIn("commit2", graph)
        self.assertIn("commit1", graph["commit2"])

    def test_generate_mermaid_graph(self):
        graph = {
            "commit1": [],
            "commit2": ["commit1"],
            "commit3": ["commit2"]
        }
        mermaid_graph = generate_mermaid_graph(graph)

        expected_mermaid = '''graph TD
  commit1 --> commit2
  commit2 --> commit3
'''
        self.assertEqual(mermaid_graph, expected_mermaid)

    @patch('subprocess.run')
    def test_generate_svg_from_mermaid(self, mock_run):
        mock_run.return_value = None  # Эмуляция успешного выполнения subprocess.run

        mermaid_code = '''graph TD
  commit1 --> commit2
  commit2 --> commit3
'''
        generate_svg_from_mermaid(mermaid_code, 'output.svg')

        # Проверка, что subprocess был вызван с правильными параметрами
        mock_run.assert_called_once_with(['mmdc', '-i', 'graph.mmd', '-o', 'output.svg'])

    @patch('os.remove')
    @patch('subprocess.run')
    def test_generate_svg_from_mermaid_removes_temp_file(self, mock_run, mock_remove):
        mock_run.return_value = None  # Эмуляция успешного выполнения subprocess.run

        mermaid_code = '''graph TD
  commit1 --> commit2
  commit2 --> commit3
'''
        generate_svg_from_mermaid(mermaid_code, 'output.svg')

        # Проверяем, что файл был удален после генерации SVG
        mock_remove.assert_called_once_with('graph.mmd')

if __name__ == '__main__':
    unittest.main()
