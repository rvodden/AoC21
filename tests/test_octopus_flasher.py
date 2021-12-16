import numpy as np

from octopus_flasher import OctopusFlasher

input_data = np.array([[5, 4, 8, 3, 1, 4, 3, 2, 2, 3],
                       [2, 7, 4, 5, 8, 5, 4, 7, 1, 1],
                       [5, 2, 6, 4, 5, 5, 6, 1, 7, 3],
                       [6, 1, 4, 1, 3, 3, 6, 1, 4, 6],
                       [6, 3, 5, 7, 3, 8, 5, 4, 7, 8],
                       [4, 1, 6, 7, 5, 2, 4, 6, 4, 5],
                       [2, 1, 7, 6, 8, 4, 1, 7, 2, 1],
                       [6, 8, 8, 2, 8, 8, 1, 1, 3, 4],
                       [4, 8, 4, 6, 8, 4, 8, 5, 5, 4],
                       [5, 2, 8, 3, 7, 5, 1, 5, 2, 6]])


class TestOctopusFlasher:
    def test_step(self):
        step_one = np.array([[6, 5, 9, 4, 2, 5, 4, 3, 3, 4],
                             [3, 8, 5, 6, 9, 6, 5, 8, 2, 2],
                             [6, 3, 7, 5, 6, 6, 7, 2, 8, 4],
                             [7, 2, 5, 2, 4, 4, 7, 2, 5, 7],
                             [7, 4, 6, 8, 4, 9, 6, 5, 8, 9],
                             [5, 2, 7, 8, 6, 3, 5, 7, 5, 6],
                             [3, 2, 8, 7, 9, 5, 2, 8, 3, 2],
                             [7, 9, 9, 3, 9, 9, 2, 2, 4, 5],
                             [5, 9, 5, 7, 9, 5, 9, 6, 6, 5],
                             [6, 3, 9, 4, 8, 6, 2, 6, 3, 7]])

        step_two = np.array([[8, 8, 0, 7, 4, 7, 6, 5, 5, 5],
                             [5, 0, 8, 9, 0, 8, 7, 0, 5, 4],
                             [8, 5, 9, 7, 8, 8, 9, 6, 0, 8],
                             [8, 4, 8, 5, 7, 6, 9, 6, 0, 0],
                             [8, 7, 0, 0, 9, 0, 8, 8, 0, 0],
                             [6, 6, 0, 0, 0, 8, 8, 9, 8, 9],
                             [6, 8, 0, 0, 0, 0, 5, 9, 4, 3],
                             [0, 0, 0, 0, 0, 0, 7, 4, 5, 6],
                             [9, 0, 0, 0, 0, 0, 0, 8, 7, 6],
                             [8, 7, 0, 0, 0, 0, 6, 8, 4, 8]])

        assert (OctopusFlasher.step(input_data)[0] == step_one).all()
        next_gen = OctopusFlasher.step(step_one)
        assert (next_gen[0] == step_two).all()

    def test_count_flashes(self):
        assert OctopusFlasher.count_flashes(input_data) == 1656

    def test_step_when_all_octopus_flash(self):
        assert OctopusFlasher.step_when_all_octopus_flash(input_data) == 195
