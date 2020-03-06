import TSP
from Algorithms import SwitchTwo,EHBSA
import visualization
import time

# Start timer
startTime = time.time()

# Get TSP instance
TSPInstance = TSP.TSP()
TSPInstance = TSPInstance.loadProblem("TSP_instances/berlin52.txt")

# # Optmize
# bestSolution, bestDistance = EHBSA.optimize(TSPInstance,10000,2)
# print("Best solution:",bestSolution)
# print("Best distance:",bestDistance)

# # End timer
# endTime = time.time()
# print(endTime-startTime)

# # Visualize
# visualization.visualize(TSPInstance,bestSolution,bestDistance)

# Plot best solution as function of number of individuals in population
import matplotlib.pyplot as plt
x = []
y = []
for numOfIterations in [10,20,50,70,100,500,1000,3000,6000,10000,15000,20000]:
    bestSolution, bestDistance = EHBSA.optimize(TSPInstance,numOfIterations,5)
    x.append(numOfIterations)
    y.append(bestDistance)
    print("Finished",numOfIterations)
plt.plot(x,y)
plt.show()