import pandas as pd

from sonar_sweep import SonarSweep


depths = pd.read_csv("input/day01.txt", header=None, names=["depth"])

print(depths)
print(SonarSweep.count_increases(depths))

print(SonarSweep.count_increases(SonarSweep.rolling_windows(depths)))
