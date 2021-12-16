import numpy as np
from paper_folder import PaperFolder

input_data = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""

output = np.array([
    [1,1,1,1,1],
    [1,0,0,0,1],
    [1,0,0,0,1],
    [1,0,0,0,1],
    [1,1,1,1,1],
    [0,0,0,0,0],
    [0,0,0,0,0]
])

class TestPaperFolder:

    def test_paper_folder(self):
        # load dots into a list of tuples
        dot_input, fold_input = input_data.split('\n\n')
        dots = [tuple(map(int, line.strip().split(','))) for line in dot_input.strip().split('\n')]

        folds = list(map( lambda x: (x[0], int(x[1])) ,[ tuple(line[-3:].strip().split('=')) for line in fold_input.strip().split('\n') ]))

        print(folds[0])
        assert PaperFolder.count_dots(dots, [folds[0]]) == 17
        out = PaperFolder.fold_dots(dots, folds) 
        print(out)
        assert (out == output).all()