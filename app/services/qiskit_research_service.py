from typing import Any, Dict

from qiskit import QuantumCircuit

from app.services.openqasm_generator import OpenQasmGenerator

try:
    from qiskit import qasm2
except Exception:
    qasm2 = None


class QiskitResearchService:

    def __init__(self):
        self.openqasm_generator = OpenQasmGenerator()

    def generate_qiskit_circuit(
            self,
            file_path: str,
            selected_column: str,
            sample_size: int = 100000,
            candidate_count: int = 5,
            learning_rate: float = 0.1
    ) -> Dict[str, Any]:

        qasm_result = self.openqasm_generator.generate_qasm(
            file_path=file_path,
            selected_column=selected_column,
            sample_size=sample_size,
            candidate_count=candidate_count,
            learning_rate=learning_rate
        )

        candidates = qasm_result["candidates"]

        qubit_count = qasm_result["qubitCount"]

        circuit = QuantumCircuit(
            qubit_count,
            qubit_count
        )

        for index in range(qubit_count):
            circuit.h(index)

        for candidate in candidates:
            circuit.ry(
                candidate["rotationAngle"],
                candidate["candidateIndex"]
            )

        for index in range(qubit_count - 1):
            circuit.cx(
                index,
                index + 1
            )

        circuit.measure(
            range(qubit_count),
            range(qubit_count)
        )

        open_qasm = self._extract_openqasm(
            circuit=circuit,
            fallback_qasm=qasm_result["openQasm"]
        )

        return {
            "rowCount": qasm_result["rowCount"],
            "sampleSizeUsed": qasm_result["sampleSizeUsed"],
            "selectedColumn": qasm_result["selectedColumn"],

            "qubitCount": circuit.num_qubits,
            "classicalBitCount": circuit.num_clbits,
            "circuitDepth": circuit.depth(),

            "selectedPivotIndex": qasm_result["selectedPivotIndex"],
            "selectedPivotValue": qasm_result["selectedPivotValue"],
            "bestPartitionImbalance": qasm_result["bestPartitionImbalance"],

            "qiskitCircuitText": str(circuit),
            "openQasm": open_qasm,

            "candidates": candidates,

            "explanation": (
                "This endpoint uses real Qiskit QuantumCircuit. "
                "Each qubit represents one AAQ pivot candidate. "
                "H gates represent superposition-inspired candidate space. "
                "RY gates encode amplitude-weighted pivot probability. "
                "CX gates represent entanglement-inspired neighbor correlation."
            )
        }

    def _extract_openqasm(
            self,
            circuit: QuantumCircuit,
            fallback_qasm: str
    ) -> str:

        if qasm2 is not None:
            try:
                return qasm2.dumps(circuit)
            except Exception:
                pass

        try:
            return circuit.qasm()
        except Exception:
            return fallback_qasm