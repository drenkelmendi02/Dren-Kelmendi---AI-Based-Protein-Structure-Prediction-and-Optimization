
def has_overlaps(coordinates):

    return len(coordinates) != len(set(coordinates))


def has_valid_connections(coordinates):
    for i in range(len(coordinates) - 1):

        x1, y1 = coordinates[i]
        x2, y2 = coordinates[i + 1]

        distance = abs(x2 - x1) + abs(y2 - y1)

        if distance != 1:
            return False

    return True


def is_valid_structure(structure):
    

    coordinates = structure.coordinates

    if has_overlaps(coordinates):
        return False

    if not has_valid_connections(coordinates):
        return False

    return True
