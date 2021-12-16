import fileinput

from path_finder import PathFinder

edges = []
for line in fileinput.input('input/day12.txt'):
    edges.append(tuple(line.strip().split("-")))

print(PathFinder.count_paths(edges))
print(PathFinder.count_paths_2(edges))