from polymerization import Polymerization


with open('input/day14.txt') as file:
    input = file.read()

input_strings, polymer_template = input.split("\n\n")
input_string = input_strings.strip()
polymer_template_map = { k: v for k, v in map( lambda s: s.split(' -> '), polymer_template.strip().split("\n"))}

print(Polymerization.most_minus_least(input_string, polymer_template_map))
print(Polymerization.most_minus_least(input_string, polymer_template_map, 40))