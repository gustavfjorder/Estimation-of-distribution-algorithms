import Sorting
import random
import math
import time
import numpy as np
from DistanceMeasures import *
from scipy import optimize
from Algorithms.MallowsTools import *

def Run(ProblemType, ProblemInstance, N, maxTime=60, NumberOfTemplateCuts = 0, findIdentity=False, DistanceMeasure = None):
    # seed = 12
    # random.seed(seed)
    # np.random.seed(seed)
    startTime = time.time()

    if N is None:
        N = 30*ProblemInstance.dim

    pop_size = N
    # pop_size = 1
    selection_size = N//2
    # selection_size = 1
    offspring_size = N-1
    # offspring_size = 1

    # Two parameters necessary for defining model
    central_permutation = None
    Theta = None

    if ProblemType == "TSP" and DistanceMeasure != None:
        DistanceMeasure = None
    elif ProblemType == "Sorting" and DistanceMeasure == None:
        DistanceMeasure = SwapDistance

    # Create initial population randomly
    population = [(ProblemInstance.Fitness(DistanceMeasure,individual), individual) for individual in [[i for i in np.random.permutation(ProblemInstance.dim)] for _ in range(pop_size)]]
    population = sorted(population, key = lambda t:(t[0],random.random()),reverse=True)

    canContinue = True
    while canContinue:

        # Make selection
        selection = population[:selection_size]


        ## Find central permutation using Borda algorithm
        # Find the average of each position
        averages = [0]*ProblemInstance.dim
        for i in range(ProblemInstance.dim):
            for individual in selection:
                averages[i] += individual[1][i]
            averages[i] = (averages[i]/len(selection), i)
        
        # Sort the averages
        averages = sorted(averages, key = lambda t:(t[0],random.random()))

        # Create central permutation
        central_permutation = [0]*ProblemInstance.dim
        for i in range(ProblemInstance.dim):
            central_permutation[averages[i][1]] = i
        # print(central_permutation)
        # print(central_permutation)
        # If we are solving the sorting problem and the central permutation is the identity, break
        if findIdentity and Sorting.IsIdentity(central_permutation):
            canContinue = False
            break

        # Calculate Theta
        sample = [perm for _,perm in selection]
        Theta = optimize.newton(LogLikelihood, 0.1, maxiter = 1000, tol = 0.0001, args=(sample, len(central_permutation), central_permutation,))
        # print(Theta)
        if Theta<0:
            raise error
        # print(Theta)
        # Make list for samples. Use length (offspring_size+1) so there is space for pop[0]
        sample = [None]*(offspring_size+1)
        sample[0] = population[0]

        for i in range(1,offspring_size+1):
            s = SampleMallowsModel(central_permutation,Theta)
            fitness = ProblemInstance.Fitness(DistanceMeasure, s)

            sample[i] = (fitness, s)

            # If we are solving the sorting problem and s is the identity, break and stop loop
            if findIdentity and Sorting.IsIdentity(s):
                canContinue = False
                # break
        
        # Sort the sample by fitness and make copy
        sample = sorted(sample, key = lambda t:(t[0],random.random()),reverse=True)
        population = [s for s in sample]

        # Check if we can continue
        if time.time()-startTime >= maxTime:
            canContinue = False
        if findIdentity and Sorting.IsIdentity(population[0][1]):
            canContinue = False
    
    # If we are solving the sorting problem, return the number of fitness evals and the time it took
    if findIdentity:
        return ProblemInstance.fitness_evaluations, time.time()-startTime

    # Return best permutation and its fitness
    return population[0][1], population[0][0]


