__author__ = 'Tom'

import random
import operator

generation_size = 100  # TODO change?
proportion = 0.3 # TODO change?


# initializes @generation_size random neural networks
def init():
    pass


# creates a new child from the parents
def crossover(parent1, parent2):
    pass


# creates mutations in the child
def mutation(child):
    pass


# selects @proportion of the existing population to breed a new generation
# last_gen is a dict with (NN, fitness)
def selection(last_gen):
    fit_sum = 0
    last_gen = {}

    for nn in last_gen:
        sum += last_gen.get(nn)

    for nn in last_gen:
        last_gen[nn] /= sum

    last_gen = sorted(last_gen.items(), key=operator.itemgetter(0), reverse=True)

    for i in xrange(len(last_gen)-1):
        last_gen[i+1] += last_gen [i]

    r = random.uniform(0, 1)

    i = 0
    while i < len(last_gen) and last_gen[i] < r:
        i += 1

    # TODO complete


   



# selects an individual parent to breed a new child
# potential_parents is a dict with (NN, fitness)
# tournament selection
def select_parent(potential_parents):
    tournament = {}
    size = 10 # TODO change?

    for i in xrange(size):
        tournament.update({random.choice(potential_parents)})

    best_fit = -1

    for nn in tournament:
        if tournament.get(nn) > best_fit:
            best_fit = tournament.get(nn)
            best_nn = nn
    return nn


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



