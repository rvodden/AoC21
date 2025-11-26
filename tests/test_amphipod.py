from amphipod import find_cheapest_path_cost, Amphipod, is_solved, create_part_two_state


class TestAmphipod:
    def test_is_solved(self):
        solved_state = (
            None, None, None, None, None, None, None,  # Hallway
            (Amphipod.AMBER, Amphipod.AMBER),          # Amber room
            (Amphipod.BRONZE, Amphipod.BRONZE),        # Bronze room
            (Amphipod.COPPER, Amphipod.COPPER),        # Copper room
            (Amphipod.DESERT, Amphipod.DESERT)         # Desert room
        )
        assert is_solved(solved_state)

    def test_example(self):
        state = (
            None, None, None, None, None, None, None,  # Hallway
            (Amphipod.BRONZE, Amphipod.AMBER),         # Amber room
            (Amphipod.COPPER, Amphipod.DESERT),        # Bronze room
            (Amphipod.BRONZE, Amphipod.COPPER),        # Copper room
            (Amphipod.DESERT, Amphipod.AMBER)          # Desert room
        )

        assert find_cheapest_path_cost(state) == 12521

    def test_part_two_example(self):
        state = (
            None, None, None, None, None, None, None,  # Hallway
            (Amphipod.BRONZE, Amphipod.AMBER),         # Amber room
            (Amphipod.COPPER, Amphipod.DESERT),        # Bronze room
            (Amphipod.BRONZE, Amphipod.COPPER),        # Copper room
            (Amphipod.DESERT, Amphipod.AMBER)          # Desert room
        )
        state = create_part_two_state(state)
        assert find_cheapest_path_cost(state) == 44169
