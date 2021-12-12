import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class CrabSubmarine:

    @staticmethod
    def calculate_crab_fuel(df: pd.DataFrame) -> int:
        ps = np.array(df['positions'])
        xs = np.array(range(df['positions'].max()))
        ys = np.array([], dtype=int)

        def _residue(x: int) -> int:
            return abs(ps - x).sum()

        residue = np.frompyfunc(_residue, 1, 1)

        ys = residue(xs)
        solution = np.where(ys == min(ys))
        plt.plot(xs, ys)
        plt.axvline(solution, color='black', linestyle='dashed')
        plt.show()

        return min(ys)

    @staticmethod
    def calculate_crab_fuel2(df: pd.DataFrame) -> int:
        ps = np.array(df['positions'])
        xs = np.array(range(ps.max()))
        ys = np.array([], dtype=int)

        def _fuel_usage(x: int) -> int:
            return x * (x + 1) // 2
        fuel_usage = np.frompyfunc(_fuel_usage, 1, 1)

        def _residue(x: int) -> int:
            return fuel_usage(abs(ps - x)).sum()
        residue = np.frompyfunc(_residue, 1, 1)

        ys = residue(xs)

        solution = np.where(ys == min(ys))
        plt.plot(xs, ys)
        plt.axvline(solution, color='black', linestyle='dashed')
        plt.show()

        return min(ys)
