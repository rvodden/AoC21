from abc import ABC, abstractmethod
from dataclasses import dataclass


class Die(ABC):
    @abstractmethod
    def roll(self) -> int:
        pass


class DeterministicDie(Die):
    _sides: int
    _state: int

    def __init__(self, sides: int = 100) -> None:
        self._sides = sides
        self._state = 0

    def roll(self) -> int:
        if self._state >= self._sides:
            self._state = 0
        self._state += 1
        return self._state


@dataclass
class Player:
    position: int
    score: int = 0


class GameWon(Exception):
    def __init__(self, rolls):
        super().__init__()
        self.rolls = rolls


class Game:
    _POSITIONS = 10
    _ROLLS = 3
    _WINNING_SCORE = 1000
    _players: list[Player]
    _die: Die

    def __init__(self, positions: list[int], die: Die) -> None:
        self._players = []
        for position in positions:
            self._players.append(Player(position))
        self._die = die

    def _move(self, player: Player, steps: int) -> None:
        player.position = ((player.position - 1) + steps) % self._POSITIONS + 1
        if player.position == 0:
            player.position = 1
        player.score += player.position

    def _run_turn(self, rolls) -> None:
        for player in self._players:
            steps = 0
            for _ in range(self._ROLLS):
                steps += self._die.roll()
            rolls += 3
            self._move(player, steps)
            if player.score >= self._WINNING_SCORE:
                raise GameWon(rolls)
        return rolls

    def run(self) -> int:
        rolls = 0
        while True:
            try:
                rolls = self._run_turn(rolls)
            except GameWon as e:
                losing_score = (
                    self._players[0].score
                    if self._players[0].score < self._WINNING_SCORE
                    else self._players[1].score
                )
                return losing_score * e.rolls
