import numpy as np
import sympy as sp

equation_matrix = np.matrix([[0.003, -0.001, 0.012], [-0.001, 0.003, 0.012]])
print(equation_matrix)
print(sp.Matrix(equation_matrix).rref())