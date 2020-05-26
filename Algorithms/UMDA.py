import Sorting
import random
import math
import time
import numpy as np
import copy
from DistanceMeasures import *

def normalize(probs):
    prob_factor = 1 / sum(probs)
    return [prob_factor * p for p in probs]


def SampleOffspring(P_global):
    P = copy.deepcopy(P_global)
    identity = list(range(len(P)))
    offspring = [None]*len(P)

    for i in range(len(offspring)):
        p = P[i]
        element = np.random.choice(identity,p=p)
        offspring[i] = element

        # Normalize probability vector for selected element
        for index in range(i+1,len(P)):
            P[index][element] = 0
            P[index] = normalize(P[index])
        
    return offspring



def Run(ProblemType, ProblemInstance, N, maxTime=60, epsilon = 0.05, NumberOfTemplateCuts = 0, findIdentity=False, DistanceMeasure = None):
    # seed = 12
    # random.seed(seed)
    # np.random.seed(seed)
    startTime = time.time()
   
    # Permutation size
    n = ProblemInstance.dim

    if ProblemType == "TSP" and DistanceMeasure != None:
        DistanceMeasure = None
    elif ProblemType == "Sorting" and DistanceMeasure == None:
        DistanceMeasure = SwapDistance

    if N is None:
        N = ProblemInstance.dim

    # Population size
    population_size = N

    # Sample size
    sample_size = 8*population_size

    # Epsilon
    # epsilon = 0.1

    t = 0
    # Generate N points randomly 
    population = [None] * population_size
    new_sample = [None] * sample_size

    # Probabilities
    P = [[1/n]*n for _ in range(n)]

    best_permutation = None
    best_fitness = None

    canContinue = True
    while canContinue:
        
        for j in range(sample_size):
            individual = SampleOffspring(P)
            fitness = ProblemInstance.Fitness(DistanceMeasure,individual)
            new_sample[j] = (fitness, individual)
            
            if best_fitness is None:
                best_permutation = [i for i in individual]
                best_fitness = fitness
            
            if time.time()-startTime >= 1.5*maxTime:
                if any(e is None for e in new_sample):
                    new_sample = [e for e in new_sample if e is not None]
                break

                
        
        new_sample = sorted(new_sample, key = lambda t:(t[0],random.random()),reverse=True)
        population = new_sample[:population_size]

        if population[0][0]>best_fitness:
            best_permutation = [i for i in population[0][1]]
            best_fitness = population[0][0]

        # Update probabilities
        for i in range(n):
            P[i] = [epsilon]*n
            
            for s in population:
                P[i][s[1][i]] += 1 
            
            P[i] = normalize(P[i])


        # Check if we can continue
        if time.time()-startTime >= maxTime:
            canContinue = False
        if findIdentity and Sorting.IsIdentity(population[0][1]):
            canContinue = False
    
    # If we are solving the sorting problem, return the number of fitness evals and the time it took
    if findIdentity:
        return ProblemInstance.fitness_evaluations, time.time()-startTime

    # Return best permutation and its fitness
    return best_permutation, best_fitness





