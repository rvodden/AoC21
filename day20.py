from trench_map import TrenchMap, Algorithm, TrenchMapEnhancer


with open("input/day20.txt") as input_file:
    text = input_file.read()

algorithm_data, trench_map_data = text.split("\n\n")

algorithm = Algorithm(algorithm_data)

trench_map = TrenchMap()

for y, line in enumerate(trench_map_data.split("\n")):
    for x, char in enumerate(line):
        if char != '#':
            continue
        trench_map[x, y] = 1


trench_map_enhancer = TrenchMapEnhancer(algorithm)

event1 = trench_map_enhancer(trench_map)
event2 = trench_map_enhancer(event1)

print(len(event2))

event = trench_map
for _ in range(50):
    event = trench_map_enhancer(event)
print(len(event))
