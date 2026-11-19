import random
from statistics import mean

from protein.representation.structure import ProteinStructure
from protein.representation.constraints import is_valid_structure

from algorithms.simulated_annealing import simulated_annealing
from algorithms.genetic_algorithm import genetic_algorithm

from evaluation.metrics import measure_performance


def run_benchmark(lengths=(10, 20, 30, 40), runs=5):

    results = []

    # Përdorim të njëjtën sasi vlerësimesh për të dy algoritmet
    population_size = 30
    generations = 100
    sa_iterations = population_size * generations

    for length in lengths:

        hp_sequence = ("HHPPHPPH" * ((length // 8) + 1))[:length]

        sa_times = []
        sa_memories = []
        sa_energies = []
        sa_validity = []

        ga_times = []
        ga_memories = []
        ga_energies = []
        ga_validity = []

        for run in range(runs):

            protein = ProteinStructure(hp_sequence)

            # Simulated Annealing
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

            # Genetic Algorithm
            random.seed(run)

            ga_result, ga_metrics = measure_performance(
                genetic_algorithm,
                protein,
                population_size=population_size,
                generations=generations,
                mutation_rate=0.05,
                crossover_rate=0.8
            )

            ga_structure, ga_energy, ga_history = ga_result

            ga_times.append(ga_metrics["execution_time"])
            ga_memories.append(ga_metrics["peak_memory_mb"])
            ga_energies.append(ga_energy)
            ga_validity.append(is_valid_structure(ga_structure))

        results.append({
            "length": length,

            "SA": {
                "average_time": mean(sa_times),
                "average_memory": mean(sa_memories),
                "best_energy": min(sa_energies),
                "average_energy": mean(sa_energies),
                "all_valid": all(sa_validity)
            },

            "GA": {
                "average_time": mean(ga_times),
                "average_memory": mean(ga_memories),
                "best_energy": min(ga_energies),
                "average_energy": mean(ga_energies),
                "all_valid": all(ga_validity)
            }
        })

    return results


if __name__ == "__main__":

    benchmark_results = run_benchmark()

    print("\n========== ALGORITHM COMPARISON ==========")

    for result in benchmark_results:

        print(f"\nProtein Length: {result['length']}")

        for algorithm in ("SA", "GA"):

            data = result[algorithm]

            print(f"\n{algorithm} Results:")
            print("Average Time:", round(data["average_time"], 6), "seconds")
            print("Average Memory:", round(data["average_memory"], 6), "MB")
            print("Best Energy:", data["best_energy"])
            print("Average Energy:", round(data["average_energy"], 2))
            print("All Structures Valid:", data["all_valid"])