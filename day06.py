import fileinput
import numpy as np

from lantern_fish import LanternFish


for line in fileinput.input("input/day06.txt"):
    if line.strip == '':
        continue
    population = np.array(list(map(int, line.strip().split(','))))

print(population)

print(f"Found {len(population)} lantern fish in generation 0.")
print(LanternFish.calculate_number_of_lantern_fish(80, population))
print(LanternFish.calculate_number_of_lantern_fish(256, population))
