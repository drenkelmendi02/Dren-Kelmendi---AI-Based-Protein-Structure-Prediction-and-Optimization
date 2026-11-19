
import matplotlib.pyplot as plt


def plot_structure(structure, title="3D Protein Structure"):

    coordinates = structure.coordinates
    hp_sequence = structure.hp_sequence

    x_values = [point[0] for point in coordinates]
    y_values = [point[1] for point in coordinates]
    z_values = [point[2] for point in coordinates]

    figure = plt.figure(figsize=(10, 8))

    ax = figure.add_subplot(111, projection="3d")

    # Draw connections between amino acids
    ax.plot(
        x_values,
        y_values,
        z_values,
        color="gray",
        linewidth=2
    )

    # Draw amino acids
    for i, (x, y, z) in enumerate(coordinates):

        if hp_sequence[i] == "H":
            color = "red"
        else:
            color = "blue"

        ax.scatter(
            x, y, z,
            color=color,
            s=350,
            edgecolors="black"
        )

        ax.text(
            x, y, z,
            f"{hp_sequence[i]}{i + 1}",
            color="white",
            ha="center",
            va="center",
            fontsize=8,
            fontweight="bold"
        )

    ax.set_title(title)

    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.set_zlabel("Z Coordinate")

    ax.set_box_aspect((1, 1, 1))

    plt.tight_layout()
    plt.show()


def plot_energy_history(energy_history, title="Energy Convergence"):

    plt.figure(figsize=(9, 5))

    plt.plot(
        range(1, len(energy_history) + 1),
        energy_history
    )

    plt.title(title)
    plt.xlabel("Iteration")
    plt.ylabel("Protein Energy")

    plt.grid(True)
    plt.tight_layout()
    plt.show()
