from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import product, groupby
from functools import cache

WINNING_SCORE = 21


class Die(ABC):
    @abstractmethod
    def roll(self, number: int) -> list[int]:
        pass


class DiracDie(Die):
    _sides: int

    def __init__(self, sides: int = 3) -> None:
        self._sides = sides

    @cache
    def roll(self, number: int = 3) -> dict[int, int]:
        faces = (x + 1 for x in range(self._sides))
        throws = sorted(map(sum, product(faces, repeat=number)))
        return {x: sum(1 for _ in y) for x, y in groupby(throws)}


@dataclass(frozen=True, unsafe_hash=True)
class Player:
    position: int
    score: int = 0

    def move(self, position: int) -> 'Player':
        return Player(
            position,
            self.score + position
        )


@dataclass(frozen=True)
class GameState:
    players: tuple[Player]
    next_player: int = 0

    def move(self, steps: int):
        def new_position(player, steps):
            return (player.position - 1 + steps) % 10 + 1
        return GameState(
            tuple([
                player if idx != self.next_player else player.move(new_position(player, steps))
                for idx, player in enumerate(self.players)
            ]),
            1 - self.next_player
        )


def sum_tuples(ts: list[tuple[int, int]]) -> tuple[int, int]:
    result = (0, 0)
    for t in ts:
        result = (t[0] + result[0], t[1] + result[1])
    return result


@cache
def count_wins(
    current_state: GameState, die: Die, current_multiplier: int = 1
) -> tuple[int, int]:
    for idx, player in enumerate(current_state.players):
        if player.score >= WINNING_SCORE:
            result = [0, 0]
            result[idx] = current_multiplier
            return tuple(result)

    states = []
    for roll, multiplier in die.roll().items():
        state = current_state.move(roll)
        states.append((state, current_multiplier * multiplier))
    return sum_tuples(
        [count_wins(state, die, multiplier) for state, multiplier in states]
    )
