import decimal
import itertools
import random
import numpy
import math

def fast_walsh_hadamard_transform(v):
    # this routine takes in the truth-table of binary function (-1 = true, 1 = false)
    # and returns the Fourier coefficients of the function
    # v needs to be a numpy array with length a power of two
    # runs in O(n log n) time
    n = len(v)
    if n & (n - 1) != 0:
        raise ValueError("Vector length must be a power of 2")

    i = 2
    while i <= n:
        for j in range(0, n, i):
            for k in range(i // 2):
                x = v[j + k]
                y = v[j + k + i // 2]
                v[j + k] = x + y
                v[j + k + i // 2] = x - y
        i *= 2

    return v/n

circuitInputs = 12 # the number of input bits to the function
functionValues = 2 ** circuitInputs # the number of function values for a circuit with circuitInputs inputs

# compute a string of the first 32 binary digits of the fracitonal part square root of 2
# this will serve as the truth table of the function
decimal.getcontext().prec = functionValues
sqrt_two = decimal.Decimal(2).sqrt()
sqrt_two = sqrt_two - int(sqrt_two)
binary_str = bin(int(sqrt_two * (2 ** functionValues)))[2:]
binary_str = binary_str.zfill(functionValues)
# print(binary_str)

# create an array of +1's and -1's from the binary string
w = []
for v in binary_str:
    if v == "0":
        w.append(1)
    else:
        w.append(-1)
w = numpy.array(w) # convert to numpy array
fourierBasis = fast_walsh_hadamard_transform(w) # apply transformation to get Fourier coefficients
print(fourierBasis)

sum = 0
i = functionValues - 1
for t in range(circuitInputs,0,-1):
    for _ in range(math.comb(circuitInputs,t)):
        sum += fourierBasis[i]**2
        i -= 1
    print("Sums of squares of coefficients of terms of size at least ", t, ":", sum)


