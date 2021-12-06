import fileinput

import pandas as pd

from hydrothermal_vent import HydrothermalVent


def gen():
    for line in fileinput.input("input/day05.txt"):
        new_line = line.replace(' -> ', ',')
        yield tuple(map(int, new_line.strip().split(',')))


df = pd.DataFrame(gen(), columns=['x1', 'y1', 'x2', 'y2'])
print(HydrothermalVent.calculate_orthogonal_overlapping_vents(df))
