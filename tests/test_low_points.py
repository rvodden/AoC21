from low_points import LowPoints

import numpy as np

class TestLowPoints:
    def test_low_points(self):
        inp = [
            [2, 1, 9, 9, 9, 4, 3, 2, 1, 0],
            [3, 9, 8, 7, 8, 9, 4, 9, 2, 1],
            [9, 8, 5, 6, 7, 8, 9, 8, 9, 2],
            [8, 7, 6, 7, 8, 9, 6, 7, 8, 9],
            [9, 8, 9, 9, 9, 6, 5, 6, 7, 8],
        ]

        assert LowPoints.sum_low_points(np.array(inp)) == 15
        assert LowPoints.product_top_three_basins(np.array(inp)) == 1134

