import json 
from drone_delivery_cython import DroneDeliveryProblem, GeneticAlgorithm

with open('tests/drone_problem_2.json', 'r') as f:
    problemData = json.load(f)

problem = DroneDeliveryProblem(problemData)
ga = GeneticAlgorithm(problem, population_size=1000, generations=1000)
best_path, best_fitness = ga.run()

with open('results/best_5_per_generation.json', 'w') as f:
        json.dump(ga.best_5_per_generation, f)
with open('results/best_path_graph.json', 'w') as f:
    points = [{"x": p['x'], "y": p['y'], "peso": p['peso']} for p in problemData['pontos']]
    json.dump({"best_path": best_path, "best_fitness": best_fitness, "coordinates": points}, f)
with open('results/fitness_over_time.json', 'w') as f:
        json.dump(ga.fitness_over_time, f)

print(f"Best path: {best_path}")
print(f"Best fitness: {best_fitness}")