__author__ = 'Tom'

import random
import operator
import math

layers = 3

generation_size = 150 # TODO change?

proportion = 0.3  # TODO change?
input_size = 234
l1_size = 10  # TODO change?
l2_size = 6 # TODO change?
output_size = 4


mutation_prob = 0.1
change_prob = 0.9

expected_mutation = 1.0
std = 0.1
std_change = 0.08

num_of_keep = 5


# creates a single random nn
def create_nn():


    nn = [[[0 for i in xrange(input_size)] for i in xrange(l1_size)],\
          [[0 for i in xrange(l1_size)] for i in xrange(l2_size)],\
          [[0 for i in xrange(l2_size)] for i in xrange(output_size)]]
    """

    nn = [[[0 for i in xrange(input_size)] for i in xrange(l1_size)],\
          [[0 for i in xrange(l1_size)] for i in xrange(output_size)]]
    """
    #random.gauss(expected_mutation,std)
    #nn = [[[0 for i in xrange(input_size)] for i in xrange(output_size)]]

    return nn


# initializes @generation_size random neural networks
def init():
    nns = []
    for i in xrange(generation_size):
        nns.append(create_nn())
        mutation(nns[i])

    return nns


# creates a new child from the parents
def crossover(parent1, parent2):
    child = create_nn()
    for i in xrange(len(parent1)):
        for j in xrange(len(parent1[i])):
            witch_p = bool(random.getrandbits(1))
            if witch_p:
                child[i][j] = list(parent1[i][j])
            else:
                child[i][j] = list(parent2[i][j])
    return child


def crossover2(parent1, parent2):
    child = create_nn()

    for i in xrange(len(parent1)):
        for j in xrange(len(parent1[i])):
            for k in xrange(len(parent1[i][j])):
                witch_p = bool(random.getrandbits(1))
                if witch_p:
                    child[i][j][k] = parent1[i][j][k]
                else:
                    child[i][j][k] = parent2[i][j][k]
    return child


# creates mutations in the child
def mutation(child):
    for i in xrange(len(child)):
        for j in xrange(len(child[i])):
            for k in range(len(child[i][j])):
                r = random.uniform(0, 1)
                if r < mutation_prob:
                    r = random.uniform(0, 1)
                    if r > change_prob:
                        child[i][j][k] = random.gauss(expected_mutation,std)
                    else:
                        child[i][j][k] += random.gauss(0,std_change)


# selects @proportion of the existing population to breed a new generation
# last_gen is a dict with (NN, fitness)
#
def selection(last_gen):
    size = 1/proportion

    potential_parents = []
    while len(last_gen) > 0:
        tournament = []
        tour_size = int(min(size, len(last_gen)))
        for i in xrange(tour_size):
            chosen_nn = random.choice(last_gen)
            tournament.append(chosen_nn)
            last_gen.remove(chosen_nn)

        best_fit = -1

        for nn in tournament:
            if nn[1] > best_fit:
                best_fit = nn[1]
                best_nn = nn

        potential_parents.append(best_nn)

    return potential_parents


def deterministic_selection(last_gen):


    potential_parents = sorted(last_gen, key=lambda x: x[1], reverse=True)

    potential_parents = potential_parents[:int(proportion*len(potential_parents))]


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
# O(size)
def select_parent(potential_parents):
    size = 10  # TODO change?

    tournament = []

    for i in xrange(size):
        chosen_nn = random.choice(potential_parents)
        tournament.append(chosen_nn)

    best_fit = -1

    for nn in tournament:
        if nn[1] > best_fit:
            best_fit = nn[1]
            best_nn = nn[0]

    return best_nn


# uses select, crossover and mutation to generate a new generation
# last_gen is a dict with (NN, fitness)
def generate_new_gen(last_gen):
    new_gen = []

    sorted_last_gen = sorted(last_gen, key=lambda x: x[1], reverse=True)

    #print([int(p[1]) for p in sorted_last_gen])
    for i in xrange(num_of_keep):
        new_gen.append(sorted_last_gen[i][0])
    potential_parents = deterministic_selection(last_gen)

    #print([int(p[1]) for p in sorted(potential_parents, key=lambda x: x[1], reverse=True)])

    for i in xrange(generation_size-num_of_keep):
        p1 = select_parent(potential_parents)
        p2 = select_parent(potential_parents)
        child = crossover(p1, p2)
        mutation(child)
        new_gen.append(child)
    return new_gen


def tester():
    gen = init()
    for i in xrange(len(gen)):
        gen[i] = (gen[i],5)

    for i in xrange(10):
        print i
        gen = generate_new_gen(gen)
        for i in xrange(len(gen)):
            gen[i] = (gen[i],5)

    print_nn(gen[0][0])


def testInit():
    gen = init()
    print_nn(gen[1])


def print_nn(nn):
    for i in xrange(len(nn)):
        for j in xrange(len(nn[i])):
            print nn[i][j]
        print


testInit()

