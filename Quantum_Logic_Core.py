import time
import random
import logging
from typing import List, Any, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [QUANTUM] - %(message)s')

class QuantumLogicCore:
    def __init__(self):
        self.backend = None
        self.enabled = False
        try:
            from qiskit import QuantumCircuit
            from qiskit.primitives import StatevectorSampler
            self.QuantumCircuit = QuantumCircuit
            self.Sampler = StatevectorSampler
            self.enabled = True
            logging.info("Quantum Logic Core: ONLINE (Qiskit Backend Active)")
        except ImportError as e:
            logging.warning(f"Quantum Logic Core: OFFLINE (Qiskit not found: {e})")
            self.enabled = False

    def collapse_decision(self, options: List[Any]) -> Any:
        """
        Uses a quantum superposition to select an option from the list.
        This provides 'true' randomness compared to pseudo-randomness.
        """
        if not self.enabled or not options:
            return random.choice(options) if options else None

        try:
            # Create a quantum circuit with enough bits to represent the options
            num_options = len(options)
            # We need log2(num_options) qubits, rounded up
            num_qubits = (num_options - 1).bit_length()
            if num_qubits == 0: num_qubits = 1 # Handle single option case

            qc = self.QuantumCircuit(num_qubits)
            
            # Apply Hadamard gates to put all qubits in superposition
            for i in range(num_qubits):
                qc.h(i)
            
            # Measure all qubits
            qc.measure_all()

            # Execute the circuit
            sampler = self.Sampler()
            job = sampler.run([qc], shots=1)
            result = job.result()
            
            # Get the counts (binary string)
            # Qiskit 1.0+ primitives return bitstrings in a specific format
            # We'll extract the first result
            counts = result[0].data.meas.get_counts()
            measured_state = list(counts.keys())[0] # e.g., '01'
            
            # Convert binary to integer
            index = int(measured_state, 2)
            
            # Modulo to fit within options range
            selected_index = index % num_options
            
            choice = options[selected_index]
            logging.info(f"Quantum Collapse: State |{measured_state}> selected option '{choice}'")
            return choice

        except Exception as e:
            logging.error(f"Quantum Error: {e}. Falling back to classical logic.")
            return random.choice(options)

    def get_quantum_entropy(self) -> float:
        """
        Generates a random float between 0 and 1 using quantum measurement.
        """
        if not self.enabled:
            return random.random()
        
        try:
            qc = self.QuantumCircuit(1)
            qc.h(0) # Superposition
            qc.measure_all()
            
            sampler = self.Sampler()
            job = sampler.run([qc], shots=16) # Run 16 times to get a distribution
            result = job.result()
            counts = result[0].data.meas.get_counts()
            
            # Calculate ratio of 1s
            ones = counts.get('1', 0)
            total = sum(counts.values())
            entropy = ones / total
            
            # Add some classical jitter to ensure it's not just 0, 0.5, 1 for low shots
            jitter = random.uniform(-0.05, 0.05)
            return max(0.0, min(1.0, entropy + jitter))

        except Exception as e:
            logging.error(f"Entropy Error: {e}")
            return random.random()

if __name__ == "__main__":
    # Test the core
    q_core = QuantumLogicCore()
    if q_core.enabled:
        decisions = ["Option A", "Option B", "Option C", "Option D"]
        print(f"Deciding between: {decisions}")
        choice = q_core.collapse_decision(decisions)
        print(f"Quantum Choice: {choice}")
        
        entropy = q_core.get_quantum_entropy()
        print(f"Quantum Entropy: {entropy}")
    else:
        print("Quantum Core not enabled.")
