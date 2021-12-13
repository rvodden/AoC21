import fileinput

from seven_segments import SevenSegments

inp = []
for line in fileinput.input("input/day08.txt"):
    signal_pattern, output_value = line.strip().split('|')
    inp.append([signal_pattern.strip().split(' '), output_value.strip().split(' ')])
print(SevenSegments.frequency(inp))
print(SevenSegments.sum(inp))