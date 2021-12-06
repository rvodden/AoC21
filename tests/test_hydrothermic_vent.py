import pandas as pd

from hydrothermal_vent import HydrothermalVent


class TestHydrothermalVent:
    def hydrothermal_vents(self):
        return pd.DataFrame([[0, 9, 5, 9],
                             [8, 0, 0, 8],
                             [9, 4, 3, 4],
                             [2, 2, 2, 1],
                             [7, 0, 7, 4],
                             [6, 4, 2, 0],
                             [0, 9, 2, 9],
                             [3, 4, 1, 4],
                             [0, 0, 8, 8],
                             [5, 5, 8, 2]], columns=["x1", "y1", "x2", "y2"])

    def test_count_orthogonal_overlapping_vents(self):
        df = self.hydrothermal_vents()
        assert HydrothermalVent.calculate_orthogonal_overlapping_vents(df) == 5

    def test_count_orthogonal_overlapping_vents_boundary_tests(self):
        # df = pd.DataFrame([
        #     [1, 1, 1, 1],
        #     [1, 1, 1, 1]
        # ], columns=["x1", "y1", "x2", "y2"])
        # assert HydrothermalVent.calculate_orthogonal_overlapping_vents(df) == 1

        df = pd.DataFrame([
            [1, 1, 2, 1],
            [1, 1, 2, 1]
        ], columns=["x1", "y1", "x2", "y2"])
        assert HydrothermalVent.calculate_orthogonal_overlapping_vents(df) == 2

        # df = pd.DataFrame([
        #     [1, 1, 5, 1],
        #     [1, 1, 2, 1],
        #     [4, 1, 5, 1]
        # ], columns=["x1", "y1", "x2", "y2"])
        # assert HydrothermalVent.calculate_orthogonal_overlapping_vents(df) == 4


    def test_get_lines_which_intersect_rectangle(self):
        df = pd.DataFrame([
            [1, 1, 2, 1]
        ], columns=["x1", "y1", "x2", "y2"])
        assert len(HydrothermalVent._get_lines_which_intersect_rectangle(
                df, 3, 1, 3, 1)) == 0

        df = pd.DataFrame([
            [1, 1, 2, 1],
            [1, 1, 5, 1]
        ], columns=["x1", "y1", "x2", "y2"])
        assert len(HydrothermalVent._get_lines_which_intersect_rectangle(
            df, 2, 1, 2, 1)) == 2

        df = pd.DataFrame([
            [1, 1, 2, 1],
            [1, 1, 2, 1]
        ], columns=["x1", "y1", "x2", "y2"])
        assert len(HydrothermalVent._get_lines_which_intersect_rectangle(
            df, 1, 1, 1, 1)) == 2

        df = pd.DataFrame([
            [1, 1, 2, 1],
            [1, 1, 2, 1]
        ], columns=["x1", "y1", "x2", "y2"])
        assert len(HydrothermalVent._get_lines_which_intersect_rectangle(
            df, 1, 1, 2, 1)) == 2

    def test_line_intersesction(self):
        df = pd.DataFrame([
            [1, 1, 2, 1]
        ], columns=["x1", "y1", "x2", "y2"])
        assert not HydrothermalVent._line_intersection(
            3, 1, 3, 1, df.x1, df.y1, df.x2, df.y2
        ).any()

        df = pd.DataFrame([
            [1, 1, 3, 1]
        ], columns=["x1", "y1", "x2", "y2"])
        assert HydrothermalVent._line_intersection(
            3, 1, 3, 1, df.x1, df.y1, df.x2, df.y2
        ).any()

        df = pd.DataFrame([
            [1, 1, 2, 1]
        ], columns=["x1", "y1", "x2", "y2"])
        assert HydrothermalVent._line_intersection(
            2, 1, 2, 1, df.x1, df.y1, df.x2, df.y2
        ).any()

        df = pd.DataFrame([
            [1, 1, 2, 1]
        ], columns=["x1", "y1", "x2", "y2"])
        assert HydrothermalVent._line_intersection(
            1, 1, 1, 1, df.x1, df.y1, df.x2, df.y2
        ).any()

        df = pd.DataFrame([
            [1, 1, 5, 1]
        ], columns=["x1", "y1", "x2", "y2"])
        assert HydrothermalVent._line_intersection(
            2, 1, 2, 1, df.x1, df.y1, df.x2, df.y2
        ).any()
