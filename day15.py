import numpy as np
from risk_mapper import RiskMapper

with open('input/day15.txt') as file:
    input = file.read()

maze = np.array([[int(c) for c in row] for row in input.splitlines()])
print(RiskMapper.least_risk_path(maze))
print(RiskMapper.least_risk_path(RiskMapper.full_maze(maze)))