import pandas as pd

from submarine import Submarine


class TestSubmarine:
    def instructions(self):
        df = pd.DataFrame([
            ["forward", 5],
            ["down", 5],
            ["forward", 8],
            ["up", 3],
            ["down", 8],
            ["forward", 2],
        ], columns=["direction", "distance"])
        df["direction"] = df["direction"].astype(pd.CategoricalDtype(["up", "down", "forward", "backward"], ordered=True))
        return df

    def test_calculate_position(self):
        df = self.instructions()
        assert Submarine.calculate_position(df) == 150
