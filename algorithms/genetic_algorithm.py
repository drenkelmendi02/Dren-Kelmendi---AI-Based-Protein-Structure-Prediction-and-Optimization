
import random

from protein.representation.structure import ProteinStructure
from protein.representation.constraints import is_valid_structure
from evaluation.energy import calculate_energy
from algorithms.moves import random_move


def create_random_structure(hp_sequence):
    """
    Creates a valid randomized protein structure.
    """

    structure = ProteinStructure(hp_sequence)

    for _ in range(max(10, len(hp_sequence) * 3)):
        new_structure = random_move(structure)

        if new_structure is not None:
            structure = new_structure

    return structure


def initialize_population(hp_sequence, population_size):
    """
    Generates the initial population of valid structures.
    """

    population = []

    for _ in range(population_size):
        structure = create_random_structure(hp_sequence)

        if is_valid_structure(structure):
            population.append(structure)

    return population


def evaluate_population(population):
    """
    Calculates the energy of every individual.
    """

    return [
        (structure, calculate_energy(structure))
        for structure in population
    ]


def selection(evaluated_population, tournament_size=3):
    """
    Selects the individual with the lowest energy
    from a randomly selected tournament.
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

        # Keep the prefix from parent 1.
        child_coordinates = list(coordinates1[:cut + 1])

        # Translate the suffix from parent 2.
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
    Attempts to improve diversity by applying
    a random valid structural movement.
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

    hp_sequence = initial_structure.hp_sequence

    population = initialize_population(
        hp_sequence,
        population_size
    )

    # Ensure the initial structure is included.
    if is_valid_structure(initial_structure):
        population.append(initial_structure)

    if not population:
        raise ValueError(
            "Could not generate a valid initial population."
        )

    best_structure = min(
        population,
        key=calculate_energy
    )

    best_energy = calculate_energy(best_structure)

    energy_history = []

    for generation in range(generations):

        evaluated_population = evaluate_population(population)

        evaluated_population.sort(
            key=lambda item: item[1]
        )

        # Elitism: preserve the best individual.
        new_population = [
            evaluated_population[0][0]
        ]

        while len(new_population) < population_size:

            parent1 = selection(
                evaluated_population,
                tournament_size
            )

            parent2 = selection(
                evaluated_population,
                tournament_size
            )

            if random.random() < crossover_rate:
                child = crossover(parent1, parent2)
            else:
                child = None

            # If crossover fails, use a copy of parent 1.
            if child is None:
                child = ProteinStructure(
                    hp_sequence,
                    list(parent1.coordinates)
                )

            if random.random() < mutation_rate:
                child = mutation(child)

            if is_valid_structure(child):
                new_population.append(child)

        population = new_population

        # Find the best individual of this generation.
        generation_best = min(
            population,
            key=calculate_energy
        )

        generation_energy = calculate_energy(
            generation_best
        )

        if generation_energy < best_energy:
            best_structure = generation_best
            best_energy = generation_energy

        energy_history.append(best_energy)

    return best_structure, best_energy, energy_history
