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

    @staticmethod
    def _value_counts(df: pd.DataFrame):
        new_df = pd.DataFrame(index=["0", "1"])
        for column in df.columns:
            new_df[column] = df[column].value_counts()
        return new_df

    @staticmethod
    def _convert_series_to_value(df):
        return int("".join(list(df)), 2)


    @staticmethod
    def calculate_gamma_rate(df: pd.DataFrame):
        new_df = Submarine._value_counts(df)
        return Submarine._convert_series_to_value(new_df.idxmax())

    @staticmethod
    def calculate_epsilon_rate(df: pd.DataFrame):
        new_df = Submarine._value_counts(df)
        return Submarine._convert_series_to_value(new_df.idxmin())

    @staticmethod
    def calculate_power_consumption(df):
        return Submarine.calculate_epsilon_rate(df) * Submarine.calculate_gamma_rate(df)

    @staticmethod
    def calculate_oxygen_generator_rating(df):
        for column in df.columns:
            count_df = Submarine._value_counts(df)

            # do we have the same number of 1s as 0s?
            if count_df[column].nunique() == 1:
                # if so, use 1
                most_used_bit = "1"
            else:
                most_used_bit = count_df[column].idxmax()

            df = df[df[column] == most_used_bit]
            if df[column].count() == 1:
                break
        return Submarine._convert_series_to_value(df.iloc[0])

    @staticmethod
    def calculate_co2_scrubber_rating(df):
        for column in df.columns:
            count_df = Submarine._value_counts(df)

            # do we have the same number of 1s as 0s?
            if count_df[column].nunique() == 1:
                # if so, use 0
                most_used_bit = "0"
            else:
                most_used_bit = count_df[column].idxmin()

            df = df[df[column] == most_used_bit]
            if df[column].count() == 1:
                break
        return Submarine._convert_series_to_value(df.iloc[0])

    @staticmethod
    def calculate_life_support_rating(df):
        return Submarine.calculate_co2_scrubber_rating(df) * Submarine.calculate_oxygen_generator_rating(df)
