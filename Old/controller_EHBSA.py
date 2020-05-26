import ProblemTypes.TSP as TSP
import ProblemTypes.Sorting as Sorting

from Algorithms import Perms_1x1EA, EHBSA, EHBSA_wt, MallowsModel, GeneralizedMallowsModel, UMDA
# import visualization
import time
import numpy as np

# Start timer
startTime = time.time()

Algorithms = [Perms_1x1EA, EHBSA, EHBSA_wt, MallowsModel, GeneralizedMallowsModel, UMDA]
Algorithms = [MallowsModel]#, EHBSA_wt, MallowsModel, GeneralizedMallowsModel, UMDA]
Algorithms = [EHBSA]
# Get TSP instance
TSPInstance = TSP.TSP()
# TSPInstance = TSPInstance.loadProblem("TSP_instances/test_small_4.txt")
# TSPInstance = TSPInstance.loadProblem("TSP_instances/test_small_10.txt")
# TSPInstance = TSPInstance.loadProblem("TSP_instances/ulysses22.txt")

maxTime = 60

for Algorithm in Algorithms:
    print("\nAlgorithm ",Algorithm)
    # # # Optmize TSP using EHBSA
    # bestSolution, bestFitness = Algorithm.Run("TSP", TSPInstance, None, NumberOfTemplateCuts=3, maxTime = maxTime)
    # print("Best solution:",bestSolution)
    # print("Best distance:",-bestFitness)


    # Create Sorting instance
    SortingInstance = Sorting.Sorting(25)

    # Optmize Sorting using EHBSA
    fitness_evals, time_used = Algorithm.Run("Sorting",SortingInstance, 10, maxTime = 60*5, NumberOfTemplateCuts=3, findIdentity = True)
    print("Fitness evals:",fitness_evals)
    print("Time used:",round(time_used,2))













# # # End timer
# endTime = time.time()
# print(endTime-startTime)

# # # Visualize
# visualization.visualize(TSPInstance,bestSolution,bestDistance)
# opt_sol = [x-1 for x in [1,14,13,12,7,6,15,5,11,9,10,19,20,21,16,3,2,17,22,4,18,8]]
# opt_dist = TSPInstance.tourLength(opt_sol)
# visualization.visualize(TSPInstance,opt_sol,opt_dist)

