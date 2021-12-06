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

    def diagnostics(self):
        df = pd.DataFrame([
            ["0","0","1","0","0"],
            ["1","1","1","1","0"],
            ["1","0","1","1","0"],
            ["1","0","1","1","1"],
            ["1","0","1","0","1"],
            ["0","1","1","1","1"],
            ["0","0","1","1","1"],
            ["1","1","1","0","0"],
            ["1","0","0","0","0"],
            ["1","1","0","0","1"],
            ["0","0","0","1","0"],
            ["0","1","0","1","0"]
        ])
        return df

    def test_calculate_position(self):
        df = self.instructions()
        assert Submarine.calculate_position(df) == 150

    def test_calculate_position2(self):
        df = self.instructions()
        assert Submarine.calculate_position2(df) == 900

    def test_gamma_rate(self):
        df = self.diagnostics()
        assert Submarine.calculate_gamma_rate(df) == 22

    def test_epsilon_rate(self):
        df = self.diagnostics()
        assert Submarine.calculate_epsilon_rate(df) == 9

    def test_power_consumption(self):
        df = self.diagnostics()
        assert Submarine.calculate_power_consumption(df) == 198

    def test_oxygen_generator_rating(self):
        df = self.diagnostics()
        assert Submarine.calculate_oxygen_generator_rating(df) == 23

    def test_co2_scrubber_rating(self):
        df = self.diagnostics()
        assert Submarine.calculate_co2_scrubber_rating(df) == 10

    def test_life_support_rating(self):
        df = self.diagnostics()
        assert Submarine.calculate_life_support_rating(df) == 230
