import math
import random

def SampleProbDist(theta, j, n):
    j += 1
    prob = 0
    rand = random.random()
    for r in range(n):
        prob += math.exp(-theta*r)/Psi_j(j,theta,n)
        print(prob)
    #     if rand<prob:

    #         return r
    # # print("returning r=",r)
    # return r 
    # print("Random that got to here:",rand,"prob:",prob,"r:",r)


def Psi_j(j,Theta,n):
    return (1-math.exp(-(n-j+1)*Theta))/(1-math.exp(-Theta))


# theta = 0.5
# SampleProbDist(theta,,10)

def InvertPermutation(permutation):
    inv_permutation = [permutation.index(j) for j in range(len(permutation))]
    return inv_permutation

a = [0,3,8,5,10,9,4,6,1,7,2]
res = InvertPermutation(a)
res = InvertPermutation(res)
print(res)