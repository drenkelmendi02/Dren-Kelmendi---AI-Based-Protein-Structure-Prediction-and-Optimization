
import random
from statistics import mean

from protein.representation.structure import ProteinStructure
from protein.representation.constraints import is_valid_structure
from algorithms.simulated_annealing import simulated_annealing
from evaluation.metrics import measure_performance


def run_benchmark(lengths=(10, 20, 30, 40), runs=5, iterations=1000):

    results = []

    for length in lengths:

        hp_sequence = ("HHPPHPPH" * ((length // 8) + 1))[:length]

        execution_times = []
        memory_usages = []
        energies = []
        validity_results = []

        for run in range(runs):

            random.seed(run)

            protein = ProteinStructure(hp_sequence)

            result, metrics = measure_performance(
                simulated_annealing,
                protein,
                initial_temperature=10.0,
                cooling_rate=0.995,
                iterations=iterations
            )

            best_structure, best_energy, energy_history = result

            execution_times.append(metrics["execution_time"])
            memory_usages.append(metrics["peak_memory_mb"])
            energies.append(best_energy)
            validity_results.append(
                is_valid_structure(best_structure)
            )

        results.append({
            "length": length,
            "average_time": mean(execution_times),
            "average_memory": mean(memory_usages),
            "best_energy": min(energies),
            "average_energy": mean(energies),
            "all_valid": all(validity_results)
        })

    return results
