import os
import json
import argparse
import matplotlib.pyplot as plt
import networkx as nx

def get_dependencies(package_name, repo_url):
    # Путь к репозиторию
    repo_path = os.path.join(os.getcwd(), package_name)

    # Клонируем репозиторий
    os.system(f'git clone {repo_url} {repo_path}')

    # Путь к файлу package.json
    package_json_path = os.path.join(repo_path, 'package.json')

    # Чтение зависимостей из package.json
    with open(package_json_path) as f:
        package_data = json.load(f)

    dependencies = package_data.get('dependencies', {})
    dev_dependencies = package_data.get('devDependencies', {})
    
    return dependencies, dev_dependencies

def create_mermaid_graph(dependencies, dev_dependencies):
    graph = "graph TD;\n"
    for dep in dependencies:
        graph += f"    {dep};\n"
    for dev_dep in dev_dependencies:
        graph += f"    {dev_dep};\n"
    return graph

def save_graph_as_png(graph, output_file):
    G = nx.parse_mermaid(graph)
    pos = nx.spring_layout(G)
    
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, arrows=True)
    plt.savefig(output_file)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description='Visualize npm package dependencies as a Mermaid graph.')
    parser.add_argument('program_path', type=str, help='Path to the visualization program')
    parser.add_argument('package_name', type=str, help='Name of the package to analyze')
    parser.add_argument('output_file', type=str, help='Path to save the dependency graph image')
    parser.add_argument('repo_url', type=str, help='URL of the repository to clone')

    args = parser.parse_args()

    dependencies, dev_dependencies = get_dependencies(args.package_name, args.repo_url)
    
    mermaid_graph = create_mermaid_graph(dependencies, dev_dependencies)

    save_graph_as_png(mermaid_graph, args.output_file)
    
    print("Граф зависимостей успешно сгенерирован и сохранен в", args.output_file)

if __name__ == '__main__':
    main()
