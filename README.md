# AI-Based Protein Structure Prediction and Optimization

## 1. Project Overview

This project implements an AI-based approach for protein structure prediction and optimization using a simplified three-dimensional Hydrophobic-Polar (HP) lattice model.

The main objective is to find protein configurations with lower energy by optimizing the spatial arrangement of amino acids.

Two optimization algorithms are implemented and compared:

- **Simulated Annealing (SA)**
- **Genetic Algorithm (GA)**

The project also provides a graphical interface for visualizing protein structures in 3D and comparing algorithm performance.

## 2. Objectives

- Represent protein sequences using the HP model.
- Generate valid three-dimensional protein structures.
- Implement Simulated Annealing and Genetic Algorithm.
- Minimize protein energy through hydrophobic interactions.
- Reduce the search space using structural validity checks and duplicate detection.
- Measure execution time and memory consumption.
- Compare the performance of both algorithms.
- Visualize optimized protein structures.

## 3. HP Model and Energy Function

The HP model classifies amino acids into two groups:

- **H (Hydrophobic):** Amino acids that tend to form contacts with other hydrophobic amino acids.
- **P (Polar):** Amino acids that are treated as polar residues.

The protein is represented as a chain on a three-dimensional cubic lattice.

The energy function is defined as:

**E(S) = -N(H-H)**

Where:

- E(S) represents the energy of a protein structure.
- N(H-H) represents the number of non-consecutive hydrophobic contacts.

The objective is to minimize the energy. Lower energy values indicate more hydrophobic contacts.

## 4. Implemented Algorithms

### 4.1 Simulated Annealing

Simulated Annealing is a probabilistic optimization algorithm inspired by the physical annealing process.

It explores neighboring protein configurations and accepts:
- Better solutions with lower energy.
- Some worse solutions according to a probability controlled by temperature.

As the temperature decreases, the probability of accepting worse solutions also decreases.

### 4.2 Genetic Algorithm

The Genetic Algorithm is inspired by natural selection and biological evolution.

It uses:
- Population initialization.
- Fitness evaluation.
- Tournament selection.
- Crossover.
- Mutation.
- Elitism.

The algorithm evolves a population of protein structures over multiple generations to find configurations with lower energy.

## 5. Technologies Used

**Backend**
- Python
- FastAPI

**Frontend**
- React
- JavaScript
- Three.js
- React Three Fiber
- React Three Drei
- CSS

**Evaluation**
- Python time measurement
- Memory profiling with tracemalloc
- CSV benchmark results
- Unit testing with unittest

## 6. Project Structure

```text
project/
├── algorithms/
│   ├── moves.py
│   ├── simulated_annealing.py
│   ├── genetic_algorithm.py
│   └── search_utils.py
├── backend/
│   └── app.py
├── evaluation/
│   ├── energy.py
│   └── metrics.py
├── experiments/
│   ├── benchmark.py
│   └── benchmark_results.csv
├── protein/
│   └── representation/
│       ├── sequence.py
│       ├── hp_model.py
│       ├── structure.py
│       └── constraints.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── index.html
├── tests/
│   ├── test_energy.py
│   ├── test_representation.py
│   ├── test_simulated_annealing.py
│   └── test_genetic_algorithm.py
├── main.py
├── requirements.txt
└── README.md
```

## 7. Installation

Clone the repository:

```bash
git clone <repository-url>
cd <project-folder>
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Install frontend dependencies:

```bash
cd frontend
npm install
```

## 8. Running the Project

### Start the Backend

From the project root directory:

```bash
uvicorn backend.app:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

### Start the Frontend

Open a second terminal:

```bash
cd frontend
npm run dev
```

Open the local URL displayed by Vite in your browser.

## 9. Running Experiments

From the project root:

```bash
python -m experiments.benchmark
```

The benchmark evaluates both algorithms using different protein sequence lengths and multiple runs.

The results are saved in:

```text
experiments/benchmark_results.csv
```

## 10. Running Tests

Run all unit tests from the project root:

```bash
python -m unittest discover -s tests -v
```

## 11. Performance Evaluation

The algorithms are evaluated using:

- Best energy achieved.
- Execution time.
- Peak memory consumption.
- Validity of generated structures.
- Number of candidate configurations.
- Number of valid, invalid and duplicate structures.

The experimental results are used to compare the optimization performance of Simulated Annealing and Genetic Algorithm.

## 12. Project Limitations

This project uses a simplified HP lattice model. It does not perform full atomistic protein structure prediction and does not model all physical and chemical interactions involved in real protein folding.

Its purpose is to demonstrate and compare optimization algorithms in a simplified protein-folding problem.

## 13. Conclusion

The project demonstrates how metaheuristic optimization algorithms can be applied to a simplified protein-folding problem.

By implementing Simulated Annealing and Genetic Algorithm, the project explores different search strategies and evaluates their effectiveness in finding low-energy protein configurations.