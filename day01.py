from sonar_sweep import sonar_sweep
import fileinput


depths = []
for line in fileinput.input("input/day01.txt"):
    depths.append(int(line))
print(sonar_sweep(depths))