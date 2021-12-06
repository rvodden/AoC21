import pandas as pd
import numpy as np
from textwrap import indent

from itertools import product


class HydrothermalVent:

    @staticmethod
    def calculate_orthogonal_overlapping_vents(df):
        df = HydrothermalVent._remove_non_orthogonal_lines(df)

        # Grab the biggest value
        mx = max(df.x1.max(), df.x2.max(), df.y1.max(), df.y2.max())

        # if mx is a power of two, notch it up one to make sure we include it in the field

        if (mx & (mx - 1) == 0) and mx != 0:
            mx += 1

        # Round up to the nearest power of two
        mx = 2 ** np.ceil(np.log2(mx)).astype(int)

        return HydrothermalVent._get_lines_in_region(df, 0, 0, mx)

    @staticmethod
    def _get_lines_in_region(df, x_min, y_min, size, level=0):
        def tw(s: str):
            return indent(s, level*4*" ")
        num_lines = len(df)

        # print(tw(f"Scanning ({x_min, y_min}) to ({x_min + size - 1}, {y_min + size - 1}): "))

        # we need to find overlapping lines, so if theres 1 or 0 lines,
        # nothing overlaps
        if num_lines <= 1:
            # print(tw("Found no overlaps."))
            return 0

        # print(tw(str(df)))
        # we know we have at least two lines in our region, so if our region is
        # 1 across, we must be an overlapping square
        if size == 1:
            # print(tw("Found an overlap!"))
            # print(tw(f"({x_min, y_min}, {size})"))
            return 1

        # print(tw(f"Passing {num_lines} objects to the next level."))

        new_size = size // 2

        total = 0
        for new_x_min, new_y_min in product(
                range(x_min, x_min + size, new_size),
                range(y_min, y_min + size, new_size)
        ):
            new_x_max = new_x_min + new_size - 1
            new_y_max = new_y_min + new_size - 1
            rdf = HydrothermalVent._get_lines_which_intersect_rectangle(df, new_x_min, new_y_min, new_x_max, new_y_max)
            total += HydrothermalVent._get_lines_in_region(rdf, new_x_min, new_y_min, new_size, level=level + 1)
        # print()
        return total

    @staticmethod
    def _remove_non_orthogonal_lines(df: pd.DataFrame):
        return df.loc[(df.x1 == df.x2) | (df.y1 == df.y2)]

    @staticmethod
    def _get_lines_which_intersect_rectangle(df, x_min, y_min, x_max, y_max):
        # get all the lines which are entirely inside the rectangle:
        new_df = df.loc[
            (x_min < df.x1) & (df.x1 < x_max) &
            (x_min < df.x2) & (df.x2 < x_max) &
            (y_min < df.y1) & (df.y1 < y_max) &
            (y_min < df.y2) & (df.y2 < y_max)
            ]

        # Any other lines must intersect an edge. There are 4 edges.
        edges = [
            [x_min, y_min, x_min, y_max],
            [x_min, y_max, x_max, y_max],
            [x_max, y_max, x_max, y_min],
            [x_max, y_min, x_min, y_min],
        ]

        def _intersects(x1, y1, x2, y2) -> bool:
            dfs = []
            for edge in edges:
                dfs.append(HydrothermalVent._line_intersection(*edge, x1, y1, x2, y2))
            return dfs[0] | dfs[1] | dfs[2] | dfs[3]

        isc = df.loc[
            _intersects(df.x1, df.y1, df.x2, df.y2)
        ]
        new_df = new_df.append(isc)

        return new_df

    @staticmethod
    def _line_intersection(x1: int, y1: int, x2: int, y2: int,
                           x3: pd.DataFrame, y3: pd.DataFrame, x4: pd.DataFrame, y4:pd.DataFrame) -> pd.DataFrame:

        if x1 == x2 and y1 == y2:
            # we have a point

            def distance(ax, ay, bx, by):
                return np.sqrt((ax - bx) ** 2 + (ay - by) ** 2)

            length = distance(x3, y3, x4, y4)
            distance_to_start = distance(x1, y1, x3, y3)
            distance_to_end = distance(x1, y1, x4, y4)

            retval = length == distance_to_start + distance_to_end
            return retval

        uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
        uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))

        # bitwise operators look wrong here, but they're necessary for pandas to work
        return (0 <= uA) & (uA <= 1) & (0 <= uB) & (uB <= 1)
