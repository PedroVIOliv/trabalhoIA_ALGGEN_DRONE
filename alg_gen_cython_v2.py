import json
import os
from drone_delivery_cython import DroneDeliveryProblem, GeneticAlgorithm
from concurrent.futures import ProcessPoolExecutor

def process_file(file_name):
    file_path = f'tests/{file_name}'    
    with open(file_path, 'r') as f:
        problemData = json.load(f)
        
    problem = DroneDeliveryProblem(problemData)
    ga = GeneticAlgorithm(problem, population_size=2000, generations=700)
    best_path, best_fitness = ga.run()
    
    file_number = file_name.split('_')[-1].split('.')[0]
    os.makedirs(f'results/{file_number}', exist_ok=True)
    
    with open(f'results/{file_number}/generation_data.json', 'w') as f:
        json.dump(ga.generation_data, f)

    with open(f'results/{file_number}/best_path_graph.json', 'w') as f:
        points = [{"x": p['x'], "y": p['y'], "peso": p['peso']} for p in problemData['pontos']]
        json.dump({"best_path": best_path, "best_fitness": best_fitness, "coordinates": points}, f)
    
    with open(f'results/{file_number}/fitness_over_time.json', 'w') as f:
        json.dump(ga.fitness_over_time, f)

    return f"{file_name} - Best path: {best_path}\n{file_name} - Best fitness: {best_fitness}\n"

if __name__ == "__main__":
    run_all = True

    if run_all:
        files = os.listdir('tests')
    else:
        # Choose a specific file
        files = ['drone_problem_3.json']

    # Use multiprocessing to process files in parallel
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_file, files))

    # Print all results
    for result in results:
        print(result)

    # Run the visualization scripts after all processes are done
    os.system('python visualizar_geracoes.py')
    os.system('python visualizar_melhor_caminho.py')
    os.system('python visualizar_fitness_over_time.py')