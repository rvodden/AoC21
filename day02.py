import pandas as pd

from submarine import Submarine

df = pd.read_table("input/day02.txt", header=None, names=['direction', 'distance'], sep=" ")
df["direction"] = df["direction"].astype(pd.CategoricalDtype(["up", "down", "forward", "backward"], ordered=True))
print(df)
print(Submarine.calculate_position(df))
print(Submarine.calculate_position2(df))
