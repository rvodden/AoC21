import numpy as np

from beacon_scanner.beacon_scanner import rotation_matrices


beacon1 = np.array([1, 2, 3])
beacon2 = np.array([3, 2, 1])

scanner1 = np.array([7, 5, 12])
scanner1_rot = rotation_matrices()[12]

scanner2 = np.array([-5, 5, 1])
scanner2_rot = rotation_matrices()[5]

scanner1_readings = np.array(
    [(beacon - scanner1) @ scanner1_rot for beacon in [beacon1, beacon2]]
)
scanner2_readings = np.array(
    [(beacon - scanner2) @ scanner2_rot for beacon in [beacon1, beacon2]]
)

scanner1_differences = scanner1_readings[None, :] - scanner1_readings[:, None]


scanner2_differences = scanner2_readings[:, None] - scanner2_readings[None, :]

print(scanner2_differences.shape)
print(rotation_matrices().shape)


scanner2_rotations = np.matmul(scanner2_differences, rotation_matrices()[:, None, :, :])

print(scanner2_rotations)

# vector = np.array([1, 2, 3])
# matrix = np.array([[1, 2, 3], [2, 3, 4], [3, 4, 5]])

# result = np.einsum("i, ij", vector, matrix)
# print(result)

# matrix_of_vectors = np.array(
#     [
#         [[1, 2, 3], [2, 3, 4], [3, 4, 5], [6, 7, 8]],
#         [[1, 2, 3], [2, 3, 4], [3, 4, 5], [6, 7, 8]],
#         [[1, 2, 3], [2, 3, 4], [3, 4, 5], [6, 7, 8]],
#         [[1, 2, 3], [2, 3, 4], [3, 4, 5], [6, 7, 8]],
#     ]
# )
# print(matrix_of_vectors.shape)

# vector_of_matrices = np.array(
#     [
#         [[1, 2, 3], [2, 3, 4], [3, 4, 5]],
#         [[1, 2, 3], [2, 3, 4], [3, 4, 5]],
#         [[1, 2, 3], [2, 3, 4], [3, 4, 5]],
#         [[1, 2, 3], [2, 3, 4], [3, 4, 5]],
#         [[1, 2, 3], [2, 3, 4], [3, 4, 5]],
#     ]
# )
# print(vector_of_matrices.shape)

# result = np.matmul(matrix_of_vectors, vector_of_matrices[:, None, :, :])
# print(result.shape)
