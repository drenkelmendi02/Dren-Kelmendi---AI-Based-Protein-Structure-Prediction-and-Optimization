
import csv
import random
from pathlib import Path
from statistics import mean

from protein.representation.structure import ProteinStructure
from protein.representation.constraints import is_valid_structure

from algorithms.simulated_annealing import simulated_annealing
from algorithms.genetic_algorithm import genetic_algorithm

from evaluation.metrics import measure_performance


# ==========================================
# BENCHMARK CONFIGURATION
# ==========================================

PROTEIN_LENGTHS = (10, 15, 20, 25, 30)

NUMBER_OF_RUNS = 3

SA_ITERATIONS = 3000

GA_POPULATION_SIZE = 30
GA_GENERATIONS = 100
GA_MUTATION_RATE = 0.3
GA_CROSSOVER_RATE = 0.8


# ==========================================
# PROTEIN SEQUENCE GENERATION
# ==========================================

def generate_hp_sequence(length):
    """
    Gjeneron një sekuencë HP për testimin
    e proteinave me gjatësi të ndryshme.
    """

    pattern = "HHPPHPPH"

    return (pattern * ((length // len(pattern)) + 1))[:length]


# ==========================================
# BENCHMARK SIMULATED ANNEALING
# ==========================================

def benchmark_sa(hp_sequence, seed):
    """
    Ekzekuton Simulated Annealing dhe mat
    performancën e tij.
    """

    random.seed(seed)

    protein = ProteinStructure(hp_sequence)

    result, performance = measure_performance(
        simulated_annealing,
        protein,
        initial_temperature=10.0,
        cooling_rate=0.995,
        iterations=SA_ITERATIONS
    )

    best_structure, best_energy, energy_history = result

    return {
        "energy": best_energy,
        "execution_time": performance["execution_time"],
        "memory_mb": performance["peak_memory_mb"],
        "valid": is_valid_structure(best_structure),
        "iterations": len(energy_history)
    }


# ==========================================
# BENCHMARK GENETIC ALGORITHM
# ==========================================

def benchmark_ga(hp_sequence, seed):
    """
    Ekzekuton Genetic Algorithm dhe mat
    performancën dhe statistikat e tij.
    """

    random.seed(seed)

    protein = ProteinStructure(hp_sequence)

    result, performance = measure_performance(
        genetic_algorithm,
        protein,
        population_size=GA_POPULATION_SIZE,
        generations=GA_GENERATIONS,
        mutation_rate=GA_MUTATION_RATE,
        crossover_rate=GA_CROSSOVER_RATE,
        return_stats=True
    )

    (
        best_structure,
        best_energy,
        energy_history,
        statistics
    ) = result

    return {
        "energy": best_energy,
        "execution_time": performance["execution_time"],
        "memory_mb": performance["peak_memory_mb"],
        "valid": is_valid_structure(best_structure),
        "generations": len(energy_history) - 1,
        "candidate_configurations": statistics["candidate_configurations"],
        "valid_structures": statistics["valid_structures"],
        "invalid_structures": statistics["invalid_structures"],
        "duplicate_structures": statistics["duplicate_structures"],
        "unique_structures": statistics["unique_structures"],
        "energy_evaluations": statistics["energy_evaluations"],
        "elimination_percentage": statistics["elimination_percentage"]
    }


# ==========================================
# AGGREGATE RESULTS
# ==========================================

def summarize_results(algorithm, length, runs):
    """
    Përmbledh rezultatet e disa ekzekutimeve
    për një algoritëm dhe një gjatësi proteine.
    """

    summary = {
        "protein_length": length,
        "algorithm": algorithm,

        "average_energy": mean(
            run["energy"] for run in runs
        ),

        "best_energy": min(
            run["energy"] for run in runs
        ),

        "average_time": mean(
            run["execution_time"] for run in runs
        ),

        "average_memory_mb": mean(
            run["memory_mb"] for run in runs
        ),

        "validity_rate": (
            sum(run["valid"] for run in runs)
            / len(runs)
        ) * 100
    }

    # Statistikat shtesë për Genetic Algorithm.
    if algorithm == "GA":

        summary.update({
            "average_candidates": mean(
                run["candidate_configurations"] for run in runs
            ),

            "average_valid_structures": mean(
                run["valid_structures"] for run in runs
            ),

            "average_invalid_structures": mean(
                run["invalid_structures"] for run in runs
            ),

            "average_duplicate_structures": mean(
                run["duplicate_structures"] for run in runs
            ),

            "average_unique_structures": mean(
                run["unique_structures"] for run in runs
            ),

            "average_energy_evaluations": mean(
                run["energy_evaluations"] for run in runs
            ),

            "average_elimination_percentage": mean(
                run["elimination_percentage"] for run in runs
            )
        })

    return summary


# ==========================================
# RUN COMPLETE BENCHMARK
# ==========================================

def run_benchmark(
    lengths=PROTEIN_LENGTHS,
    number_of_runs=NUMBER_OF_RUNS
):

    all_results = []

    for length in lengths:

        print(f"\n{'=' * 55}")
        print(f"PROTEIN LENGTH: {length}")
        print(f"{'=' * 55}")

        hp_sequence = generate_hp_sequence(length)

        sa_runs = []
        ga_runs = []

        for run_index in range(number_of_runs):

            seed = length * 1000 + run_index

            print(
                f"\nRun {run_index + 1}/{number_of_runs}"
            )

            # Simulated Annealing
            sa_result = benchmark_sa(
                hp_sequence,
                seed
            )

            sa_runs.append(sa_result)

            # Genetic Algorithm
            ga_result = benchmark_ga(
                hp_sequence,
                seed
            )

            ga_runs.append(ga_result)

        # Përmbledhja e rezultateve.
        sa_summary = summarize_results(
            "SA",
            length,
            sa_runs
        )

        ga_summary = summarize_results(
            "GA",
            length,
            ga_runs
        )

        all_results.append(sa_summary)
        all_results.append(ga_summary)

        print("\nSIMULATED ANNEALING")
        print("Average Energy:", round(sa_summary["average_energy"], 2))
        print("Average Time:", round(sa_summary["average_time"], 4), "s")
        print("Average Memory:", round(sa_summary["average_memory_mb"], 4), "MB")

        print("\nGENETIC ALGORITHM")
        print("Average Energy:", round(ga_summary["average_energy"], 2))
        print("Average Time:", round(ga_summary["average_time"], 4), "s")
        print("Average Memory:", round(ga_summary["average_memory_mb"], 4), "MB")

    return all_results


# ==========================================
# SAVE RESULTS TO CSV
# ==========================================

def save_results_to_csv(results):
    """
    Ruajtja e rezultateve në CSV
    për analiza dhe grafikë të mëvonshëm.
    """

    output_path = (
        Path(__file__).resolve().parent
        / "benchmark_results.csv"
    )

    fieldnames = sorted({
        key
        for result in results
        for key in result.keys()
    })

    with open(
        output_path,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(results)

    print("\nBenchmark results saved to:")
    print(output_path)


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    results = run_benchmark()

    save_results_to_csv(results)

    print("\n========== BENCHMARK COMPLETED ==========")
