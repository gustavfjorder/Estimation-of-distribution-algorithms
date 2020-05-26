# Hamming distance
def HammingDistance(permutation): # first in report
    count = 0
    for i in range(len(permutation)):
        if i != permutation[i]:
            count+= 1
    return count

def SwapDistance(permutation, second_permutation = None): # second in report ## Kendall
    if second_permutation == None:
        second_permutation = [i for i in range(len(permutation))]
    
    # First find composition of the two permutations
    inv_permutation = [permutation.index(j) for j in range(len(permutation))]

    composition = [second_permutation[inv_permutation[j]] for j in range(len(permutation))]

    X = [V(j,composition) for j in range(len(permutation)-1)]

    return sum(X)

# Function that swap distance needs
def V(j,composition):
    if j>=len(composition):
        raise Error

    dist = 0
    for i in range(j+1,len(composition)):
        if composition[j]>composition[i]:
            dist += 1
    return dist

def V_j(j_start, permutation, second_permutation = None):
    if second_permutation == None:
        second_permutation = [i for i in range(len(permutation))]
    if j_start>=len(permutation):
        raise Error
    
    # First find composition of the two permutations
    inv_permutation = [permutation.index(j) for j in range(len(permutation))]

    composition = [second_permutation[inv_permutation[j]] for j in range(len(permutation))]

    X = [V(j,composition) for j in range(j_start,len(permutation)-1)]

    return sum(X)


# s1 = [4,3,2,1,0]
# s2 = [0,1,2,3,4]
# # print(V(3,s1))
# print(V_j(4,s1,s2))

def CayleyDistance(permutation): # third in report ## CayleyDist ##
    # Find inverse of permutation
    inv_permutation = [permutation.index(j) for j in range(len(permutation))]
    
    X_vec = [X(j,inv_permutation) for j in range(len(permutation)-1)]
    
    return sum(X_vec)

# Function that CayleyDist needs
def X(j,composition):
    next_index = j
    cont = True
    while cont:
        next_index = composition[next_index]
        if next_index > j:
            return 1
        if next_index == j:
            cont = False
    return 0

def PairsInCorrectOrder(permutation): # fourth in report
    count = 0
    for i in range(len(permutation)):
        for j in range(i+1,len(permutation)):
            if permutation[i]<permutation[j]:
                count+=1
    return count

def NumberOfSortedBlocks(permutation): # fifth in report
    count = 0
    for i in range(1,len(permutation)):
        if permutation[i-1]>permutation[i]:
            count += 1
    return count + 1

def NegativeLengthOfLongestAscendingSubsequence(permutation): # sixth in report
    longest = 0
    current = 0
    i = 1
    while i<len(permutation):
        if permutation[i-1] < permutation[i]:
            current += 1
            if current>longest:
                longest = current
        else:
            current = 0
        i += 1
    return 1 + longest

