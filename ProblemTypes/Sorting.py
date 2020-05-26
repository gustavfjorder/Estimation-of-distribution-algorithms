import numpy as np
from DistanceMeasures import *
class Sorting:
    def __init__(self,length):
        self.dim = length
        self.fitness_evaluations = 0

    def ResetFitnessCount(self):
        self.fitness_evaluations = 0

    def Fitness(self, func, solution):
        """Calculates fitness of solution
        
        Arguments:
            func {Function} -- Distance measure function
            solution {List} -- Order of cities to visit. Must contain integers from 0 to 51 for a problem of size 52
        
        Returns:
            Fitness [float] -- Fitness of tour/solution using given distance measure
        """
        self.fitness_evaluations += 1
        if func == HammingDistance:
            return -HammingDistance(solution)
        
        if func == SwapDistance:
            return -SwapDistance(solution)
        
        if func == CayleyDistance:
            return -CayleyDistance(solution)
        
        if func == PairsInCorrectOrder:
            return PairsInCorrectOrder(solution)
        
        if func == NumberOfSortedBlocks:
            return -NumberOfSortedBlocks(solution)
        
        if func == NegativeLengthOfLongestAscendingSubsequence:
            return NegativeLengthOfLongestAscendingSubsequence(solution)
        
# Returns true if permutation is identity permutation
def IsIdentity(permutation):
    # first = permutation[0]
    first = 0
    for i in range(len(permutation)):
        if i != permutation[(i+first)%len(permutation)]:
            return False
    return True

