import pandas as pd


class Submarine:
    @staticmethod
    def calculate_position(df: pd.DataFrame):
        df = df.groupby("direction").sum().T
        df["down"] = df["down"] - df["up"]
        df = df.drop(columns=["up"])
        df["forward"] = df["forward"] - df["backward"]
        df = df.drop(columns=["backward"])
        return df.product(axis=1)[0]

