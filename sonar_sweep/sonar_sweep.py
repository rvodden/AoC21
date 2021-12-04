import pandas as pd


class SonarSweep:
    @staticmethod
    def count_increases(df: pd.DataFrame):
        df = df.diff()
        return df[df > 0].count()[0]

    @staticmethod
    def rolling_windows(df: pd.DataFrame):
        return df.rolling(window=3).sum()
