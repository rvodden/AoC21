import fileinput
import pandas as pd

from crab_submarine import CrabSubmarine


for line in fileinput.input("input/day07.txt"):
    if line.strip == '':
        continue
    population = pd.DataFrame(list(map(int, line.strip().split(','))), columns=['positions'])

print(population)
print(CrabSubmarine.calculate_crab_fuel(population))
print(CrabSubmarine.calculate_crab_fuel2(population))

