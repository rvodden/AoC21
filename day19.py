from beacon_scanner import BeaconScanner, Scanner
from itertools import combinations
import numpy as np
import json

with open('input/day19.txt') as file:
    input = file.read()

scanner_texts = input.split("\n\n")
scanners = []
for scanner_text in scanner_texts:
    beacons = []
    for beacon_text in scanner_text.splitlines()[1:]:
        beacons.append(np.array(list(map(int, beacon_text.split(","))), dtype="int32"))
    scanners.append(Scanner(beacons))

beacon_scanner = BeaconScanner(scanners)
beacons = beacon_scanner.beacons()
# print(json.dumps(sorted(beacons), indent=4))

print(len(beacons))

def manhatten_distance(lhs: tuple[int, int, int], rhs: tuple[int, int, int]) -> int:
    return abs(rhs[0] - lhs[0]) + abs(rhs[1] - lhs[1]) + abs(rhs[2] - lhs[2])

max_distance = 0
for scanner_pair in combinations((scanner.location for scanner in beacon_scanner._scanners), 2):
    max_distance = max(max_distance, manhatten_distance(scanner_pair[0], scanner_pair[1]))

print(max_distance)