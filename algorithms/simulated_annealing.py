
import math
import random

from algorithms.moves import random_move
from evaluation.energy import calculate_energy


def simulated_annealing(
    initial_structure,
    initial_temperature=10.0,
    cooling_rate=0.995,
    iterations=1000
):
    
    current_structure = initial_structure
    current_energy = calculate_energy(current_structure)

    best_structure = current_structure
    best_energy = current_energy

    temperature = initial_temperature
    energy_history = []


    for iteration in range(iterations):

        new_structure = random_move(current_structure)

        if new_structure is None:
            energy_history.append(current_energy)
            temperature *= cooling_rate
            continue


        new_energy = calculate_energy(new_structure)


        delta_energy = new_energy - current_energy


        if delta_energy <= 0:
            current_structure = new_structure
            current_energy = new_energy

        else:
            probability = math.exp(-delta_energy / temperature)

            if random.random() < probability:
                current_structure = new_structure
                current_energy = new_energy


        if current_energy < best_energy:
            best_structure = current_structure
            best_energy = current_energy


        energy_history.append(current_energy)


        temperature *= cooling_rate

        if temperature < 1e-10:
            break

    return best_structure, best_energy, energy_history
