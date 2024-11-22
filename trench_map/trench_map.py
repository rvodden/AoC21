from functools import cache


class Algorithm:
    def __init__(self, alg: str):
        self._alg = alg

    def __getitem__(self, value: int) -> bool:
        return self._alg[value] == "#"

    def flipper(self) -> bool:
        return self._alg[0] == '#' and self._alg[511] == '.'


class TrenchMap:
    _light_squares: set[tuple[int, int]]
    default_state: bool

    def __init__(self, default_state=False):
        self._light_squares = set()
        self.default_state = default_state

    def __getitem__(self, key: tuple[int, int]) -> bool:
        minx, miny, maxx, maxy = self.bounds()
        if minx > key[0] or key[0] > maxx or miny > key[1] or key[1] > maxy:
            # print(f"{key[0], key[1]} is out of bounds x = ({minx}, {maxx}), y = ({miny}, {maxy})!")
            return self.default_state
        return key in self._light_squares

    def __setitem__(self, key: tuple[int, int], value: bool):
        if value:
            self._light_squares.add(key)
        else:
            try:
                self._light_squares.remove(key)
            except KeyError:
                # we do not care if we're deleting something which does not exist
                pass

    def __len__(self):
        return len(self._light_squares)

    @cache
    def bounds(self) -> tuple[int, int, int, int]:
        xs = [i[0] for i in self._light_squares]
        ys = [i[1] for i in self._light_squares]

        return (min(xs), min(ys), max(xs), max(ys))

    def get_binary_number(self, key: tuple[int, int]) -> int:
        x1, y1 = key

        binary_string = ""

        for y in [y1 - 1, y1, y1 + 1]:
            for x in [x1 - 1, x1, x1 + 1]:
                binary_string = binary_string + ("1" if self[x, y] else "0")

        return int(binary_string, 2)

    def __str__(self):
        retval = ""
        minx, miny, maxx, maxy = self.bounds()
        for y in range(miny - 2, maxy + 3):
            for x in range(minx - 2, maxx + 3):
                retval = retval + ("#" if self[x, y] else ".")
            retval = retval + "\n"

        return retval


class TrenchMapEnhancer:
    def __init__(self, algorithm: Algorithm):
        self._algorithm = algorithm

    def __call__(self, input: TrenchMap) -> TrenchMap:
        minx, miny, maxx, maxy = input.bounds()

        default_state = (not input.default_state) if self._algorithm.flipper() else input.default_state
        retval = TrenchMap(default_state=default_state)
        for x in range(minx - 2, maxx + 3):
            for y in range(miny - 2, maxy + 3):
                retval[x, y] = self._algorithm[input.get_binary_number((x, y))]

        return retval
