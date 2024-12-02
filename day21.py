from deterministic_die import Game, DeterministicDie
from dirac_dice import GameState, count_wins, Player, DiracDie

if __name__ == "__main__":
    with open("input/day21.txt") as input_text:
        lines = input_text.readlines()

    starting_positions = []
    for line in lines:
        starting_positions.append(int(line.split(":")[1]))

    game = Game(starting_positions, DeterministicDie())
    print(game.run())

    players = tuple([Player(position) for position in starting_positions])
    
    game_state = GameState(players)
    print(max(count_wins(game_state, DiracDie())))
