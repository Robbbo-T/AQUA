#!/usr/bin/env python3
"""
Quantum Simulator [152]
Classical simulation of quantum circuits for AQUA OS
Used when quantum hardware is not available
"""

import numpy as np
import cmath
from typing import Dict, List, Tuple, Optional
import logging
import time

class QuantumSimulator:
    """
    Classical simulation of quantum circuits
    Supports up to ~20 qubits on classical hardware
    """
    
    def __init__(self, max_qubits: int = 20):
        self.max_qubits = max_qubits
        self.logger = logging.getLogger("quantum_simulator")
        
        # Gate matrices
        self.gates = self._initialize_gate_matrices()
        
        self.logger.info(f"Quantum Simulator initialized (max {max_qubits} qubits)")
    
    def _initialize_gate_matrices(self) -> Dict[str, np.ndarray]:
        """Initialize quantum gate matrices"""
        return {
            'I': np.array([[1, 0], [0, 1]], dtype=complex),
            'X': np.array([[0, 1], [1, 0]], dtype=complex),
            'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
            'Z': np.array([[1, 0], [0, -1]], dtype=complex),
            'H': np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2),
            'S': np.array([[1, 0], [0, 1j]], dtype=complex),
            'T': np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex),
            'CNOT': np.array([
                [1, 0, 0, 0],
                [0, 1, 0, 0], 
                [0, 0, 0, 1],
                [0, 0, 1, 0]
            ], dtype=complex)
        }
    
    def execute(self, circuit, shots: int = 1024) -> Dict[str, int]:
        """Execute quantum circuit and return measurement counts"""
        if circuit.num_qubits > self.max_qubits:
            raise ValueError(f"Circuit too large: {circuit.num_qubits} > {self.max_qubits}")
        
        start_time = time.time()
        
        # Initialize state vector (|00...0⟩)
        n_states = 2 ** circuit.num_qubits
        state_vector = np.zeros(n_states, dtype=complex)
        state_vector[0] = 1.0
        
        # Apply gates
        for gate_type, qubits, params in circuit.gates:
            state_vector = self._apply_gate(state_vector, gate_type, qubits, params, circuit.num_qubits)
        
        # Simulate measurements
        probabilities = np.abs(state_vector) ** 2
        
        # Sample measurements
        measurements = np.random.choice(n_states, size=shots, p=probabilities)
        
        # Convert to bit strings and count
        counts = {}
        for measurement in measurements:
            bit_string = format(measurement, f'0{circuit.num_qubits}b')
            counts[bit_string] = counts.get(bit_string, 0) + 1
        
        execution_time = time.time() - start_time
        self.logger.debug(f"Simulated {circuit.circuit_id} in {execution_time:.3f}s")
        
        return counts
    
    def _apply_gate(self, state_vector: np.ndarray, gate_type, qubits: List[int], 
                   params: List[float], total_qubits: int) -> np.ndarray:
        """Apply quantum gate to state vector"""
        
        if gate_type.value in ['X', 'Y', 'Z', 'H', 'S', 'T']:
            # Single qubit gates
            qubit = qubits[0]
            gate_matrix = self.gates[gate_type.value]
            return self._apply_single_qubit_gate(state_vector, gate_matrix, qubit, total_qubits)
            
        elif gate_type.value in ['RX', 'RY', 'RZ']:
            # Parameterized single qubit gates
            qubit = qubits[0]
            angle = params[0] if params else 0
            gate_matrix = self._get_rotation_matrix(gate_type.value, angle)
            return self._apply_single_qubit_gate(state_vector, gate_matrix, qubit, total_qubits)
            
        elif gate_type.value == 'CNOT':
            # Two qubit CNOT gate
            control, target = qubits[0], qubits[1]
            return self._apply_cnot_gate(state_vector, control, target, total_qubits)
            
        else:
            self.logger.warning(f"Gate {gate_type.value} not implemented in simulator")
            return state_vector
    
    def _get_rotation_matrix(self, gate_type: str, angle: float) -> np.ndarray:
        """Get rotation gate matrix"""
        if gate_type == 'RX':
            return np.array([
                [np.cos(angle/2), -1j*np.sin(angle/2)],
                [-1j*np.sin(angle/2), np.cos(angle/2)]
            ], dtype=complex)
        elif gate_type == 'RY':
            return np.array([
                [np.cos(angle/2), -np.sin(angle/2)],
                [np.sin(angle/2), np.cos(angle/2)]
            ], dtype=complex)
        elif gate_type == 'RZ':
            return np.array([
                [np.exp(-1j*angle/2), 0],
                [0, np.exp(1j*angle/2)]
            ], dtype=complex)
        else:
            return self.gates['I']
    
    def _apply_single_qubit_gate(self, state_vector: np.ndarray, gate_matrix: np.ndarray,
                                qubit: int, total_qubits: int) -> np.ndarray:
        """Apply single qubit gate to state vector"""
        n_states = len(state_vector)
        new_state = np.zeros_like(state_vector)
        
        for i in range(n_states):
            # Extract qubit value
            qubit_value = (i >> qubit) & 1
            
            # Apply gate
            for new_qubit_value in [0, 1]:
                amplitude = gate_matrix[new_qubit_value, qubit_value]
                if abs(amplitude) > 1e-10:  # Avoid numerical errors
                    # Calculate new state index
                    new_i = i ^ (qubit_value << qubit) ^ (new_qubit_value << qubit)
                    new_state[new_i] += amplitude * state_vector[i]
        
        return new_state
    
    def _apply_cnot_gate(self, state_vector: np.ndarray, control: int, target: int, 
                        total_qubits: int) -> np.ndarray:
        """Apply CNOT gate to state vector"""
        n_states = len(state_vector)
        new_state = np.copy(state_vector)
        
        for i in range(n_states):
            control_bit = (i >> control) & 1
            target_bit = (i >> target) & 1
            
            if control_bit == 1:  # Apply X gate to target
                # Flip target bit
                new_i = i ^ (1 << target)
                new_state[new_i] = state_vector[i]
                new_state[i] = 0
        
        return new_state
    
    def get_state_vector(self, circuit) -> np.ndarray:
        """Get final state vector without measurement"""
        if circuit.num_qubits > self.max_qubits:
            raise ValueError(f"Circuit too large: {circuit.num_qubits} > {self.max_qubits}")
        
        # Initialize state vector
        n_states = 2 ** circuit.num_qubits
        state_vector = np.zeros(n_states, dtype=complex)
        state_vector[0] = 1.0
        
        # Apply gates (without measurements)
        for gate_type, qubits, params in circuit.gates:
            state_vector = self._apply_gate(state_vector, gate_type, qubits, params, circuit.num_qubits)
        
        return state_vector
    
    def calculate_expectation_value(self, circuit, observable: np.ndarray) -> float:
        """Calculate expectation value of observable"""
        state_vector = self.get_state_vector(circuit)
        
        # Calculate ⟨ψ|O|ψ⟩
        expectation = np.real(np.conj(state_vector).T @ observable @ state_vector)
        
        return expectation
    
    def get_fidelity(self, circuit, target_state: np.ndarray) -> float:
        """Calculate fidelity with target state"""
        actual_state = self.get_state_vector(circuit)
        
        # Calculate |⟨ψ_target|ψ_actual⟩|²
        overlap = np.abs(np.vdot(target_state, actual_state)) ** 2
        
        return overlap

# Quantum noise models for realistic simulation
class NoiseModel:
    """Quantum noise model for realistic simulation"""
    
    def __init__(self, error_rate: float = 0.01):
        self.error_rate = error_rate
        self.gate_errors = {
            'single_qubit': error_rate,
            'two_qubit': error_rate * 2,
            'measurement': error_rate * 0.5
        }
    
    def apply_noise(self, state_vector: np.ndarray, gate_type: str) -> np.ndarray:
        """Apply noise to state vector based on gate type"""
        if gate_type in ['X', 'Y', 'Z', 'H', 'S', 'T', 'RX', 'RY', 'RZ']:
            error_prob = self.gate_errors['single_qubit']
        elif gate_type in ['CNOT', 'CZ']:
            error_prob = self.gate_errors['two_qubit']
        else:
            error_prob = 0
        
        # Apply depolarizing noise (simplified)
        if np.random.random() < error_prob:
            # Add small random noise
            noise = np.random.normal(0, 0.01, len(state_vector)) + \
                   1j * np.random.normal(0, 0.01, len(state_vector))
            state_vector += noise
            
            # Renormalize
            norm = np.linalg.norm(state_vector)
            if norm > 0:
                state_vector /= norm
        
        return state_vector

# Export for use by quantum algorithms
def create_quantum_simulator(max_qubits: int = 20, noise: bool = False) -> QuantumSimulator:
    """Factory function for quantum simulator"""
    simulator = QuantumSimulator(max_qubits)
    
    if noise:
        simulator.noise_model = NoiseModel()
    
    return simulator

if __name__ == "__main__":
    # Test the simulator
    from quantum_algorithms import QuantumCircuit, GateType
    
    simulator = create_quantum_simulator()
    
    # Create simple test circuit
    circuit = QuantumCircuit(
        num_qubits=2,
        num_classical_bits=2,
        gates=[
            (GateType.HADAMARD, [0], []),
            (GateType.CNOT, [0, 1], [])
        ],
        measurements=[(0, 0), (1, 1)],
        circuit_id="bell_state_test",
        depth=2
    )
    
    # Execute circuit
    counts = simulator.execute(circuit)
    print(f"Bell state measurement counts: {counts}")
    
    # Check fidelity
    bell_state = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
    fidelity = simulator.get_fidelity(circuit, bell_state)
    print(f"Bell state fidelity: {fidelity:.3f}")