# target area: x=236..262, y=-78..-58

from probe_launcher import ProbeLauncher

p = ProbeLauncher((236, 262), (-78, -58))
print(p.maximize_height())
print(p.count_hits())