from snailfish_number import SnailfishNumberBuilder, max_sum

with open('input/day18.txt') as file:
    input = file.read()

sfns = list(map(SnailfishNumberBuilder.build, input.strip().splitlines()))
sum = sfns[0]
for sfn in sfns[1:]:
    sum += sfn
sfns = list(map(SnailfishNumberBuilder.build, input.strip().splitlines()))
print(max_sum(sfns))
