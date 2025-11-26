from enum import Enum, auto
from heapq import heapify, heappop, heappush


class Amphipod(Enum):
    AMBER = 1
    BRONZE = 10
    COPPER = 100
    DESERT = 1000

# Room indices in the flat state tuple
ROOM_AMBER = 7
ROOM_BRONZE = 8
ROOM_COPPER = 9
ROOM_DESERT = 10

ROOM_MAP = {
    Amphipod.AMBER: ROOM_AMBER,
    Amphipod.BRONZE: ROOM_BRONZE,
    Amphipod.COPPER: ROOM_COPPER,
    Amphipod.DESERT: ROOM_DESERT
}

"""
Model state as a flat tuple:
(h0, h1, h2, h3, h4, h5, h6, room_A, room_B, room_C, room_D)

where h0-h6 are hallway positions (can be None or Amphipod)
and room_A/B/C/D are tuples of amphipods in each room

Example initial state:
(None, None, None, None, None, None, None,
 (Amphipod.BRONZE, Amphipod.AMBER),    # Amber room
 (Amphipod.COPPER, Amphipod.DESERT),   # Bronze room
 (Amphipod.BRONZE, Amphipod.COPPER),   # Copper room
 (Amphipod.DESERT, Amphipod.AMBER))    # Desert room
"""

"""
Hallway positions are numbered ignoring the positions outside of the rooms which 
cannot be occupied. Like this:

#############
#01.2.3.4.56#
###.#.#.#.###
  #.#.#.#.#
  #########

The rooms are identifed by their eventual occupants (A = Amber, B = Bronze, C = Copper, D = Desert):

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########

PATHS captures the hallway positions which need to be transitioned
in order to get from a hallway position to a room type, including 
the starting position. For example, to get from hallway position 0 to an ammber room, 
positions 0 and 1 must be moved through.
"""

PATHS = {
    0: {Amphipod.AMBER: [0, 1],          Amphipod.BRONZE: [0, 1, 2],    Amphipod.COPPER: [0, 1, 2, 3], Amphipod.DESERT: [0, 1, 2, 3, 4]},
    1: {Amphipod.AMBER: [1],             Amphipod.BRONZE: [1, 2],       Amphipod.COPPER: [1, 2, 3],    Amphipod.DESERT: [1, 2, 3, 4]},
    2: {Amphipod.AMBER: [2],             Amphipod.BRONZE: [2],          Amphipod.COPPER: [2, 3],       Amphipod.DESERT: [2, 3, 4]},
    3: {Amphipod.AMBER: [3, 2],          Amphipod.BRONZE: [3],          Amphipod.COPPER: [3],          Amphipod.DESERT: [3, 4]},
    4: {Amphipod.AMBER: [4, 3, 2],       Amphipod.BRONZE: [4, 3],       Amphipod.COPPER: [4],          Amphipod.DESERT: [4]},
    5: {Amphipod.AMBER: [5, 4, 3, 2],    Amphipod.BRONZE: [5, 4, 3],    Amphipod.COPPER: [5, 4],       Amphipod.DESERT: [5]},
    6: {Amphipod.AMBER: [6, 5, 4, 3, 2], Amphipod.BRONZE: [6, 5, 4, 3], Amphipod.COPPER: [6, 5, 4],    Amphipod.DESERT: [6, 5]}
}

def state_hash(state: tuple) -> int:
    """State is already a tuple, so it's directly hashable."""
    return hash(state)

def move_steps(hallway_position: int, room_type: Amphipod, room_position: int) -> int:
    """Returns the number of steps required to execute a move from a hallway position to a room position

    this is given by the double the length of the entry in PATHS, (with one subtracted if the starting position is 0 or 6)
    plus the room position (zero is nearer the hallway, 1 is further inside).

    """
    return 2 * len(PATHS[hallway_position][room_type]) + room_position - (1 if hallway_position in [0, 6] else 0)

def is_solved(state: tuple) -> bool:
    """Returns true if the state is the end state."""
    return (all(state[ROOM_AMBER][i] == Amphipod.AMBER for i in range(len(state[ROOM_AMBER]))) and
            all(state[ROOM_BRONZE][i] == Amphipod.BRONZE for i in range(len(state[ROOM_BRONZE]))) and
            all(state[ROOM_COPPER][i] == Amphipod.COPPER for i in range(len(state[ROOM_COPPER]))) and
            all(state[ROOM_DESERT][i] == Amphipod.DESERT for i in range(len(state[ROOM_DESERT]))))

def is_room_open(state: tuple, room: Amphipod) -> bool:
    """Returns true if a room is available for an Amphipod to traverse to it."""
    room_idx = ROOM_MAP[room]
    return all(occupant in [None, room] for occupant in state[room_idx])

def is_path_to_room_clear(state: tuple, starting_hallway_position: int, ending_room_type: Amphipod) -> bool:
    """Returns true if there are no Amphipods in any of the hallway positions necessary to be traversed to traverse to a room."""
    for hallway_position in PATHS[starting_hallway_position][ending_room_type]:
        if hallway_position != starting_hallway_position and state[hallway_position] is not None:
            return False
    return True

def next_available_room_position(state: tuple, room: Amphipod) -> int:
    room_idx = ROOM_MAP[room]
    room_tuple = state[room_idx]
    return len(room_tuple) - 1 - room_tuple[::-1].index(None)

def make_move(state: tuple, from_idx: int, from_position: int, to_idx: int, to_position: int) -> tuple:
    """Return a new state tuple with the move applied.

    from_idx/to_idx: 0-6 for hallway positions, 7-10 for rooms
    from_position/to_position: position within room (0 for hallway moves)

    No validation is done - the move is made even if it's illegal.
    """
    state_list = list(state)

    # Get the amphipod being moved
    if from_idx < 7:  # From hallway
        amphipod = state[from_idx]
        state_list[from_idx] = None
    else:  # From room
        room_tuple = state[from_idx]
        amphipod = room_tuple[from_position]
        room_list = list(room_tuple)
        room_list[from_position] = None
        state_list[from_idx] = tuple(room_list)

    # Place amphipod in destination
    if to_idx < 7:  # To hallway
        state_list[to_idx] = amphipod
    else:  # To room
        room_tuple = state_list[to_idx]
        room_list = list(room_tuple)
        room_list[to_position] = amphipod
        state_list[to_idx] = tuple(room_list)

    return tuple(state_list)

def next_possible_states(state: tuple, current_cost: int) -> list[tuple[tuple, int]]:

    # chunter through all the amphipods in the hallway and see
    # if they can get back to their rooms. If this is the
    # case then this is definitely the best next move as
    # it will have to be done at some point, and doing it before
    # anythig else opens up more possibilities for the subsequent move.
    for hallway_position in PATHS:
        amphipod_type = state[hallway_position]
        if amphipod_type and is_room_open(state, amphipod_type) and is_path_to_room_clear(state, hallway_position, amphipod_type):
            room_position = next_available_room_position(state, amphipod_type)
            room_idx = ROOM_MAP[amphipod_type]
            cost = current_cost + (move_steps(hallway_position, amphipod_type, room_position) * amphipod_type.value)
            return [(make_move(state, hallway_position, 0, room_idx, room_position), cost)]

    # if we can't move anyone from the hallway into a room, we had better move Amphipods
    # from the room to the hallway
    next_states = []
    for room_type in Amphipod:
        if not is_room_open(state, room_type):
            # the room isn't open, so there must be an amphipod in
            # the room which is not of the room type. Grab it
            room_idx = ROOM_MAP[room_type]
            room_tuple = state[room_idx]
            amphipod_type = next(filter(bool, room_tuple))
            room_position = room_tuple.index(amphipod_type)
            for hallway_position in PATHS:
                # if the position in the hallway is clear, and the path is clear - this is an option
                if not state[hallway_position] and is_path_to_room_clear(state, hallway_position, room_type):
                    new_state = make_move(state, room_idx, room_position, hallway_position, 0)
                    cost = current_cost + (move_steps(hallway_position, room_type, room_position) * amphipod_type.value)
                    next_states.append((new_state, cost))

    return next_states

def heuristic(state: tuple) -> int:
    cost = 0
    # Add cost for amphipods in hallway
    for pos in range(7):
        amphipod = state[pos]
        if amphipod:
            min_steps = len(PATHS[pos][amphipod])
            cost += min_steps * amphipod.value

    # Add cost for amphipods in wrong rooms
    for room_type in Amphipod:
        room_idx = ROOM_MAP[room_type]
        room_tuple = state[room_idx]
        for pos, amphipod in enumerate(room_tuple):
            if amphipod and amphipod != room_type:
                # Estimate cost to exit and enter correct room
                cost += (pos + 2) * amphipod.value  # rough estimate
    return cost

class StateCost:
    state: tuple
    g_cost: int  # actual cost
    f_cost: int  # g_cost + heuristic (for priority)

    def __init__(self, state_cost: tuple[tuple, int]):
        self.state, self.g_cost = state_cost
        self.f_cost = self.g_cost + heuristic(self.state)

    def __lt__(self, other: 'StateCost'):
        return self.f_cost < other.f_cost

    def __repr__(self):
        return f"""
Cost: {self.g_cost} (f={self.f_cost})
Hallway: {self.state[:7]}
Amber: {self.state[ROOM_AMBER]}
Bronze: {self.state[ROOM_BRONZE]}
Copper: {self.state[ROOM_COPPER]}
Desert: {self.state[ROOM_DESERT]}
"""


def find_cheapest_path_cost(state: tuple) -> int:
    heap = []
    visited = {}
    heappush(heap, StateCost((state, 0)))

    while heap:
        state_cost = heappop(heap)
        current_state = state_cost.state
        cost = state_cost.g_cost

        if is_solved(current_state):
            return cost

        current_state_hash = state_hash(current_state)
        if current_state_hash in visited and visited[current_state_hash] <= cost:
            continue
        visited[current_state_hash] = cost

        for next_possible_state, next_cost in next_possible_states(current_state, cost):
            next_hash = state_hash(next_possible_state)
            if next_hash not in visited or next_cost < visited[next_hash]:
                heappush(heap, StateCost((next_possible_state, next_cost)))

    raise(RuntimeError("Shouldn't ever get here"))


def parse_state(text: str) -> tuple:
    """Parse the text representation of the burrow into a state tuple.

    Expected format:
    #############
    #...........#
    ###A#B#C#D###
      #A#B#C#D#
      #########
    """
    lines = text.strip().split('\n')

    # Map characters to Amphipod types
    char_to_amphipod = {
        'A': Amphipod.AMBER,
        'B': Amphipod.BRONZE,
        'C': Amphipod.COPPER,
        'D': Amphipod.DESERT,
        '.': None
    }

    # Extract room positions from lines 2 and 3 (0-indexed)
    # Line 2: ###A#B#C#D###  -> positions 3,5,7,9
    # Line 3:   #A#B#C#D#    -> positions 3,5,7,9
    room_line_top = lines[2]
    room_line_bottom = lines[3]

    # Parse the four rooms
    amber_top = char_to_amphipod.get(room_line_top[3])
    amber_bottom = char_to_amphipod.get(room_line_bottom[3])

    bronze_top = char_to_amphipod.get(room_line_top[5])
    bronze_bottom = char_to_amphipod.get(room_line_bottom[5])

    copper_top = char_to_amphipod.get(room_line_top[7])
    copper_bottom = char_to_amphipod.get(room_line_bottom[7])

    desert_top = char_to_amphipod.get(room_line_top[9])
    desert_bottom = char_to_amphipod.get(room_line_bottom[9])

    return (
        None, None, None, None, None, None, None,  # Hallway (7 positions)
        (amber_top, amber_bottom),                   # Amber room
        (bronze_top, bronze_bottom),                 # Bronze room
        (copper_top, copper_bottom),                 # Copper room
        (desert_top, desert_bottom)                  # Desert room
    )

def create_part_two_state(state: tuple) -> tuple:
    """Convert part 1 state to part 2 by inserting additional amphipods."""
    # Part 2 inserts:
    #  D D in Amber room
    #  C B in Bronze room
    #  B A in Copper room
    #  A C in Desert room
    state_list = list(state)

    # Amber room: [top, D, D, bottom]
    amber = list(state[ROOM_AMBER])
    amber.insert(1, Amphipod.DESERT)
    amber.insert(1, Amphipod.DESERT)
    state_list[ROOM_AMBER] = tuple(amber)

    # Bronze room: [top, C, B, bottom]
    bronze = list(state[ROOM_BRONZE])
    bronze.insert(1, Amphipod.BRONZE)
    bronze.insert(1, Amphipod.COPPER)
    state_list[ROOM_BRONZE] = tuple(bronze)

    # Copper room: [top, B, A, bottom]
    copper = list(state[ROOM_COPPER])
    copper.insert(1, Amphipod.AMBER)
    copper.insert(1, Amphipod.BRONZE)
    state_list[ROOM_COPPER] = tuple(copper)

    # Desert room: [top, A, C, bottom]
    desert = list(state[ROOM_DESERT])
    desert.insert(1, Amphipod.COPPER)
    desert.insert(1, Amphipod.AMBER)
    state_list[ROOM_DESERT] = tuple(desert)

    return tuple(state_list)