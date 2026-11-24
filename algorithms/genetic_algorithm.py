
import random

from protein.representation.structure import ProteinStructure
from protein.representation.constraints import is_valid_structure

from evaluation.energy import calculate_energy

from algorithms.moves import random_move
from algorithms.search_utils import (
    register_structure,
    get_structure_signature
)


def create_random_structure(hp_sequence):
    """
    Creates a randomized valid protein structure.
    """

    structure = ProteinStructure(hp_sequence)

    for _ in range(max(10, len(hp_sequence) * 3)):
        new_structure = random_move(structure)

        if new_structure is not None:
            structure = new_structure

    return structure


def initialize_population(
    hp_sequence,
    population_size,
    visited_states
):
    """
    Generates an initial population of unique valid structures.
    """

    population = []
    attempts = 0
    max_attempts = population_size * 30

    while (
        len(population) < population_size
        and attempts < max_attempts
    ):
        structure = create_random_structure(hp_sequence)
        attempts += 1

        if not is_valid_structure(structure):
            continue

        if register_structure(structure, visited_states):
            population.append(structure)

    return population


def evaluate_population(population, energy_cache):
    """
    Evaluates individuals and caches previously calculated energies.
    """

    evaluated_population = []

    for structure in population:
        signature = get_structure_signature(structure)

        if signature not in energy_cache:
            energy_cache[signature] = calculate_energy(structure)

        evaluated_population.append(
            (structure, energy_cache[signature])
        )

    return evaluated_population


def selection(evaluated_population, tournament_size=3):
    """
    Tournament selection: chooses the individual
    with the lowest energy.
    """

    tournament_size = min(
        tournament_size,
        len(evaluated_population)
    )

    candidates = random.sample(
        evaluated_population,
        tournament_size
    )

    return min(
        candidates,
        key=lambda item: item[1]
    )[0]


def crossover(parent1, parent2):
    """
    Combines two parent structures using a random
    crossover point.

    Invalid offspring are rejected.
    """

    hp_sequence = parent1.hp_sequence
    length = len(hp_sequence)

    if length < 3:
        return None

    for _ in range(10):

        cut = random.randint(1, length - 2)

        coordinates1 = parent1.coordinates
        coordinates2 = parent2.coordinates

        child_coordinates = list(coordinates1[:cut + 1])

        x1, y1, z1 = coordinates1[cut]
        x2, y2, z2 = coordinates2[cut]

        dx = x1 - x2
        dy = y1 - y2
        dz = z1 - z2

        for x, y, z in coordinates2[cut + 1:]:
            child_coordinates.append(
                (x + dx, y + dy, z + dz)
            )

        child = ProteinStructure(
            hp_sequence,
            child_coordinates
        )

        if is_valid_structure(child):
            return child

    return None


def mutation(structure):
    """
    Applies a random valid structural movement.
    """

    for _ in range(10):

        new_structure = random_move(structure)

        if (
            new_structure is not None
            and is_valid_structure(new_structure)
        ):
            return new_structure

    return structure


def genetic_algorithm(
    initial_structure,
    population_size=30,
    generations=100,
    mutation_rate=0.3,
    crossover_rate=0.8,
    tournament_size=3
):
    """
    Genetic Algorithm for 3D protein structure optimization.

    The objective is to minimize protein energy.
    """

    if population_size < 2:
        raise ValueError("Population size must be at least 2.")

    if generations < 1:
        raise ValueError("Generations must be at least 1.")

    if not 0 <= mutation_rate <= 1:
        raise ValueError("Mutation rate must be between 0 and 1.")

    if not 0 <= crossover_rate <= 1:
        raise ValueError("Crossover rate must be between 0 and 1.")

    if not is_valid_structure(initial_structure):
        raise ValueError("Initial protein structure is invalid.")

    hp_sequence = initial_structure.hp_sequence

    # Store all previously explored structures.
    visited_states = set()

    # Cache calculated energy values.
    energy_cache = {}

    # Generate initial population.
    population = initialize_population(
        hp_sequence,
        population_size,
        visited_states
    )

    # Include the initial structure if it is not a duplicate.
    if register_structure(initial_structure, visited_states):
        if len(population) < population_size:
            population.append(initial_structure)

    if not population:
        population = [initial_structure]

    # Evaluate the initial population.
    evaluated_population = evaluate_population(
        population,
        energy_cache
    )

    best_structure, best_energy = min(
        evaluated_population,
        key=lambda item: item[1]
    )

    energy_history = []

    # Main Genetic Algorithm loop.
    for generation in range(generations):

        evaluated_population.sort(
            key=lambda item: item[1]
        )

        # Elitism: preserve the best individual.
        new_population = [
            evaluated_population[0][0]
        ]

        # Track structures inside the current generation.
        generation_signatures = {
            get_structure_signature(evaluated_population[0][0])
        }

        attempts = 0
        max_attempts = population_size * 50

        while (
            len(new_population) < population_size
            and attempts < max_attempts
        ):
            attempts += 1

            # Select parents.
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
                child = ProteinStructure(
                    hp_sequence,
                    list(parent1.coordinates)
                )

            if child is None:
                continue

            # Mutation.
            if random.random() < mutation_rate:
                child = mutation(child)

            # Reject invalid structures.
            if not is_valid_structure(child):
                continue

            signature = get_structure_signature(child)

            # Reject duplicates from all previous generations
            # and duplicates in the current population.
            if signature in generation_signatures:
                continue

            if not register_structure(child, visited_states):
                continue

            generation_signatures.add(signature)
            new_population.append(child)

        # If there are not enough new unique structures,
        # reuse previous individuals to complete the population.
        for structure, energy in evaluated_population:

            if len(new_population) >= population_size:
                break

            signature = get_structure_signature(structure)

            if signature not in generation_signatures:
                generation_signatures.add(signature)
                new_population.append(structure)

        population = new_population

        # Evaluate the new population.
        evaluated_population = evaluate_population(
            population,
            energy_cache
        )

        # Find the best structure in this generation.
        generation_best, generation_energy = min(
            evaluated_population,
            key=lambda item: item[1]
        )

        if generation_energy < best_energy:
            best_structure = generation_best
            best_energy = generation_energy

        # Save the best energy after every generation.
        energy_history.append(best_energy)

    return best_structure, best_energy, energy_history
