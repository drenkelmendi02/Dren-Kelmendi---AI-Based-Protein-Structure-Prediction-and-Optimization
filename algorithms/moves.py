

import random

from protein.representation.structure import ProteinStructure


def end_move(structure):

    coordinates = structure.coordinates.copy()
    length = len(coordinates)

    if length < 2:
        return None

    # Select the first or last amino acid
    if random.choice([True, False]):
        index = 0
        anchor_index = 1
    else:
        index = length - 1
        anchor_index = length - 2

    anchor_x, anchor_y = coordinates[anchor_index]

    # Find occupied positions
    occupied = set(coordinates)

    # Possible neighboring positions
    possible_positions = [
        (anchor_x + 1, anchor_y),
        (anchor_x - 1, anchor_y),
        (anchor_x, anchor_y + 1),
        (anchor_x, anchor_y - 1)
    ]

    # Remove occupied positions
    valid_positions = [
        position
        for position in possible_positions
        if position not in occupied
    ]

    if not valid_positions:
        return None

    # Select a random valid position
    new_position = random.choice(valid_positions)

    coordinates[index] = new_position

    return ProteinStructure(
        structure.hp_sequence,
        coordinates
    )
