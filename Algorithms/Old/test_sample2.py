import random
import math

def SampleProbDist(theta, j, n):
    j+=1
    prob = 0
    rand = random.random()
    for r in range(n):
        prob += math.exp(-theta*r)/Psi_j(j,theta,n)
        if rand<prob:
            return r
    print("returning r=",r)
    return r 
    # print("Random that got to here:",rand,"prob:",prob,"r:",r)


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



n = 10
Theta=1
central_permutation = [0,1,2,3,4,5,6,7,8,9]
Vs_vector = [-1]*(n-1)
for j in range(n-1):
    Vs_vector[j] = SampleProbDist(Theta,j, n)
# Vs_vector = [1,0,0,0,0,0,0,0,0]
Vs_vector = [1]*9
print(list(range(10)))
if any(a==None for a in Vs_vector):
    raise Error
print(Vs_vector,"      vs")
inv_permutation = GetNewInvPermutation(Vs_vector)
print(inv_permutation,"   inv")

# Invert it
inv_inv_permutation = InvertPermutation(inv_permutation)
print(inv_inv_permutation,"   inv_inv")

# Compose with censensus to get new permutation
# ORIGINAL:
composition = ComposePermutations(inv_inv_permutation, central_permutation)
print(composition,"   comp")



