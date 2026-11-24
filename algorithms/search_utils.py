
def get_structure_signature(structure):
    """
    Creates a unique signature for a protein structure.

    Structures with identical coordinates have
    identical signatures.
    """

    return tuple(structure.coordinates)


def is_duplicate_structure(structure, visited_states):
    """
    Checks whether a structure has already been explored.
    """

    signature = get_structure_signature(structure)

    return signature in visited_states


def register_structure(structure, visited_states):
    """
    Registers a structure if it has not been explored before.

    Returns True if the structure is new.
    Returns False if it is a duplicate.
    """

    signature = get_structure_signature(structure)

    if signature in visited_states:
        return False

    visited_states.add(signature)

    return True
