import networkx as nx
import matplotlib.pyplot as plt

class PathFinder:
    @staticmethod
    def count_paths(edges: list[tuple[str, str]]) -> int:
        g = nx.Graph(edges)
        return PathFinder._count_paths(g)

    def _count_paths(g: nx.Graph, start_node: str = "start") -> int:
        if start_node == 'end':
            return 1
        
        next_nodes = list(g.neighbors(start_node))
        
        if start_node.islower():
            g.remove_node(start_node)
        
        if not next_nodes:
            return 0

        
        return sum([PathFinder._count_paths(g.copy(), n) for n in next_nodes])

    def count_paths_2(edges: list[tuple[str, str]]) -> int:
        g = nx.Graph(edges)
        paths = []
        for n in [n for n in g.nodes if n.islower() and n not in ['start', 'end']]:
            new_node = n + "a"
            g.add_node(new_node)
            g.add_edges_from([(new_node, g) for g in g.neighbors(n)])
            new_paths = PathFinder._get_paths(g.copy())
            # filter out all paths which don't end at 'end'
            # and replace {new_node} with {n} so that paths a dedupped correctly
            paths += [[p if p != new_node else n for p in path] for path in new_paths if path[-1] == 'end']
            g.remove_node(new_node)
        dedupped_list_of_paths = list(map(list,set(map(tuple,paths))))
        for d in dedupped_list_of_paths:
            print(d)
        return len(dedupped_list_of_paths)

    def _get_paths(g: nx.Graph, start_node: str = 'start') -> list[list[str]]:
        if start_node == 'end':
            return [['end']]
        
        next_nodes = list(g.neighbors(start_node))
        
        if start_node.islower():
            g.remove_node(start_node)
        
        if not next_nodes:
            return [[]]
        

        return [[start_node] + path for next_node in next_nodes for path in PathFinder._get_paths(g.copy(), next_node)]
