import pandas as pd

from sonar_sweep import SonarSweep


depths = pd.read_csv("input/day01.txt")
print(SonarSweep.count_increases(depths))
