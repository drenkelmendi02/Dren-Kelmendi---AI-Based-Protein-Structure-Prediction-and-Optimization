
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from protein.representation.sequence import validate_sequence
from protein.representation.hp_model import convert_to_hp
from protein.representation.structure import ProteinStructure
from protein.representation.constraints import is_valid_structure

from algorithms.simulated_annealing import simulated_annealing
from evaluation.metrics import measure_performance


app = FastAPI(
    title="Protein Structure Optimization API",
    description="3D Protein Folding using Simulated Annealing",
    version="1.0.0"
)


# React Frontend Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Request Model
class ProteinRequest(BaseModel):
    sequence: str
    iterations: int = Field(default=1000, ge=1, le=100000)
    initial_temperature: float = Field(default=10.0, gt=0)
    cooling_rate: float = Field(default=0.995, gt=0, le=1)


# API Home
@app.get("/")
def home():
    return {
        "message": "Protein Structure Optimization API is running"
    }


# Protein Optimization
@app.post("/optimize")
def optimize_protein(request: ProteinRequest):

    try:
        sequence = validate_sequence(request.sequence)

        hp_sequence = convert_to_hp(sequence)

        initial_structure = ProteinStructure(hp_sequence)

        result, performance = measure_performance(
            simulated_annealing,
            initial_structure,
            initial_temperature=request.initial_temperature,
            cooling_rate=request.cooling_rate,
            iterations=request.iterations
        )

        best_structure, best_energy, energy_history = result

        if not is_valid_structure(best_structure):
            raise HTTPException(
                status_code=500,
                detail="Optimization produced an invalid structure"
            )

        return {
            "sequence": sequence,
            "hp_sequence": hp_sequence,

            "coordinates": [
                {
                    "x": x,
                    "y": y,
                    "z": z
                }
                for x, y, z in best_structure.coordinates
            ],

            "energy": best_energy,
            "energy_history": energy_history,
            "iterations": len(energy_history),

            "is_valid": is_valid_structure(best_structure),

            "execution_time": performance["execution_time"],
            "peak_memory_mb": performance["peak_memory_mb"]
        }

    except (TypeError, ValueError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
