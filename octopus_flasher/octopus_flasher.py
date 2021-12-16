import numpy as np


class OctopusFlasher:

    @staticmethod
    def step(input_data: np.ndarray) -> tuple[np.ndarray, int]:
        next_gen = input_data + 1

        flashed = np.full_like(input_data, 0)

        flashes = np.argwhere(next_gen > 9)
        for flash in flashes:
            next_gen, flashed = OctopusFlasher.flash(next_gen, flashed, flash)

        flashed_args = np.argwhere(flashed).T

        next_gen[flashed_args[0], flashed_args[1]] = 0

        return next_gen, np.count_nonzero(flashed)

    @staticmethod
    def flash(input_data: np.ndarray, flashed: np.ndarray, coords: np.array) -> tuple[np.ndarray, np.ndarray]:
        if flashed[coords[0], coords[1]]:
            return input_data, flashed
        y_max, x_max = input_data.shape
        y, x = tuple(coords)
        flashed[y, x] = 1

        potential_neighbours = [(y - 1, x - 1), (y - 1, x), (y - 1, x + 1),
                                (y, x - 1), (y, x + 1),
                                (y + 1, x - 1), (y + 1, x), (y + 1, x + 1)]
        neighbours = np.array([p for p in potential_neighbours if y_max > p[0] >= 0 and x_max > p[1] >= 0]).T
        input_data[neighbours[0], neighbours[1]] = input_data[neighbours[0], neighbours[1]] + 1

        for neighbour in neighbours.T:
            y, x = neighbour[0], neighbour[1]
            if input_data[y, x] > 9 and not flashed[y, x]:
                input_data, flashed = OctopusFlasher.flash(input_data, flashed, np.array([y, x]))

        return input_data, flashed

    @staticmethod
    def count_flashes(input_data: np.ndarray, steps=100) -> int:
        flashes = 0
        for _ in range(steps):
            input_data, new_flashes = OctopusFlasher.step(input_data)
            flashes += new_flashes

        return flashes

    @staticmethod
    def step_when_all_octopus_flash(input_data: np.ndarray) -> int:
        step = 0
        while (input_data != 0).any():
            step += 1
            input_data, _ = OctopusFlasher.step(input_data)
        return step
