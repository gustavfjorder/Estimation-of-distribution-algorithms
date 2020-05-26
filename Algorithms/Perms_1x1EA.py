import random
import time
import numpy as np
from DistanceMeasures import *
import Sorting

# Performs (1+1)EA for permutations
# def Run(permutation,Fitness,DistanceMeasure,return_evaluations_and_time=True):
def Run(ProblemType, ProblemInstance, N, NumberOfTemplateCuts = 0, maxTime=60, findIdentity=False, DistanceMeasure = None):

    if ProblemType == "TSP" and DistanceMeasure != None:
        DistanceMeasure = None
    elif ProblemType == "Sorting" and DistanceMeasure == None:
        DistanceMeasure = SwapDistance

    
    # Start timer
    startTime = time.time()

    permutation = [i for i in np.random.permutation(ProblemInstance.dim)]
    n = len(permutation)

    canContinue = True
    while canContinue:
        new_permutation = [e for e in permutation]
        for index in range(n):
            swap_this_element = random.random()<1/n
            if swap_this_element:
                swap_with_index = random.choice(list(range(n)))

                # Swap elements
                temp = new_permutation[swap_with_index]
                new_permutation[swap_with_index] = new_permutation[index]
                new_permutation[index] = temp
        
        # Check if improved
        if ProblemInstance.Fitness(DistanceMeasure,new_permutation) > ProblemInstance.Fitness(DistanceMeasure,permutation):
            permutation = [e for e in new_permutation]
        
        # Check if we can continue
        if time.time()-startTime >= maxTime:
            canContinue = False
        if findIdentity and Sorting.IsIdentity(permutation):
            canContinue = False

    if findIdentity:
        return ProblemInstance.fitness_evaluations, time.time()-startTime

    return permutation, ProblemInstance.Fitness(DistanceMeasure,permutation)
