import TSP
import randomized
import visualization
import time

# Start timer
startTime = time.time()

# Get TSP instance
TSPInstance = TSP.TSP()
TSPInstance = TSPInstance.loadProblem("TSP_instances/berlin52.txt")

# Optmize
bestSolution, bestDistance = randomized.optimize(TSPInstance,1000000)
print("Best solution:",bestSolution)
print("Best distance:",bestDistance)

# End timer
endTime = time.time()
print(endTime-startTime)
# Visualize
visualization.visualize(TSPInstance,bestSolution,bestDistance)
