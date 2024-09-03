import json
import matplotlib.pyplot as plt
from adjustText import adjust_text
import numpy as np
import matplotlib.colors as mcolors

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
num_subroutes = best_path.count(0)
best_path = [0] + best_path + [0]

# Extrair coordenadas na ordem do melhor caminho
ordered_coordinates = [coordinates[i] for i in best_path]

# Criar listas para os eixos X, Y e os pesos
x_values = [coord["x"] for coord in ordered_coordinates]
y_values = [coord["y"] for coord in ordered_coordinates]
pesos = [coord["peso"] for coord in ordered_coordinates]

# Criar a figura e o eixo
fig, ax = plt.subplots(figsize=(10, 6))

# Plotar o primeiro ponto do objeto "coordinates" em vermelho com marcador de quadrado
first_coordinate = coordinates[0]
ax.plot(first_coordinate['x'], first_coordinate['y'], marker='s', color='red', label='Base Inicial')
# Definir colormap
colors = plt.cm.rainbow(np.linspace(0, 1, num_subroutes + 1))

# Plotar segmentos com a cor correspondente de cada subrota
color_index = 0
current_color = colors[color_index]

# Adicionar números e setas entre os pontos para indicar o caminho percorrido
for i in range(len(best_path) - 1):
    x_start, y_start = x_values[i], y_values[i]
    x_end, y_end = x_values[i + 1], y_values[i + 1]
    
    # Plotar segmento
    ax.plot([x_start, x_end], [y_start, y_end], marker='o', color=current_color, lw=2,
            label=f'Subrota {color_index+1}' if i == 0 or best_path[i] == 0 else "")
    
    # Cor de seta escura
    darker_color = mcolors.to_rgba(current_color, alpha=1.0)
    darker_color = (darker_color[0] * 0.7, darker_color[1] * 0.7, darker_color[2] * 0.7, darker_color[3])
    arrow_x = (x_start + x_end) / 2
    arrow_y = (y_start + y_end) / 2
    dx = x_end - x_start
    dy = y_end - y_start
    ax.annotate('', xy=(arrow_x + dx * 0.001, arrow_y + dy * 0.001), xytext=(arrow_x, arrow_y),
                arrowprops=dict(arrowstyle="-|>", color=darker_color, lw=2),
                annotation_clip=False)

    # Muda de cor ao voltar pra base
    if best_path[i + 1] == 0:
        color_index += 1
        if color_index <= num_subroutes:
            current_color = colors[color_index]

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
