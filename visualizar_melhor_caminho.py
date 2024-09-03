import json
import matplotlib.pyplot as plt
from adjustText import adjust_text

# Carregar o arquivo JSON
with open('results/best_path_graph.json') as f:
    data = json.load(f)

# Extrair o melhor caminho, as coordenadas e o melhor fitness
best_path = data["best_path"]
coordinates = data["coordinates"]
best_fitness = data["best_fitness"]

# Arredondar o valor de best_fitness para duas casas decimais
best_fitness_rounded = round(best_fitness, 2)

# Adicionar o ponto base (0) ao início e ao final do caminho
best_path = [0] + best_path + [0]

# Extrair coordenadas na ordem do melhor caminho
ordered_coordinates = [coordinates[i] for i in best_path]

# Criar listas para os eixos X, Y e os pesos
x_values = [coord["x"] for coord in ordered_coordinates]
y_values = [coord["y"] for coord in ordered_coordinates]
pesos = [coord["peso"] for coord in ordered_coordinates]

# Criar a figura e o eixo
fig, ax = plt.subplots(figsize=(10, 6))

# Plotar os pontos de entrega
ax.plot(x_values[1:-1], y_values[1:-1], marker='o', color='blue', label='Pontos de Entrega')

# Plotar o primeiro ponto do objeto "coordinates" em vermelho com marcador de quadrado
first_coordinate = coordinates[0]
ax.plot(first_coordinate['x'], first_coordinate['y'], marker='s', color='red', label='Base Inicial')

# Adicionar números e setas entre os pontos para indicar o caminho percorrido
for i in range(len(best_path) - 1):
    x_start, y_start = x_values[i], y_values[i]
    x_end, y_end = x_values[i + 1], y_values[i + 1]
    
    # Adicionar setas pequenas
    ax.annotate('', xy=(x_end, y_end), xytext=(x_start, y_start),
                arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))

texts = []
for i, (x, y, peso, idx) in enumerate(zip(x_values, y_values, pesos, best_path)):
    text = ax.text(x + 0.1, y + 0.1, f'{idx} ({peso})', fontsize=10, ha='right')
    texts.append(text)

# Ajustar textos para evitar sobreposição
adjust_text(texts, arrowprops=dict(arrowstyle="->", color='red', lw=0.5))

# Configurações do gráfico
ax.set_title(f'Consumo de Bateria {best_fitness_rounded:.2f}')
ax.grid(True)
ax.legend()

# Ajustar o layout para evitar sobreposição
plt.tight_layout()

# Mostrar o gráfico
plt.show()
