"""Assignment 3: Matrices as nested lists.

A matrix is a list of rows. matrix[r][c] is the item in row r, column c.
Functions return NEW matrices and never change their arguments.
"""

Matrix = list[list[int]]


def transpose(matrix: Matrix) -> Matrix:
    """Swap rows and columns.

    transpose([[1, 2, 3], [4, 5, 6]]) -> [[1, 4], [2, 5], [3, 6]]
    transpose([[7]])                  -> [[7]]
    transpose([])                     -> []
    """
    # TODO: zip(*matrix) pairs up the columns; turn each tuple into a list.
    ...


def identity(n: int) -> Matrix:
    """Return the n x n identity matrix (1 on the diagonal, 0 elsewhere).

    identity(3) -> [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    identity(0) -> []

    Build each row separately: [[0] * n] * n would share one row.
    """
    # TODO: a nested comprehension, or loops. Do not repeat one row object.
    ...


def multiply(a: Matrix, b: Matrix) -> Matrix:
    """Multiply two matrices (rows of a times columns of b).

    The item at row r, column c is the sum of a[r][k] * b[k][c] over k.

    multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]]) -> [[19, 22], [43, 50]]
    multiply([[1, 2, 3]], [[1], [1], [1]])       -> [[6]]

    Raise ValueError if the number of columns in a differs from the number of rows in b.
    """
    # TODO: check the shapes, then a sum of products for every row/column pair.
    ...


def rotate_clockwise(matrix: Matrix) -> Matrix:
    """Rotate a matrix 90 degrees clockwise.

    rotate_clockwise([[1, 2, 3], [4, 5, 6]]) -> [[4, 1], [5, 2], [6, 3]]

    Hint: transpose it, then reverse every row.
    """
    # TODO: use transpose, then reverse each row.
    ...


if __name__ == "__main__":
    print(transpose([[1, 2, 3], [4, 5, 6]]))
    print(multiply([[1, 2], [3, 4]], identity(2)))
    print(rotate_clockwise([[1, 2, 3], [4, 5, 6]]))
