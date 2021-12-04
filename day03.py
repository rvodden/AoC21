import pandas as pd

from submarine import Submarine

diags = pd.read_csv(
    "input/day03.txt",
    header=None,
    names=["diags"],
    dtype=str)['diags'].apply(lambda x: pd.Series(list(x))).astype(str)

print(Submarine.calculate_power_consumption(diags))
print(Submarine.calculate_life_support_rating(diags))
