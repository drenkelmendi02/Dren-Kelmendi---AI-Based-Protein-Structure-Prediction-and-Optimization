
export default function EnergyChart({ energyHistory = [] }) {

    if (energyHistory.length === 0) {
        return null;
    }

    const width = 800;
    const height = 300;
    const padding = 40;

    const minEnergy = Math.min(...energyHistory);
    const maxEnergy = Math.max(...energyHistory);

    const range = maxEnergy - minEnergy || 1;

    const points = energyHistory.map((energy, index) => {
        const x = padding +
            (index / Math.max(energyHistory.length - 1, 1)) *
            (width - 2 * padding);

        const y = height - padding -
            ((energy - minEnergy) / range) *
            (height - 2 * padding);

        return `${x},${y}`;
    }).join(" ");

    return (
        <div className="energy-chart">

            <h2>Energy Convergence</h2>

            <svg
                viewBox={`0 0 ${width} ${height}`}
                width="100%"
                role="img"
                aria-label="Energy history during Simulated Annealing"
            >
                <line
                    x1={padding}
                    y1={padding}
                    x2={padding}
                    y2={height - padding}
                    stroke="#94a3b8"
                />

                <line
                    x1={padding}
                    y1={height - padding}
                    x2={width - padding}
                    y2={height - padding}
                    stroke="#94a3b8"
                />

                <polyline
                    points={points}
                    fill="none"
                    stroke="#38bdf8"
                    strokeWidth="2.5"
                    strokeLinejoin="round"
                    strokeLinecap="round"
                />

                <text
                    x={width / 2}
                    y={height - 5}
                    textAnchor="middle"
                    fill="#94a3b8"
                    fontSize="13"
                >
                    Iterations
                </text>

                <text
                    x={15}
                    y={height / 2}
                    textAnchor="middle"
                    fill="#94a3b8"
                    fontSize="13"
                    transform={`rotate(-90 15 ${height / 2})`}
                >
                    Energy
                </text>
            </svg>

            <p>
                Initial Energy: {energyHistory[0]}
            </p>

            <p>
                Final Energy: {energyHistory[energyHistory.length - 1]}
            </p>

        </div>
    );
}
