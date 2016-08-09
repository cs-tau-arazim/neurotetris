__author__ = 'Tom'

import random
import operator
import math

generation_size = 100  # TODO change?
proportion = 0.3  # TODO change?


# initializes @generation_size random neural networks
def init():
    #TODO change
    matList = [[[]]]
    return [matList for i in xrange(generation_size)]



# creates a new child from the parents
def crossover(parent1, parent2):
    pass


# creates mutations in the child
def mutation(child):
    pass


# selects @proportion of the existing population to breed a new generation
# last_gen is a dict with (NN, fitness)
# O(
def selection(last_gen):

    last_gen = {}  # TODO REMOVE
    size = 1/proportion

    potential_parents = {}
    while len(last_gen) > 0:
        tournament = {}
        tour_size = min(size, len(last_gen))
        for i in xrange(tour_size):
            chosen_nn = random.choice(last_gen)
            tournament.update({chosen_nn})
            last_gen.pop(chosen_nn)

        best_fit = -1

        for nn in tournament:
            if tournament[nn] > best_fit:
                best_fit = tournament.get(nn)
                best_nn = nn

            potential_parents.update({best_nn})

    return potential_parents


# selects an individual parent to breed a new child
# potential_parents is a dict with (NN, fitness)
# fitness proportionate selection
# O(nlogn)
def select_parent_fitness_proportionate(potential_parents):
    fit_sum = 0

    for nn in potential_parents:
        sum += potential_parents.get(nn)

    for nn in potential_parents:
        potential_parents[nn] /= sum

    potential_parents = sorted(potential_parents.items(), key=operator.itemgetter(0), reverse=True)

    for i in xrange(len(potential_parents) - 1):
        potential_parents[i + 1] += potential_parents[i]

    r = random.uniform(0, 1)

    # search TODO binary?
    i = 0
    while i < len(potential_parents) and potential_parents[i] < r:
        i += 1

    return potential_parents[i]


# selects an individual parent to breed a new child
# potential_parents is a dict with (NN, fitness)
# tournament selection
# O(nlogn)
def select_parent(potential_parents):
    potential_parents = {}  # TODO REMOVE
    size = 10  # TODO change?

    tournament = {}

    for i in xrange(size):
        chosen_nn = random.choice(potential_parents)
        tournament.update({chosen_nn})

    best_fit = -1

    for nn in tournament:
        if tournament[nn] > best_fit:
            best_fit = tournament.get(nn)
            best_nn = nn

    return best_nn

# uses select, crossover and mutation to generate a new generation
# last_gen is a dict with (NN, fitness)
def generate_new_gen(last_gen):
    potential_parents = selection(last_gen)
    new_gen = []
    for i in xrange(generation_size):
        p1 = select_parent(potential_parents)
        p2 = select_parent(potential_parents)
        child = crossover(p1, p2)
        mutation(child)
        new_gen.append(child)
    return new_gen
