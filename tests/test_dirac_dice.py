import pytest

from dirac_dice import DiracDie, GameState, count_wins, Player

test_input = "Player 1 starting position: 4\nPlayer 2 starting position: 8\n"


@pytest.fixture
def dirac_die() -> DiracDie:
    return DiracDie()


class TestPlayer:
    player = Player(1)
    assert player.__hash__ is not None


class TestDiracDie:
    def test_roll(self, dirac_die):
        assert dirac_die.roll(3) == {
            3: 1,
            4: 3,
            5: 6,
            6: 7,
            7: 6,
            8: 3,
            9: 1,
        }

    def test_count_wins(self, dirac_die):
        game_state = GameState(players=(Player(4), Player(8)))
        p1wins, p2wins = count_wins(game_state, dirac_die)
        print(p1wins)
        print(p2wins)
        assert max(p1wins, p2wins) == 444356092776315

