import io
from bits_decoder import BitsDecoder

with open('input/day16.txt') as file:
    input = file.read()

print(BitsDecoder.sum_versions(io.StringIO(input.strip())))
print(BitsDecoder.evaluate(io.StringIO(input.strip())))