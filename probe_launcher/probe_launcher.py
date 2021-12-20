from functools import reduce
from itertools import count
import operator
from typing import Optional
import numpy as np
from scipy.optimize import minimize


class MissedTarget(Exception):
    ...

class Undershot(MissedTarget):
    ...

class Overshot(MissedTarget):
    ...

class Probe:
    def __init__(self, dx: int, dy: int, tx: tuple[int, int], ty: tuple[int, int]):
        self._dx = dx
        self._dy = dy
        self._tx = tx
        self._ty = ty
        self._x = 0
        self._y = 0

    def step(self):
        self._x += self._dx
        self._y += self._dy
        self._dx -= 1 if self._dx > 0 else -1 if self._dx > 0 else 0
        self._dy -= 1

    def in_target(self):
        return (self._tx[0] <= self._x <= self._tx[1]) and (self._ty[0] <= self._y <= self._ty[1])

    def fire(self) -> Optional[int]:
        max_y = 0
        while not self.in_target():
            max_y = self._y if self._y > max_y else max_y
            if self._x > self._tx[1]:
                raise Overshot
            
            if (self._x < self._tx[0]) and (self._dx == 0):
                raise Undershot

            if (self._y < self._ty[0]):
                raise Overshot
            self.step()
        return max_y

class ProbeLauncher:
    def __init__(self, tx: tuple[int, int], ty: tuple[int, int]):
        if tx[0] > tx[1]:
            tx = (tx[1], tx[0])
        if ty[0] > ty[1]:
            ty = (ty[1], ty[0])
        print(f"Target {tx} ; {ty}}}")
        self._tx = tx
        self._ty = ty

    def launch(self, dx, dy):
        p = Probe(dx, dy, self._tx, self._ty)
        return p.fire()

    def maximize_height(self):
        # find the dx which gives us the most steps
        # as dx reduces by 1 each step, we're summing consecutive integers
        # so we need to find the first triange number bigger than tx[0]

        triangle = 0
        dxs = []
        number = count(1,1)
        while triangle <= self._tx[1]:
            if triangle >= self._tx[0]:
                dxs.append(n)
            n = next(number)
            triangle += n

        if len(dxs) == 0:
            raise ValueError(f"No triangle number exists between tx[0]{self._tx[0]} and tx[1]{self._tx[1]}")

        print(f"Using {dxs} for dx, which will take us to {list(map(lambda x: x * (x+1) / 2, dxs)) }.")
        dy = abs(self._ty[0] + 1)
        print(f"Trying {dy} as dy.")
        
        height = max(map(lambda dx : self.launch(dx, dy), dxs))
        print(f"Height is {height}")
        return height

    def count_hits(self):
        hits = 0
        for dx in range(0, self._tx[1] + 1):
            for dy in range(self._ty[0], -self._ty[0]):
                try:
                    self.launch(dx, dy)
                    hits += 1
                except MissedTarget:
                    ...
        return hits
