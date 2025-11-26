from amphipod import find_cheapest_path_cost, parse_state, create_part_two_state

if __name__ == "__main__":
    with open("input/day23.txt") as input_text:
        state = parse_state(input_text.read())

    print(find_cheapest_path_cost(state))

    create_part_two_state(state)

    print(find_cheapest_path_cost(state))
    