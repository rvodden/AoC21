from __future__ import annotations
from copy import deepcopy
import io
from math import ceil, floor
from re import I
from typing import Union

class SnailfishNumber:
    def __init__(self, fst: SnailfishNumber | int, snd: SnailfishNumber | int, depth: int = 1, parent: SnailfishNumber | None = None):
        self._fst = fst
        if self._is_snailfish_number(fst):
            fst._parent = self
        self._snd = snd
        if self._is_snailfish_number(snd):
            snd._parent = self
        self._depth = depth
        self._parent = parent

    def __eq__(self, other) -> bool:

        return type(self) == type(other) and self._snd == other._snd and self._fst == other._fst

    def __str__(self) -> str:
        return f"[{self._fst},{self._snd}]"

    def __abs__(self) -> int:
        fst_val = self._fst if isinstance(self._fst, int) else abs(self._fst)
        snd_val = self._snd if isinstance(self._snd, int) else abs(self._snd)
        return 3 * fst_val + 2 * snd_val

    def __add__(self, other) -> SnailfishNumber:
        sfn = SnailfishNumber(self, other)
        sfn.depth = 1
        sfn.reduce()
        return sfn

    @staticmethod
    def _is_snailfish_number(n: any) -> bool:
        return isinstance(n, SnailfishNumber)

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, depth):
        self._depth = depth
        if self._is_snailfish_number(self._fst):
            self._fst.depth = depth + 1
        if self._is_snailfish_number(self._snd):
            self._snd.depth = depth + 1
        

    @property
    def left(self) -> int:
        if self._depth == 1:
            return 0
        
        if self._parent._fst is self:
            return self._parent.left
        
        l = self._parent._fst
        while self._is_snailfish_number(l):
            l = l._snd
        return l

    @left.setter
    def left(self, value: int) -> None:
        if self._depth == 1:
            return
        
        if self._parent._fst is self:
            self._parent.left = value
            return

        l = self._parent._fst
        if isinstance(l, int):
            self._parent._fst = value
            return
        
        while self._is_snailfish_number(l._snd):
            l = l._snd
        l._snd = value

    @property
    def right(self) -> int:
        if self._depth == 1:
            return 0
        
        if self._parent._snd is self:
            return self._parent.right
        
        r = self._parent._snd
        while self._is_snailfish_number(r):
            r = r._fst
        return r

    @right.setter
    def right(self, value: int) -> None:
        if self._depth == 1:
            return
        
        if self._parent._snd is self:
            self._parent.right = value
            return

        r = self._parent._snd
        if isinstance(r, int):
            self._parent._snd = value
            return

        while self._is_snailfish_number(r._fst):
            r = r._fst
        r._fst = value
    
    def explode(self) -> bool:
        if self._depth < 4:
            changed = False
            if self._is_snailfish_number(self._fst):
                if self._fst.explode():
                    return True

            if self._is_snailfish_number(self._snd):
                return self._snd.explode()
            return False

        if isinstance(self._fst, SnailfishNumber):
            #explode this, as its the first one.
            if not isinstance(self._fst._fst, int) or not isinstance(self._fst._snd, int):
                raise ValueError(f"5th level SnailfishNumbers must always be integers.")
            self._fst.left = self._fst.left + self._fst._fst
            self._fst.right = self._fst.right + self._fst._snd
            self._fst = 0
            return True

        if isinstance(self._snd, SnailfishNumber):
            #explode this, as its the first one.
            if not isinstance(self._snd._fst, int) or not isinstance(self._snd._snd, int):
                raise ValueError(f"5th level SnailfishNumbers must always be integers.")
            self._snd.left = self._snd.left + self._snd._fst
            self._snd.right = self._snd.right + self._snd._snd
            self._snd = 0
            return True
        
        return False

    def split(self) -> bool:
        if self._is_snailfish_number(self._fst):
            changed = self._fst.split()
            if changed:
                return True
        elif self._fst > 9:
            self._fst = SnailfishNumber(floor(self._fst / 2.0), ceil(self._fst / 2.0), depth = self._depth + 1, parent = self)
            return True

        if self._is_snailfish_number(self._snd):
            changed = self._snd.split()
            if changed:
                return True
        elif self._snd > 9:
            self._snd = SnailfishNumber(floor(self._snd / 2.0), ceil(self._snd / 2.0), depth = self._depth + 1, parent = self)
            return True

        return False

    def reduce(self):
        while self.explode() or self.split():
            ...
        

class SnailfishNumberBuilder:

    @staticmethod
    def _read_element(input, depth) -> SnailfishNumber | int:
        char = input.read(1)
        buffer = b""
        match char:
            case b'[':
                input.seek(-1, io.SEEK_CUR)
                return SnailfishNumberBuilder._build(input, depth=depth+1)
            case b'0' | b'1' | b'2' | b'3' | b'4' | b'5' | b'6' | b'7' | b'8' | b'9':
                while char not in [b',', b']']:
                    buffer += char
                    char = input.read(1)
                input.seek(-1, io.SEEK_CUR)
                return int(buffer)
            case default:
                raise ValueError(f"Unexpected: {char}.")
    
    @staticmethod
    def _build(input: io.BytesIO, depth: int = 1) -> SnailfishNumber:
        char = input.read(1)
        if char != b'[':
            raise ValueError(f"First character of a snail fish must be '[' not '{char}'")

        fst = SnailfishNumberBuilder._read_element(input, depth)

        char = input.read(1)
        if char != b',':
            raise ValueError(f"Expected ',' not '{char}'")

        snd = SnailfishNumberBuilder._read_element(input, depth)
        
        char = input.read(1)
        if char != b']':
            raise ValueError(f"SnailfishNumbers must terminate with ']' not '{char}'")

        sfn = SnailfishNumber(fst, snd, depth=depth)
        if isinstance(fst, SnailfishNumber):
            fst._parent = sfn
        if isinstance(snd, SnailfishNumber):
            snd._parent = sfn
        return sfn

    @staticmethod
    def build(input: str):
        bytes = str.encode(input)
        stream = io.BytesIO(bytes)
        return SnailfishNumberBuilder._build(stream)


def max_sum(sfns: list[SnailfishNumber]) -> int:
    return max([abs(deepcopy(a) + deepcopy(b)) for a in sfns for b in sfns if a != b])
