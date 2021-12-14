import fileinput

import numpy as np

from low_points import LowPoints

inp = []
for line in fileinput.input("input/day09.txt"):
    inp.append([int(c) for c in line.strip()])

# print(LowPoints.sum_low_points(inp))
print(LowPoints.product_top_three_basins(np.array(inp)))