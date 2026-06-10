from fastapi import APIRouter, HTTPException

from app.models.quantum_amplitude_request import QuantumAmplitudeRequest
from app.models.quantum_amplitude_response import QuantumAmplitudeResponse
from app.models.quantum_interference_request import QuantumInterferenceRequest
from app.models.quantum_interference_response import QuantumInterferenceResponse
from app.models.quantum_qasm_request import QuantumQasmRequest
from app.models.quantum_qasm_response import QuantumQasmResponse
from app.services.quantum_amplitude_simulator import QuantumAmplitudeSimulator
from app.services.quantum_interference_simulator import QuantumInterferenceSimulator
from app.services.openqasm_generator import OpenQasmGenerator
from app.models.qiskit_circuit_response import QiskitCircuitResponse
from app.services.qiskit_research_service import QiskitResearchService

router = APIRouter(
    prefix="/quantum",
    tags=["Quantum Support"]
)

amplitude_simulator = QuantumAmplitudeSimulator()

interference_simulator = QuantumInterferenceSimulator()

openqasm_generator = OpenQasmGenerator()
qiskit_research_service = QiskitResearchService()


@router.post(
    "/amplitude-simulate",
    response_model=QuantumAmplitudeResponse
)
def simulate_amplitude(
        request: QuantumAmplitudeRequest
):

    try:

        result = amplitude_simulator.simulate_amplitude(
            file_path=request.filePath,
            selected_column=request.selectedColumn,
            sample_size=request.sampleSize,
            candidate_count=request.candidateCount,
            learning_rate=request.learningRate
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post(
    "/interference-simulate",
    response_model=QuantumInterferenceResponse
)
def simulate_interference(
        request: QuantumInterferenceRequest
):

    try:

        result = interference_simulator.simulate_interference(
            file_path=request.filePath,
            selected_column=request.selectedColumn,
            sample_size=request.sampleSize,
            candidate_count=request.candidateCount,
            learning_rate=request.learningRate,
            reinforcement_strength=request.reinforcementStrength,
            suppression_strength=request.suppressionStrength
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post(
    "/generate-qasm",
    response_model=QuantumQasmResponse
)
def generate_qasm(
        request: QuantumQasmRequest
):

    try:

        result = openqasm_generator.generate_qasm(
            file_path=request.filePath,
            selected_column=request.selectedColumn,
            sample_size=request.sampleSize,
            candidate_count=request.candidateCount,
            learning_rate=request.learningRate
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.post(
    "/qiskit-circuit",
    response_model=QiskitCircuitResponse
)
def generate_qiskit_circuit(
        request: QuantumQasmRequest
):

    try:

        result = qiskit_research_service.generate_qiskit_circuit(
            file_path=request.filePath,
            selected_column=request.selectedColumn,
            sample_size=request.sampleSize,
            candidate_count=request.candidateCount,
            learning_rate=request.learningRate
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )   