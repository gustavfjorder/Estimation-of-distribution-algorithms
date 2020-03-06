import random
import copy
import numpy as np

def optimize(TSPinstance,maxIterations,N):
    # Number of individuals in population
    # N = 1
    
    # Length of solutions
    L = TSPinstance.dim

    # Define B_ratio that controls pressure towards random permutations and calculate epsilon
    B_ratio = 0.04
    epsilon = (2*N)/(L-1)*B_ratio
    
    # Create N individuals at random 
    individuals = [np.random.permutation(L) for _ in range(N)]

    # Generate initial EHM
    EHM = [[0 for _ in range(L)] for _ in range(L)]

    # Fill EHM
    for i in range(L):
        for j in range(L):
            EHM[i][j] = e(i,j,epsilon,N,L,individuals)

    for _ in range(maxIterations):
        # Sample new individual
        newIndividual = sampleNewIndividual(N,L,EHM)
        
        # Compare new individual to a random exisiting individual
        randomExisitingIndividual = random.randint(0,N-1)
        if TSPinstance.tourLength(newIndividual)<TSPinstance.tourLength(individuals[randomExisitingIndividual]):
            individuals[randomExisitingIndividual] = newIndividual.copy()
            # Recalculate EHM
            for i in range(L):
                for j in range(L):
                    EHM[i][j] = e(i,j,epsilon,N,L,individuals)

    
    
    bestSolution = 0
    bestDistance = TSPinstance.tourLength(individuals[0])
    for individual in range(1,N):
        distance = TSPinstance.tourLength(individuals[individual])
        if distance < bestDistance:
            bestDistance = distance
            bestSolution = individual
    return individuals[bestSolution], bestDistance




# Delta function
def delta(i,j,k,L,individuals):
    """Returns 1 if i and j are consective in individual k, otherwise 0
    
    Arguments:
        i {int} -- index of first city
        j {int} -- index of second city
        k {int} -- individual of population to look at
    
    Returns:
        int -- 1 if i and j appear at index x and x+1, otherwise 0
    """
    for index in range(L):
        if individuals[k][index]==i and individuals[k][(index+1)%L]==j:
            return 1
    return 0

def e(i,j,epsilon,N,L,individuals):
    """Calculates single value for edge histogram matrix at position i,j
    
    Arguments:
        i {int} -- index 1
        j {int} -- index 2
    
    Returns:
        float -- value for edge histogram matrix
    """
    if i==j:
        return 0
    return sum(delta(i,j,k,L,individuals) + delta(j,i,k,L,individuals) for k in range(N)) + epsilon

def sampleNewIndividual(N,L,EHM):

    # Array to represent new individual
    newIndividual = [None for _ in range(L)]

    # randomly select initial element
    newIndividual[0] = random.randint(0,L-1)

    # Create a copy of EHM in which we set values to 0 to simulate roulette wheel
    EHM_RouletteWheel = copy.deepcopy(EHM)

    # Sample a new city
    for i in range(1,L):

        # Set probability of re-drawing previous city to 0 to avoid cycles
        for usedIndex in range(L):
            EHM_RouletteWheel[usedIndex][newIndividual[i-1]] = 0

        # Normalize probabilities so we can select a new element
        probDistSum = sum(EHM_RouletteWheel[newIndividual[i-1]])
        probDistNormalized = [p/probDistSum if probDistSum>0 else 0 for p in EHM_RouletteWheel[newIndividual[i-1]]]

        # Check that the sum of normalized probabilites is 1
        # print(EHM_RouletteWheel)
        if round(sum(probDistNormalized),3)!=1:
            # print(i,EHM_RouletteWheel)
            print(newIndividual)
        assert(round(sum(probDistNormalized),3)==1) 

        # Draw new city
        newIndividual[i] = random.choices(population = list(range(L)), weights = probDistNormalized,k=1)[0]

    return newIndividual


# print(probDist)
# print(probDistNormalized)
# for i in range(1,L):


# print(EHM)