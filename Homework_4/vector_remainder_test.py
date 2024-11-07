# Python script to perform element-wise modulus operation on two vectors of length 6

def vector_remainder(vector1, vector2):
    """Performs element-wise modulus operation on two vectors."""
    if len(vector1) != len(vector2):
        raise ValueError("Both vectors must be of the same length.")
    
    result_vector = [v1 % v2 if v2 != 0 else 0 for v1, v2 in zip(vector1, vector2)]
    return result_vector

# Sample vectors
vector1 = [10, 20, 30, 40, 50, 60]
vector2 = [3, 7, 4, 8, 6, 5]

# Perform the operation
result_vector = vector_remainder(vector1, vector2)

# Print the result
print("Vector 1:", vector1)
print("Vector 2:", vector2)
print("Result Vector (Remainders):", result_vector)

# If needed, save the result to a file
with open("vector_remainder_result.csv", "w") as file:
    file.write("Index, Remainder\n")
    for index, value in enumerate(result_vector):
        file.write(f"{index}, {value}\n")
