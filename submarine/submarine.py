import pandas as pd
import numpy as np


class Submarine:
    @staticmethod
    def calculate_position(df: pd.DataFrame):
        df = df.groupby("direction").sum().T
        df["down"] = df["down"] - df["up"]
        df = df.drop(columns=["up"])
        df["forward"] = df["forward"] - df["backward"]
        df = df.drop(columns=["backward"])
        return df.product(axis=1)[0]

    @staticmethod
    def calculate_position2(df: pd.DataFrame):
        df['aim_delta'] = 0
        df.loc[df['direction'] == 'down', 'aim_delta'] = df.loc[df['direction'] == 'down', 'distance']
        df.loc[df['direction'] == 'up', 'aim_delta'] = - df.loc[df['direction'] == 'up', 'distance']
        df['aim'] = df['aim_delta'].cumsum()
        df['h_delta'] = df.loc[df['direction'] == 'forward', 'distance']
        df['d_delta'] = df.loc[df['direction'] == 'forward', 'distance'] * df.loc[df['direction'] == 'forward', 'aim']
        df = df.replace(np.nan, 0)
        df['horizontal'] = df['h_delta'].cumsum()
        df['depth'] = df['d_delta'].cumsum()
        return df[['horizontal', 'depth']].iloc[-1].product()
