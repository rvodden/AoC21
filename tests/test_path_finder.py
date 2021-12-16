from path_finder import PathFinder

example_1 = """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

class TestPathFinder:

    def test_path_finder(self):
        edges = []
        for line in example_1.split("\n"):
            edges.append(tuple(line.strip().split("-")))

        edges = [e for e in edges if e != ('',)]

        assert PathFinder.count_paths(edges) == 10

    def test_path_finder_2(self):
        edges = []
        for line in example_1.split("\n"):
            edges.append(tuple(line.strip().split("-")))

        edges = [e for e in edges if e != ('',)]
        print(edges)
        assert PathFinder.count_paths_2(edges) == 36