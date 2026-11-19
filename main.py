
from protein.representation.hp_model import convert_to_hp
from protein.representation.structure import ProteinStructure
from protein.representation.constraints import is_valid_structure

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
