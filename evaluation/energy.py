
def calculate_energy(structure, hydrophobic_contact_weight=1.0):
    """
    Calculates protein structure energy using the HP model.

    Each non-consecutive hydrophobic contact contributes
    a negative energy value.

    Args:
        structure: ProteinStructure object.
        hydrophobic_contact_weight: Strength of each
            hydrophobic contact. Default is 1.0.

    Returns:
        Total energy of the protein structure.
    """

    if hydrophobic_contact_weight < 0:
        raise ValueError(
            "Hydrophobic contact weight cannot be negative."
        )

    hp_sequence = structure.hp_sequence
    coordinates = structure.coordinates

    energy = 0

    for i in range(len(hp_sequence)):
        if hp_sequence[i] != 'H':
            continue

        for j in range(i + 2, len(hp_sequence)):
            if hp_sequence[j] != 'H':
                continue

            x1, y1, z1 = coordinates[i]
            x2, y2, z2 = coordinates[j]

            distance = (
                abs(x2 - x1) +
                abs(y2 - y1) +
                abs(z2 - z1)
            )

            if distance == 1:
                energy -= hydrophobic_contact_weight

    return energy
