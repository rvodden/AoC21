import fileinput
import numpy as np

from octopus_flasher import OctopusFlasher

input_data = []
for line in fileinput.input('input/day11.txt'):
    input_data.append([int(c) for c in line.strip()])

input_data = np.array(input_data)

print(OctopusFlasher.count_flashes(input_data))
print(OctopusFlasher.step_when_all_octopus_flash(input_data))