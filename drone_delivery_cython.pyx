# drone_delivery_cython.pyx
import json
import random
import math
cimport cython
from libc.math cimport sqrt
from cpython cimport array
import array
import time

cdef class Point:
    cdef public double x
    cdef public double y
    cdef public double weight

    def __init__(self, double x, double y, double weight):
        self.x = x
        self.y = y
        self.weight = weight

cdef class DroneDeliveryProblem:
    cdef public list points
    cdef public Point base
    cdef public double drone_weight
    cdef public double max_capacity
    cdef public double battery_capacity
    cdef public bint viable_solution
    cdef public double mutation_rate

    def __init__(self, data):
        self.points = [Point(p['x'], p['y'], p['peso']) for p in data['pontos']]
        self.base = self.points[0]  # Assuming first and last points are the base
        self.drone_weight = data['drone_weight']
        self.max_capacity = data['max_capacity']
        self.battery_capacity = data['battery_capacity']
        self.viable_solution = False
        self.mutation_rate = 0.8

    @cython.cdivision(True)
    cdef double distance(self, Point p1, Point p2):
        return sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef double calculate_fitness(self, list path):
        cdef bint is_viable_solution = True
        cdef double total_battery_usage = 0
        cdef double current_weight = self.drone_weight
        cdef double current_battery = self.battery_capacity
        cdef Point current_point, next_point
        cdef double distance, battery_usage
        
        path = [0] + path + [0]  # Start and end with base
        cdef int i, path_len = len(path)

        for i in range(path_len-1, 0, -1):
            current_point = self.points[path[i]]
            next_point = self.points[path[i-1]]

            distance = self.distance(current_point, next_point)
            battery_usage = distance * current_weight
            current_weight += next_point.weight
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

cdef class Individual:
    cdef public list path
    cdef public DroneDeliveryProblem problem
    cdef public double fitness

    def __init__(self, list path, DroneDeliveryProblem problem):
        self.path = path
        self.problem = problem
        self.fitness = 0.0
        self.normalize()
        if random.random() < self.problem.mutation_rate:
            self.mutate()
        self.calculate_fitness()

    cpdef void calculate_fitness(self):
        self.fitness = self.problem.calculate_fitness(self.path)

    cpdef void mutate(self):
        cdef int i, j
        if random.random() < 0.5:
            if random.random() < 0.5:
                i = random.randint(1, len(self.path) - 1)
                self.path.insert(i, 0)
            else:
                zero_indexes = [i for i, x in enumerate(self.path) if x == 0]
                if len(zero_indexes) > 1:
                    self.path.pop(random.choice(zero_indexes))
        else:
            city_indexes = [i for i, x in enumerate(self.path) if x != 0]
            if len(city_indexes) > 1:
                i, j = random.sample(city_indexes, 2)
                self.path[i], self.path[j] = self.path[j], self.path[i]

        self.normalize()

    cpdef void normalize(self):
        cdef int i = 0
        while i < len(self.path):
            if self.path[i] == 0 and (i == 0 or i == len(self.path) - 1 or self.path[i - 1] == 0):
                self.path.pop(i)
                i-=1
            else:
                i += 1

cdef class GeneticAlgorithm:
    cdef public DroneDeliveryProblem problem
    cdef public int population_size
    cdef public int generations
    cdef public list generation_data
    cdef public int stagnation_counter
    cdef public double best_fitness
    cdef public list fitness_over_time

    def __init__(self, DroneDeliveryProblem problem, int population_size=2000, int generations=2000):
        self.problem = problem
        self.population_size = population_size
        self.generations = generations
        self.generation_data = []
        self.stagnation_counter = 0
        self.best_fitness = float('inf')
        self.fitness_over_time = []

    cpdef void adaptive_mutation_rate(self):
        if self.stagnation_counter > 50:
            self.problem.mutation_rate = 0.9
            self.stagnation_counter = 0
        elif self.problem.mutation_rate > 0.1:
            self.problem.mutation_rate -= 0.01

    cpdef Individual create_individual(self):
        cdef list path = list(range(1, len(self.problem.points) - 1))
        random.shuffle(path)
        return Individual(path, self.problem)

    cpdef Individual partially_matched_crossover(self, Individual parent1, Individual parent2):
        cdef list parent1_path = parent1.path.copy()
        cdef list parent2_path = parent2.path.copy()
        cdef list parent1_subroutes = []
        cdef list parent2_subroutes = []
        cdef list route = []
        cdef int i
        cdef list already_added_cities = []
        cdef list child_route = []

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

        while len(parent1_subroutes) > 0 and len(parent2_subroutes) > 0:
            if len(parent1_subroutes) > 0:
                subroute_1 = parent1_subroutes.pop(random.randint(0,len(parent1_subroutes)-1))
                for i in subroute_1:
                    if i not in already_added_cities:
                        already_added_cities.append(i)
                        child_route.append(i)
                child_route.append(0)
            if len(parent2_subroutes) > 0:
                subroute_2 = parent2_subroutes.pop(random.randint(0,len(parent2_subroutes)-1))
                for i in subroute_2:
                    if i not in already_added_cities:
                        already_added_cities.append(i)
                        child_route.append(i)
                child_route.append(0)
        return Individual(child_route, self.problem)

    cdef tuple tournament_selection(self, list population, int tournament_size=3):
        cdef list tournament1 = random.sample(population, tournament_size)
        cdef Individual min_individual1 = self._find_min_individual(tournament1)
        cdef list tournament2 = random.sample(population, tournament_size)
        cdef Individual min_individual2 = self._find_min_individual(tournament2)
        return min_individual1, min_individual2

    cdef Individual _find_min_individual(self, list tournament):
        cdef Individual min_individual = tournament[0]
        cdef Individual individual
        for individual in tournament[1:]:
            if individual.fitness < min_individual.fitness:
                min_individual = individual
        return min_individual

    cpdef tuple run(self):
        cdef list population = [self.create_individual() for _ in range(self.population_size)]
        cdef int generation
        cdef double current_best_fitness
        cdef int elitism_number
        cdef list new_population
        cdef Individual parent1, parent2, child, best_solution
        cdef double start_time = time.time()

        for generation in range(self.generations):
            population.sort(key=self._get_fitness)

            current_best_fitness = population[0].fitness
            current_worst_fitness = population[-1].fitness
            mean_fitness = sum([ind.fitness for ind in population]) / self.population_size
            self.generation_data.append({
                'best_fitness': current_best_fitness,
                'worst_fitness': current_worst_fitness,
                'mean_fitness': mean_fitness
            })

            elapsed_time = time.time() - start_time
            self.fitness_over_time.append((current_best_fitness, elapsed_time))

            if current_best_fitness < self.best_fitness:
                self.best_fitness = current_best_fitness
                self.stagnation_counter = 0
            else:
                self.stagnation_counter += 1

            self.adaptive_mutation_rate()

            #if generation % 2 == 0:
            #    print(f"Generation {generation}: Best fitness = {self.best_fitness}")
            #    print(f'Best solution: {population[0].path}')

            elitism_number = int(self.population_size * 0.05)
            elitism_number += elitism_number % 2
            new_population = population[:elitism_number]

            while len(new_population) < self.population_size:
                parent1, parent2 = self.tournament_selection(population)
                child = self.partially_matched_crossover(parent1, parent2)
                new_population.append(child)

            population = new_population

        best_solution = self._find_min_individual(population)
        return best_solution.path, best_solution.fitness

    cdef double _get_fitness(self, Individual individual):
        return individual.fitness