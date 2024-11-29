import os
import subprocess
import argparse
from datetime import datetime

def get_git_commits(repo_path, date):
    # Формируем команду для получения коммитов до указанной даты
    date_str = date.strftime("%Y-%m-%d")
    cmd = ["git", "log", "--before", date_str, "--pretty=format:%H %p"]
    
    result = subprocess.run(cmd, cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise Exception(f"Git command failed: {result.stderr.decode()}")

    commits = result.stdout.decode().strip().split("\n")
    return [line.split() for line in commits]

def create_mermaid_graph(commits):
    graph = "graph TD\n"
    for commit in commits:
        commit_hash = commit[0]
        parents = commit[1:]
        for parent in parents:
            graph += f"  {commit_hash}[{commit_hash}] --> {parent}[{parent}]\n"
    return graph

def generate_graph(graph, visualizer_path, output_path):
    with open("graph.mmd", "w") as f:
        f.write(graph)
    
    cmd = [visualizer_path, "-i", "graph.mmd", "-o", output_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise Exception(f"Mermaid visualizer failed: {result.stderr.decode()}")

def main():
    parser = argparse.ArgumentParser(description="Git commit dependency visualizer.")
    parser.add_argument("--repo", required=True, help="Path to the git repository")
    parser.add_argument("--date", required=True, help="Date to filter commits (format: YYYY-MM-DD)")
    parser.add_argument("--visualizer", required=True, help="Path to mermaid-cli executable")
    parser.add_argument("--output", required=True, help="Path to output image (e.g., graph.png)")

    args = parser.parse_args()

    # Преобразуем строку в объект даты
    date = datetime.strptime(args.date, "%Y-%m-%d")

    # Получаем список коммитов и их зависимостей
    commits = get_git_commits(args.repo, date)

    # Генерируем граф в формате Mermaid
    graph = create_mermaid_graph(commits)

    # Генерируем изображение
    generate_graph(graph, args.visualizer, args.output)

    print(f"Graph generated at {args.output}")

if __name__ == "__main__":
    main()
