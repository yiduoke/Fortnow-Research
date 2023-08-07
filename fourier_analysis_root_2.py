import decimal
import itertools

def nth_digit_of_sqrt_two(i):
    if i <= 0:
        raise ValueError("The input must be a positive decimal number.")
    
    # Calculate the square root of two with arbitrary precision
    decimal.getcontext().prec = i + 1
    sqrt_two = decimal.Decimal(2).sqrt()
    
    # Convert the square root to a binary string
    binary_str = bin(int(sqrt_two * (2 ** i)))[2:]
    
    # Pad the binary string with leading zeros if necessary
    binary_str = binary_str.zfill(i)
    
    # Return the i-th digit
    return int(binary_str[i - 1])

sqrt_2 = "101101010000010011110"
for i in range(1,20):
    print(i,nth_digit_of_sqrt_two(i), sqrt_2[i-1])


#################################################################################
