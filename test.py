import numpy as np

def boolean_function_to_truth_table(boolean_function):
    """
    Converts the boolean function in the form of a dictionary to a truth table as a list of tuples.

    Args:
        boolean_function (dict): The boolean function where keys are input assignments and values are Boolean outputs.

    Returns:
        list: A list of tuples representing the truth table with input assignments and Boolean outputs.
    """
    truth_table = list(boolean_function.items())
    return truth_table

def fourier_coefficients(boolean_function):
    """
    Calculates the Fourier coefficients of the Boolean function.

    Args:
        boolean_function (dict): The boolean function where keys are input assignments and values are Boolean outputs.

    Returns:
        dict: A dictionary with keys representing the Fourier coefficients and values being their corresponding values.
    """
    truth_table = boolean_function_to_truth_table(boolean_function)
    num_inputs = len(truth_table[0][0])
    num_outputs = len(truth_table)

    # Initialize the output dictionary to store Fourier coefficients
    coefficients = {}

    for k in range(num_inputs + 1):
        for i in range(num_outputs):
            x = np.array(truth_table[i][0])  # Input assignment as binary array
            y = truth_table[i][1]  # Boolean output
            # Calculate the phase of the Fourier coefficient
            phase = np.prod(np.where(x == -1, -1, 1))  # 1 if all elements of x are 1, -1 if any element is -1
            # Add the contribution of this output to the coefficient
            if k in coefficients:
                coefficients[k] += y * phase
            else:
                coefficients[k] = y * phase

    # Normalize the coefficients
    coefficients = {k: v / num_outputs for k, v in coefficients.items()}
    return coefficients

def boolean_function_expansion(fourier_coeffs):
    """
    Generates the Fourier expansion of the Boolean function from its Fourier coefficients.

    Args:
        fourier_coeffs (dict): A dictionary with keys representing the Fourier coefficients and values being their corresponding values.

    Returns:
        str: The Fourier expansion of the Boolean function as a string.
    """
    num_inputs = len(next(iter(fourier_coeffs.keys())))
    expansion = ""
    for k, coeff in fourier_coeffs.items():
        if k == 0:
            expansion += "{:.2f} + ".format(coeff)
        else:
            expansion += "{:.2f} * ".format(coeff)
            for i in range(num_inputs):
                expansion += "x{} * ".format(i + 1 if i != num_inputs - 1 else i + 1)
            expansion = expansion[:-3] + " + "
    return expansion[:-3]

# Example usage:
if __name__ == "__main__":
    boolean_function = {
        (1, 1): 1,
        (-1, 1): 1,
        (1, -1): 1,
        (-1, -1): -1
    }

    fourier_coeffs = fourier_coefficients(boolean_function)
    fourier_expansion = boolean_function_expansion(fourier_coeffs)
    print("Fourier expansion: " + fourier_expansion)
