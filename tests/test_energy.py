
import unittest

from protein.representation.structure import ProteinStructure
from evaluation.energy import calculate_energy


class TestEnergy(unittest.TestCase):

    def test_straight_structure_has_zero_energy(self):
        structure = ProteinStructure("HHHH")

        energy = calculate_energy(structure)

        self.assertEqual(energy, 0)

    def test_non_consecutive_hydrophobic_contact(self):
        coordinates = [
            (0, 0, 0),
            (1, 0, 0),
            (1, 1, 0),
            (0, 1, 0)
        ]

        structure = ProteinStructure(
            "HPPH",
            coordinates
        )

        energy = calculate_energy(structure)

        self.assertEqual(energy, -1)

    def test_polar_residues_do_not_create_contacts(self):
        coordinates = [
            (0, 0, 0),
            (1, 0, 0),
            (1, 1, 0),
            (0, 1, 0)
        ]

        structure = ProteinStructure(
            "HPPP",
            coordinates
        )

        energy = calculate_energy(structure)

        self.assertEqual(energy, 0)


if __name__ == "__main__":
    unittest.main()
