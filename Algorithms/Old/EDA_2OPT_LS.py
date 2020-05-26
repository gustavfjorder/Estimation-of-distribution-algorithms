import math
import numpy as np
import random
import copy
import time

def optimize(TSPinstance,maxIterations, N,startTime, fastRestart):#,N, NumberOfTemplateCuts = 0):
    """Optimizes using EDA with 2-OPT local search
    
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
    ## Step 0: Useful parameters
    # Population size
    n = TSPinstance.dim
    # Number of new solutions generated at each generation
    M = N//2 
    # Number of generations in the restart condition
    L = 30 # TODO change back to 30
    # Control parameter for Guided Mutation
    alpha = 0.3 # try with 0.5
    # Control parameter for Updating Probability Matrix
    beta = 0.3 # try with 0.1


    ## Step 1: Initialization as described by 2.2
    # Start time 
    t = 0
    # Create N individuals at random 
    individuals = [np.random.permutation(TSPinstance.dim) for _ in range(N)]

    # Improve the individuals
    population = []
    bestSolutionLength = math.inf
    print("Starting initial 2-opt on population")
    for solution in individuals:
        newSolution, newSolutionLength = LocalSearch_2OPT(solution, TSPinstance)
        population.append((newSolution,newSolutionLength))
        # Update best solution
        if newSolutionLength < bestSolutionLength:
            bestSolutionLength = newSolutionLength
            bestSolution = newSolution
    print("Finished initial 2-opt on population in",(time.time()-startTime)//60,":",(time.time()-startTime)%60)
    # Initialize probability matrix
    val = 1/n
    probMatrix = [[val for _ in range(n)] for _ in range(n)]

    # Update probability matrix with values based on initial population
    UpdateProbabilityMatrix(beta,n,N,population,probMatrix)
    
    RunStepTwo = True
    oldAverageLength = 0
    averageLength_UnchangedFor_Generations = 0
    while RunStepTwo:
        print("Run",t)
        print("Lengths",[e[1] for e in population])
        ## Step 2: guided mutation for j=1,2,...,M
        # Keep track of individuals in population so we dont pick the same twice
        possiblePicks = [i for i in range(N)]
        M_new_solutions = []
        for j in range(M):
            # Pick random individual in population
            solution = population[possiblePicks.pop(random.randint(0,len(possiblePicks)-1))][0]
            # Create new solution using Guided Mutation
            newSolution = GuidedMutation(alpha,solution,n,probMatrix)
            # Improve new solution using 2-OPT Local Search
            newSolution, newSolutionLength = LocalSearch_2OPT(newSolution,TSPinstance)
            # Save new solution
            M_new_solutions.append((newSolution,newSolutionLength))
        ## Step 3: New population
        # Choose the N best solutions from M_new and Population
        union = population + M_new_solutions
        population = sorted(union,key=lambda x:x[1])[0:N]
        
        # Update time
        t += 1
        # Update best solution
        if population[0][1] < bestSolutionLength:
            bestSolution = population[0][0]
            bestSolutionLength = population[0][1]
            print(bestSolutionLength,"found here 1 at",(time.time()-startTime)//60,":",(time.time()-startTime)%60)
        # Update probability matrix
        UpdateProbabilityMatrix(beta,n,N,population,probMatrix)
    
        stoppingConditionMet = t > maxIterations or round(bestSolutionLength,2)<=75.31
        if stoppingConditionMet:
            return bestSolution, bestSolutionLength
        
        newAverageLength = sum([sol[1] for sol in population])//N
        if newAverageLength == oldAverageLength:
            averageLength_UnchangedFor_Generations += 1
            print("Same for",averageLength_UnchangedFor_Generations,"runs")
        else:
            averageLength_UnchangedFor_Generations = 0
        oldAverageLength = newAverageLength

        restartCondition1Met = averageLength_UnchangedFor_Generations>L
        # If all rows have n-1 probabilities that are 0 then we are no longer generating new solutions 
        restartCondition2Met = fastRestart and all([sum([round(e,3)==0 for e in l])==(n-1) for l in probMatrix])

        if restartCondition1Met or restartCondition2Met:
            print("Restarting due to condition",1 if restartCondition1Met else 2)
            ## Step 6
            bestNewSolution = None
            bestNewSolutionLength = math.inf
            population = []
            for _ in range(N):
                newSolution, newSolutionLength = Restart(probMatrix,n,TSPinstance)
                population.append((newSolution, newSolutionLength))
                if newSolutionLength < bestNewSolutionLength:
                    bestNewSolution = newSolution
                    bestNewSolutionLength = newSolutionLength
            if bestSolutionLength > bestNewSolutionLength:
                bestSolutionLength = bestNewSolutionLength
                bestSolution = bestNewSolution
                print(bestSolutionLength,"found here 2 at",(time.time()-startTime)//60,":",(time.time()-startTime)%60)
            print("Prob matrix before",probMatrix)
            UpdateProbabilityMatrix(beta,n,N,population,probMatrix)
            print("Prob matrix after",probMatrix)
            averageLength_UnchangedFor_Generations = 0


    return 
    


## 2-OPT Local search
def LocalSearch_2OPT(solution, TSPinstance):
    newBestFound = True
    bestSolutionLength = math.inf
    bestSolution = [city for city in solution]
    while newBestFound:
        newBestFound = False

        # Search through all swaps of this solution
        for i in range(len(solution)):
            if newBestFound:
                break
            for j in range(i+1,len(solution)):
                if newBestFound:
                    break
                temp = bestSolution[i]
                bestSolution[i] = bestSolution[j]
                bestSolution[j] = temp
                
                # TODO this can be optimized by simply looking at the difference in length of the swap instead of recalculating the whole thing
                newSolutionLength = TSPinstance.tourLength(bestSolution) 
                if newSolutionLength < bestSolutionLength:
                    bestSolutionLength = newSolutionLength
                    newBestFound = True
                else:
                    temp = bestSolution[i]
                    bestSolution[i] = bestSolution[j]
                    bestSolution[j] = temp

    return bestSolution, bestSolutionLength



## 2.3 Update of prob. matrix
def UpdateProbabilityMatrix(beta, n, N, population, probMatrix):
    for i in range(n):
        for j in range(n):
            sum_of_I = 0
            for element in population:
                # Get index of city i
                individual = element[0]
                idx = individual.index(i)
                # if (idx == n-1 and j == individual[0]) or (idx < n-1 and j == individual[idx+1]):
                if j == individual[(idx+1)%n]: 
                    sum_of_I += 1
            probMatrix[i][j] = round((1-beta)/N*sum_of_I+beta*probMatrix[i][j],5)



## 2.4 Generation of new solutions: guided mutation
def GuidedMutation(alpha, existingSolution, n, probMatrixOriginal):
    probMatrix = copy.deepcopy(probMatrixOriginal)
    newSolution = [-1 for _ in range(n)]
    number_of_K = round(alpha*n)
    assert(0 < number_of_K and number_of_K <= n)

    # Step 1
    K = random.sample([city for city in range(n)],k=number_of_K)
    V = [element for element in list(range(n)) if element not in K]
    U = list(range(n))
    
    # Step 2
    for i in K:
        newSolution[i] = existingSolution[i]
        U.remove(existingSolution[i])

    # Step 3
    ## Adjusted from QAP to TSP
    for i in K:
        for row in probMatrix:
            row[existingSolution[i]] = 0

    while len(K)>0:
        i = K[random.randint(0,len(K)-1)]
        if newSolution[(i+1)%n] != -1:
            K.remove(i)
        else:
            prev = newSolution[i]
            probabilities = probMatrix[prev]
            # assert(round(sum(probabilities),2)==1)
            probDistSum = sum(probabilities)
            if round(probDistSum,3) == 0:
                # choose random city from the remaining cities
                nextCity = U.pop(random.randint(0,len(U)-1))
            else:
                probDistNormalized = [p/probDistSum if probDistSum>0 else 0 for p in probabilities]
                nextCity = random.choices(population = list(range(n)), weights = probDistNormalized, k=1)[0]
                U.remove(nextCity)
                assert(round(sum(probDistNormalized),2)==1)

            # if round(sum(probDistNormalized),2)!=1:


            newSolution[(i+1)%n] = nextCity
            for row in probMatrix:
                row[nextCity] = 0
            K.remove(i)
            

            K.append((i+1)%n)

    assert(all([newSolution.count(x)==1 for x in list(range(n))]))
    return newSolution    

# Step 2.5: Restarting
def Restart(probMatrixOriginal,n,TSPinstance):
    probMatrix = copy.deepcopy(probMatrixOriginal)
    for i in range(n):
        for j in range(n):
            probMatrix[i][j] = 1-probMatrix[i][j]

    newSolution = [-1 for _ in range(n)]

    U = list(range(n))
    
    ## Adjusted from QAP to TSP
    # Find first city
    newSolution[0] = U.pop(random.randint(0,len(U)-1))
    for row in probMatrix:
        row[newSolution[0]] = 0

    # Find rest of cities
    for i in range(n-2):
        prev = newSolution[i]
        probabilities = probMatrix[prev]
        probDistSum = sum(probabilities)
        probDistNormalized = [p/probDistSum if probDistSum>0 else 0 for p in probabilities]
        if round(sum(probDistNormalized),2)!=1:
            assert(round(sum(probDistNormalized),2)==1)

        nextCity = random.choices(population = list(range(n)), weights = probDistNormalized, k=1)[0]
        newSolution[i+1] = nextCity
        for row in probMatrix:
            row[nextCity] = 0
        U.remove(nextCity)
    newSolution[n-1] = U[0]
    assert(all([newSolution.count(x)==1 for x in list(range(n))]))

    # Improve solution using 2-opt local search
    newSolution, newSolutionLength = LocalSearch_2OPT(newSolution,TSPinstance)

    return newSolution, newSolutionLength
