
import unittest

from protein.representation.sequence import (
    validate_sequence,
    get_sequence_length,
    get_amino_acid_count
)
from protein.representation.hp_model import convert_to_hp
from protein.representation.structure import ProteinStructure
from protein.representation.constraints import (
    has_overlaps,
    has_valid_connections,
    is_valid_structure
)


class TestProteinRepresentation(unittest.TestCase):

    def test_valid_sequence(self):
        sequence = validate_sequence("ACDEFG")
        self.assertEqual(sequence, "ACDEFG")

    def test_sequence_is_converted_to_uppercase(self):
        sequence = validate_sequence("acdefg")
        self.assertEqual(sequence, "ACDEFG")

    def test_empty_sequence_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_sequence("")

    def test_invalid_amino_acid_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_sequence("ABCX")

    def test_sequence_length(self):
        self.assertEqual(get_sequence_length("ACDEFG"), 6)

    def test_amino_acid_count(self):
        counts = get_amino_acid_count("AACC")
        self.assertEqual(counts["A"], 2)
        self.assertEqual(counts["C"], 2)

    def test_hp_conversion(self):
        self.assertEqual(convert_to_hp("ACDEFG"), "HHPPHP")
    def test_initial_structure(self):
        structure = ProteinStructure("HHPH")

        self.assertEqual(
            structure.coordinates,
            [(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0)]
        )

    def test_structure_without_overlaps(self):
        structure = ProteinStructure("HHPH")
        self.assertFalse(has_overlaps(structure))

    def test_structure_with_overlaps(self):
        structure = ProteinStructure(
            "HHPH",
            [(0, 0, 0), (1, 0, 0), (1, 0, 0), (2, 0, 0)]
        )

        self.assertTrue(has_overlaps(structure))

    def test_valid_connections(self):
        structure = ProteinStructure("HHPH")
        self.assertTrue(has_valid_connections(structure))

    def test_invalid_connections(self):
        structure = ProteinStructure(
            "HHPH",
            [(0, 0, 0), (1, 0, 0), (3, 0, 0), (4, 0, 0)]
        )

        self.assertFalse(has_valid_connections(structure))

    def test_valid_structure(self):
        structure = ProteinStructure("HHPH")
        self.assertTrue(is_valid_structure(structure))


if __name__ == "__main__":
    unittest.main()
