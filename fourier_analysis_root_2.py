import decimal
import itertools

def nth_digit_of_sqrt_two(binary_i):
    try:
        i = int(binary_i, 2)
    except ValueError:
        raise ValueError("Invalid binary input. Please enter a valid binary number.")
    
    if i <= 0:
        raise ValueError("The input must be a positive binary number.")
    
    # Calculate the square root of two with arbitrary precision
    decimal.getcontext().prec = i + 1
    sqrt_two = decimal.Decimal(2).sqrt()
    
    # Convert the square root to a binary string
    binary_str = bin(int(sqrt_two * (2 ** i)))[2:]
    
    # Pad the binary string with leading zeros if necessary
    binary_str = binary_str.zfill(i)
    
    # Return the i-th digit
    return int(binary_str[i - 1])

#################################################################################

def boolean_function_fourier_coefficients(boolean_function_dict):
    n = len(next(iter(boolean_function_dict)))  # Number of variables in the boolean function
    num_coefficients = 2 ** n  # Total number of Fourier coefficients

    coefficients = []

    # Replace 0's with -1's in the boolean function dictionary (keys and values)
    boolean_function_dict = {k: -1 if v == 0 else v for k, v in boolean_function_dict.items()}

    # Generate all possible input combinations (0, 1) for n variables
    input_combinations = list(itertools.product([0, 1], repeat=n))

    # Calculate Fourier coefficients by computing inner product with Fourier basis functions
    for k in range(num_coefficients):
        coefficient = 0

        # Generate the k-th Fourier basis function
        for input_vals in input_combinations:
            input_binary = ''.join(str(bit) for bit in input_vals)
            x = boolean_function_dict.get(input_binary, 0)
            basis_function = ((-1) ** (sum(input_vals) & k))  # Fourier basis function
            coefficient += x * basis_function

        coefficient /= num_coefficients  # Normalize the coefficient
        coefficients.append(coefficient)

    return coefficients


# def boolean_function_fourier_coefficients(boolean_function_dict):
#     n = len(next(iter(boolean_function_dict)))  # Number of variables in the boolean function
#     num_coefficients = 2 ** n  # Total number of Fourier coefficients

#     coefficients = []

#     # Generate all possible input combinations (0, 1) for n variables
#     input_combinations = list(itertools.product([0, 1], repeat=n))

#     # Calculate Fourier coefficients by computing inner product with Fourier basis functions
#     for k in range(num_coefficients):
#         coefficient = 0

#         # Generate the k-th Fourier basis function
#         for input_vals in input_combinations:
#             input_binary = ''.join(str(bit) for bit in input_vals)
#             x = boolean_function_dict[input_binary]
#             basis_function = ((-1) ** (sum(input_vals) & k))  # Fourier basis function
#             coefficient += x * basis_function

#         coefficient /= num_coefficients  # Normalize the coefficient
#         coefficients.append(coefficient)

#     return coefficients

def boolean_function_fourier_expansion(boolean_function_dict):
    n = len(next(iter(boolean_function_dict)))  # Number of variables in the boolean function
    num_coefficients = 2 ** n  # Total number of Fourier coefficients

    coefficients = []

    # Generate all possible input combinations (0, 1) for n variables
    input_combinations = list(itertools.product([0, 1], repeat=n))

    # Calculate Fourier coefficients by computing inner product with Fourier basis functions
    for k in range(num_coefficients):
        coefficient = 0

        # Generate the k-th Fourier basis function
        for input_vals in input_combinations:
            input_binary = ''.join(str(bit) for bit in input_vals)
            x = boolean_function_dict[input_binary]
            basis_function = ((-1) ** (sum(input_vals) & k))  # Fourier basis function
            coefficient += x * basis_function

        coefficient /= num_coefficients  # Normalize the coefficient
        coefficients.append(coefficient)

    # Construct the full Fourier expansion string with variable names x1, x2, x3
    expansion = []
    for k in range(num_coefficients):
        coefficient = coefficients[k]
        if coefficient != 0:
            terms = []
            for i in range(1, n + 1):
                basis_function = ((-1) ** ((k >> (n - i)) & 1))  # Fourier basis function
                if basis_function != 1:
                    term = f"{basis_function:+}*x{i}"
                    terms.append(term)
            expansion.append(f"{coefficient:+} {' + '.join(terms)}")

    full_expansion = ' '.join(expansion)
    return full_expansion

# Example usage:
if __name__ == "__main__":
    # Define a boolean function in the form of a dictionary
    # Example: f(x, y, z) = x XOR y XOR z
    boolean_function_dict = {
        '000': 0,
        '001': 1,
        '010': 1,
        '011': 0,
        '100': 1,
        '101': 0,
        '110': 0,
        '111': 1,
    }

    boolean_function_dict_1 = {
        '11': 1,
        '01': 1,
        '10': 1,
        '00': 0
    }

    # Calculate Fourier coefficients
    coefficients = boolean_function_fourier_coefficients(boolean_function_dict_1)

    # Output Fourier coefficients
    print("Fourier coefficients:", coefficients)

        # Get the full Fourier expansion as a string
    # expansion_string = boolean_function_fourier_expansion(boolean_function_dict)

    # Output the full Fourier expansion
    # print("Full Fourier expansion:")
    # print(expansion_string)

