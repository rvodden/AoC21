import numpy as np
from typing import Callable


class LanternFish:

    @staticmethod
    def generate(generations: int, population: np.array, new_fish: int = 0) -> int:
        if generations == 0:
            return len(population)

        gen_next: Callable[[np.array], np.array] = np.frompyfunc(lambda p: p - 1 if p != 0 else 6, 1, 1)
        new_population: np.array = gen_next(population)

        number_of_new_lantern_fish: int = np.sum(new_population == 0).item()
        new_population = np.append(new_population, np.full(shape=new_fish, fill_value=8, dtype=int))

        return LanternFish.generate(generations - 1, new_population, number_of_new_lantern_fish)

    @staticmethod
    def calculate_number_of_lantern_fish(generations: int, population: np.array):
        y = np.bincount(population)
        ii = np.nonzero(y)[0]

        population_distribution = np.vstack((ii, y[ii])).T

        for i in range(9):
            if i not in population_distribution[:, 0]:
                population_distribution = np.vstack([population_distribution, [i, 0]])

        print(population_distribution[:, 0].T)
        print(population_distribution[:, 1].T)
        return LanternFish.generate2(generations - 1, population_distribution)

    @staticmethod
    def generate2(generations: int, population_distribution: np.array) -> int:
        if generations == 0:
            return np.sum(population_distribution[:, 1]).item()

        new_fish = population_distribution[0][1].item()
        population_distribution = np.delete(population_distribution, 0, 0)
        population_distribution[:, 0] = population_distribution[:, 0] - 1
        population_distribution[6, 1] = population_distribution[6, 1] + new_fish

        population_distribution = np.vstack([population_distribution, [8, new_fish]])
        print(population_distribution[:, 1].T)

        return LanternFish.generate2(generations - 1, population_distribution)
