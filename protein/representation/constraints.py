
def _get_coordinates(structure):
    if hasattr(structure, "coordinates"):
        return structure.coordinates

    return structure


def has_overlaps(structure):
    coordinates = _get_coordinates(structure)

    return len(coordinates) != len(set(coordinates))


def has_valid_connections(structure):
    coordinates = _get_coordinates(structure)

    for i in range(len(coordinates) - 1):
        distance = sum(
            abs(coordinates[i][j] - coordinates[i + 1][j])
            for j in range(3)
        )

        if distance != 1:
            return False

    return True


def is_valid_structure(structure):
    return (
        not has_overlaps(structure)
        and has_valid_connections(structure)
    )
