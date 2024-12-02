from dataclasses import dataclass
from typing import Self

@dataclass(frozen=True)
class Cuboid:
    x: tuple[int, int]
    y: tuple[int, int]
    z: tuple[int, int]

    def overlap(self, other: "Step") -> Self | None:
        x = (max(self.x[0], other.x[0]), min(self.x[1], other.x[1]))
        y = (max(self.y[0], other.y[0]), min(self.y[1], other.y[1]))
        z = (max(self.z[0], other.z[0]), min(self.z[1], other.z[1]))

        if x[0] > x[1] or y[0] > y[1] or z[0] > z[1]:
            return None

        return Cuboid(x, y, z)

    def volume(self) -> int:
        return (
            (self.x[1] - self.x[0] + 1)
            * (self.y[1] - self.y[0] + 1)
            * (self.z[1] - self.z[0] + 1)
        )


@dataclass(frozen=True)
class Step:
    state: bool
    cuboid: Cuboid


def parse_step(text: str) -> Step | None:
    # on x=10..12,y=10..12,z=10..12
    state, cuboid = text.split(" ")
    state = state == "on"
    ranges = [
        tuple([int(num) for num in range.split("=")[1].split("..")])
        for range in cuboid.split(",")
    ]
    for x, y in ranges:
        if x < -50 or x > 50 or y < -50 or y > 50:
            return None
    return Step(state, Cuboid(*ranges))


class Grid:
    def __init__(self):
        self._additive_cuboids = []
        self._subtractive_cuboids = []

    def add_cuboid(self, cuboid: Cuboid):
        for additive_cuboid in self._additive_cuboids:
            if overlap := additive_cuboid.overlap(cuboid):
                self._subtractive_cuboids.append(overlap)
        self._additive_cuboids.append(cuboid)
        
    def subtract_cuboid(self, cuboid: Cuboid):
        new_subs = []
        for additive_cuboid in self._additive_cuboids:
            if overlap := additive_cuboid.overlap(cuboid):
                new_subs.append(overlap)
                
        for subtractive_cuboid in self._subtractive_cuboids:
            if overlap := subtractive_cuboid.overlap(cuboid):
                self._additive_cuboids.append(overlap)
                
        self._subtractive_cuboids.extend(new_subs)

    def on_cubes(self) -> int:
        result = 0
        for additive_cuboid in self._additive_cuboids:
            result += additive_cuboid.volume()
            
        for subtractive_cuboid in self._subtractive_cuboids:
            result -= subtractive_cuboid.volume()
            
        return result

