import math


def count_binary_digits(decimal_number):
    # Convert the decimal number to binary and remove the '0b' prefix
    binary_representation = bin(decimal_number)[2:]
    
    # Return the number of digits in the binary representation
    return len(binary_representation)

def binary_padding(x, y):
    # Convert the decimal number x to binary with y digits
    binary_representation = bin(x)[2:]

    # Calculate the number of zeros to pad
    num_zeros_to_pad = max(0, y - len(binary_representation))

    # Pad zeros to the binary representation
    padded_binary = '0' * num_zeros_to_pad + binary_representation

    return padded_binary

# Example usage:
decimal_input = 25
desired_digits = 8
result = binary_padding(decimal_input, desired_digits)
print(f"The binary representation of {decimal_input} with {desired_digits} digits is: {result}")

# Example usage:
decimal_input = 25
result = count_binary_digits(decimal_input)
print(f"The number of binary digits for {decimal_input} is: {result}")


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

def insert_dot(x):
    # Check if the string has at least two characters
    if len(x) < 2:
        return x  # Return the original string if it has less than two characters

    # Insert a "." between the first and second characters
    result_string = x[:1] + '.' + x[1:]
    return result_string

# Example usage:
input_string = "example"
result = insert_dot(input_string)

print(f"String with dot inserted: {result}")


def process_string(x):
    # Find the index of the dot
    dot_index = x.find('.')

    # If dot is not found, return the original string and 0
    if dot_index == -1:
        return x, 0

    # Remove the dot from the string
    string_without_dot = x[:dot_index] + x[dot_index + 1:]

    # Calculate the number of characters after the dot
    chars_after_dot = len(x) - dot_index - 1

    return string_without_dot, chars_after_dot

# Example usage:
input_string = "example.input"
result_string, num_chars_after_dot = process_string(input_string)

print(f"String without the dot: {result_string}")
print(f"Number of characters after the dot: {num_chars_after_dot}")


def floating_bin_to_dec(floating_bin):
    bin_without_dot, num_digits_after_dot = process_string(floating_bin)
    decimal_without_dot = int(bin_without_dot,2)
    return decimal_without_dot / 2 ** num_digits_after_dot

floating_bin = "110.01"
print(f"the binary number 0.11001 in decimal is {floating_bin_to_dec(floating_bin)}")


def majority_sequence(until_x):
    sequence_string = ""
    num_digits = count_binary_digits(until_x)
    for number in range(until_x):

        sequence_string += str(more_ones_than_zeros(binary_padding(number, num_digits)))

    sequence_string = insert_dot(sequence_string)
    decimal_form = floating_bin_to_dec(sequence_string)
    return sequence_string, decimal_form

binary_sequence, dec_form = majority_sequence(2**3-1)
print(binary_sequence)
print(dec_form)
# print(floating_bin_to_dec(binary_sequence))

# def is_there_convergence(power_of_two):
#     lst = []
#     for power in range(power_of_two):




