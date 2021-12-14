import numpy as np
from scipy.ndimage import generic_filter


class LowPoints:

    @staticmethod
    def sum_low_points(heights: np.ndarray) -> int:
        low_points = LowPoints.low_points(heights)
        lp = low_points.T
        lp = heights[lp[0], lp[1]]
        return np.sum(lp + 1).item()

    @staticmethod
    def product_top_three_basins(heights: np.ndarray) -> int:
        print()
        low_points = LowPoints.low_points(heights)

        basin_sizes = []
        for lp in low_points:
            basins = list(set(LowPoints.higher_neighbours(heights, lp)))
            print(basins)
            basin_sizes += [len(basins) + 1]

        return np.prod(sorted(basin_sizes)[-3:]).item()

    @staticmethod
    def higher_neighbours(heights: np.ndarray, coords: np.ndarray):
        y_max, x_max = heights.shape
        y, x = tuple(coords)

        higher_neighbours = []

        height = heights[y, x]
        potential_neighbours = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        neighbours = [p for p in potential_neighbours if x_max > p[0] >= 0 and y_max > p[1] >= 0]

        for neighbour in neighbours:
            neighbour_height = heights[neighbour[1], neighbour[0]]
            if height < neighbour_height < 9:
                higher_neighbours += [neighbour] + LowPoints.higher_neighbours(
                    heights, np.array([neighbour[1], neighbour[0]]))

        return higher_neighbours

    @staticmethod
    def low_points(heights: np.ndarray) -> np.ndarray:
        def _low_point(ps: list[int, int]) -> bool:
            # takes a 3x3 array and returns True if the centre element is smaller than all the others
            return np.sum((ps[4] - ps) < 0) == 8  # ps[4] - ps[4] will always be 0 :-)

        return np.argwhere(generic_filter(heights, _low_point, size=(3, 3), mode='constant', cval=9))
