
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from protein.representation.sequence import validate_sequence
from protein.representation.hp_model import convert_to_hp
from protein.representation.structure import ProteinStructure
from protein.representation.constraints import is_valid_structure

from algorithms.simulated_annealing import simulated_annealing
from algorithms.genetic_algorithm import genetic_algorithm

from evaluation.metrics import measure_performance


app = FastAPI(
    title="AI-Based Protein Structure Prediction and Optimization",
    description="3D Protein Folding using Simulated Annealing and Genetic Algorithm",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class ProteinRequest(BaseModel):
    sequence: str

    # Simulated Annealing
    iterations: int = Field(default=1000, ge=1, le=100000)
    initial_temperature: float = Field(default=10.0, gt=0)
    cooling_rate: float = Field(default=0.995, gt=0, le=1)

    # Genetic Algorithm
    population_size: int = Field(default=30, ge=2, le=500)
    generations: int = Field(default=100, ge=1, le=10000)
    mutation_rate: float = Field(default=0.3, ge=0, le=1)
    crossover_rate: float = Field(default=0.8, ge=0, le=1)


def format_coordinates(structure):
    return [
        {"x": x, "y": y, "z": z}
        for x, y, z in structure.coordinates
    ]


def format_algorithm_result(
    structure,
    energy,
    energy_history,
    performance,
    statistics
):
    return {
        "coordinates": format_coordinates(structure),
        "energy": energy,
        "energy_history": energy_history,
        "is_valid": is_valid_structure(structure),
        "execution_time": performance["execution_time"],
        "peak_memory_mb": performance["peak_memory_mb"],
        "statistics": statistics
    }


@app.get("/")
def home():
    return {
        "message": "Protein Structure Optimization API is running",
        "algorithms": [
            "Simulated Annealing",
            "Genetic Algorithm"
        ]
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/optimize")
def optimize_protein(request: ProteinRequest):

    try:
        # 1. Validimi i sekuencës.
        sequence = validate_sequence(request.sequence)

        # 2. Konvertimi në modelin HP.
        hp_sequence = convert_to_hp(sequence)

        # 3. Krijimi i strukturës fillestare.
        initial_structure = ProteinStructure(hp_sequence)

        if not is_valid_structure(initial_structure):
            raise ValueError("Initial protein structure is invalid.")

        # ==========================================
        # SIMULATED ANNEALING
        # ==========================================

        sa_result, sa_performance = measure_performance(
            simulated_annealing,
            initial_structure,
            initial_temperature=request.initial_temperature,
            cooling_rate=request.cooling_rate,
            iterations=request.iterations,
            return_stats=True
        )

        (
            sa_structure,
            sa_energy,
            sa_history,
            sa_statistics
        ) = sa_result

        sa_data = format_algorithm_result(
            sa_structure,
            sa_energy,
            sa_history,
            sa_performance,
            sa_statistics
        )

        sa_data["iterations"] = sa_statistics["iterations_completed"]

        # ==========================================
        # GENETIC ALGORITHM
        # ==========================================

        ga_result, ga_performance = measure_performance(
            genetic_algorithm,
            initial_structure,
            population_size=request.population_size,
            generations=request.generations,
            mutation_rate=request.mutation_rate,
            crossover_rate=request.crossover_rate,
            return_stats=True
        )

        (
            ga_structure,
            ga_energy,
            ga_history,
            ga_statistics
        ) = ga_result

        ga_data = format_algorithm_result(
            ga_structure,
            ga_energy,
            ga_history,
            ga_performance,
            ga_statistics
        )

        ga_data["generations"] = len(ga_history) - 1

        # ==========================================
        # KRAHASIMI I ALGORITMEVE
        # ==========================================

        comparison = {
            "best_energy": (
                "Genetic Algorithm"
                if ga_energy < sa_energy
                else "Simulated Annealing"
                if sa_energy < ga_energy
                else "Equal"
            ),

            "faster_algorithm": (
                "Simulated Annealing"
                if sa_performance["execution_time"]
                < ga_performance["execution_time"]
                else "Genetic Algorithm"
            ),

            "lower_memory_usage": (
                "Simulated Annealing"
                if sa_performance["peak_memory_mb"]
                < ga_performance["peak_memory_mb"]
                else "Genetic Algorithm"
            )
        }

        # ==========================================
        # RESPONSE
        # ==========================================

        return {
            "sequence": sequence,
            "hp_sequence": hp_sequence,

            # Rezultatet kryesore të SA për frontend-in aktual.
            "coordinates": sa_data["coordinates"],
            "energy": sa_data["energy"],
            "energy_history": sa_data["energy_history"],
            "iterations": sa_data["iterations"],
            "is_valid": sa_data["is_valid"],
            "execution_time": sa_data["execution_time"],
            "peak_memory_mb": sa_data["peak_memory_mb"],

            # Rezultatet e të dy algoritmeve.
            "algorithms": {
                "simulated_annealing": sa_data,
                "genetic_algorithm": ga_data
            },

            # Krahasimi automatik.
            "comparison": comparison
        }

    except (ValueError, TypeError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Optimization error: {str(error)}"
        )
