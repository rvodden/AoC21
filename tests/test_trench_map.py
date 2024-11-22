from trench_map import TrenchMap, TrenchMapEnhancer, Algorithm

import pytest


@pytest.fixture
def algorithm():
    return Algorithm(
        "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##"
        "#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###"
        ".######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#."
        ".#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#....."
        ".#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.."
        "...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#....."
        "..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#"
    )


@pytest.fixture
def trench_map():
    retval = TrenchMap()
    retval[0, 0] = 1
    retval[3, 0] = 1
    retval[0, 1] = 1
    retval[0, 2] = 1
    retval[1, 2] = 1
    retval[4, 2] = 1
    retval[2, 3] = 1
    retval[2, 4] = 1
    retval[3, 4] = 1
    retval[4, 4] = 1

    print("\n" + str(retval))

    return retval

@pytest.fixture
def trench_map_enhancer(algorithm):
    return TrenchMapEnhancer(algorithm)


class TestTrenchMap:

    def test_get_binary_number(self, trench_map: TrenchMap):
        assert trench_map.get_binary_number((2, 2)) == 34


class TestAlgorithm:

    def test_flipper(self, algorithm):
        assert not algorithm.flipper()


class TestTrenchMapEnhancer:
    
    def test_call(self, trench_map, trench_map_enhancer):
        event1 = trench_map_enhancer(trench_map)
        print(event1)
        event2 = trench_map_enhancer(event1)
        print(event2)

        assert len(event2) == 35

    def test_part_2(self, trench_map, trench_map_enhancer):
        event = trench_map
        for _ in range(50):
            event = trench_map_enhancer(event)

        assert len(event) == 3351
