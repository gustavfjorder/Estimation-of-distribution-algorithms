import random
import math

def SampleProbDist(theta, j, n):
    prob = 0
    rand = random.random()
    for r in range(10):
        prob += math.exp(-theta*r)/Psi_j(j,theta,n)
        if rand<prob:
            return r


def Psi_j(j,Theta,n):
    return (1-math.exp(-(n-j+1)*Theta))/(1-math.exp(-Theta))





def GetNewInvPermutation(Vs_vector):
    new = []
    length = len(Vs_vector)
    new.insert(0,length)
    for j in range(length-1,-1,-1):
        new.insert(Vs_vector[j],j)

    return new


def InvertPermutation(permutation):
    inv_permutation = [permutation.index(j) for j in range(len(permutation))]
    return inv_permutation

def ComposePermutations(p1, p2):
    composition = [p2[p1[j]] for j in range(len(p1))]
    return composition

Theta = 1

# Sample
# Probability distribution defined by (8)
Vs_vector = [-1]*5
for j in range(5):
    Vs_vector[j] = SampleProbDist(Theta,j,5)

Vs_vector = [2,0,1,0]
inv_permutation = GetNewInvPermutation(Vs_vector)
inv_inv_permutation = InvertPermutation(inv_permutation)

# Compose with consensus
consensus = [4,3,2,1,0]
composition = ComposePermutations(inv_inv_permutation, consensus)
print(composition)