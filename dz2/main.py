import argparse
import pygit2
from datetime import datetime
import subprocess
import os

# Функция для получения коммитов до заданной даты
def get_commits(repo_path, before_date):
    repo = pygit2.init_repository(repo_path, bare=True)
    commits = []

    # Итерируем по всем коммитам в репозитории
    for commit in repo.walk(repo.head.target, pygit2.GIT_SORT_TIME):
        if commit.commit_time < before_date.timestamp():
            commits.append(commit)

    return commits

# Функция для построения графа зависимостей
def build_dependency_graph(commits):
    graph = {}
    commit_index = {commit.id: i for i, commit in enumerate(commits)}

    for commit in commits:
        commit_str = f'{commit_index[commit.id]}__{commit.id}'
        parents_str = [f'{commit_index[parent.id]}__{parent.id}' for parent in commit.parents]
        graph[commit_str] = parents_str

    return graph

# Функция для генерации графа в формате Mermaid
def generate_mermaid_graph(graph):
    mermaid = 'graph TD\n'

    for commit, parents in graph.items():
        for parent in parents:
            mermaid += f'  {parent} --> {commit}\n'

    return mermaid

# Функция для создания SVG-файла с помощью mermaid-cli
def generate_svg_from_mermaid(mermaid_code, output_file):
    # Сохраняем Mermaid код в файл
    with open("graph.mmd", "w") as f:
        f.write(mermaid_code)

    # Используем mermaid-cli для конвертации в SVG
    subprocess.run(['mmdc', '-i', 'graph.mmd', '-o', output_file])

    # Удаляем временный файл
    os.remove("graph.mmd")

# Основная логика программы
def main():
    parser = argparse.ArgumentParser(description='Visualize git commit dependencies.')
    parser.add_argument('repo_path', type=str, help='Path to the Git repository')
    parser.add_argument('date', type=str, help='Date for filtering commits (YYYY-MM-DD)')
    parser.add_argument('output_svg', type=str, help='Path to output SVG file')
    args = parser.parse_args()

    # Конвертируем строку в объект datetime
    date = datetime.strptime(args.date, "%Y-%m-%d")

    # Получаем список коммитов до заданной даты
    commits = get_commits(args.repo_path, date)

    # Если коммиты не найдены
    if not commits:
        print("No commits found before the specified date.")
        return

    # Строим граф зависимостей
    graph = build_dependency_graph(commits)

    # Генерируем граф в формате Mermaid
    mermaid_graph = generate_mermaid_graph(graph)

    # Отладочный вывод графа Mermaid

    # Генерируем SVG из Mermaid
    generate_svg_from_mermaid(mermaid_graph, args.output_svg)

# Запуск основной функции
if __name__ == "__main__":
    main()
