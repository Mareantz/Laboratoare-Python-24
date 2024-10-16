# Write a function that receives as parameter a matrix and will return the matrix obtained by replacing all the
# elements under the main diagonal with 0 (zero).

def modify_matrix(matrix: list):
    n = len(matrix)
    for i in range(n):
        for j in range(i):
            matrix[i][j] = 0
    return matrix


a = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

result = modify_matrix(a)
for row in result:
    print(row)
