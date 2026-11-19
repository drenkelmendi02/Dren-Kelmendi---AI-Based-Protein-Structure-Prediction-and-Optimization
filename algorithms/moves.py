

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

def pivot_move(structure):
    """
    Rotate a part of the protein around a randomly
    selected pivot amino acid.
    """

    coordinates = structure.coordinates.copy()
    length = len(coordinates)

    if length < 3:
        return None

    # Select a pivot position
    pivot_index = random.randint(0, length - 2)

    pivot_x, pivot_y = coordinates[pivot_index]

    # Select a rotation angle
    angle = random.choice([90, 180, 270])

    # Rotate all amino acids after the pivot
    for i in range(pivot_index + 1, length):

        x, y = coordinates[i]

        dx = x - pivot_x
        dy = y - pivot_y

        if angle == 90:
            new_dx, new_dy = -dy, dx

        elif angle == 180:
            new_dx, new_dy = -dx, -dy

        else:
            new_dx, new_dy = dy, -dx

        coordinates[i] = (
            pivot_x + new_dx,
            pivot_y + new_dy
        )

    # Reject structures with overlapping positions
    if len(coordinates) != len(set(coordinates)):
        return None

    return ProteinStructure(
        structure.hp_sequence,
        coordinates
    )


def random_move(structure):
    """
    Generate a new structure using a random
    movement operation.
    """

    for _ in range(10):

        move = random.choice([end_move, pivot_move])

        new_structure = move(structure)

        if new_structure is not None:
            return new_structure

    return None
