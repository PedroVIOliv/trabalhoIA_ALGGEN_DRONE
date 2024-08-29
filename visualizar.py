import json
import matplotlib.pyplot as plt
import argparse

def load_json(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

def plot_route(ax, points, route, generation):
    x = [points[i]['x'] for i in route]
    y = [points[i]['y'] for i in route]
    ax.plot(x, y, '-o')
    ax.set_title(f'Geração {generation}')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

def main():
    parser = argparse.ArgumentParser(description='Visualize rotas do algoritmo genético.')
    parser.add_argument('--last', action='store_true', help='Mostrar apenas a última geração')
    args = parser.parse_args()

    # Carregar dados
    problem_data = load_json('drone_problem.json')
    generations_data = load_json('best_5_per_generation.json')

    points = problem_data['pontos']

    # Decidir quais gerações plotar
    if True:
        generations_to_plot = [generations_data[-1]]
        num_generations = 1
    else:
        generations_to_plot = generations_data
        num_generations = len(generations_data)

    # Configurar o plot
    fig, axs = plt.subplots(num_generations, 1, figsize=(10, 5*num_generations), squeeze=False)
    fig.suptitle('Evolução das Rotas por Geração', fontsize=16)

    # Plotar cada geração
    for gen, route in enumerate(generations_to_plot):
        plot_route(axs[gen, 0], points, route, len(generations_data) if args.last else gen+1)

    # Ajustar o layout e mostrar o plot
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()