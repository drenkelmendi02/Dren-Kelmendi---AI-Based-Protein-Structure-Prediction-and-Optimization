
import random
import unittest

from protein.representation.structure import ProteinStructure
from protein.representation.constraints import is_valid_structure
from evaluation.energy import calculate_energy
from algorithms.simulated_annealing import simulated_annealing


class TestSimulatedAnnealing(unittest.TestCase):

    def setUp(self):
        random.seed(42)
        self.initial_structure = ProteinStructure("HHPHHP")

    def test_returns_expected_results(self):
        result = simulated_annealing(
            self.initial_structure,
            initial_temperature=10.0,
            cooling_rate=0.995,
            iterations=50
        )

        best_structure, best_energy, history = result

        self.assertIsInstance(best_structure, ProteinStructure)
        self.assertIsInstance(best_energy, (int, float))
        self.assertIsInstance(history, list)

    def test_best_structure_is_valid(self):
        best_structure, _, _ = simulated_annealing(
            self.initial_structure,
            initial_temperature=10.0,
            cooling_rate=0.995,
            iterations=50
        )

        self.assertTrue(is_valid_structure(best_structure))

    def test_energy_is_calculated_correctly(self):
        best_structure, best_energy, _ = simulated_annealing(
            self.initial_structure,
            initial_temperature=10.0,
            cooling_rate=0.995,
            iterations=50
        )

        self.assertEqual(
            best_energy,
            calculate_energy(best_structure)
        )

    def test_history_contains_initial_and_final_values(self):
        _, _, history = simulated_annealing(
            self.initial_structure,
            initial_temperature=10.0,
            cooling_rate=0.995,
            iterations=50
        )

        self.assertEqual(len(history), 51)

    def test_zero_iterations(self):
        best_structure, best_energy, history = simulated_annealing(
            self.initial_structure,
            initial_temperature=10.0,
            cooling_rate=0.995,
            iterations=0
        )

        self.assertTrue(is_valid_structure(best_structure))
        self.assertEqual(best_energy, calculate_energy(best_structure))
        self.assertEqual(len(history), 1)


if __name__ == "__main__":
    unittest.main()
