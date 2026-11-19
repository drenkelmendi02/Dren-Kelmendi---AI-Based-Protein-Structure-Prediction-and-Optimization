
import random
from statistics import mean

from protein.representation.structure import ProteinStructure
from protein.representation.constraints import is_valid_structure

from algorithms.simulated_annealing import simulated_annealing
from evaluation.metrics import measure_performance


def run_benchmark(lengths=(10, 20, 30, 40), runs=5):

    results = []

    sa_iterations = 3000

    for length in lengths:

        hp_sequence = ("HHPPHPPH" * ((length // 8) + 1))[:length]

        sa_times = []
        sa_memories = []
        sa_energies = []
        sa_validity = []

        for run in range(runs):

            protein = ProteinStructure(hp_sequence)

            random.seed(run)

            sa_result, sa_metrics = measure_performance(
                simulated_annealing,
                protein,
                initial_temperature=10.0,
                cooling_rate=0.995,
                iterations=sa_iterations
            )

            sa_structure, sa_energy, sa_history = sa_result

            sa_times.append(sa_metrics["execution_time"])
            sa_memories.append(sa_metrics["peak_memory_mb"])
            sa_energies.append(sa_energy)
            sa_validity.append(is_valid_structure(sa_structure))

        results.append({
            "length": length,
            "SA": {
                "average_time": mean(sa_times),
                "average_memory": mean(sa_memories),
                "best_energy": min(sa_energies),
                "average_energy": mean(sa_energies),
                "all_valid": all(sa_validity)
            }
        })

    return results


if __name__ == "__main__":

    benchmark_results = run_benchmark()

    print("\n========== SIMULATED ANNEALING BENCHMARK ==========")

    for result in benchmark_results:

        data = result["SA"]

        print(f"\nProtein Length: {result['length']}")
        print("Average Time:", round(data["average_time"], 6), "seconds")
        print("Average Memory:", round(data["average_memory"], 6), "MB")
        print("Best Energy:", data["best_energy"])
        print("Average Energy:", round(data["average_energy"], 2))
        print("All Structures Valid:", data["all_valid"])
