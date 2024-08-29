import math
import json

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
                return float('inf') # Invalid solution
            
            if(path[i-1] == 0):
                current_weight = self.drone_weight
                current_battery = self.battery_capacity

        return total_battery_usage
    
problem = DroneDeliveryProblem('drone_problem.json')

caso_de_teste = [8, 0, 13, 0, 12, 0, 3, 4, 0, 5, 0, 14, 0, 9, 0, 6, 0, 2, 0, 7, 0, 10, 0, 11, 1]



print(problem.calculate_fitness(caso_de_teste))