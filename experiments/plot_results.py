
import csv
from pathlib import Path
from statistics import mean

import matplotlib.pyplot as plt


# ==========================================
# CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

CSV_FILE = BASE_DIR / "benchmark_results.csv"


# ==========================================
# LOAD RESULTS
# ==========================================

def load_results():
    results = []

    with open(
        CSV_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            results.append({
                "protein_length": int(row["protein_length"]),
                "sequence_type": row["sequence_type"],
                "algorithm": row["algorithm"],
                "average_energy": float(row["average_energy"]),
                "average_time": float(row["average_time"]),
                "average_memory_mb": float(row["average_memory_mb"]),
                "average_elimination_percentage": float(
                    row["average_elimination_percentage"]
                )
            })

    return results


# ==========================================
# AGGREGATE RESULTS
# ==========================================

def aggregate_results(results):
    """
    Llogarit mesataren e rezultateve për secilën
    gjatësi dhe algoritëm, duke përfshirë të gjitha
    llojet e sekuencave.
    """

    grouped = {}

    for result in results:

        key = (
            result["protein_length"],
            result["algorithm"]
        )

        grouped.setdefault(key, []).append(result)

    aggregated = []

    for (length, algorithm), group in grouped.items():

        aggregated.append({
            "protein_length": length,
            "algorithm": algorithm,

            "average_energy": mean(
                item["average_energy"] for item in group
            ),

            "average_time": mean(
                item["average_time"] for item in group
            ),

            "average_memory_mb": mean(
                item["average_memory_mb"] for item in group
            ),

            "average_elimination_percentage": mean(
                item["average_elimination_percentage"]
                for item in group
            )
        })

    return aggregated


# ==========================================
# CREATE PLOT
# ==========================================

def create_plot(
    results,
    metric,
    title,
    ylabel,
    filename
):

    algorithms = ["SA", "GA"]

    lengths = sorted({
        result["protein_length"]
        for result in results
    })

    plt.figure(figsize=(9, 5))

    for algorithm in algorithms:

        values = []

        for length in lengths:

            matching = next(
                (
                    result for result in results
                    if result["protein_length"] == length
                    and result["algorithm"] == algorithm
                ),
                None
            )

            if matching is None:
                values.append(None)
            else:
                values.append(matching[metric])

        plt.plot(
            lengths,
            values,
            marker="o",
            linewidth=2,
            label=algorithm
        )

    plt.title(title)
    plt.xlabel("Protein Length")
    plt.ylabel(ylabel)

    plt.xticks(lengths)

    plt.grid(
        True,
        linestyle="--",
        alpha=0.5
    )

    plt.legend()
    plt.tight_layout()

    output_file = BASE_DIR / filename

    plt.savefig(
        output_file,
        dpi=300
    )

    plt.close()

    print(f"Graph saved: {output_file}")


# ==========================================
# MAIN
# ==========================================

def main():

    results = load_results()

    aggregated_results = aggregate_results(results)

    create_plot(
        aggregated_results,
        "average_energy",
        "Average Energy Comparison",
        "Average Energy",
        "energy_comparison.png"
    )

    create_plot(
        aggregated_results,
        "average_time",
        "Execution Time Comparison",
        "Execution Time (seconds)",
        "time_comparison.png"
    )

    create_plot(
        aggregated_results,
        "average_memory_mb",
        "Memory Usage Comparison",
        "Memory (MB)",
        "memory_comparison.png"
    )

    create_plot(
        aggregated_results,
        "average_elimination_percentage",
        "Search Space Reduction Comparison",
        "Search Space Reduction (%)",
        "search_space_reduction.png"
    )

    print("\nAll graphs generated successfully.")


if __name__ == "__main__":
    main()
