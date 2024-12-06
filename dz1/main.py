import os
import zipfile
import shutil
import tempfile
import tkinter as tk
from tkinter import scrolledtext
import json


class Emulator:
    """
    Класс для эмуляции файловой системы и выполнения команд,
    аналогичных shell-командам.
    """

    def __init__(self, config_path):
        """
        Инициализация эмулятора, чтение конфигурации.
        """
        self.config = self.read_config(config_path)
        self.user_name = self.config['user_name']
        self.computer_name = self.config['computer_name']
        self.vfs_path = self.config['vfs_path']
        self.current_dir = ''
        self.previous_dirs = []
        self.temp_dir = tempfile.mkdtemp()
        self.init_vfs()

    def read_config(self, config_path):
        """
        Читает конфигурационный файл JSON и возвращает параметры.
        """
        try:
            with open(config_path, 'r') as file:
                config = json.load(file)
            return config
        except Exception as e:
            raise RuntimeError(f"Error reading config file: {e}")

    def init_vfs(self):
        """
        Инициализирует виртуальную файловую систему: разархивирует ZIP-файл.
        """
        try:
            with zipfile.ZipFile(self.vfs_path, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
            self.current_dir = self.temp_dir
        except Exception as e:
            raise RuntimeError(f"Error initializing VFS: {e}")

    def save_vfs(self):
        """
        Архивирует изменения обратно в ZIP-файл.
        """
        try:
            with zipfile.ZipFile(self.vfs_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
                for root, dirs, files in os.walk(self.temp_dir):
                    for file in files:
                        abs_path = os.path.join(root, file)
                        arcname = os.path.relpath(abs_path, self.temp_dir)
                        zip_ref.write(abs_path, arcname)
        except Exception as e:
            raise RuntimeError(f"Error saving VFS: {e}")

    def cleanup(self):
        """
        Очищает временные ресурсы.
        """
        self.save_vfs()
        shutil.rmtree(self.temp_dir)

    def run_command(self, command, output_widget=None):
        """
        Выполняет указанную команду и выводит результат.
        """
        parts = command.split()
        if not parts:
            return

        cmd = parts[0]
        args = parts[1:]

        if output_widget:
            output_widget.insert(tk.END, f"{self.user_name}@{self.computer_name}$ {command}\n")

        if cmd == 'ls':
            result = self.ls()
        elif cmd == 'cd':
            result = self.cd(args[0]) if args else "cd: missing path"
        elif cmd == 'exit':
            result = self.exit()
        elif cmd == 'mkdir':
            result = self.mkdir(args[0]) if args else "mkdir: missing directory name"
        elif cmd == 'mv':
            result = self.mv(args[0], args[1]) if len(args) == 2 else "mv: missing arguments"
        elif cmd == 'cp':
            result = self.cp(args[0], args[1]) if len(args) == 2 else "cp: missing arguments"
        else:
            result = f"{cmd}: command not found"

        if output_widget:
            output_widget.insert(tk.END, result + "\n")
            output_widget.see(tk.END)

        return result

    def ls(self):
        """
        Выполняет команду 'ls': список файлов и директорий.
        """
        try:
            return "\n".join(sorted(os.listdir(self.current_dir)))
        except Exception as e:
            return f"ls: Error: {str(e)}"

    def cd(self, path):
        """
        Выполняет команду 'cd'.
        """
        try:
            new_path = os.path.abspath(os.path.join(self.current_dir, path))
            # Проверяем, что новый путь не выходит за пределы домашней директории
            if os.path.commonpath([new_path, self.temp_dir]) != self.temp_dir:
                return "cd: Access denied: cannot go beyond home directory"
            
            if os.path.isdir(new_path):
                self.previous_dirs.append(self.current_dir)
                self.current_dir = new_path
                # Получаем относительный путь от домашней директории
                relative_path = os.path.relpath(self.current_dir, self.temp_dir)
                return f"Changed directory to {relative_path}"
            return f"cd: {path}: No such file or directory"
        except Exception as e:
            return f"cd: Error: {str(e)}"


    def mkdir(self, directory_name):
        """
        Выполняет команду 'mkdir'.
        """
        try:
            dir_path = os.path.join(self.current_dir, directory_name)
            os.makedirs(dir_path, exist_ok=True)
            return f"Created directory {directory_name}"
        except Exception as e:
            return f"mkdir: Error: {str(e)}"

    def mv(self, source, destination):
        """
        Выполняет команду 'mv'.
        """
        try:
            src_path = os.path.join(self.current_dir, source)
            dst_path = os.path.join(self.current_dir, destination)
            shutil.move(src_path, dst_path)
            return f"Moved {source} to {destination}"
        except Exception as e:
            return f"mv: Error: {str(e)}"

    def cp(self, source, destination):
        """
        Выполняет команду 'cp'.
        """
        try:
            src_path = os.path.join(self.current_dir, source)
            dst_path = os.path.join(self.current_dir, destination)
            shutil.copy(src_path, dst_path)
            return f"Copied {source} to {destination}"
        except Exception as e:
            return f"cp: Error: {str(e)}"

    def exit(self):
        """
        Выполняет команду 'exit'.
        """
        self.cleanup()
        exit()


class ShellGUI:
    """
    Класс GUI оболочки.
    """
    def __init__(self, emulator):
        self.emulator = emulator
        self.root = tk.Tk()
        self.root.title("Shell Emulator")
        self.root.resizable(width=False,height=False)
        self.output = scrolledtext.ScrolledText(self.root, height=20, width=80, state=tk.NORMAL)
        self.output.pack()
        self.entry = tk.Entry(self.root, width=80)
        self.entry.pack()
        self.entry.bind('<Return>', self.execute_command)

    def execute_command(self, event):
        command = self.entry.get()
        self.emulator.run_command(command, output_widget=self.output)
        self.entry.delete(0, tk.END)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    config_path = 'config.json'
    emulator = Emulator(config_path)
    gui = ShellGUI(emulator)
    gui.run()
