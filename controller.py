import TSP
from Algorithms import SwitchTwo,EHBSA,EDA_2OPT_LS
import visualization
import time

# Start timer
# startTime = time.time()

# Get TSP instance
TSPInstance = TSP.TSP()
TSPInstance = TSPInstance.loadProblem("TSP_instances/ulysses22.txt")

# Optmize using EHBSA
# bestSolution, bestDistance = EDA_2OPT_LS.optimize(TSPInstance, 1000, 6, startTime)
# print("Best solution:",bestSolution)
# print("Best distance:",bestDistance)

# # End timer

# endTime = time.time()
# print("Total time:",(time.time()-startTime)//60,":",(time.time()-startTime)%60)

# # Visualize
# visualization.visualize(TSPInstance,bestSolution,bestDistance)
# opt_sol = [x-1 for x in [1,14,13,12,7,6,15,5,11,9,10,19,20,21,16,3,2,17,22,4,18,8]]
# print(opt_sol)
# opt_dist = TSPInstance.tourLength(opt_sol)
# visualization.visualize(TSPInstance,opt_sol,opt_dist)

# # Plot time taken to find best solution as function of number of individuals in population
import matplotlib.pyplot as plt
x = []
y = []
sols = []
for numOfIndividuals in [i for i in range(2,50)]:#,50,100,500,1000,3000,6000,10000,15000,25000,40000,60000]:
    startTime = time.time()
    for trial in range(3):
        bestSolution, bestDistance = EDA_2OPT_LS.optimize(TSPInstance,100000,numOfIndividuals,startTime, fastRestart = True)
    totalTime = round(time.time()-startTime)
    timePerTrial = totalTime/3
    x.append(numOfIndividuals)
    y.append(totalTime)
    sols.append(bestSolution)
    print("Finished",numOfIndividuals,"in",int(time.time()-startTime),"seconds")
    print("Best distance",bestDistance)
    print("Best solution",bestSolution)
    print()
plt.plot(x,y,label="With fast restart")


x = []
y = []
sols = []
for numOfIndividuals in [i for i in range(2,50)]:#,50,100,500,1000,3000,6000,10000,15000,25000,40000,60000]:
    startTime = time.time()
    for trial in range(3):
        bestSolution, bestDistance = EDA_2OPT_LS.optimize(TSPInstance,100000,numOfIndividuals,startTime, fastRestart = False)
    totalTime = round(time.time()-startTime)
    timePerTrial = totalTime/3
    x.append(numOfIndividuals)
    y.append(totalTime)
    sols.append(bestSolution)
    print("Finished",numOfIndividuals,"in",int(time.time()-startTime),"seconds")
    print("Best distance",bestDistance)
    print("Best solution",bestSolution)
    print()
plt.plot(x,y,label="Without fast restart")
plt.legend()


plt.xlabel("Number of individuals in population")
plt.ylabel("Time taken to find optimal tour (s)")
plt.show()
# visualization.visualize(TSPInstance,bestSolution,bestDistance)
print(bestSolution,bestDistance)

# x = []
# y = []
# sols = []
# for numOfIterations in [10,50,100,500,1000,3000,6000,10000,15000,25000,40000,60000]:
#     bestSolution, bestDistance = EHBSA.optimize(TSPInstance,numOfIterations,5,NumberOfTemplateCuts=3)
#     x.append(numOfIterations)
#     y.append(bestDistance)
#     sols.append(bestSolution)
#     print("Finished",numOfIterations,"in",int(time.time()-startTime),"seconds")
#     print("Best distance",bestDistance)
#     print("Best solution",bestSolution)
#     print()
# # # End timer
# endTime = time.time()
# print(endTime-startTime)

# plt.plot(x,y)
# plt.legend(["Without template","With template (n=3)"],loc="upper left")
# plt.xlabel("Number of iterations")
# plt.ylabel("Shortest tour found")
# plt.show()
# print(bestSolution,bestDistance)
# visualization.visualize(TSPInstance,bestSolution,bestDistance)