from dataclasses import dataclass
from typing import List, Tuple

VOWELS = ['A', 'E', 'I', 'O', 'U', 'Y']
VALID_KNIGHT_COORDINATE_MOVEMENTS = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]


@dataclass
class GridItem:
    value: str
    x: int
    y: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return self.value

    @property
    def is_vowel(self):
        return self.value in VOWELS


class Grid:

    def __init__(self):
        self.items = [
            [None, GridItem('1', 1, 0), GridItem('2', 2, 0), GridItem('3', 3, 0), None],
            [GridItem('K', 0, 1), GridItem('L', 1, 1), GridItem('M', 2, 1), GridItem('N', 3, 1), GridItem('O', 4, 1)],
            [GridItem('F', 0, 2), GridItem('G', 1, 2), GridItem('H', 2, 2), GridItem('I', 3, 2), GridItem('J', 4, 2)],
            [GridItem('A', 0, 3), GridItem('B', 1, 3), GridItem('C', 2, 3), GridItem('D', 3, 3), GridItem('E', 4, 3)]
        ]

    def get_item(self, x: int, y: int):
        if x < 0 or y < 0:
            return
        try:
            return self.items[y][x]
        except IndexError:
            return

    def get_by_value(self, value: str):  # only used for initial user input
        match = None
        for x_col in self.items:
            for item in x_col:
                if item and item.value.lower() == value.lower():
                    match = item
        if not match:
            raise ValueError('Not on grid!')
        return match


def get_available_locations_after_knight_move(grid: Grid, start_location: GridItem) -> List[GridItem]:
    valid_coordinates_after_move = []
    for x, y in VALID_KNIGHT_COORDINATE_MOVEMENTS:
        grid_item = grid.get_item(start_location.x + x, start_location.y + y)  # could be None if not on grid
        if grid_item:
            valid_coordinates_after_move.append(grid_item)
    return valid_coordinates_after_move


def extend_sequences(grid: Grid, sequences: List[Tuple[GridItem]]) -> List[Tuple[GridItem, GridItem]]:
    """
    Returns a list of sequences generated after each sequence in the given list is extended by one move.

    Example: the sequences [(A, L), (A, H)] will be extended to
    [(A, L, 3), (A, L, I), (A, L, C), (A, H, E), (A, H, O), (A, H, 1), (A, H, 3), (A, H, K)]
    """
    new_sequences = []

    for seq in sequences:
        last_move = seq[-1]
        next_moves = get_available_locations_after_knight_move(grid=grid, start_location=last_move)
        valid_moves = [m for m in next_moves if m not in seq]
        for move in valid_moves:
            new_seq = seq + (move,)
            new_sequences.append(new_seq)
    return new_sequences


if __name__ == '__main__':
    grid_ = Grid()
    initial_keypress = grid_.get_by_value(input('Enter the initial keypress pls: '))

    completed_sequences = []
    sequences_to_extend = [(initial_keypress,)]
    while True:
        extended_sequences = extend_sequences(grid_, sequences_to_extend)
        sequences_to_extend_again = []
        for seq_ in extended_sequences:
            if len([v for v in seq_ if v.is_vowel]) > 2:
                continue
            if len(seq_) == 10:
                completed_sequences.append(seq_)
            else:
                sequences_to_extend_again.append(seq_)
        if not sequences_to_extend_again:
            break
        sequences_to_extend = sequences_to_extend_again
    for s in completed_sequences:
        print(s)
    print(f'TOTAL: {len(completed_sequences)}')
