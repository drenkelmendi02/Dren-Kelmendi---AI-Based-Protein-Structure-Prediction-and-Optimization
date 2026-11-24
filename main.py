
from protein.representation.hp_model import convert_to_hp
from protein.representation.structure import ProteinStructure
from protein.representation.constraints import is_valid_structure
from algorithms.genetic_algorithm import genetic_algorithm

from algorithms.simulated_annealing import simulated_annealing

from evaluation.metrics import measure_performance
from evaluation.energy import calculate_energy


# Original protein sequence
sequence = "ACDEFGHIKL"

# Convert sequence to HP representation
hp_sequence = convert_to_hp(sequence)

# Create initial protein structure
protein = ProteinStructure(hp_sequence)


print("\n========== PROTEIN INFORMATION ==========")

print("Original Sequence:", sequence)
print("HP Sequence:", hp_sequence)
print("Protein Length:", protein.get_length())

print("\nInitial Coordinates:")

for i in range(protein.get_length()):
    print(
        i + 1,
        protein.get_amino_acid_type(i),
        protein.get_coordinate(i)
    )


# Initial structure validation
print("\nInitial Structure Valid:", is_valid_structure(protein))

# Initial energy
initial_energy = calculate_energy(protein)

print("Initial Energy:", initial_energy)


# Run Simulated Annealing
result, performance = measure_performance(
    simulated_annealing,
    protein,
    initial_temperature=10.0,
    cooling_rate=0.995,
    iterations=1000
)

best_structure, best_energy, energy_history = result


print("\n========== SIMULATED ANNEALING RESULTS ==========")

print("Best Energy:", best_energy)
print("Iterations:", len(energy_history))

print(
    "Best Structure Valid:",
    is_valid_structure(best_structure)
)

print("\nBest Coordinates:")

for i in range(best_structure.get_length()):
    print(
        i + 1,
        best_structure.get_amino_acid_type(i),
        best_structure.get_coordinate(i)
    )


# Performance metrics
print("\n========== PERFORMANCE METRICS ==========")

print(
    "Execution Time:",
    performance["execution_time"],
    "seconds"
)

print(
    "Peak Memory:",
    performance["peak_memory_mb"],
    "MB"
)


print("\n========== GENETIC ALGORITHM ==========")

ga_result, ga_performance = measure_performance(
    genetic_algorithm,
    protein,
    population_size=30,
    generations=100,
    mutation_rate=0.3,
    crossover_rate=0.8,
    return_stats=True
)

ga_structure, ga_energy, ga_history, ga_stats = ga_result

print("Best Energy:", ga_energy)
print("Generations:", len(ga_history))
print("Valid Structure:", is_valid_structure(ga_structure))

print("\n========== GENETIC ALGORITHM STATISTICS ==========")

print(
    "Candidate Configurations:",
    ga_stats["candidate_configurations"]
)

print(
    "Valid Structures:",
    ga_stats["valid_structures"]
)

print(
    "Invalid Structures:",
    ga_stats["invalid_structures"]
)

print(
    "Duplicate Structures:",
    ga_stats["duplicate_structures"]
)

print(
    "Unique Structures:",
    ga_stats["unique_structures"]
)

print(
    "Energy Evaluations:",
    ga_stats["energy_evaluations"]
)

print(
    "Elimination Percentage:",
    round(ga_stats["elimination_percentage"], 2), "%"
)

print("\n========== PERFORMANCE METRICS ==========")

print(
    "Execution Time:",
    round(ga_performance["execution_time"], 4),
    "seconds"
)

print(
    "Peak Memory:",
    round(ga_performance["peak_memory_mb"], 4),
    "MB"
)

