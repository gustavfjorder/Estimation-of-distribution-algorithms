import math
import random

def LogLikelihoodSingleJ(Theta, j, sample, n, central_permutation):
    left = V_j_mean(j, sample, central_permutation)
    # print(Theta)
    try:
        first = (1)/(math.exp(Theta)-1)
    except OverflowError:
        # print(Theta)
        first = math.inf

    local_j = j + 1
    
    try:
        second = (n-local_j+1)/(math.exp((n-local_j+1)*Theta)-1)
    except OverflowError:
        second = math.inf
        # print(n,local_j,Theta)
        # exit(0)
    res = first - second - left
    return res

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
    try:
        first = (n-1)/(math.exp(Theta)-1)
    except OverflowError:
        first = math.inf

    second = 0
    for j in range(1,n):
        try:
            second += (n-j+1)/(math.exp((n-j+1)*Theta)-1)
        except OverflowError:
            second += math.inf

    # second2 = 0
    # for j in range(0,n-1):
    #     try:
    #         second2 += (n-j+1)/(math.exp((n-j+1)*Theta)-1)
    #     except:
    #         second2 += 
    # second = second1
    # assert(second1==second2)
    res = first - second - left
    return res

def V_j_mean(j, sample, central_permutation):
    sum_of_vs = 0
    for s in sample:
        sum_of_vs += V_j(j,s,central_permutation)
    
    mean = sum_of_vs/len(sample)
    return mean

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


def SampleMallowsModel(centralPermutation, Theta):

    # Sample Vj vector 
    Vj_vector = SampleVjVector(centralPermutation, Theta)

    # Transform Vj vector into pi_inv
    Pi_Inv = GetInverseVjVector(Vj_vector)

    # Invert it
    Pi_Inv_Inv = InvertPermutation(Pi_Inv)

    # Compose with central permutation
    # SampledPermutation = ComposePermutations(Pi_Inv_Inv, centralPermutation)
    SampledPermutation = ComposePermutations(centralPermutation, Pi_Inv_Inv)


    return SampledPermutation


def SampleVjVector(centralPermutation, Theta):
    Vj_vector = [-1]*(len(centralPermutation)-1)

    if isinstance(Theta, list):
        # generalized
        for i in range(len(centralPermutation)-1):
            Vj_vector[i] = SampleProbabilityDistribution(len(centralPermutation), Theta[i], i)
        return Vj_vector
    elif isinstance(Theta, float):
        # simple
        for i in range(len(centralPermutation)-1):
            Vj_vector[i] = SampleProbabilityDistribution(len(centralPermutation), Theta, i)
        return Vj_vector
    else:
        raise error



def GetInverseVjVector(Vj_vector):
    pi_inv = []
    pi_inv.insert(0,len(Vj_vector))

    for i in range(len(Vj_vector)-1,-1,-1):
        index = Vj_vector[i]
        val = i
        pi_inv.insert(index,val)
    
    return pi_inv


def InvertPermutation(permutation):
    inv_permutation = [permutation.index(j) for j in range(len(permutation))]
    return inv_permutation

def ComposePermutations(p1, p2):
    composition = [p2[p1[j]] for j in range(len(p1))]
    return composition


def SampleProbabilityDistribution(n, Theta, j):
    prob = 0
    rand = random.random()
    # rand = 0.96
    # From 0 to 1 indexed
    j = j + 1
    for r in range(n):
        new_prob = math.exp(-Theta*r)/Psi_j(Theta, j, n)
        prob += new_prob
        if rand <= prob:
            return r
    raise error
    print("ERROR didnt return r")

def Psi_j(Theta, j, n):
    numerator = 1-math.exp(-(n-j+1)*Theta)
    denominator = 1-math.exp(-Theta)
    return numerator/denominator