import random
import math

theta = 1

j = 1
n=5
sum_probs = 0

def Psi_j(j,Theta,n):
    return (1-math.exp(-(n-j+1)*Theta))/(1-math.exp(-Theta))

def SampleProbDist(theta, j, n):
    prob = 0
    rand = random.random()
n = 5
prob = 0
for r in range(n):
    prob += math.exp(-theta*r)/Psi_j(j,theta,n)
    print(prob)
    # if rand<prob:
    #     return r



# print(SampleProbDist(theta,j))