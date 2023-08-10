import decimal
import itertools
import random

def convert_zero_neg_one(input_number):
    if input_number == 0:
        return -1
    elif input_number == 1:
        return 1
    else:
        raise ValueError("Input must be either 0 or 1")

# Test cases
# input_value = 0
# output = convert_zero_neg_one(input_value)
# print(f"Input: {input_value}, Output: {output}")

# input_value = 1
# output = convert_zero_neg_one(input_value)
# print(f"Input: {input_value}, Output: {output}")


def nth_digit_of_sqrt_two(i):
    if i < 0:
        raise ValueError("The input must be a positive decimal number.")
        
    
    # Calculate the square root of two with arbitrary precision
    decimal.getcontext().prec = i + 1
    sqrt_two = decimal.Decimal(2).sqrt()
    
    # Convert the square root to a binary string
    binary_str = bin(int(sqrt_two * (2 ** i)))[2:]
    
    # Pad the binary string with leading zeros if necessary
    binary_str = binary_str.zfill(i)
    
    # Return the i-th digit
    return convert_zero_neg_one(int(binary_str[i]))

sqrt_2 = "101101010000010011110"
for i in range(0,20):
    print(i,nth_digit_of_sqrt_two(i), convert_zero_neg_one(int(sqrt_2[i])))


#################################################################################

# the input boolean_fxn should be a dictionary in the form of 
# the keys being tuples consisting of +1's and -1's and 
# and the values being +1 and -1's
# An example:
# {(-1, +1): -1, 
#  (+1, -1): -1, 
#  (-1, -1): 1, 
#  (+1, +1): 1}
# def give_fourier_coefficients(boolean_fxn):

def multiply_elements_by_indices(input_tuple, indices_list):
    """
    Multiplies the elements in the input tuple whose indices are given in the indices list.

    :param input_tuple: The input tuple.
    :param indices_list: A list of numbers representing the indices to multiply.
    :return: The result of multiplying the selected elements.
    """
    result = 1
    for index in indices_list:
        # Check if the index is within the valid range of the tuple
        if 0 <= index-1 < len(input_tuple):
            result *= input_tuple[index-1]
        else:
            print(f"Warning: Index {index} is out of range for the input tuple.")
    return result

print(multiply_elements_by_indices((1,1,1,-1),[3]))


def generate_combinations(x, y):
    """
    Generates all combinations of length x from the numbers [0, 1, ..., y].

    :param x: The length of the combinations.
    :param y: The maximum number to consider in the combinations.
    :return: A list containing all combinations of length x in the from of tuples.
    """
    numbers = list(range(1,y + 1))
    return list(itertools.combinations(numbers, x))

# Example usage:
x = 2
y = 3
combinations = generate_combinations(x, y)
print(combinations)


def generate_all_combinations(y):
    """
    Generates all combinations of natural numbers no more than the given natural number
    in the order of increasing length.

    :param n: The natural number.
    :return: A list containing all combinations of natural numbers in the form of tuples.
    """
    big_list = []
    for i in range(y+1):
        big_list += generate_combinations(i,y)
    return big_list



# Example usage:
n = 4
combinations = generate_all_combinations(n)
# print("combinations of {}!".format(n), combinations)


def calculate_expectation(dictionary):
    """
    Calculates the expectation (average) of all the values in the dictionary.

    :param dictionary: The input dictionary with numerical values.
    :return: The expectation of all the values in the dictionary.
    """
    if not dictionary:
        return None

    total_sum = sum(dictionary.values())
    num_entries = len(dictionary)
    return total_sum / num_entries

# Example usage:
input_dict = {'a': 1, 'b': -1, 'c': -1}
expectation = calculate_expectation(input_dict)
print(expectation)

def generate_binary_strings(length):
    """
    Generates all binary numbers of the given length.

    :param length: The length of the binary strings.
    :return: A list containing all binary strings of the given length as tuples.
    """
    if length <= 0:
        return []

    def backtrack(path, result):
        if len(path) == length:
            result.append(tuple(path))
            return

        path.append(0)
        backtrack(path, result)
        path.pop()

        path.append(1)
        backtrack(path, result)
        path.pop()

    result = []
    backtrack([], result)
    return result

# Example usage:
length = 3
binary_strings = generate_binary_strings(length)
# print(binary_strings)


def binary_tuple_to_decimal(binary_tuple):
    """
    Converts a binary tuple to its corresponding decimal representation.

    :param binary_tuple: The input binary tuple.
    :return: The decimal number corresponding to the binary tuple.
    """
    binary_str = ''.join(map(str, binary_tuple))
    return int(binary_str, 2)

# Example usage:
binary_input = (1, 1, 0)
decimal_output = binary_tuple_to_decimal(binary_input)
# print(decimal_output)

def replace_zeros_with_minus_ones(binary_tuple):
    """
    Replaces all the 0's in the binary tuple with -1's.

    :param binary_tuple: The input binary tuple.
    :return: A new tuple with 0's replaced by -1's.
    """
    return tuple(-1 if bit == 0 else bit for bit in binary_tuple)

# Example usage:
binary_input = (1, 1, 0, 1, 0)
modified_tuple = replace_zeros_with_minus_ones(binary_input)
# print(modified_tuple)

def sum_squared_vars_longer_than_t(t, input_dict):
    result = 0
    for key in input_dict.keys():
        if len(key) > t:
            print("line 202: ", input_dict[key] ** 2)
            result += input_dict[key] ** 2
    return result

# Example dictionary
data_dict = {('apple', 'banana'): 3, ('cherry', 'date', 'elderberry'): 5, ('fig', 'grape', 'honeydew', 'kiwi'): 2}

# Calculate sum of squares of values with keys longer than t
t_value = 2
total_sum = sum_squared_vars_longer_than_t(t_value, data_dict)
print(f"Sum of squares of values with keys longer than {t_value}: {total_sum}")


#####################################################

def boolean_function_fourier_coeffs(boolean_func_dict):
    """
    Computes the coefficients of the Fourier expansion for the given boolean function.

    :param boolean_func_dict: A dictionary with tuples of (-1, +1) as keys and boolean function outputs (-1, +1) as values.
    :return: A dictionary whose keys are the terms of the Fourier expansion and the values are the coefficients.
    """
    all_terms = generate_all_combinations(len(random.choice(list(boolean_func_dict.keys()))))
    normalization_factor = 1/(len(boolean_func_dict))

    coeff_dict = {}
    for term in all_terms:
        if len(term)>0:
            dot_product = 0
            for key, value in boolean_func_dict.items():
                dot_product += multiply_elements_by_indices(key,term) * value
            coeff_dict[term] = normalization_factor * dot_product
        else:
            coeff_dict[term] = calculate_expectation(boolean_func_dict)
    return coeff_dict


# Example boolean function represented as a dictionary
max2_func_dict = {
    (-1, +1): +1, 
    (+1, -1): +1, 
    (-1, -1): -1, 
    (+1, +1): +1}


max2_coefficients = boolean_function_fourier_coeffs(max2_func_dict)
# print("COEFFICIENTS OF MAX2!!!")
# print(max2_coefficients)

majority3_function_dict = {
    (-1, -1, -1): -1,
    (-1, -1, +1): -1,
    (-1, +1, -1): -1,
    (-1, +1, +1): +1,

    (+1, -1, -1): -1,
    (+1, -1, +1): +1,
    (+1, +1, -1): +1,
    (+1, +1, +1): +1,
}

maj3_coefficients = boolean_function_fourier_coeffs(majority3_function_dict)
# print("COEFFICIENTS OF MAJ3!!!")
# print(maj3_coefficients)

length_bin = 2

sqrt_boolean_fxn = {}
for i in generate_binary_strings(length_bin):
    for boolean_input in generate_binary_strings(length_bin):
        sqrt_boolean_fxn[replace_zeros_with_minus_ones(boolean_input)] = nth_digit_of_sqrt_two(binary_tuple_to_decimal(boolean_input))
print("boolean fxn of sqrt 2 at length {length_bin}}: ", sqrt_boolean_fxn)
print("sqrt 2 fourier expansion:", boolean_function_fourier_coeffs(sqrt_boolean_fxn))

print("test of max2: ", sum_squared_vars_longer_than_t(-1, boolean_function_fourier_coeffs(majority3_function_dict)))
# def lemma7(t,M,d,fourier_expansion):
#     for 


# need to do tests that the lemma works on these small fxns, then test on root 2