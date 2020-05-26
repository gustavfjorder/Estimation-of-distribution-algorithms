import math
# from DistanceMeasures import V_j


def derivative(f, x, h):
      return (f(x+h) - f(x-h)) / (2.0*h)  # might want to return a small non-zero if ==0

def quadratic(x,y):
    return 2*x*x+5*x-1     # just a function to show it works

def solve(f, x0, h):
    lastX = x0
    nextX = lastX + 10* h  # "different than lastX so loop starts OK
    while (abs(lastX - nextX) > h):  # this is how you terminate the loop - note use of abs()
        newY = f(nextX)                     # just for debug... see what happens
        print("f(", nextX, ") = ", newY)    # print out progress... again just debug
        lastX = nextX
        nextX = lastX - newY / derivative(f, lastX, h)  # update estimate using N-R
    return nextX

# xFound = solve(quadratic, 5, 0.01)    # call the solver
# print("solution: x = ", xFound)        # print the result


from scipy import optimize

def V_j_mean(j, sample, central_permutation):
    sum_of_vs = 0
    for s in sample:
        obtained_simple = V_j(j,s,central_permutation)
        # inv_central = InvertPermutation(central_permutation)
        # composition = ComposePermutations(s, inv_central)
        # obtained_compose = V_j(j,composition)
        # if obtained_simple!=obtained_compose:
        # assert(obtained_simple == obtained_compose)
            # hi=1
            # inv_central = InvertPermutation(central_permutation)
            # composition = ComposePermutations(s, central_permutation)
            # obtained_compose = V_j(j,composition)
        sum_of_vs += obtained_simple
    
    mean = sum_of_vs/len(sample)
    return mean


def LogLikelihood(Theta, sample, n, central_permutation):
    left = 0
    sum_of_V_j_means1 = 0
    for j in range(n-1):
        sum_of_V_j_means1 += V_j_mean(j, sample, central_permutation)

    sum_of_V_j_means2 = 0
    for j in range(n):
        sum_of_V_j_means2 += V_j_mean(j, sample, central_permutation)

    assert(sum_of_V_j_means1==sum_of_V_j_means2)
    left = sum_of_V_j_means1

    first = (n-1)/(math.exp(Theta)-1)
    
    second1 = 0
    for j in range(1,n):
        second1 += (n-j+1)/(math.exp((n-j+1)*Theta)-1)
    
    second2 = 0
    for j in range(0,n-1):
        second2 += (n-j+1)/(math.exp((n-j+1)*Theta)-1)
    
    second = second2
    # assert(second1==second2)
    res = first - second - left
    return res


def LogLikelihoodSingleJ(Theta, j, sample, n, central_permutation):
    left = V_j_mean(j, sample, central_permutation)
    # left2 = V_j_mean(j, sample, central_permutation)
    j=j+1 # TODO what do we do with this?

    first = (1)/(math.exp(Theta)-1)
    
    second = (n-j+1)/(math.exp((n-j+1)*Theta)-1)
    
    # assert(second1==second2)
    res = first - second - left
    return res

## DELETE
def V(j,composition):
    if j>=len(composition):
        raise Error

    dist = 0
    
    for i in range(j+1,len(composition)):
        # if composition.index(i)<composition.index(j):
        if composition[j]>composition[i]:
            dist += 1
    return dist

def V_j(j_start, permutation, second_permutation):
    if second_permutation == None:
        raise Error
        second_permutation = [i for i in range(len(permutation))]
        # permutation = [i for i in range(len(permutation))]

    if j_start>=len(permutation):
        raise Error
    
    # First find composition of the two permutations
    # inv_permutation = [permutation.index(j) for j in range(len(permutation))]
    
    # inv_permutation = [permutation.index(j) for j in range(len(permutation))]

    # composition = [second_permutation[inv_permutation[j]] for j in range(len(permutation))]
    
    inv_permutation = [second_permutation.index(j) for j in range(len(permutation))]

    composition = [permutation[inv_permutation[j]] for j in range(len(permutation))]
    
    return V(j_start,composition)
    # X = [V(j,composition) for j in range(j_start,len(permutation)-1)]

    # return sum(X)

## END DELETE

def InvertPermutation(permutation):
    inv_permutation = [permutation.index(j) for j in range(len(permutation))]
    return inv_permutation

def ComposePermutations(p1, p2):
    composition = [p2[p1[j]] for j in range(len(p1))]
    return composition

# print("Test V")

# print(V(3,[4,5,2,1,0,3]))
# exit(0)
print("Test Vj_mean")
# sample = [[0,1,2,3],[3,1,2,0],[1,0,2,3]]
# central_permutation = [0,1,2,3,4]
correct_answer = 9
sample_permutation = [4,3,0,1,2]
central_permutation = [0,1,4,2,3]

# FROM WIKIPEDIA
sample_permutation = [0,1,2,3,4]
central_permutation = [2,3,0,1,4]
# central_permutation = [0,1,3,2]
# sample_permutation = [2,3,0,1]

sum_1 =0
sum_2 =0
sum_v = 0
n = len(central_permutation)
for j in range(n):
    sum_1 += V_j(j,sample_permutation,central_permutation)
    print(V_j(j,sample_permutation,central_permutation))

# print(sum_1)
# exit(0)

sample = [[0,1,3,2],[0,1,3,2],[0,1,3,2]]
# sample = [sample[0]]
n = len(sample[0])
central_permutation = [0,1,3,2]
Theta = 100
# print(LogLikelihood(0, sample, n, central_permutation))
import matplotlib.pyplot as plt

x = []
y = []
j=2
import numpy as np
for Theta in np.arange(0.001,5,0.1):
    x.append(Theta)
    # val = LogLikelihood(Theta, sample, n, central_permutation)
    val = LogLikelihoodSingleJ(Theta, j , sample, n, central_permutation)
    # print(val)
    y.append(val)

# x=[1,2,3]
# y=[1,2,3]
# plt.plot(x,y)
# plt.show()

j=2
# root = optimize.newton(quadratic,5, args=(1,))
root = optimize.newton(LogLikelihoodSingleJ, 0.1, tol=0.005, args=(j, sample, n, central_permutation,))
# root = optimize.newton(LogLikelihood, 0.1, args=(sample, n, central_permutation,))

print(root)