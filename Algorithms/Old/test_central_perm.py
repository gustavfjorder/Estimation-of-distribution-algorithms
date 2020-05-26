import numpy as np
import random

n = 10
selection = [(1,[i for i in np.random.permutation(n)]) for _ in range(100)]
averages = [0]*n
for i in range(n):
    for individual in selection:
        averages[i] += individual[1][i]
    
    averages[i] = (averages[i]/len(selection), i)


averages = sorted(averages, key = lambda t:(t[0],random.random()))

central_permutation = [0]*n
for i in range(n):
    central_permutation[averages[i][1]] = i

print(central_permutation)