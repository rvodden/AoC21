from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, auto
from typing import Self


class Amphipod(Enum):
    AMBER = 1
    BRONZE = 10
    COPPER = 100
    DESERT = 1000


class Space:
    _neighbours: list[Self]
    _occupant: None | Amphipod
    _successfull_occupant: None | Amphipod
    _occupiable: bool
    _room: bool

    def __init__(self, successfull_occupant: Amphipod | None, occupiable: bool = True):
        self._neighbours = []
        self._occupant = None
        self._occupiable = occupiable
        self._successfull_occupant = successfull_occupant
        self._room = successfull_occupant is not None

    def add_neighbour(self, space: Self):
        self._neighbours.append(space)
        space._neighbours.append(self)

    def vacate(self):
        self._occupant = None

    def occupy(self, amphipod: Amphipod):
        self._occupant = amphipod

    @property
    def occupant(self) -> Amphipod | None:
        return self._occupant

    @property
    def neighbours(self) -> list[Self]:
        return self._neighbours

    @property
    def occupyable(self) -> bool:
        return self._occupiable

    @property
    def is_room(self) -> bool:
        return self._room

    @property
    def successful_occupant(self) -> Amphipod:
        return self._successfull_occupant

    def __str__(self) -> str:
        return f"Occupant: {self.occupant}"


@dataclass
class Move:
    start: Space
    finish: Space
    steps: int


class Burrow:
    _spaces: list[Space]

    def __init__(self, occupants: list[Space]):
        self._spaces = []

        def make_room(amphipod: Amphipod) -> list[Space]:
            room = [Space(amphipod) for _ in range(2)]
            room[0].add_neighbour(room[1])
            return room

        rooms = [make_room(a) for a in Amphipod]
        # Amphipods will never stop on the space immediately outside any room.
        unnocupiable = [2, 4, 6, 8]
        hallways = [Space(None, x not in unnocupiable) for x in range(11)]

        for hallway1, hallway2 in zip(hallways, hallways[1:]):
            hallway1.add_neighbour(hallway2)

        rooms[0][1].add_neighbour(hallways[2])
        rooms[1][1].add_neighbour(hallways[4])
        rooms[2][1].add_neighbour(hallways[6])
        rooms[3][1].add_neighbour(hallways[8])

        occupant_iter = iter(occupants)
        for room in rooms:
            room[0].occupy(next(occupant_iter))
            room[1].occupy(next(occupant_iter))
            self._spaces.extend(room)
        self._spaces.extend(hallways)

    def _is_valid_move(self, starting_position: Space, next_position: Space):
        # we can only go to a hallway if we're in a room
        valid_path = next_position.is_room or starting_position.is_room

        # if we're going to a room, it must be our destination
        valid_destination = not next_position.is_room or (
            starting_position.occupant == next_position.successful_occupant
        )
        return next_position.occupyable and valid_path and valid_destination

    def _get_moves_starting_from(
        self,
        starting_space: Space,
        current_position: Space,
        visited: None | list[Space] = None,
    ) -> list[Move]:
        moves = []
        if visited is None:
            visited = [starting_space]
        else:
            visited.append(current_position)

        for next_position in current_position.neighbours:
            # if something is in this space, we cannot move here
            if next_position in visited or next_position.occupant is not None:
                continue

            if (
                next_position.occupyable
                and starting_space.is_room != next_position.is_room
            ):
                moves.append(Move(starting_space, next_position, len(visited)))
            new_moves = self._get_moves_starting_from(
                starting_space, next_position, visited
            )
            moves.extend(new_moves)

        return moves

    def get_moves(self) -> list[Move]:

        moves = []
        for space in self._spaces:
            if space.occupant is not None:
                moves.extend(self._get_moves_starting_from(space, space))
        return moves
    
    def effect_move(self, move: Move) -> Self:
        retval = deepcopy(self)
        
