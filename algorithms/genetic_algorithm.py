
import random

from protein.representation.structure import ProteinStructure
from protein.representation.constraints import is_valid_structure
from evaluation.energy import calculate_energy
from algorithms.moves import random_move
from algorithms.search_utils import (
    get_structure_signature,
    register_structure
)


def create_random_structure(hp_sequence):
    """
    Krijon një strukturë fillestare dhe përpiqet
    ta ndryshojë për të krijuar një konfigurim të rastësishëm.
    """
    structure = ProteinStructure(hp_sequence)

    for _ in range(len(hp_sequence) * 3):
        new_structure = random_move(structure)

        if new_structure is not None:
            structure = new_structure

    return structure


def initialize_population(
    hp_sequence,
    population_size,
    visited_states,
    statistics
):
    """
    Krijon popullatën fillestare duke ruajtur
    vetëm strukturat valide dhe unike.
    """
    population = []

    attempts = 0
    max_attempts = population_size * 100

    while len(population) < population_size and attempts < max_attempts:
        attempts += 1
        statistics["candidate_configurations"] += 1

        structure = create_random_structure(hp_sequence)

        if not is_valid_structure(structure):
            statistics["invalid_structures"] += 1
            continue

        statistics["valid_structures"] += 1

        signature = get_structure_signature(structure)

        if signature in visited_states:
            statistics["duplicate_structures"] += 1
            continue

        register_structure(structure, visited_states)
        statistics["unique_structures"] += 1

        population.append(structure)

    if not population:
        raise RuntimeError(
            "Could not generate a valid initial population."
        )

    # Nëse nuk arrihet madhësia e kërkuar,
    # popullata plotësohet me struktura ekzistuese.
    while len(population) < population_size:
        population.append(random.choice(population))

    return population


def evaluate_population(population, energy_cache, statistics):
    """
    Llogarit energjinë për secilën strukturë.
    Përdor cache për të shmangur llogaritjet e përsëritura.
    """
    evaluated_population = []

    for structure in population:
        signature = get_structure_signature(structure)

        if signature not in energy_cache:
            energy_cache[signature] = calculate_energy(structure)
            statistics["energy_evaluations"] += 1

        energy = energy_cache[signature]

        evaluated_population.append((structure, energy))

    return evaluated_population


def selection(evaluated_population, tournament_size=3):
    """
    Tournament selection:
    zgjedh strukturën me energjinë më të mirë
    nga një grup kandidatësh të rastësishëm.
    """
    tournament_size = min(
        tournament_size,
        len(evaluated_population)
    )

    candidates = random.sample(
        evaluated_population,
        tournament_size
    )

    return min(candidates, key=lambda item: item[1])[0]


def crossover(parent1, parent2):
    """
    Kombinon dy prindër duke marrë një pjesë
    nga struktura e parë dhe pjesën tjetër nga e dyta.

    Kthimi bëhet vetëm nëse struktura e krijuar është valide.
    """
    hp_sequence = parent1.hp_sequence

    if len(hp_sequence) < 3:
        return None

    cut_point = random.randint(1, len(hp_sequence) - 2)

    coordinates1 = parent1.coordinates
    coordinates2 = parent2.coordinates

    child_coordinates = list(coordinates1[:cut_point])

    # Zhvendosja e pjesës së dytë për të ruajtur
    # lidhjen mes aminoacideve në pikën e prerjes.
    p1_x, p1_y, p1_z = coordinates1[cut_point - 1]
    p2_x, p2_y, p2_z = coordinates2[cut_point - 1]

    offset = (
        p1_x - p2_x,
        p1_y - p2_y,
        p1_z - p2_z
    )

    for x, y, z in coordinates2[cut_point:]:
        child_coordinates.append((
            x + offset[0],
            y + offset[1],
            z + offset[2]
        ))

    child = ProteinStructure(
        hp_sequence,
        child_coordinates
    )

    if not is_valid_structure(child):
        return None

    return child


def mutation(structure, mutation_rate):
    """
    Mutacioni ndryshon strukturën përmes një lëvizjeje
    të rastësishme në hapësirën 3D.
    """
    if random.random() < mutation_rate:
        return random_move(structure)

    return structure


def genetic_algorithm(
    initial_structure,
    population_size=30,
    generations=100,
    mutation_rate=0.3,
    crossover_rate=0.8,
    tournament_size=3,
    return_stats=False
):
    """
    Genetic Algorithm për optimizimin e strukturës
    së proteinës në modelin 3D HP.

    Objektivi:
    Minimizimi i energjisë E = -N_HH.
    """

    # Kontrollimi i parametrave.
    if population_size < 2:
        raise ValueError("Population size must be at least 2.")

    if generations < 1:
        raise ValueError("Generations must be at least 1.")

    if not 0 <= mutation_rate <= 1:
        raise ValueError("Mutation rate must be between 0 and 1.")

    if not 0 <= crossover_rate <= 1:
        raise ValueError("Crossover rate must be between 0 and 1.")

    if tournament_size < 1:
        raise ValueError("Tournament size must be at least 1.")

    if not is_valid_structure(initial_structure):
        raise ValueError("Initial structure must be valid.")

    hp_sequence = initial_structure.hp_sequence

    # Statistikat e algoritmit.
    statistics = {
        "candidate_configurations": 0,
        "valid_structures": 0,
        "invalid_structures": 0,
        "duplicate_structures": 0,
        "unique_structures": 0,
        "energy_evaluations": 0,
        "elimination_percentage": 0.0
    }

    visited_states = set()
    energy_cache = {}

    # Krijimi i popullatës fillestare.
    population = initialize_population(
        hp_sequence,
        population_size,
        visited_states,
        statistics
    )

    # Vlerësimi i popullatës.
    evaluated_population = evaluate_population(
        population,
        energy_cache,
        statistics
    )

    best_structure, best_energy = min(
        evaluated_population,
        key=lambda item: item[1]
    )

    energy_history = [best_energy]

    # Regjistrimi i strukturës fillestare.
    initial_signature = get_structure_signature(
        initial_structure
    )

    statistics["candidate_configurations"] += 1
    statistics["valid_structures"] += 1

    if initial_signature in visited_states:
        statistics["duplicate_structures"] += 1
    else:
        register_structure(
            initial_structure,
            visited_states
        )

        statistics["unique_structures"] += 1

    # Përdorimi i Energy Cache.
    if initial_signature not in energy_cache:
        energy_cache[initial_signature] = calculate_energy(
            initial_structure
        )

        statistics["energy_evaluations"] += 1

    initial_energy = energy_cache[initial_signature]

    if initial_energy < best_energy:
        best_structure = initial_structure
        best_energy = initial_energy

    # Evolucioni i popullatës.
    for generation in range(generations):

        evaluated_population = evaluate_population(
            population,
            energy_cache,
            statistics
        )

        evaluated_population.sort(
            key=lambda item: item[1]
        )

        # Elitizmi: ruhen dy strukturat më të mira.
        new_population = [
            evaluated_population[0][0]
        ]

        if len(evaluated_population) > 1:
            new_population.append(
                evaluated_population[1][0]
            )

        # Kufizimi i tentimeve për të parandaluar
        # ciklet e pafundme gjatë krijimit të popullatës.
        max_attempts = population_size * 100
        attempts = 0

        while (
            len(new_population) < population_size
            and attempts < max_attempts
        ):

            attempts += 1

            parent1 = selection(
                evaluated_population,
                tournament_size
            )

            parent2 = selection(
                evaluated_population,
                tournament_size
            )

            # Crossover.
            if random.random() < crossover_rate:
                child = crossover(parent1, parent2)
            else:
                child = parent1

            if child is None:
                statistics["candidate_configurations"] += 1
                statistics["invalid_structures"] += 1
                continue

            # Mutation.
            child = mutation(child, mutation_rate)

            if child is None:
                statistics["candidate_configurations"] += 1
                statistics["invalid_structures"] += 1
                continue

            statistics["candidate_configurations"] += 1

            # Kontrollimi i validitetit.
            if not is_valid_structure(child):
                statistics["invalid_structures"] += 1
                continue

            statistics["valid_structures"] += 1

            signature = get_structure_signature(child)

            # Eliminimi i strukturave duplikate.
            if signature in visited_states:
                statistics["duplicate_structures"] += 1
                continue

            register_structure(child, visited_states)

            statistics["unique_structures"] += 1

            new_population.append(child)

        # Plotësimi i popullatës nëse nuk janë krijuar
        # mjaftueshëm struktura të reja.
        while len(new_population) < population_size:
            new_population.append(
                random.choice(evaluated_population)[0]
            )

        population = new_population

        # Vlerësimi i gjeneratës së re.
        evaluated_population = evaluate_population(
            population,
            energy_cache,
            statistics
        )

        generation_best_structure, generation_best_energy = min(
            evaluated_population,
            key=lambda item: item[1]
        )

        if generation_best_energy < best_energy:
            best_structure = generation_best_structure
            best_energy = generation_best_energy

        energy_history.append(best_energy)

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
