import json 
from drone_delivery_cython import DroneDeliveryProblem, GeneticAlgorithm

# Usage
problem = DroneDeliveryProblem('drone_problem_2.json')
ga = GeneticAlgorithm(problem)
best_path, best_fitness = ga.run()

with open('best_5_per_generation.json', 'w') as f:
    json.dump(ga.best_5_per_generation, f)

print(f"Best path: {best_path}")
print(f"Best fitness: {best_fitness}")