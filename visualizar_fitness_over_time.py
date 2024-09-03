import json
import os
import matplotlib.pyplot as plt

def filtrar_pontos(tempo, fitness, distancia_minima=5):
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
    file_path = f'results/{file_name}/fitness_over_time.json'
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Extrair fitness e tempo
    fitness = [item[0] for item in data]
    tempo = [item[1] for item in data]
    
    # Filtrar pontos semelhantes
    tempo_filtrado, fitness_filtrado = filtrar_pontos(tempo, fitness)

    # Criar o gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(tempo_filtrado, fitness_filtrado, marker='o', linestyle='-', color='b')

    # Adicionar título e rótulos
    plt.title('Fitness over Time')
    plt.xlabel('Tempo Decorrido (s)')
    plt.ylabel('Valor de Fitness')
    plt.tight_layout()
    plt.grid(True)

    # Exibir o gráfico
    # plt.show()
    os.makedirs(f'graphics/{file_name}', exist_ok=True)
    plt.savefig(f'graphics/{file_name}/fitness_over_time.png')