import fileinput

from bingo import Bingo

infile = fileinput.input("input/day04.txt")

sequence = [int(s) for s in next(infile).strip().split(',')]

boards = []
line_no = 0
board = []
for line in infile:
    line = line.strip()
    if line == "":
        continue
    for num in line.split(" "):
        if num.strip() == '':
            continue
        board.append(int(num))
    if line_no == 4:
        boards.append(board)
        line_no = -1
        board = []
    line_no += 1

print(f"{len(boards)} boards have been loaded.")
print(f"{len(sequence)} numbers are in the bingo readout.")

for board in boards:
    if len(board) != 25:
        print()
        print(f"{board} is the wrong length")
        exit(255)

# print(Bingo.bingo(sequence, boards))
print(Bingo.bingo_last_board(sequence, boards))
