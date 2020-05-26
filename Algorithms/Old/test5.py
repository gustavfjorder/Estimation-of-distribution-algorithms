import math

Theta = 1
n = 4

for j in range(1,n):
    numerator = 1-math.exp(-(n-j+1)*Theta)
    denominator = 1-math.exp(-Theta)
    print(numerator/denominator)