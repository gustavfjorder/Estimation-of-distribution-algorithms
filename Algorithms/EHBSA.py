import random
import copy
import numpy as np

def optimize(TSPinstance,maxIterations,N, NumberOfTemplateCuts = 0):
    """Optimizes using EHBSA
    
    Arguments:
        TSPinstance {TSP} -- The instance of TSP for which a solution is needed
        maxIterations {int} -- Number of iterations to run algorithm
        N {int} -- Number of individuals in population
    
    Keyword Arguments:
        NumberOfTemplateCuts {int} -- Number of cuts when running algorithm. Use 0 to get EHBSA/WO (default: {0})
    
    Returns:
        Solution -- The best permutation found
        Distance -- The length of the best tour found 
    """
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
        if NumberOfTemplateCuts <= 1:
            newIndividual = sampleNewIndividual(N,L,EHM)
        else:
            randomIndividual = random.choice(individuals)
            newIndividual = sampleNewIndividualWithTemplate(N,L,EHM,randomIndividual,NumberOfTemplateCuts)

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

def sampleNewIndividualWithTemplate(N,L,EHM,randomIndividual,NumberOfTemplateCuts):

    # Array to represent new individual
    newIndividual = [city for city in randomIndividual]

    # Pick random cut points
    randomCutPoints = random.sample(range(L),NumberOfTemplateCuts)
    # TODO remove this assertion because it takes O(n^2)
    assert(all(randomCutPoints.count(x) == 1 for x in randomCutPoints))
    # Pick random points among the cut points
    startPoint = random.choice(randomCutPoints)
    # Find next point which will be end point
    endPoint = L
    for num in randomCutPoints:
        if num > startPoint and num < endPoint:
            endPoint = num
    if endPoint == L:
        endPoint = startPoint
        startPoint = min(randomCutPoints)

    rangeToMutate = list(range(startPoint,endPoint+1))
    for index in rangeToMutate:
        newIndividual[index] = -1

    # randomly select initial element
    newIndividual[startPoint] = randomIndividual[random.choice(rangeToMutate)]

    # Create a copy of EHM in which we set values to 0 to simulate roulette wheel
    EHM_RouletteWheel = copy.deepcopy(EHM)

    for i in range(L):
        for j in range(L):
            if j not in rangeToMutate:
                EHM_RouletteWheel[i][randomIndividual[j]] = 0
    # print(EHM_RouletteWheel)
    # Sample a new city
    for i in range(startPoint+1,endPoint+1):

        # Set probability of re-drawing previous city to 0 to avoid cycles
        for usedIndex in range(L):
            EHM_RouletteWheel[usedIndex][newIndividual[(i-1)%L]] = 0

        # Normalize probabilities so we can select a new element
        probDistSum = sum(EHM_RouletteWheel[newIndividual[(i-1)%L]])
        probDistNormalized = [p/probDistSum if probDistSum>0 else 0 for p in EHM_RouletteWheel[newIndividual[(i-1)%L]]]

        # Check that the sum of normalized probabilites is 1
        # print(EHM_RouletteWheel)
        if round(sum(probDistNormalized),3)!=1:
            # print(i,EHM_RouletteWheel)
            print("failed on",i,"with",sum(probDistNormalized))
            print(rangeToMutate)
            print(randomIndividual)
            print(newIndividual)
            print(randomIndividual[startPoint:endPoint])
            print(newIndividual[startPoint:endPoint])
        assert(round(sum(probDistNormalized),3)==1) 

        # Draw new city
        newIndividual[i] = random.choices(population = list(range(L)), weights = probDistNormalized,k=1)[0]
        if newIndividual[i] in newIndividual[:i]:
            print("goes wrong here")
    if any(newIndividual.count(x)>1 for x in list(range(0,L))):
        r = randomIndividual[startPoint:endPoint+1]
        rnew = newIndividual[startPoint:endPoint+1]
        print("somethings wrong here!")
    return newIndividual
