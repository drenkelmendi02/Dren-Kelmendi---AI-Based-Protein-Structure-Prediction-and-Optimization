
import { useState } from "react";
import ProteinViewer from "./components/ProteinViewer";
import EnergyChart from "./components/EnergyChart";
import "./App.css";
function App() {
    const [sequence, setSequence] = useState("ACDEFGHIKL");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const optimizeProtein = async () => {
        setLoading(true);
        setError("");
        setResult(null);

        try {
            const response = await fetch("http://127.0.0.1:8000/optimize", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    sequence: sequence,
                    iterations: 1000,
                    initial_temperature: 10.0,
                    cooling_rate: 0.995
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Optimization failed");
            }

            setResult(data);

        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app">

            <header>
                <h1>AI-Based Protein Structure Prediction</h1>
                <p>3D Protein Folding and Optimization using Simulated Annealing</p>
            </header>

            <main>

                <section className="input-section">
                    <h2>Protein Sequence</h2>

                    <input
                        type="text"
                        value={sequence}
                        onChange={(e) => setSequence(e.target.value.toUpperCase())}
                        placeholder="Enter amino acid sequence"
                    />

                    <button
                        onClick={optimizeProtein}
                        disabled={loading || !sequence.trim()}
                    >
                        {loading ? "Optimizing..." : "Optimize Protein"}
                    </button>

                    {error && (
                        <p className="error">{error}</p>
                    )}
                </section>

                {result && (
                    <>
                        <section className="results-section">
                            <h2>Optimization Results</h2>

                            <div className="metrics">
                                <div className="metric">
                                    <h3>Energy</h3>
                                    <p>{result.energy}</p>
                                </div>

                                <div className="metric">
                                    <h3>Iterations</h3>
                                    <p>{result.iterations}</p>
                                </div>

                                <div className="metric">
                                    <h3>Execution Time</h3>
                                    <p>{result.execution_time.toFixed(4)} s</p>
                                </div>

                                <div className="metric">
                                    <h3>Memory</h3>
                                    <p>{result.peak_memory_mb.toFixed(4)} MB</p>
                                </div>
                            </div>

                            <p>
                                HP Sequence: <strong>{result.hp_sequence}</strong>
                            </p>

                            <p>
                                Valid Structure: <strong>{result.is_valid ? "Yes" : "No"}</strong>
                            </p>
                        </section>

                        <section className="viewer-section">
                            <h2>3D Protein Structure</h2>

                            <ProteinViewer
                                coordinates={result.coordinates}
                                hpSequence={result.hp_sequence}
                            />
                        </section>
                        <section className="results-section">
                        <EnergyChart
                        energyHistory={result.energy_history}
                        />
                          </section>
                    </>
                )}

            </main>
        </div>
    );
}

export default App;
