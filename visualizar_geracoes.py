import json
import os
import matplotlib.pyplot as plt

run_all = True

if run_all:
    files = os.listdir('results')
else:
    # Choose a specific file
    files = ['results/0/generation_data.json']
    

for file_name in files:
    file_path = f'results/{file_name}/generation_data.json'
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Remove entries with -1 values    
    data = [entry for entry in data if entry["best_fitness"] != -1]
    
    best_fitness = [entry["best_fitness"] for entry in data]
    worst_fitness = [entry["worst_fitness"] for entry in data]
    mean_fitness = [entry["mean_fitness"] for entry in data]    
    generations = [entry["generation"] for entry in data]
    
    plt.figure(figsize=(10, 6))
    plt.plot(generations, best_fitness, label="Best Fitness", marker='o')
    plt.plot(generations, worst_fitness, label="Worst Fitness", marker='o')
    plt.plot(generations, mean_fitness, label="Mean Fitness", marker='o')
    
    
    plt.title("Fitness Over Generations")
    plt.xlabel("Generation")
    plt.ylabel("Fitness Value")

    # Adding a legend
    plt.legend()

    # Show the plot
    plt.grid(True)
    plt.tight_layout()
    
    os.makedirs(f'graphics/{file_name}', exist_ok=True)
    plt.savefig(f'graphics/{file_name}/fitness_over_generations.png')
      