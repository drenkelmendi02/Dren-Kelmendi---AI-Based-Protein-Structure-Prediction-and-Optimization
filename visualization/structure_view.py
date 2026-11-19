
import matplotlib.pyplot as plt


def plot_structure(structure, title="2D Protein Structure"):

    coordinates = structure.coordinates
    hp_sequence = structure.hp_sequence

    x_values = [point[0] for point in coordinates]
    y_values = [point[1] for point in coordinates]

    plt.figure(figsize=(9, 7))

    # Draw connections between amino acids
    plt.plot(
        x_values,
        y_values,
        color="gray",
        linewidth=2,
        zorder=1
    )

    # Draw each amino acid
    for i, (x, y) in enumerate(coordinates):

        if hp_sequence[i] == "H":
            color = "red"
        else:
            color = "blue"

        plt.scatter(
            x,
            y,
            color=color,
            s=350,
            edgecolors="black",
            zorder=2
        )

        plt.text(
            x,
            y,
            f"{hp_sequence[i]}{i + 1}",
            ha="center",
            va="center",
            color="white",
            fontsize=9,
            fontweight="bold",
            zorder=3
        )

    plt.title(title)
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.axis("equal")
    plt.tight_layout()
    plt.show()


def plot_energy_history(energy_history, title="Energy Convergence"):

    plt.figure(figsize=(9, 5))

    plt.plot(
        range(1, len(energy_history) + 1),
        energy_history
    )

    plt.title(title)
    plt.xlabel("Iteration / Generation")
    plt.ylabel("Protein Energy")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
