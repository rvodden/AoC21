import numpy as np

from lantern_fish import LanternFish


class TestLanternFish:
    def test_example_population(self):
        population = np.array([3, 4, 3, 1, 2], dtype=int)
        assert LanternFish.generate(18, population) == 26
        assert LanternFish.generate(80, population) == 5934

    def test_example_population2(self):
        population = np.array([3, 4, 3, 1, 2], dtype=int)
        assert LanternFish.calculate_number_of_lantern_fish(18, population) == 26
        assert LanternFish.calculate_number_of_lantern_fish(80, population) == 5934
