import random
import math

def Psi_j(Theta, j, n):
    numerator = 1-math.exp(-(n-j+1)*Theta)
    denominator = 1-math.exp(-Theta)
    return numerator/denominator

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

# def SampleVjVector(centralPermutation, Theta):
#     Vj_vector = [-1]*(len(centralPermutation)-1)

#     for i in range(len(centralPermutation)-1):
#         # j is now 1 indexed. We get values j=1..n-1
#         # j = i+1
#         j=i
#         Vj_vector[i] = SampleProbabilityDistribution(len(centralPermutation), Theta, j)
    
#     return Vj_vector

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


def V(j,composition):
    if j>=len(composition):
        raise Error

    dist = 0
    
    for i in range(j+1,len(composition)):
        # if composition.index(i)<composition.index(j):
        if composition[j]>composition[i]:
            dist += 1
    return dist

# def V_two_perms(j,p1,p2):
#     assert(len(p1)==len(p2))
#     assert(j<len(p1))
#     if j>=len(p1):
#         raise Error

#     dist = 0
    
#     for i in range(j+1,len(p1)):
#         # if composition.index(i)<composition.index(j):
#         if p1[i]<p1[j] and p2[i]>p2[j]:
#             dist += 1
#         elif p1[i]>p1[j] and p2[i]<p2[j]:
#             dist += 1
            
#     return dist

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


def V_j_mean(j, sample, central_permutation):
    sum_of_vs = 0
    for s in sample:
        sum_of_vs += V_j(j,s,central_permutation)
    
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
    
    second = second1
    # assert(second1==second2)
    res = first - second - left
    return res

def LogLikelihoodSingleJ(Theta, j, sample, n, central_permutation):
    left = V_j_mean(j, sample, central_permutation)


    first = (1)/(math.exp(Theta)-1)
    
    local_j = j + 1
    
    second = (n-local_j+1)/(math.exp((n-local_j+1)*Theta)-1)
    
    res = first - second - left
    return res

# Sample
# np.random.seed(5)
random.seed(5)
central = [1,3,0,2]
central = [5,8,1,3,6,9,0,7,2,4]
theta = [4]*(len(central)-1)
number_of_samples = 10**4
sample = [None]*number_of_samples
for i in range(number_of_samples):
    s = SampleMallowsModel(central,theta)
    sample[i] = s
from scipy import optimize

print("Done")
# for i in range(len(central)):
    # total = 0
    # for s in sample:
        # total += s[i]
    # print(total/len(sample))

averages = [0]*len(central)
for i in range(len(central)):
    for individual in sample:
        averages[i] += individual[i]
    
    averages[i] = (averages[i]/len(sample), i)
    print(i,averages[i])


# averages = sorted(averages, key = lambda t:(t[0]))#,random.random()))
averages.sort()
central = [0]*len(central)
for i in range(len(central)):
    central[averages[i][1]] = i

print(central)


sample = [[1, 7, 17, 9, 2, 13, 10, 8, 6, 0, 15, 14, 4, 3, 16, 11, 5, 12]]
central = [1, 3, 12, 8, 6, 9, 11, 4, 5, 2, 17, 14, 10, 0, 16, 15, 7, 13]
print(V_j_mean(16,sample,central))

print(V_j(15,sample[0],central))
exit(0)
# Calculate Theta using Newton Rapson
# Theta = optimize.newton(LogLikelihood, 0.1,  tol = 0.0001,args=(sample, len(central), central,))
for j_theta in range(len(central)-1):
    if j_theta >= 14:
        stop=1
    Theta = optimize.newton(LogLikelihoodSingleJ, 0.1,  tol = 0.0001,args=(j_theta, sample, len(central), central,))

    print(Theta)
