
import random
from protein.representation.structure import ProteinStructure
from protein.representation.constraints import is_valid_structure


# Drejtimet e mundshme në hapësirën 3D
DIRECTIONS = [
    (1, 0, 0),   # Right
    (-1, 0, 0),  # Left
    (0, 1, 0),   # Up
    (0, -1, 0),  # Down
    (0, 0, 1),   # Forward
    (0, 0, -1)   # Backward
]


def get_neighbors(coordinate):
    x, y, z = coordinate

    neighbors = []

    for dx, dy, dz in DIRECTIONS:
        neighbors.append((x + dx, y + dy, z + dz))

    return neighbors


def end_move(structure):
    coordinates = structure.coordinates[:]

    endpoint = random.choice([0, len(coordinates) - 1])

    occupied = set(coordinates)

    current_position = coordinates[endpoint]

    possible_positions = get_neighbors(current_position)

    possible_positions = [
        position for position in possible_positions
        if position not in occupied
    ]

    if not possible_positions:
        return None

    new_position = random.choice(possible_positions)

    coordinates[endpoint] = new_position

    new_structure = ProteinStructure(
        structure.hp_sequence,
        coordinates
    )

    if is_valid_structure(new_structure):
        return new_structure

    return None


def pivot_move(structure):
    coordinates = structure.coordinates[:]

    if len(coordinates) < 3:
        return None

    pivot_index = random.randint(0, len(coordinates) - 3)

    pivot_x, pivot_y, pivot_z = coordinates[pivot_index]

    rotation = random.choice(["xy", "xz", "yz"])

    angle = random.choice([90, 180, 270])

    new_coordinates = coordinates[:]

    for i in range(pivot_index + 1, len(coordinates)):
        x, y, z = coordinates[i]

        dx = x - pivot_x
        dy = y - pivot_y
        dz = z - pivot_z

        if rotation == "xy":
            if angle == 90:
                dx, dy = -dy, dx
            elif angle == 180:
                dx, dy = -dx, -dy
            else:
                dx, dy = dy, -dx

        elif rotation == "xz":
            if angle == 90:
                dx, dz = -dz, dx
            elif angle == 180:
                dx, dz = -dx, -dz
            else:
                dx, dz = dz, -dx

        else:
            if angle == 90:
                dy, dz = -dz, dy
            elif angle == 180:
                dy, dz = -dy, -dz
            else:
                dy, dz = dz, -dy

        new_coordinates[i] = (
            pivot_x + dx,
            pivot_y + dy,
            pivot_z + dz
        )

    new_structure = ProteinStructure(
        structure.hp_sequence,
        new_coordinates
    )

    if is_valid_structure(new_structure):
        return new_structure

    return None


def random_move(structure):
    move_functions = [end_move, pivot_move]

    for _ in range(10):
        move = random.choice(move_functions)

        new_structure = move(structure)

        if new_structure is not None:
            return new_structure

    return None
