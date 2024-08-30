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
        self.drone_weight = data['drone_weight']
        self.max_capacity = data['max_capacity']
        self.battery_capacity = data['battery_capacity']
        self.viable_solution = False
        self.mutation_rate = 0.8

    def distance(self, p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def calculate_fitness(self, path):
        is_viable_solution = True
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
                total_battery_usage += 50000
                is_viable_solution = False
            
            if path[i-1] == 0:
                current_weight = self.drone_weight
                current_battery = self.battery_capacity

        if not self.viable_solution and is_viable_solution:
            self.viable_solution = True
            self.mutation_rate = 0.1
        return total_battery_usage

class Individual:
    def __init__(self, path, problem):
        self.path = path
        self.problem = problem
        self.fitness = None
        self.normalize()
        self.calculate_fitness()
        

    def calculate_fitness(self):
        self.fitness = self.problem.calculate_fitness(self.path)

    def mutate(self):
        if random.random() < 0.5:
            if random.random() < 0.5:
                i = random.randint(1, len(self.path) - 1)
                self.path.insert(i, 0)
            else:
                #take out a random 0
                zero_indexes = [i for i, x in enumerate(self.path) if x == 0]
                if len(zero_indexes) > 1:
                    self.path.pop(random.choice(zero_indexes))
        else:
            i, j = random.sample(range(1, len(self.path)), 2)
            self.path[i], self.path[j] = self.path[j], self.path[i]
        
        self.normalize()
        self.calculate_fitness()

    def normalize(self):
        i = 0
        while i < len(self.path):
            if self.path[i] == 0 and (i == 0 or i == len(self.path) - 1 or self.path[i - 1] == 0):
                self.path.pop(i)
            else:
                i += 1

class GeneticAlgorithm:
    def __init__(self, problem, population_size=2000, generations=200):
        self.problem = problem
        self.population_size = population_size
        self.generations = generations
        self.best_5_per_generation = []
        self.stagnation_counter = 0
        self.best_fitness = float('inf')

    def adaptive_mutation_rate(self):
        if self.stagnation_counter > 50:  # Example threshold
            self.problem.mutation_rate = 0.8
            self.stagnation_counter = 0  # Reset counter after adapting
        elif self.problem.mutation_rate > 0.1:
            self.problem.mutation_rate -= 0.01  # Gradually reduce mutation rate

    def create_individual(self):
        path = list(range(1, len(self.problem.points) - 1))
        random.shuffle(path)
        return Individual(path, self.problem)

    def order_crossover(self, parent1, parent2):
        start, end = sorted(random.sample(range(len(parent1.path)), 2))
        child_path = [-1] * len(parent1.path)
        child_path[start:end] = parent1.path[start:end]
        i = end
        for gene in parent2.path[end:] + parent2.path[:end]:
            if gene not in child_path and gene != 0:
                child_path[i % len(parent1.path)] = gene
                i += 1
        while -1 in child_path:
            child_path[child_path.index(-1)] = 0
        child = Individual(child_path, self.problem)
        return child
    
    def partially_matched_crossover(self, parent1, parent2):
        # Subroutes and in a 0
        parent1_path = parent1.path.copy()
        parent2_path = parent2.path.copy()
        parent1_subroutes = []
        parent2_subroutes = []
        route = []
        for i in parent1_path:
            if i == 0:
                parent1_subroutes.append(route)
                route = []
            else:
                route.append(i)
        if len(route) > 0:
            parent1_subroutes.append(route)
        route = []
        for i in parent2_path:
            if i == 0:
                parent2_subroutes.append(route)
                route = []
            else:
                route.append(i)
        if len(route) > 0:
            parent2_subroutes.append(route)

        # Crossover
        already_added_cities = []
        child_route = []
        while len(parent1_subroutes) > 0 and len(parent2_subroutes) > 0:
            #select random subroute from parent1
            if len(parent1_subroutes) > 0:
                subroute_1 = parent1_subroutes.pop(random.randint(0,len(parent1_subroutes)-1))
                for i in subroute_1:
                    if i not in already_added_cities:
                        already_added_cities.append(i)
                        child_route.append(i)
                child_route.append(0)
            #select random subroute from parent2
            if len(parent2_subroutes) > 0:
                subroute_2 = parent2_subroutes.pop(random.randint(0,len(parent2_subroutes)-1))
                for i in subroute_2:
                    if i not in already_added_cities:
                        already_added_cities.append(i)
                        child_route.append(i)
                child_route.append(0)
        child = Individual(child_route, self.problem)
        return child



        



    def tournament_selection(self, population, tournament_size=3):
        tournament = random.sample(population, tournament_size)
        return min(tournament, key=lambda individual: individual.fitness)
    

    def run(self):
        population = [self.create_individual() for _ in range(self.population_size)]

        for generation in range(self.generations):
            population.sort(key=lambda individual: individual.fitness)
            self.best_5_per_generation.append([ind.path for ind in population[:5]])
            
            current_best_fitness = population[0].fitness
            if current_best_fitness < self.best_fitness:
                self.best_fitness = current_best_fitness
                self.stagnation_counter = 0
            else:
                self.stagnation_counter += 1

            self.adaptive_mutation_rate()

            if generation % 2 == 0:
                print(f"Generation {generation}: Best fitness = {self.best_fitness}")
                print(f'Best solution: {population[0].path}')

            new_population = population[:2]  # Elitism

            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(population[:50], 2)
                child = self.partially_matched_crossover(parent1, parent2)
                if random.random() < self.problem.mutation_rate:
                    child.mutate()
                new_population.append(child)

            population = new_population

        best_solution = min(population, key=lambda individual: individual.fitness)
        return best_solution.path, best_solution.fitness

# Usage
problem = DroneDeliveryProblem('drone_problem.json')
ga = GeneticAlgorithm(problem)
best_path, best_fitness = ga.run()

with open('best_5_per_generation.json', 'w') as f:
    json.dump(ga.best_5_per_generation, f)

print(f"Best path: {best_path}")
print(f"Best fitness: {best_fitness}")