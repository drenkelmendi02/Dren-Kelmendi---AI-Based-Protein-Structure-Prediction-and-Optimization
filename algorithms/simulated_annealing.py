
import math
import random

from algorithms.moves import random_move
from algorithms.search_utils import get_structure_signature
from evaluation.energy import calculate_energy
from protein.representation.constraints import is_valid_structure


def simulated_annealing(
    initial_structure,
    initial_temperature=10.0,
    cooling_rate=0.995,
    iterations=1000,
    return_stats=False
):
    """
    Simulated Annealing për optimizimin e strukturës së proteinës.

    Objektivi:
    Minimizimi i energjisë E = -N_HH.

    Nëse return_stats=True, kthen edhe statistikat
    e konfigurimeve të eksploruara.
    """

    if initial_temperature <= 0:
        raise ValueError("Initial temperature must be greater than zero.")

    if not 0 < cooling_rate <= 1:
        raise ValueError("Cooling rate must be between 0 and 1.")

    if iterations < 0:
        raise ValueError("Iterations cannot be negative.")

    if not is_valid_structure(initial_structure):
        raise ValueError("Initial protein structure is invalid.")

    # Struktura dhe energjia fillestare.
    current_structure = initial_structure
    current_energy = calculate_energy(current_structure)

    best_structure = current_structure
    best_energy = current_energy

    temperature = initial_temperature

    # Historiku fillon me energjinë fillestare.
    energy_history = [current_energy]

    # Ruajtja e konfigurimeve të vizituara.
    visited_states = {
        get_structure_signature(initial_structure)
    }

    # Statistikat e algoritmit.
    statistics = {
        "candidate_configurations": 0,
        "valid_structures": 0,
        "invalid_structures": 0,
        "duplicate_structures": 0,
        "unique_structures": 1,
        "energy_evaluations": 1,
        "iterations_completed": 0,
        "elimination_percentage": 0.0
    }

    for iteration in range(iterations):

        statistics["candidate_configurations"] += 1

        # Gjenerimi i një konfigurimi të ri.
        new_structure = random_move(current_structure)

        # Nëse nuk gjendet lëvizje valide.
        if new_structure is None:
            statistics["invalid_structures"] += 1
            energy_history.append(current_energy)
            statistics["iterations_completed"] += 1

            temperature *= cooling_rate

            if temperature < 1e-10:
                break

            continue

        # Kontrollimi i validitetit.
        if not is_valid_structure(new_structure):
            statistics["invalid_structures"] += 1
            energy_history.append(current_energy)
            statistics["iterations_completed"] += 1

            temperature *= cooling_rate

            if temperature < 1e-10:
                break

            continue

        statistics["valid_structures"] += 1

        # Kontrollimi i konfigurimeve të përsëritura.
        signature = get_structure_signature(new_structure)

        if signature in visited_states:
            statistics["duplicate_structures"] += 1
            energy_history.append(current_energy)
            statistics["iterations_completed"] += 1

            temperature *= cooling_rate

            if temperature < 1e-10:
                break

            continue

        # Regjistrimi i konfigurimit unik.
        visited_states.add(signature)
        statistics["unique_structures"] += 1

        # Llogaritja e energjisë vetëm për konfigurime unike.
        new_energy = calculate_energy(new_structure)
        statistics["energy_evaluations"] += 1

        # Diferenca e energjisë.
        delta_energy = new_energy - current_energy

        # Pranimi i zgjidhjes.
        if delta_energy <= 0:
            current_structure = new_structure
            current_energy = new_energy

        else:
            probability = math.exp(
                -delta_energy / temperature
            )

            if random.random() < probability:
                current_structure = new_structure
                current_energy = new_energy

        # Ruajtja e zgjidhjes më të mirë.
        if current_energy < best_energy:
            best_structure = current_structure
            best_energy = current_energy

        energy_history.append(current_energy)

        statistics["iterations_completed"] += 1

        # Ulja e temperaturës.
        temperature *= cooling_rate

        if temperature < 1e-10:
            break

    # Llogaritja e përqindjes së konfigurimeve të eliminuara.
    total_candidates = statistics["candidate_configurations"]

    eliminated = (
        statistics["invalid_structures"]
        + statistics["duplicate_structures"]
    )

    if total_candidates > 0:
        statistics["elimination_percentage"] = (
            eliminated / total_candidates
        ) * 100

    if return_stats:
        return (
            best_structure,
            best_energy,
            energy_history,
            statistics
        )

    return best_structure, best_energy, energy_history
