
from protein.representation.hp_model import convert_to_hp
from visualization.structure_view import plot_structure, plot_energy_history
from algorithms.moves import end_move
from protein.representation.structure import ProteinStructure
from algorithms.simulated_annealing import simulated_annealing
from protein.representation.constraints import is_valid_structure
from evaluation.metrics import measure_performance
from evaluation.energy import calculate_energy


# Original protein sequence
sequence = "ACDEFGHIKL"

# Convert sequence to HP representation
hp_sequence = convert_to_hp(sequence)

# Create initial protein structure
protein = ProteinStructure(hp_sequence)

print("HP Sequence:", hp_sequence)
print("Protein Length:", protein.get_length())
print("Coordinates:")

for i in range(protein.get_length()):
    print(
        i + 1,
        protein.get_amino_acid_type(i),
        protein.get_coordinate(i)
    )

# Check structure validity
print("Is structure valid:", is_valid_structure(protein))

# Calculate initial protein energy
energy = calculate_energy(protein)
print("Protein Energy:", energy)


# Test End Move
new_protein = end_move(protein)

print("\n--- END MOVE TEST ---")

if new_protein is not None:
    print("New Coordinates:")

    for i in range(new_protein.get_length()):
        print(
            i + 1,
            new_protein.get_amino_acid_type(i),
            new_protein.get_coordinate(i)
        )

    print(
        "New Structure Valid:",
        is_valid_structure(new_protein)
    )
else:
    print("No valid move available.")


# Measure Simulated Annealing performance
result, performance = measure_performance(
    simulated_annealing,
    protein,
    initial_temperature=10.0,
    cooling_rate=0.995,
    iterations=1000
)

best_structure, best_energy, energy_history = result

print("\n--- PERFORMANCE METRICS ---")
print("Execution Time:", performance["execution_time"], "seconds")
print("Peak Memory:", performance["peak_memory_mb"], "MB")

print("\n--- SIMULATED ANNEALING RESULTS ---")
print("Best Energy:", best_energy)
print("Iterations:", len(energy_history))
print("Best Structure Valid:", is_valid_structure(best_structure))

print("Best Coordinates:")

for i in range(best_structure.get_length()):
    print(
        i + 1,
        best_structure.get_amino_acid_type(i),
        best_structure.get_coordinate(i)
    )


# Visualize the best structure and energy history
plot_structure(best_structure, "Simulated Annealing - Best Structure")
plot_energy_history(energy_history, "Simulated Annealing - Energy Convergence")
