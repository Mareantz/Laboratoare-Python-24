# Write a Python class that simulates a matrix of size NxM, with N and M provided at initialization. The class should
# provide methods to access elements (get and set methods) and some mathematical functions such as transpose,
# matrix multiplication and a method that allows iterating through all elements from a matrix an apply a
# transformation over them (via a lambda function).

class Matrix:
    def __init__(self, n, m):
        self.matrix = [[0 for _ in range(m)] for _ in range(n)]
        self.n = n
        self.m = m

    def get(self, i, j):
        return self.matrix[i][j]

    def set(self, i, j, value):
        self.matrix[i][j] = value

    def transpose(self):
        transposed_matrix = Matrix(self.m, self.n)
        for i in range(self.n):
            for j in range(self.m):
                transposed_matrix.matrix[j][i] = self.matrix[i][j]
        return transposed_matrix

    def __mul__(self, other):
        if not isinstance(other, Matrix):
            raise ValueError("Can only multiply with another Matrix.")
        if self.m != other.n:
            raise ValueError("Invalid matrix dimensions for multiplication.")
        result = Matrix(self.n, other.m)
        for i in range(self.n):
            for j in range(other.m):
                for k in range(self.m):
                    result.matrix[i][j] += self.matrix[i][k] * other.matrix[k][j]
        return result

    def apply(self, func):
        for i in range(self.n):
            for j in range(self.m):
                self.matrix[i][j] = func(self.matrix[i][j])

    def __str__(self):
        return '\n'.join(['\t'.join(map(str, row)) for row in self.matrix])


# Testing the Matrix class
matrix = Matrix(2, 2)
matrix.set(0, 0, 1)
matrix.set(0, 1, 2)
matrix.set(1, 0, 3)
matrix.set(1, 1, 4)
print("Matrix:")
print(matrix)

matrix2 = matrix.transpose()
print("\nTransposed Matrix:")
print(matrix2)

matrix3 = matrix * matrix2
print("\nMatrix * Transposed Matrix:")
print(matrix3)

matrix4 = Matrix(2, 3)
matrix4.set(0, 0, 1)
matrix4.set(0, 1, 2)
matrix4.set(0, 2, 3)
matrix4.set(1, 0, 4)
matrix4.set(1, 1, 5)
matrix4.set(1, 2, 6)
print("\nMatrix 4:")
print(matrix4)

matrix5 = matrix * matrix4
print("\nMatrix * Matrix4:")
print(matrix5)
