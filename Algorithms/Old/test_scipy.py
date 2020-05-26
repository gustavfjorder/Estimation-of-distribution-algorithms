from scipy import optimize
import matplotlib.pyplot as plt
import math

# Equation (7) from ICONIP_2011
def f(theta, sum_of_Vjs, n):
    first = (n-1)/(math.exp(theta)-1)
    
    second = 0
    for j in range(1,n):
        second += (n-j+1)/(math.exp((n-j+1)*theta)-1)
    
    return first - second - sum_of_Vjs



sum_of_Vjs1 = 10
n1 = 25
func = lambda theta, sum_of_Vjs=sum_of_Vjs1, n = n1 : f(theta, sum_of_Vjs, n)

root = optimize.newton(f,1.5)
print(root)