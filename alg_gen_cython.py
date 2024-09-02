import json 
from drone_delivery_cython import DroneDeliveryProblem, GeneticAlgorithm

# Usage
problem = DroneDeliveryProblem('drone_problem_2.json')
ga = GeneticAlgorithm(problem,population_size=1000,generations=2000)
best_path, best_fitness = ga.run()

with open('best_5_per_generation.json', 'w') as f:
        json.dump(ga.best_5_per_generation, f)
with open('fitness_over_time.json', 'w') as f:
        json.dump(ga.fitness_over_time, f)

print(f"Best path: {best_path}")
print(f"Best fitness: {best_fitness}")