
import random
import unittest

from protein.representation.structure import ProteinStructure
from protein.representation.constraints import is_valid_structure
from evaluation.energy import calculate_energy
from algorithms.genetic_algorithm import genetic_algorithm


class TestGeneticAlgorithm(unittest.TestCase):

    def setUp(self):
        random.seed(42)
        self.hp_sequence = "HHPHHP"
        self.initial_structure = ProteinStructure(self.hp_sequence)

    def test_initial_structure_is_valid(self):
        self.assertTrue(
            is_valid_structure(self.initial_structure)
        )

    def test_genetic_algorithm_returns_valid_structure(self):
        best_structure, best_energy, history = genetic_algorithm(
            self.initial_structure,
            population_size=6,
            generations=5,
            mutation_rate=0.3,
            crossover_rate=0.8
        )

        self.assertTrue(is_valid_structure(best_structure))
        self.assertEqual(best_energy, calculate_energy(best_structure))

    def test_energy_history_is_non_increasing(self):
        _, _, history = genetic_algorithm(
            self.initial_structure,
            population_size=6,
            generations=5,
            mutation_rate=0.3,
            crossover_rate=0.8
        )

        self.assertEqual(len(history), 6)

        for i in range(1, len(history)):
            self.assertLessEqual(history[i], history[i - 1])

    def test_algorithm_returns_statistics(self):
        result = genetic_algorithm(
            self.initial_structure,
            population_size=6,
            generations=5,
            mutation_rate=0.3,
            crossover_rate=0.8,
            return_stats=True
        )

        self.assertEqual(len(result), 4)

        best_structure, best_energy, history, statistics = result

        self.assertTrue(is_valid_structure(best_structure))
        self.assertIsInstance(best_energy, int)
        self.assertEqual(len(history), 6)

        self.assertIn("candidate_configurations", statistics)
        self.assertIn("valid_structures", statistics)
        self.assertIn("invalid_structures", statistics)
        self.assertIn("duplicate_structures", statistics)
        self.assertIn("unique_structures", statistics)
        self.assertIn("energy_evaluations", statistics)
        self.assertIn("elimination_percentage", statistics)


if __name__ == "__main__":
    unittest.main()
