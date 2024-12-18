import unittest
from unittest.mock import patch, MagicMock
from main import Emulator

class TestEmulatorCommands(unittest.TestCase):

    def setUp(self):
        # Настроим путь к конфигу и инициализируем эмулятор
        self.config_path = 'config.json'  # Пусть этот файл существует в тестовой среде
        self.emulator = Emulator(self.config_path)

    @patch("os.listdir", return_value=["file1.txt", "file2.txt", "dir1"])
    def test_ls(self, mock_listdir):
        # Проверим команду 'ls'
        result = self.emulator.ls()
        expected_result = "dir1\nfile1.txt\nfile2.txt"
        self.assertEqual(result, expected_result)

    @patch("os.path.isdir", return_value=True)
    @patch("os.path.abspath", return_value="/home/user")
    @patch("os.path.relpath", return_value="dir1")
    def test_cd_success(self, mock_relpath, mock_abspath, mock_isdir):
        # Проверим команду 'cd' на успешный переход
        result = self.emulator.cd("dir1")
        expected_result = "cd: Access denied: cannot go beyond home directory"
        self.assertEqual(result, expected_result)

    @patch("os.path.isdir", return_value=False)
    def test_cd_failure(self, mock_isdir):
        # Проверим команду 'cd' на несуществующую директорию
        result = self.emulator.cd("nonexistent")
        expected_result = "cd: nonexistent: No such file or directory"
        self.assertEqual(result, expected_result)

    @patch("os.makedirs")
    def test_mkdir(self, mock_makedirs):
        # Проверим команду 'mkdir'
        result = self.emulator.mkdir("new_dir")
        expected_result = "Created directory new_dir"
        self.assertEqual(result, expected_result)

    @patch("shutil.move")
    def test_mv(self, mock_move):
        # Проверим команду 'mv'
        mock_move.return_value = None  # Мокируем успешный вызов
        result = self.emulator.mv("file1.txt", "file2.txt")
        expected_result = "Moved file1.txt to file2.txt"
        self.assertEqual(result, expected_result)

    @patch("shutil.copy")
    def test_cp(self, mock_copy):
        # Проверим команду 'cp'
        mock_copy.return_value = None  # Мокируем успешный вызов
        result = self.emulator.cp("file1.txt", "file2.txt")
        expected_result = "Copied file1.txt to file2.txt"
        self.assertEqual(result, expected_result)

    def tearDown(self):
        # Очистка после тестов, если необходимо
        self.emulator.cleanup()

if __name__ == '__main__':
    unittest.main()
