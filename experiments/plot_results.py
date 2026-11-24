
import csv
from pathlib import Path

import matplotlib.pyplot as plt


# Folderi ku gjendet ky fajll.
BASE_DIR = Path(__file__).resolve().parent

# Leximi i rezultateve nga CSV.
CSV_FILE = BASE_DIR / "benchmark_results.csv"


def load_results():
    results = []

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            results.append({
                "protein_length": int(row["protein_length"]),
                "algorithm": row["algorithm"],
                "average_energy": float(row["average_energy"]),
                "average_time": float(row["average_time"]),
                "average_memory_mb": float(row["average_memory_mb"])
            })

    return results


def create_plot(results, metric, title, ylabel, filename):
    algorithms = ["SA", "GA"]

    lengths = sorted(set(
        result["protein_length"] for result in results
    ))

    plt.figure(figsize=(9, 5))

    for algorithm in algorithms:
        values = []

        for length in lengths:
            matching = next(
                result for result in results
                if result["protein_length"] == length
                and result["algorithm"] == algorithm
            )

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
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()

    output_file = BASE_DIR / filename
    plt.savefig(output_file, dpi=300)
    plt.close()

    print(f"Graph saved: {output_file}")


def main():
    results = load_results()

    create_plot(
        results,
        "average_energy",
        "Average Energy Comparison",
        "Average Energy",
        "energy_comparison.png"
    )

    create_plot(
        results,
        "average_time",
        "Execution Time Comparison",
        "Execution Time (seconds)",
        "time_comparison.png"
    )

    create_plot(
        results,
        "average_memory_mb",
        "Memory Usage Comparison",
        "Memory (MB)",
        "memory_comparison.png"
    )

    print("\nAll graphs generated successfully.")


if __name__ == "__main__":
    main()
