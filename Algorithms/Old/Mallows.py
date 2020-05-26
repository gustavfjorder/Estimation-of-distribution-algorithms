import random
import math
# Define Kendall's Tau distance
def KendallDistance1(s1, s2):
    value = 0

    n = len(s1)
    for i in range(n):
        for j in range(i+1,n):
            if (s1[i]<s1[j] and s2[i]>s2[j]) or (s2[i]<s2[j] and s1[i]>s1[j]):
                value+=1
    return value


def KendallDistUsingComposition(s1,s2):
    # First find composition of the two permutations
    inv_s1 = [s1.index(j) for j in range(len(s1))]
    # print(inv_s1)
    
    
    composition = [s2[inv_s1[j]] for j in range(len(s1))]
    # print(composition)
    dist = 0
    n = len(s1)
    X = [V(j,composition) for j in range(n-1)]

    return sum(X)
def V(j, sigma1, sigma2):
    inv_sigma1 = [sigma1.index(j) for j in range(len(sigma1))]
    composition = [sigma2[inv_sigma1[j]] for j in range(len(sigma1))]
    return V_composition(j, composition)



def V_composition(j,composition):
    dist = 0
    for i in range(j+1,len(composition)):
        if composition[j]>composition[i]:
            dist += 1
    return dist

s1 = [0,2,3,4,1]
s2 = [0,1,2,3,4]

print(V(3,s1,s2))

# ## DELETE FROM HERE
# nums = list(range(50))
# t1 = random.sample(nums,len(nums))
# t2 = random.sample(nums,len(nums))
# # t1 = [2, 0, 1]
# # t2 = [0,1,2]
# print(t1)
# print(t2)
# print("Dist 1:",KendallDistance1(t1,t2))
# print("Dist 2:",KendallDistUsingComposition(t1,t2))
# ## DELETE UNTIL HERE

# def Psi(j,theta,n):
#     return (1-math.exp(-(n-j+1)*theta))/(1-math.exp(-theta))

# def Psi(theta,n):
#     product = 1
#     for j in range(1,n):
#         product *= Psi(j,theta,n)
#     return product

 
# def P(s, s0, theta, n):
#     D = KendallDistUsingComposition
#     return (math.exp(-theta*D(s,s0)))/(Psi(theta,n))

# ## 3.2 Learning and sampling a Mallows Model
# # Use Maximum likelihood
