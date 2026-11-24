
import { useState } from "react";

import ProteinViewer from "./components/ProteinViewer";
import EnergyChart from "./components/EnergyChart";

import "./App.css";


function App() {
    const [sequence, setSequence] = useState("ACDEFGHIKL");

    const [results, setResults] = useState(null);

    const [selectedAlgorithm, setSelectedAlgorithm] = useState(
        "simulated_annealing"
    );

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const optimizeProtein = async () => {
        setLoading(true);
        setError("");
        setResults(null);

        try {
            const response = await fetch(
                "http://127.0.0.1:8000/optimize",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        sequence: sequence,
                        iterations: 1000,
                        initial_temperature: 10,
                        cooling_rate: 0.995,
                        population_size: 30,
                        generations: 100,
                        mutation_rate: 0.3,
                        crossover_rate: 0.8
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.detail || "Optimization failed."
                );
            }

            setResults(data);
            setSelectedAlgorithm("simulated_annealing");

        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const selectedResult = results?.algorithms?.[selectedAlgorithm];

    const saResult = results?.algorithms?.simulated_annealing;
    const gaResult = results?.algorithms?.genetic_algorithm;

    const comparison = results?.comparison;

    return (
        <div className="app-container">

            {/* HEADER */}
            <header className="app-header">
                <div>
                    <h1>AI-Based Protein Structure Prediction</h1>

                    <p>
                        3D Protein Folding and Optimization
                        using Artificial Intelligence
                    </p>
                </div>
            </header>


            {/* INPUT SECTION */}
            <section className="input-section">

                <h2>Protein Sequence</h2>

                <p>
                    Enter an amino acid sequence to optimize
                    its 3D structure using two algorithms.
                </p>

                <input
                    type="text"
                    value={sequence}
                    onChange={(event) =>
                        setSequence(event.target.value.toUpperCase())
                    }
                    placeholder="Enter protein sequence..."
                    className="sequence-input"
                />

                <button
                    onClick={optimizeProtein}
                    disabled={loading || !sequence.trim()}
                    className="optimize-button"
                >
                    {loading ? "Optimizing..." : "Optimize Protein"}
                </button>

                {error && (
                    <p className="error-message">
                        {error}
                    </p>
                )}

            </section>


            {/* LOADING */}
            {loading && (
                <div className="loading-section">
                    <p>
                        Running Simulated Annealing and
                        Genetic Algorithm...
                    </p>
                </div>
            )}


            {/* RESULTS */}
            {results && (
                <>

                    {/* PROTEIN INFORMATION */}
                    <section className="results-section">

                        <h2>Protein Information</h2>

                        <div className="info-grid">

                            <div className="info-card">
                                <span>Original Sequence</span>
                                <strong>{results.sequence}</strong>
                            </div>

                            <div className="info-card">
                                <span>HP Representation</span>
                                <strong>{results.hp_sequence}</strong>
                            </div>

                            <div className="info-card">
                                <span>Protein Length</span>
                                <strong>{results.sequence.length}</strong>
                            </div>

                        </div>

                    </section>


                    {/* ALGORITHM SELECTION */}
                    <section className="results-section">

                        <h2>Algorithm Results</h2>

                        <div className="algorithm-tabs">

                            <button
                                className={
                                    selectedAlgorithm === "simulated_annealing"
                                        ? "algorithm-tab active"
                                        : "algorithm-tab"
                                }
                                onClick={() =>
                                    setSelectedAlgorithm("simulated_annealing")
                                }
                            >
                                Simulated Annealing
                            </button>

                            <button
                                className={
                                    selectedAlgorithm === "genetic_algorithm"
                                        ? "algorithm-tab active"
                                        : "algorithm-tab"
                                }
                                onClick={() =>
                                    setSelectedAlgorithm("genetic_algorithm")
                                }
                            >
                                Genetic Algorithm
                            </button>

                        </div>


                        {selectedResult && (
                            <>

                                {/* ENERGY AND PERFORMANCE */}
                                <div className="info-grid">

                                    <div className="info-card">
                                        <span>Best Energy</span>
                                        <strong>{selectedResult.energy}</strong>
                                    </div>

                                    <div className="info-card">
                                        <span>Execution Time</span>
                                        <strong>
                                            {selectedResult.execution_time.toFixed(4)} s
                                        </strong>
                                    </div>

                                    <div className="info-card">
                                        <span>Peak Memory</span>
                                        <strong>
                                            {selectedResult.peak_memory_mb.toFixed(4)} MB
                                        </strong>
                                    </div>

                                    <div className="info-card">
                                        <span>Valid Structure</span>
                                        <strong>
                                            {selectedResult.is_valid ? "Yes" : "No"}
                                        </strong>
                                    </div>

                                </div>


                                {/* ALGORITHM DETAILS */}
                                <div className="algorithm-details">

                                    <h3>
                                        {selectedAlgorithm === "simulated_annealing"
                                            ? "Simulated Annealing Details"
                                            : "Genetic Algorithm Details"}
                                    </h3>

                                    {selectedAlgorithm === "simulated_annealing" ? (

                                        <p>
                                            Iterations: {selectedResult.iterations}
                                        </p>

                                    ) : (

                                        <>
                                            <p>
                                                Generations: {selectedResult.generations}
                                            </p>

                                            <div className="info-grid">

                                                <div className="info-card">
                                                    <span>Candidate Configurations</span>
                                                    <strong>
                                                        {selectedResult.statistics.candidate_configurations}
                                                    </strong>
                                                </div>

                                                <div className="info-card">
                                                    <span>Valid Structures</span>
                                                    <strong>
                                                        {selectedResult.statistics.valid_structures}
                                                    </strong>
                                                </div>

                                                <div className="info-card">
                                                    <span>Invalid Structures</span>
                                                    <strong>
                                                        {selectedResult.statistics.invalid_structures}
                                                    </strong>
                                                </div>

                                                <div className="info-card">
                                                    <span>Duplicate Structures</span>
                                                    <strong>
                                                        {selectedResult.statistics.duplicate_structures}
                                                    </strong>
                                                </div>

                                                <div className="info-card">
                                                    <span>Unique Structures</span>
                                                    <strong>
                                                        {selectedResult.statistics.unique_structures}
                                                    </strong>
                                                </div>

                                                <div className="info-card">
                                                    <span>Energy Evaluations</span>
                                                    <strong>
                                                        {selectedResult.statistics.energy_evaluations}
                                                    </strong>
                                                </div>

                                                <div className="info-card">
                                                    <span>Elimination Percentage</span>
                                                    <strong>
                                                        {selectedResult.statistics.elimination_percentage.toFixed(2)}%
                                                    </strong>
                                                </div>

                                            </div>
                                        </>

                                    )}

                                </div>


                                {/* 3D PROTEIN VIEWER */}
                                <section className="visualization-section">

                                    <h2>3D Protein Structure</h2>

                                    <p>
                                        Red spheres represent hydrophobic (H)
                                        amino acids, while blue spheres
                                        represent polar (P) amino acids.
                                    </p>

                                    <div className="protein-viewer-container">

                                        <ProteinViewer
                                            coordinates={selectedResult.coordinates}
                                            hpSequence={results.hp_sequence}
                                        />

                                    </div>

                                </section>


                                {/* ENERGY CHART */}
                                <section className="visualization-section">

                                    <h2>Energy Convergence</h2>

                                    <EnergyChart
                                        energyHistory={selectedResult.energy_history}
                                    />

                                </section>

                            </>
                        )}

                    </section>


                    {/* ALGORITHM COMPARISON */}
                    <section className="results-section">

                        <h2>Algorithm Comparison</h2>

                        <div className="comparison-grid">

                            <div className="comparison-card">

                                <h3>Simulated Annealing</h3>

                                <p>
                                    Best Energy:
                                    <strong> {saResult.energy}</strong>
                                </p>

                                <p>
                                    Execution Time:
                                    <strong>
                                        {" "}
                                        {saResult.execution_time.toFixed(4)} s
                                    </strong>
                                </p>

                                <p>
                                    Memory:
                                    <strong>
                                        {" "}
                                        {saResult.peak_memory_mb.toFixed(4)} MB
                                    </strong>
                                </p>

                            </div>


                            <div className="comparison-card">

                                <h3>Genetic Algorithm</h3>

                                <p>
                                    Best Energy:
                                    <strong> {gaResult.energy}</strong>
                                </p>

                                <p>
                                    Execution Time:
                                    <strong>
                                        {" "}
                                        {gaResult.execution_time.toFixed(4)} s
                                    </strong>
                                </p>

                                <p>
                                    Memory:
                                    <strong>
                                        {" "}
                                        {gaResult.peak_memory_mb.toFixed(4)} MB
                                    </strong>
                                </p>

                            </div>

                        </div>


                        <div className="comparison-summary">

                            <h3>Comparison Summary</h3>

                            <p>
                                Best Energy:
                                <strong> {comparison.best_energy}</strong>
                            </p>

                            <p>
                                Faster Algorithm:
                                <strong> {comparison.faster_algorithm}</strong>
                            </p>

                            <p>
                                Lower Memory Usage:
                                <strong> {comparison.lower_memory_usage}</strong>
                            </p>

                        </div>

                    </section>

                </>
            )}


            {/* FOOTER */}
            <footer className="app-footer">
                <p>
                    AI-Based Protein Structure Prediction and Optimization
                </p>
                <span>3D HP Lattice Model | Simulated Annealing | Genetic Algorithm</span>
            </footer>

        </div>
    );
}

export default App;
