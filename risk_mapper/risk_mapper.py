import sys
import numpy as np

inf = np.iinfo(np.int64).max

class RiskMapper:
    @staticmethod
    def least_risk_path(maze: np.ndarray) -> int:
        target = maze.shape
        tx, ty = target[1] - 1, target[0] - 1
        # tx, ty = 3, 3
        
        risk_map = np.full_like(maze, inf)
        visited = np.full_like(maze, False)
        risk_map[0,0] = 0

        def _potential_neighbours(x, y):
            return [
                (x, y - 1),
                (x - 1, y),
                (x + 1, y),
                (x, y + 1)
            ]

        def _next_step(x: int, y: int):

            if visited[y, x]:
                raise ValueError("Visiting already visited node.")

            current_node_risk = risk_map[y, x]

            neighbours = [p for p in _potential_neighbours(x, y) if 0 <= p[0] <= tx and 0 <= p[1] <= ty]
            neighbours = [n for n in neighbours if not visited[n[1], n[0]]]

            for n in neighbours:
                d = current_node_risk + maze[n[1], n[0]]
                if risk_map[n[1], n[0]] > d:
                    risk_map[n[1], n[0]] = d

            d_n_map = { risk_map[n]: n for n in neighbours}
            visited[y,x] = True


        while not visited[ty, tx]:
            modified_risk_map = np.where(np.logical_not(visited), risk_map, inf)
            p = np.unravel_index(modified_risk_map.argmin(), modified_risk_map.shape)
            y, x = p[0], p[1]
            _next_step(x, y)

        # with np.printoptions(linewidth=np.nan, threshold=sys.maxsize):
        #     print()
        #     print(risk_map)

        return risk_map[ty, tx]

    def full_maze(maze: np.ndarray, tx: int = 5, ty: int = 5):
        full_maze = maze - 1
        full_maze = np.concatenate([(full_maze + i) % 9 for i in range(tx)], axis=0)
        full_maze = np.concatenate([(full_maze + i) % 9 for i in range(tx)], axis=1)
        full_maze = full_maze + 1
        # with np.printoptions(linewidth=np.nan, threshold=sys.maxsize):
        #     print()
        #     print(full_maze)
        return full_maze