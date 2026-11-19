
import random

from protein.representation.structure import ProteinStructure
from protein.representation.constraints import is_valid_structure
from evaluation.energy import calculate_energy


# Direction encoding for the 2D lattice
DIRECTIONS = {
    0: (1, 0),    # Right
    1: (0, 1),    # Up
    2: (-1, 0),   # Left
    3: (0, -1)    # Down
}


def decode_chromosome(hp_sequence, chromosome):
    """
    Convert a direction chromosome into a protein structure.
    Return None if the structure contains overlaps.
    """

    coordinates = [(0, 0)]

    x, y = 0, 0

    for gene in chromosome:

        dx, dy = DIRECTIONS[gene]

        x += dx
        y += dy

        new_position = (x, y)

        if new_position in coordinates:
            return None

        coordinates.append(new_position)

    structure = ProteinStructure(hp_sequence, coordinates)

    if not is_valid_structure(structure):
        return None

    return structure


def create_random_chromosome(length, max_attempts=1000):
    """
    Generate a random valid self-avoiding walk.
    """

    for _ in range(max_attempts):

        chromosome = []
        coordinates = [(0, 0)]

        x, y = 0, 0

        for _ in range(length - 1):

            possible_genes = []

            for gene, (dx, dy) in DIRECTIONS.items():

                new_position = (x + dx, y + dy)

                if new_position not in coordinates:
                    possible_genes.append(gene)

            if not possible_genes:
                break

            gene = random.choice(possible_genes)
            chromosome.append(gene)

            dx, dy = DIRECTIONS[gene]
            x += dx
            y += dy

            coordinates.append((x, y))

        if len(chromosome) == length - 1:
            return chromosome

    raise RuntimeError("Could not generate a valid initial chromosome.")


def evaluate_chromosome(hp_sequence, chromosome):
    """
    Evaluate a chromosome using the HP energy function.
    """

    structure = decode_chromosome(hp_sequence, chromosome)

    if structure is None:
        return None, None

    energy = calculate_energy(structure)

    return structure, energy


def tournament_selection(population, scores, tournament_size=3):
    """
    Select the chromosome with the lowest energy
    from a randomly selected tournament.
    """

    candidates = random.sample(
        range(len(population)),
        min(tournament_size, len(population))
    )

    winner = min(candidates, key=lambda index: scores[index])

    return population[winner][:]


def crossover(parent1, parent2):
    """
    Combine two parent chromosomes using one-point crossover.
    """

    if len(parent1) < 2:
        return parent1[:], parent2[:]

    point = random.randint(1, len(parent1) - 1)

    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    return child1, child2


def mutate(chromosome, mutation_rate=0.05):
    """
    Randomly change directions in a chromosome.
    """

    mutated = chromosome[:]

    for i in range(len(mutated)):

        if random.random() < mutation_rate:

            possible_genes = [
                gene for gene in DIRECTIONS
                if gene != mutated[i]
            ]

            mutated[i] = random.choice(possible_genes)

    return mutated


def genetic_algorithm(
    initial_structure,
    population_size=30,
    generations=100,
    mutation_rate=0.05,
    crossover_rate=0.8,
    tournament_size=3
):
    """
    Optimize a protein structure using Genetic Algorithm.

    Returns:
        best_structure: Best structure found.
        best_energy: Energy of the best structure.
        energy_history: Best energy in each generation.
    """

    hp_sequence = initial_structure.hp_sequence
    length = len(hp_sequence)

    # Create the initial population
    population = [
        create_random_chromosome(length)
        for _ in range(population_size)
    ]

    best_structure = None
    best_energy = float("inf")
    energy_history = []

    for generation in range(generations):

        scores = []
        structures = []

        # Evaluate the population
        for chromosome in population:

            structure, energy = evaluate_chromosome(
                hp_sequence,
                chromosome
            )

            structures.append(structure)
            scores.append(
                energy if energy is not None else float("inf")
            )

        # Find the best individual in this generation
        best_index = min(
            range(len(scores)),
            key=lambda index: scores[index]
        )

        if scores[best_index] < best_energy:

            best_energy = scores[best_index]
            best_structure = structures[best_index]

        energy_history.append(best_energy)

        # Keep the best chromosome (elitism)
        new_population = [
            population[best_index][:]
        ]

        # Create the next generation
        while len(new_population) < population_size:

            parent1 = tournament_selection(
                population, scores, tournament_size
            )

            parent2 = tournament_selection(
                population, scores, tournament_size
            )

            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1[:], parent2[:]

            for child in (child1, child2):

                child = mutate(child, mutation_rate)

                child_structure = decode_chromosome(
                    hp_sequence, child
                )

                # Keep only valid offspring
                if child_structure is not None:
                    new_population.append(child)
                else:
                    new_population.append(parent1[:])

                if len(new_population) >= population_size:
                    break

        population = new_population

    return best_structure, best_energy, energy_history
