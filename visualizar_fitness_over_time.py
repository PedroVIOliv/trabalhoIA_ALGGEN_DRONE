import json
import matplotlib.pyplot as plt

def filtrar_pontos(tempo, fitness, distancia_minima=0.01):
    """Remove pontos próximos com base na distância mínima."""
    pontos_filtrados = []
    ult_tempo, ult_fitness = None, None
    
    for t, f in zip(tempo, fitness):
        if ult_tempo is None or abs(t - ult_tempo) > distancia_minima or abs(f - ult_fitness) > distancia_minima:
            pontos_filtrados.append((t, f))
            ult_tempo, ult_fitness = t, f
            
    return zip(*pontos_filtrados)

# Ler o arquivo JSON
with open('results/fitness_over_time.json', 'r') as file:
    data = json.load(file)

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
plt.show()
