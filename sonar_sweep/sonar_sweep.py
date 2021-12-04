import pandas as pd


class SonarSweep:
    @staticmethod
    def count_increases(depths: pd.DataFrame):
        diffs = depths.diff()
        return diffs[diffs > 0].count()[0]
