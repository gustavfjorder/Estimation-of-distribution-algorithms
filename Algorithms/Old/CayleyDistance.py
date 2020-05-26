import random
import math

def CayleyDist(s1,s2):
    # First find composition of the two permutations
    inv_s1 = [s1.index(j) for j in range(len(s1))]
    # print(inv_s1)
    
    
    composition = [s2[inv_s1[j]] for j in range(len(s1))]
    # print(composition,"composition")
    X_vec = [X(j,composition) for j in range(len(s1)-1)]
    # print(X_vec)
    
    
    return sum(X_vec)

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

# Define Psi for Cayley distance
def Psi(n,theta):
    product = 1
    for j in range(1,n-1):
        product *= (n-j)*math.exp(-theta)+1
    return product

nums = list(range(3))
t1 = random.sample(nums,len(nums))
t2 = random.sample(nums,len(nums))
t1 = [0,3,1,2]
t2 = [3,2,0,1]
print("s1:",t1)
print("s2:",t2)
print(CayleyDist(t1,t2))

