import pytest

from snailfish_number import SnailfishNumberBuilder, max_sum

class TestSnailfishNumber:


    build_values = [
        "[1,2]",
        "[[1,2],3]",
        "[9,[8,7]]",
        "[[1,9],[8,5]]",
        "[[[[1,2],[3,4]],[[5,6],[7,8]]],9]",
        "[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]",
        "[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]", 
    ]

    @pytest.mark.parametrize("input", build_values)
    def test_build(self, input):
        result = SnailfishNumberBuilder.build(input)
        print(result)
        assert str(result) == input

    magnitude_values = { 
        ("[9,1]", 29),
        ("[[9,1],[1,9]]", 129),
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
        ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
        ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
        ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488)
    }

    @pytest.mark.parametrize("value,result", magnitude_values)
    def test_magnitude(self, value, result):
        assert abs(SnailfishNumberBuilder.build(value)) == result

    explode_values = [
        ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
        ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
        ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
        ("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"),
        ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"),
        ("[[[[4,0],[5,4]],[[7,0],[[7,8],5]]],[10,[[11,9],[11,0]]]]","[[[[4,0],[5,4]],[[7,7],[0,13]]],[10,[[11,9],[11,0]]]]")
    ]

    @pytest.mark.parametrize("input,output", explode_values)
    def test_explode(self, input, output):
        sfn = SnailfishNumberBuilder.build(input)
        sfn.explode()
        assert str(sfn) == output

    split_values = [
        ("[10,0]","[[5,5],0]"),
        ("[11,0]","[[5,6],0]")
    ]

    @pytest.mark.parametrize("input,output", split_values)
    def test_split(self, input, output):
        sfn = SnailfishNumberBuilder.build(input)
        sfn.split()
        assert str(sfn) == output

    reduce_values = [
        ("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")
    ]
    
    @pytest.mark.parametrize("input,output", reduce_values)
    def test_reduce(self, input, output):
        sfn = SnailfishNumberBuilder.build(input)
        sfn.reduce()
        assert str(sfn) == output


    add_values = [
        ("""[1,1]
[2,2]
[3,3]
[4,4]""","[[[[1,1],[2,2]],[3,3]],[4,4]]"),
("""[1,1]
[2,2]
[3,3]
[4,4]
[5,5]""","[[[[3,0],[5,3]],[4,4]],[5,5]]"),
("""[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]""","[[[[5,0],[7,4]],[5,5]],[6,6]]"),
("""[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]""","[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"),
("""[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""","[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]"),
("""[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]""","[[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]]")
    ]

    @pytest.mark.parametrize("input,output", add_values)
    def test_add(self, input, output):
        sfns = list(map(SnailfishNumberBuilder.build, input.strip().splitlines()))
        sum = sfns[0]
        for sfn in sfns[1:]:
            sum += sfn
        assert str(sum) == output

    
    def test_max_sum(self):
        input = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""
        sfns = list(map(SnailfishNumberBuilder.build, input.strip().splitlines()))
        print([str(sfn) for sfn in sfns])
        assert max_sum(sfns) == 3993
