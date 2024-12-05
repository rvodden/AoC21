from amphipod import Amphipod, Burrow


class TestAmphipod:
    def test_get_moves(self):
        burrow = Burrow([
            Amphipod.AMBER,
            Amphipod.BRONZE,
            Amphipod.DESERT,
            Amphipod.COPPER,
            Amphipod.COPPER,
            Amphipod.BRONZE,
            Amphipod.AMBER,
            Amphipod.DESERT
        ])
        moves = burrow.get_moves()
        print(moves)
        assert False
