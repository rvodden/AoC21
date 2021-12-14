import fileinput
from syntax_checker import SyntaxChecker

file = fileinput.input('input/day10.txt')
print(SyntaxChecker.syntax_score(file))

file = fileinput.input('input/day10.txt')
print(SyntaxChecker.completion_score(file))