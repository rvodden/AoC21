import numpy as np
from paper_folder import PaperFolder

with open('input/day13.txt') as file:
    input_data = file.read()

# load dots into a list of tuples
dot_input, fold_input = input_data.split('\n\n')

dots = [tuple(map(int, line.strip().split(','))) for line in dot_input.strip().split('\n')]
folds = list(map( lambda x: (x[0], int(x[1])) ,[ tuple(line.strip().split(' ')[-1].split('=')) for line in fold_input.strip().split('\n') ]))

print(PaperFolder.count_dots(dots, [folds[0]]))
np.set_printoptions(linewidth=np.inf)
result = PaperFolder.fold_dots(dots, folds)

for row in result:
    for c in row:
        print(chr(9608) if c else ' ', end="")
    print("")
