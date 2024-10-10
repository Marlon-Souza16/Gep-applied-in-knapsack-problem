import random
import math

POPULATION_SIZE = 20
GENOME_DEPTH = 5  
GENERATIONS = 50  
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.9
ELITISM_COUNT = 2
KNAPSACK_CAPACITY = 15
TIME_LIMIT = 15

items = [(2, 3, 2), (3, 4, 3), (4, 5, 4), (5, 8, 5),
         (8, 10, 8), (4, 7, 4), (2, 6, 2), (1, 2, 1)]

FUNCTIONS = ['+', '-', '*', '/', '>', '<', 'and', 'or']
TERMINALS = ['w', 'v', 't'] + [str(i) for i in range(-10, 11) if i != 0]

def create_random_expression(depth=0):
    if depth > GENOME_DEPTH or (depth > 0 and random.random() < 0.3):
        return random.choice(TERMINALS)
    else:
        func = random.choice(FUNCTIONS)
        if func in ['and', 'or', '>', '<']:
            return [func, create_random_expression(depth + 1), create_random_expression(depth + 1)]
        else:
            return [func, create_random_expression(depth + 1), create_random_expression(depth + 1)]

def evaluate_expression(expr, item_properties):
    if isinstance(expr, list):
        func = expr[0]
        arg1 = evaluate_expression(expr[1], item_properties)
        arg2 = evaluate_expression(expr[2], item_properties)
        try:
            if func == '+':
                return arg1 + arg2
            elif func == '-':
                return arg1 - arg2
            elif func == '*':
                return arg1 * arg2
            elif func == '/':
                return arg1 / arg2 if arg2 != 0 else 1
            elif func == '>':
                return arg1 > arg2
            elif func == '<':
                return arg1 < arg2
            elif func == 'and':
                return arg1 and arg2
            elif func == 'or':
                return arg1 or arg2
            else:
                return 0
        except Exception:
            return 0
    else:
        if expr in ['w', 'v', 't']:
            return item_properties[expr]
        else:
            try:
                return float(expr)
            except ValueError:
                return 0

def get_included_items(expression):
    included_items = []
    total_weight = 0
    total_time = 0
    for index, (w, v, t) in enumerate(items):
        item_properties = {'w': w, 'v': v, 't': t}
        result = evaluate_expression(expression, item_properties)
        if isinstance(result, bool) and result:
            included_items.append(index)
            total_weight += w
            total_time += t
    if total_weight > KNAPSACK_CAPACITY or total_time > TIME_LIMIT:
        return [], 0, 0
    return included_items, total_weight, total_time

def fitness(expression):
    included_items, total_weight, total_time = get_included_items(expression)
    total_value = sum(items[i][1] for i in included_items)
    return total_value

def mutate(expression, depth=0):
    if isinstance(expression, list):
        if random.random() < MUTATION_RATE:
            new_func = random.choice(FUNCTIONS)
            return [new_func, mutate(expression[1], depth + 1), mutate(expression[2], depth + 1)]
        else:
            return [expression[0], mutate(expression[1], depth + 1), mutate(expression[2], depth + 1)]
    else:
        if random.random() < MUTATION_RATE:
            return random.choice(TERMINALS)
        else:
            return expression

def crossover(expr1, expr2, depth=0):
    if random.random() < CROSSOVER_RATE and depth < GENOME_DEPTH:
        if isinstance(expr1, list) and isinstance(expr2, list):
            return expr2
        else:
            return expr1
    else:
        if isinstance(expr1, list) and isinstance(expr2, list):
            return [expr1[0],
                    crossover(expr1[1], expr2[1], depth + 1),
                    crossover(expr1[2], expr2[2], depth + 1)]
        else:
            return expr1

def selection(population):
    total_fitness = sum(fitness(ind) for ind in population)
    if total_fitness == 0:
        return random.choices(population, k=POPULATION_SIZE)
    selection_probs = [fitness(ind) / total_fitness for ind in population]
    selected = random.choices(population, weights=selection_probs, k=POPULATION_SIZE)
    return selected

def evolve(population):
    sorted_population = sorted(population, key=lambda ind: fitness(ind), reverse=True)
    new_population = sorted_population[:ELITISM_COUNT]
    selected_parents = selection(population)
    while len(new_population) < POPULATION_SIZE:
        parent1 = random.choice(selected_parents)
        parent2 = random.choice(selected_parents)
        child = crossover(parent1, parent2)
        child = mutate(child)
        new_population.append(child)
    return new_population

def print_expression(expr):
    if isinstance(expr, list):
        return f"({print_expression(expr[1])} {expr[0]} {print_expression(expr[2])})"
    else:
        return str(expr)

population = [create_random_expression() for _ in range(POPULATION_SIZE)]

for generation in range(GENERATIONS):
    population = evolve(population)
    best_individual = max(population, key=lambda ind: fitness(ind))
    best_fitness = fitness(best_individual)
    print(f"Generation {generation + 1}: Best Fitness = {best_fitness}")

best_individual = max(population, key=lambda ind: fitness(ind))
print("\nBest Solution Expression:")
print(print_expression(best_individual))

included_items, total_weight, total_time = get_included_items(best_individual)
selected_items = [items[i] for i in included_items]
print("\nSelected Items:")
for item in selected_items:
    print(f"Weight: {item[0]}, Value: {item[1]}, Time: {item[2]}")
print(f"\nTotal Weight: {total_weight}, Total Time: {total_time}")
