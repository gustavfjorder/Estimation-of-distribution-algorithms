import random
import TSP

def optimize(TSPInstance:TSP, maxIterations):
    # Initial best solution is simply [0,1,2,...]
    bestSolution = [i for i in range(TSPInstance.dim)]
    bestDistance = TSPInstance.tourLength(bestSolution)

    # Optimize
    for _ in range(maxIterations):

        newSolution = bestSolution.copy()

        if random.random()>=1/2:#TSPInstance.dim:
        # Switch two cities
            city1,city2 = 1,1
            while city1 == city2:
                city1 = random.randint(0,TSPInstance.dim-1)
                city2 = random.randint(0,TSPInstance.dim-1)
            newSolution[city1] = bestSolution[city2]
            newSolution[city2] = bestSolution[city1]

        else:
            # Switch random number of cities
            allCities = [i for i in range(TSPInstance.dim)]
            citiesToSwitch = []
            for _ in range(random.randint(2,TSPInstance.dim-1)):
                citiesToSwitch.append(allCities.pop(random.randrange(len(allCities))))
            
            for cityIndex in range(len(citiesToSwitch)-1):
                newSolution[citiesToSwitch[cityIndex]]=bestSolution[citiesToSwitch[cityIndex+1]]
            newSolution[citiesToSwitch[len(citiesToSwitch)-1]] = bestSolution[citiesToSwitch[0]]
        
        # Get tour distance
        newDistance = TSPInstance.tourLength(newSolution)

        # Update best
        if newDistance < bestDistance:
            bestDistance = newDistance
            bestSolution = newSolution.copy()

    return (bestSolution), bestDistance


