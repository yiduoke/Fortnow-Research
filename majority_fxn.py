def more_ones_than_zeros(binary_string):
    # Initialize counters for ones and zeros
    ones_count = 0
    zeros_count = 0

    # Iterate through the binary string
    for bit in binary_string:
        if bit == '1':
            ones_count += 1
        elif bit == '0':
            zeros_count += 1

    # Compare the counts and return the result
    if ones_count > zeros_count:
        return 1
    else:
        return 0

# Example usage:
binary_str = "110"
result = more_ones_than_zeros(binary_str)
print(result)  # Output: 1

def decimal_to_binary(decimal_number):
    if decimal_number < 0:
        raise ValueError("Input must be a non-negative integer.")

    binary_string = bin(decimal_number)[2:]  # Convert to binary and remove the '0b' prefix
    return binary_string

# Example usage:
decimal_num = 5
binary_str = decimal_to_binary(decimal_num)
print(binary_str)  # Output: "101010"


def majority_sequence(until_x):
    sequence_string = ""
    for number in range(until_x):
        # print(number)
        # print(decimal_to_binary(number))
        # print(more_ones_than_zeros(decimal_to_binary(number)))
        # print()

        sequence_string += str(more_ones_than_zeros(decimal_to_binary(number)))
    return sequence_string

print(majority_sequence(4000))

binary_str = "0.101011100010111000101110111111100000001000101110001011101111111000000010001011100010111011111110001011101111111011111111111111100000000000000010000000100010111000000010001011100010111011111110000000100010111000101110111111100010111011111110111111111111111000000000000000100000001000101110000000100010111000101110111111100000001000101110001011101111111000101110111111101111111111111110000000000000000100000001000101110000000100010111000101110111111100000001000101110001011101111111000101110111111101111111111111110000000000000001000000010001011100000001000101110001011101111111000000000000000100000001000101110000000100010111000101110111111100000001000101110001011101111111000101110111111101111111111111110000000001000101110001011101111111000101110111111101111111111111110001011101111111011111111111111101111111"

# Split the binary string into integer and fractional parts
integer_part, fractional_part = binary_str.split('.')

# Convert the integer part to decimal
decimal_integer = int(integer_part, 2)

# Convert the fractional part to decimal
decimal_fraction = sum(int(bit) * 2**(-i) for i, bit in enumerate(fractional_part, start=1))

# Combine the integer and fractional parts to get the decimal number
decimal_number = decimal_integer + decimal_fraction

print(decimal_number)



