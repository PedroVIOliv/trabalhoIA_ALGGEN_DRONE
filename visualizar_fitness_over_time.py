import json
import os
import matplotlib.pyplot as plt

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

def extract_data(data):
    return [item[0] for item in data], [item[1] for item in data]

def plot_data(x, y, label, color):
    plt.plot(x, y, marker='o', linestyle='-', label=label, color=color)

def filtrar_pontos(tempo, fitness, distancia_minima=1):
    """Remove pontos próximos com base na distância mínima."""
    pontos_filtrados = []
    ult_tempo, ult_fitness = None, None
    
    for t, f in zip(tempo, fitness):
        if ult_tempo is None or abs(t - ult_tempo) > distancia_minima or abs(f - ult_fitness) > distancia_minima:
            pontos_filtrados.append((t, f))
            ult_tempo, ult_fitness = t, f
            
    return zip(*pontos_filtrados)

run_all = True

if run_all:
    files = os.listdir('results')
else:
    # Choose a specific file
    files = ['results/0/best_path_graph.json']
    
for file_name in files:
    file_path_ag = f'results/{file_name}/fitness_over_time.json'
    file_path_simplex = f'results/{file_name}/simplex.json'
    
    # Load data
    data_ag = load_json(file_path_ag)
    data_simplex = load_json(file_path_simplex)
    
    # Extract fitness and time
    fitness_ag, tempo_ag = extract_data(data_ag)
    fitness_simplex, tempo_simplex = extract_data(data_simplex)
    
    # Filter points
    tempo_filtrado_ag, fitness_filtrado_ag = filtrar_pontos(tempo_ag, fitness_ag)
    
    # Plot the data
    plt.figure(figsize=(10, 6))
    plot_data(tempo_filtrado_ag, fitness_filtrado_ag, label='AG', color='b')

    if data_simplex:
        tempo_filtrado_simplex, fitness_filtrado_simplex = filtrar_pontos(tempo_simplex, fitness_simplex)
        plot_data(tempo_filtrado_simplex, fitness_filtrado_simplex, label='Simplex', color='r')
    
    # Add title, labels, and legend
    plt.title('Fitness over Time')
    plt.xlabel('Tempo Decorrido (s)')
    plt.ylabel('Valor de Fitness')
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    
    # Save the graph
    os.makedirs(f'graphics/{file_name}', exist_ok=True)
    plt.savefig(f'graphics/{file_name}/fitness_over_time.png')
    # plt.show()  # Uncomment if you want to display the plot