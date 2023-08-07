import numpy as np
import itertools

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
        if 0 <= index < len(input_tuple):
            result *= input_tuple[index]
        else:
            print(f"Warning: Index {index} is out of range for the input tuple.")
    return result

print (multiply_elements_by_indices((1,1,1,-1),[3]))


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

def concatenate_lists_of_tuples(list_of_lists):
    """
    Concatenates a list of lists of tuples into a single big list.

    :param list_of_lists: The list of lists of tuples.
    :return: A single list containing all the tuples from the input lists.
    """
    return [item for sublist in list_of_lists for item in sublist]

# Example usage:
list_of_lists = [[(1, 2), (3, 4)], [(5, 6), (7, 8)], [(9, 10)]]
result = concatenate_lists_of_tuples(list_of_lists)
print(result)


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
print("combinations of {}!".format(n), combinations)


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




def boolean_function_fourier_coeffs(boolean_func_dict, num_terms):
    """
    Computes the coefficients of the Fourier expansion for the given boolean function.

    :param boolean_func_dict: A dictionary with tuples of (-1, +1) as keys and boolean function outputs (-1, +1) as values.
    :param num_terms: The number of Fourier terms to compute (excluding the constant term).
    :return: A list of coefficients of the Fourier expansion.
    """
    values = [boolean_func_dict[(-1, +1)], boolean_func_dict[(+1, -1)], boolean_func_dict[(-1, -1)], boolean_func_dict[(+1, +1)]]
    # Compute the Fourier coefficients using DFT
    fourier_coeffs = np.fft.fft(values)
    
    # Take the magnitudes of the coefficients to get the actual Fourier coefficients
    fourier_coeffs_magnitudes = np.abs(fourier_coeffs)
    
    # Keep only the desired number of terms (excluding the constant term)
    coefficients = fourier_coeffs_magnitudes[:num_terms + 1].tolist()
    
    return coefficients

# Example boolean function represented as a dictionary
max2_func_dict = {(-1, +1): 1, (+1, -1): 1, (-1, -1): -1, (+1, +1): 1}


# coefficients = boolean_function_fourier_coeffs(max2_func_dict)
# print(coefficients)

