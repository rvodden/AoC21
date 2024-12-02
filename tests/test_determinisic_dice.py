import pytest

from deterministic_die import DeterministicDie, Game

test_input = "Player 1 starting position: 4\nPlayer 2 starting position: 8\n"


@pytest.fixture
def deterministic_die() -> DeterministicDie:
    return DeterministicDie()


@pytest.fixture
def game(deterministic_die) -> Game:
    return Game([4, 8], deterministic_die)


class TestDeterministicDice:
    def test_roll(self, deterministic_die):
        for i in range(200):
            assert deterministic_die.roll() == (i % 100) + 1


class TestGame:
    def test_init(self, game):
        assert game._players[0].position == 4
        assert game._players[1].position == 8

    def test_move(self, game):
        game._move(game._players[0], 6)
        assert game._players[0].position == 10
        assert game._players[0].score == 10

        game._move(game._players[0], 24)
        assert game._players[0].position == 4
        assert game._players[0].score == 14

    def test_run_turn(self, game):
        rolls = game._run_turn(0)
        assert game._players[0].position == 10
        assert game._players[0].score == 10
        assert game._players[1].position == 3
        assert game._players[1].score == 3
        assert rolls == 6

    def test_run(self, game):
        assert game.run() == 739785
