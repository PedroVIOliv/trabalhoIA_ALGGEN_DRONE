import json
import random
import math

class Point:
    def __init__(self, x, y, weight):
        self.x = x
        self.y = y
        self.weight = weight

class DroneDeliveryProblem:
    def __init__(self, json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
        self.points = [Point(p['x'], p['y'], p['peso']) for p in data['pontos']]
        self.base = self.points[0]  # Assuming first and last points are the base
        self.drone_weight = 10  # Example drone weight
        self.max_capacity = 25 # Example max capacity
        self.battery_capacity = 2200  # Example battery capacity

    def distance(self, p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def calculate_fitness(self, path):
        if(path[1] == 0):
            pass #debug
        path = [0] + path + [0]  # Start and end with base
        total_battery_usage = 0
        current_weight = self.drone_weight
        current_battery = self.battery_capacity

        for i in range(len(path) - 1, 0, -1):
            current_point = self.points[path[i]]
            next_point = self.points[path[i-1]]
            
            distance = self.distance(current_point, next_point)
            current_weight += next_point.weight
            battery_usage = distance * current_weight
            
            total_battery_usage += battery_usage
            current_battery -= battery_usage

            if current_battery < 0 or current_weight > self.max_capacity:
                #apply a penalty to the fitness function
                total_battery_usage += 50000
            
            if(path[i-1] == 0):
                current_weight = self.drone_weight
                current_battery = self.battery_capacity

        return total_battery_usage

class GeneticAlgorithm:
    def __init__(self, problem, population_size=1000, generations=2000):
        self.problem = problem
        self.population_size = population_size
        self.generations = generations
        self.best_5_per_generation = []

    def create_individual(self):
        path = list(range(1, len(self.problem.points) - 1))
        random.shuffle(path)
        return path  # Start and end with base

    def crossover(self, parent1, parent2):
        for i in range(len(parent1)):
            if parent1[i] == 0 or (len(parent2)>i and parent2[i] == 0):
                break #debug
        # Order crossover
        start, end = sorted(random.sample(range(len(parent1)), 2))
        child = [-1] * len(parent1)
        child[start:end] = parent1[start:end]
        i = end
        for gene in parent2[end:] + parent2[:end]:
            if gene not in child and gene != 0:
                child[i % len(parent1)] = gene
                i += 1
        while -1 in child:
            child[child.index(-1)] = 0
        if 1 not in child or 2 not in child or 3 not in child:
            pass
        return child

    def mutate(self, individual):
    # Introduce a random mutation that adds a return to the base at a random position
        if random.random() < 0.5: #inserts a return to the base
            i = random.randint(1, len(individual) - 1)
            individual.insert(i, 0)
            if random.random()<0.1:
                self.mutate(individual)
            return

        # Traditional mutation: swap two points
        i, j = random.sample(range(1, len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]
        if random.random() < 0.1:
            self.mutate(individual)

    def normalize(self, individual):
        #removes multiple returns to the base in a row or 0 at the begin or end
        i = 0
        while i < len(individual):
            if individual[i] == 0 and (i == 0 or i == len(individual) - 1 or individual[i - 1] == 0):
                individual.pop(i)
            else:
                i += 1
        return individual

    def run(self):
        population = [self.create_individual() for _ in range(self.population_size)]

        for generation in range(self.generations):
            population = sorted(population, key=lambda x: self.problem.calculate_fitness(x))
            
            self.best_5_per_generation.append(population[:5])

            
            if generation % 100 == 0:
                print(f"Generation {generation}: Best fitness = {self.problem.calculate_fitness(population[0])}")
                print(f'Best solution: {population[0]}')

            new_population = population[:2]  # Elitism

            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(population[:50], 2)
                child = self.crossover(parent1, parent2)
                if random.random() < 0.1:
                    self.mutate(child)
                #lets take out multiple returns to the base in a row or 0 at the begin or end with a function
                child = self.normalize(child)
                new_population.append(child)

            population = new_population

        best_solution = min(population, key=lambda x: self.problem.calculate_fitness(x))
        return best_solution, self.problem.calculate_fitness(best_solution)

# Usage
problem = DroneDeliveryProblem('drone_problem.json')
ga = GeneticAlgorithm(problem)
best_path, best_fitness = ga.run()

#save the best 5 of each generation to a file

with open('best_5_per_generation.json', 'w') as f:
    json.dump(ga.best_5_per_generation, f)

print(f"Best path: {best_path}")
print(f"Best fitness: {best_fitness}")