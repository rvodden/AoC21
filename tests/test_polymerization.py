from polymerization import Polymerization

input = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

class TestPolymerization:
    def test_most_minus_least(self):
        input_strings, polymer_template = input.split("\n\n")

        input_string = input_strings.strip()

        polymer_template_map = { k: v for k, v in map( lambda s: s.split(' -> '), polymer_template.strip().split("\n"))}

        assert Polymerization.most_minus_least(input_string, polymer_template_map) == 1588
        assert Polymerization.most_minus_least(input_string, polymer_template_map, 40) == 2188189693529