
function EnergyChart({ energyHistory = [] }) {

    if (!energyHistory || energyHistory.length === 0) {
        return (
            <div className="energy-chart">
                <p>No energy data available.</p>
            </div>
        );
    }

    const width = 900;
    const height = 350;

    const paddingLeft = 65;
    const paddingRight = 30;
    const paddingTop = 30;
    const paddingBottom = 55;

    const values = energyHistory.map(Number);

    const minEnergy = Math.min(...values);
    const maxEnergy = Math.max(...values);

    const energyRange = maxEnergy - minEnergy || 1;

    const chartWidth = width - paddingLeft - paddingRight;
    const chartHeight = height - paddingTop - paddingBottom;

    const points = values.map((energy, index) => {

        const x = paddingLeft +
            (index / Math.max(values.length - 1, 1)) * chartWidth;

        const y = paddingTop +
            ((maxEnergy - energy) / energyRange) * chartHeight;

        return {
            x,
            y,
            energy
        };
    });

    const polylinePoints = points
        .map(point => `${point.x},${point.y}`)
        .join(" ");

    const firstEnergy = values[0];
    const finalEnergy = values[values.length - 1];

    const improvement = firstEnergy - finalEnergy;

    const yLabels = Array.from(
        { length: 5 },
        (_, index) => maxEnergy - (energyRange * index) / 4
    );

    return (
        <div className="energy-chart">

            <div className="chart-header">
                <div>
                    <h3>Energy Convergence</h3>
                    <p>Energy changes during optimization</p>
                </div>
            </div>

            <svg
                viewBox={`0 0 ${width} ${height}`}
                role="img"
                aria-label="Energy convergence graph"
            >

                {/* Horizontal grid lines and Y labels */}
                {yLabels.map((value, index) => {

                    const y = paddingTop +
                        (index / 4) * chartHeight;

                    return (
                        <g key={index}>

                            <line
                                x1={paddingLeft}
                                y1={y}
                                x2={width - paddingRight}
                                y2={y}
                                stroke="#263449"
                                strokeDasharray="5 5"
                            />

                            <text
                                x={paddingLeft - 12}
                                y={y + 4}
                                textAnchor="end"
                            >
                                {value.toFixed(1)}
                            </text>

                        </g>
                    );
                })}

                {/* X and Y axes */}
                <line
                    x1={paddingLeft}
                    y1={paddingTop}
                    x2={paddingLeft}
                    y2={height - paddingBottom}
                    stroke="#64748b"
                />

                <line
                    x1={paddingLeft}
                    y1={height - paddingBottom}
                    x2={width - paddingRight}
                    y2={height - paddingBottom}
                    stroke="#64748b"
                />

                {/* Energy curve */}
                <polyline
                    points={polylinePoints}
                    fill="none"
                    stroke="#38bdf8"
                    strokeWidth="3"
                    strokeLinejoin="round"
                    strokeLinecap="round"
                />

                {/* Starting point */}
                <circle
                    cx={points[0].x}
                    cy={points[0].y}
                    r="5"
                    fill="#f59e0b"
                />

                {/* Final point */}
                <circle
                    cx={points[points.length - 1].x}
                    cy={points[points.length - 1].y}
                    r="6"
                    fill="#22c55e"
                />

                {/* X axis labels */}
                <text
                    x={paddingLeft}
                    y={height - 20}
                    textAnchor="start"
                >
                    0
                </text>

                <text
                    x={width - paddingRight}
                    y={height - 20}
                    textAnchor="end"
                >
                    {values.length - 1}
                </text>

                <text
                    x={width / 2}
                    y={height - 3}
                    textAnchor="middle"
                >
                    Iterations / Generations
                </text>

                <text
                    x="17"
                    y={height / 2}
                    textAnchor="middle"
                    transform={`rotate(-90 17 ${height / 2})`}
                >
                    Energy
                </text>

            </svg>

            {/* Chart statistics */}
            <div className="chart-statistics">

                <div>
                    <span>Initial Energy</span>
                    <strong>{firstEnergy}</strong>
                </div>

                <div>
                    <span>Best Energy</span>
                    <strong>{Math.min(...values)}</strong>
                </div>

                <div>
                    <span>Final Energy</span>
                    <strong>{finalEnergy}</strong>
                </div>

                <div>
                    <span>Improvement</span>
                    <strong>{improvement.toFixed(2)}</strong>
                </div>

            </div>

        </div>
    );
}

export default EnergyChart;
