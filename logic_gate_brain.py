"""
Logic Gate Brain System
A brain system built entirely from logic gates, simulating digital circuit computation.

Components:
- LogicGate: Base class for all logic gates
- AND, OR, NOT, NAND, NOR, XOR, XNOR gates
- LogicCircuit: Complex circuits built from gates
- LogicGateBrain: Brain system using logic gates
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
import time

# Import from actual comprehensive brain system
try:
    from comprehensive_brain_template import BrainRegion
    USING_REAL_BRAIN_SYSTEM = True
except ImportError:
    class BrainRegion:
        """Fallback brain region."""
        CORTEX = "cortex"
        HIPPOCAMPUS = "hippocampus"
    USING_REAL_BRAIN_SYSTEM = False


# =============================================================================
# LOGIC GATE BASE
# =============================================================================

@dataclass
class LogicGate:
    """Base class for logic gates."""
    id: str
    inputs: List[int] = field(default_factory=list)
    output: int = 0
    gate_type: str = "UNKNOWN"
    
    def compute(self) -> int:
        """Compute gate output (to be overridden)."""
        raise NotImplementedError
    
    def set_inputs(self, inputs: List[int]):
        """Set gate inputs."""
        self.inputs = [int(bool(x)) for x in inputs]
    
    def get_truth_table(self) -> List[Tuple[Tuple[int, ...], int]]:
        """Get truth table for the gate."""
        raise NotImplementedError


# =============================================================================
# BASIC LOGIC GATES
# =============================================================================

class ANDGate(LogicGate):
    """AND logic gate."""
    
    def __init__(self, id: str, num_inputs: int = 2):
        super().__init__(id, gate_type="AND")
        self.num_inputs = num_inputs
    
    def compute(self) -> int:
        """Compute AND: all inputs must be 1."""
        if len(self.inputs) < self.num_inputs:
            return 0
        return 1 if all(self.inputs) else 0
    
    def get_truth_table(self) -> List[Tuple[Tuple[int, ...], int]]:
        """Get AND truth table."""
        if self.num_inputs == 2:
            return [
                ((0, 0), 0),
                ((0, 1), 0),
                ((1, 0), 0),
                ((1, 1), 1)
            ]
        return []


class ORGate(LogicGate):
    """OR logic gate."""
    
    def __init__(self, id: str, num_inputs: int = 2):
        super().__init__(id, gate_type="OR")
        self.num_inputs = num_inputs
    
    def compute(self) -> int:
        """Compute OR: any input must be 1."""
        if len(self.inputs) < self.num_inputs:
            return 0
        return 1 if any(self.inputs) else 0
    
    def get_truth_table(self) -> List[Tuple[Tuple[int, ...], int]]:
        """Get OR truth table."""
        if self.num_inputs == 2:
            return [
                ((0, 0), 0),
                ((0, 1), 1),
                ((1, 0), 1),
                ((1, 1), 1)
            ]
        return []


class NOTGate(LogicGate):
    """NOT logic gate (inverter)."""
    
    def __init__(self, id: str):
        super().__init__(id, gate_type="NOT")
        self.num_inputs = 1
    
    def compute(self) -> int:
        """Compute NOT: invert input."""
        if len(self.inputs) < 1:
            return 0
        return 1 - self.inputs[0]
    
    def get_truth_table(self) -> List[Tuple[Tuple[int, ...], int]]:
        """Get NOT truth table."""
        return [
            ((0,), 1),
            ((1,), 0)
        ]


class NANDGate(LogicGate):
    """NAND logic gate (NOT AND)."""
    
    def __init__(self, id: str, num_inputs: int = 2):
        super().__init__(id, gate_type="NAND")
        self.num_inputs = num_inputs
    
    def compute(self) -> int:
        """Compute NAND: NOT of AND."""
        if len(self.inputs) < self.num_inputs:
            return 1
        return 0 if all(self.inputs) else 1
    
    def get_truth_table(self) -> List[Tuple[Tuple[int, ...], int]]:
        """Get NAND truth table."""
        if self.num_inputs == 2:
            return [
                ((0, 0), 1),
                ((0, 1), 1),
                ((1, 0), 1),
                ((1, 1), 0)
            ]
        return []


class NORGate(LogicGate):
    """NOR logic gate (NOT OR)."""
    
    def __init__(self, id: str, num_inputs: int = 2):
        super().__init__(id, gate_type="NOR")
        self.num_inputs = num_inputs
    
    def compute(self) -> int:
        """Compute NOR: NOT of OR."""
        if len(self.inputs) < self.num_inputs:
            return 1
        return 0 if any(self.inputs) else 1
    
    def get_truth_table(self) -> List[Tuple[Tuple[int, ...], int]]:
        """Get NOR truth table."""
        if self.num_inputs == 2:
            return [
                ((0, 0), 1),
                ((0, 1), 0),
                ((1, 0), 0),
                ((1, 1), 0)
            ]
        return []


class XORGate(LogicGate):
    """XOR logic gate (exclusive OR)."""
    
    def __init__(self, id: str, num_inputs: int = 2):
        super().__init__(id, gate_type="XOR")
        self.num_inputs = num_inputs
    
    def compute(self) -> int:
        """Compute XOR: odd number of 1s."""
        if len(self.inputs) < self.num_inputs:
            return 0
        return sum(self.inputs) % 2
    
    def get_truth_table(self) -> List[Tuple[Tuple[int, ...], int]]:
        """Get XOR truth table."""
        if self.num_inputs == 2:
            return [
                ((0, 0), 0),
                ((0, 1), 1),
                ((1, 0), 1),
                ((1, 1), 0)
            ]
        return []


class XNORGate(LogicGate):
    """XNOR logic gate (exclusive NOR, equivalence)."""
    
    def __init__(self, id: str, num_inputs: int = 2):
        super().__init__(id, gate_type="XNOR")
        self.num_inputs = num_inputs
    
    def compute(self) -> int:
        """Compute XNOR: NOT of XOR (even number of 1s)."""
        if len(self.inputs) < self.num_inputs:
            return 1
        return 1 - (sum(self.inputs) % 2)
    
    def get_truth_table(self) -> List[Tuple[Tuple[int, ...], int]]:
        """Get XNOR truth table."""
        if self.num_inputs == 2:
            return [
                ((0, 0), 1),
                ((0, 1), 0),
                ((1, 0), 0),
                ((1, 1), 1)
            ]
        return []


# =============================================================================
# LOGIC CIRCUIT
# =============================================================================

class LogicCircuit:
    """Complex circuit built from logic gates."""
    
    def __init__(self, name: str):
        self.name = name
        self.gates: Dict[str, LogicGate] = {}
        self.connections: Dict[str, List[str]] = defaultdict(list)  # gate_id -> connected gate_ids
        self.inputs: List[str] = []
        self.outputs: List[str] = []
    
    def add_gate(self, gate: LogicGate):
        """Add a gate to the circuit."""
        self.gates[gate.id] = gate
    
    def connect(self, source_id: str, target_id: str):
        """Connect output of one gate to input of another."""
        self.connections[source_id].append(target_id)
    
    def set_inputs(self, gate_id: str, inputs: List[int]):
        """Set inputs for a specific gate."""
        if gate_id in self.gates:
            self.gates[gate_id].set_inputs(inputs)
    
    def compute(self) -> Dict[str, int]:
        """Compute circuit outputs."""
        # Topological sort for gate execution
        visited = set()
        outputs = {}
        
        def visit(gate_id: str):
            if gate_id in visited:
                return
            visited.add(gate_id)
            
            gate = self.gates.get(gate_id)
            if not gate:
                return
            
            # Visit connected gates first (for dependencies)
            for connected_id in self.connections[gate_id]:
                visit(connected_id)
            
            # Compute this gate
            gate.output = gate.compute()
            outputs[gate_id] = gate.output
        
        # Visit all gates
        for gate_id in self.gates:
            visit(gate_id)
        
        return outputs
    
    def get_output(self, gate_id: str) -> int:
        """Get output from specific gate."""
        if gate_id in self.gates:
            return self.gates[gate_id].output
        return 0


# =============================================================================
# LOGIC GATE BRAIN
# =============================================================================

class LogicGateBrain:
    """Brain system using logic gates."""
    
    def __init__(self, num_gates: int = 100):
        self.num_gates = num_gates
        self.circuits: Dict[str, LogicCircuit] = {}
        self.active_circuit: Optional[LogicCircuit] = None
        self.is_integrated = USING_REAL_BRAIN_SYSTEM
        self._initialize_brain()
    
    def _initialize_brain(self):
        """Initialize logic gate brain with circuits."""
        # Create main circuit
        main_circuit = LogicCircuit("main_circuit")
        
        # Add various gates
        gate_types = [ANDGate, ORGate, NOTGate, NANDGate, NORGate, XORGate, XNORGate]
        
        for i in range(self.num_gates):
            gate_type = gate_types[i % len(gate_types)]
            gate = gate_type(f"gate_{i}")
            main_circuit.add_gate(gate)
        
        # Create random connections
        gate_ids = list(main_circuit.gates.keys())
        for i in range(len(gate_ids)):
            # Connect to 2-3 random gates
            num_connections = 2
            for _ in range(num_connections):
                target_id = gate_ids[(i + random.randint(1, 5)) % len(gate_ids)]
                main_circuit.connect(gate_ids[i], target_id)
        
        self.circuits["main_circuit"] = main_circuit
        self.active_circuit = main_circuit
    
    def create_circuit(self, name: str, gate_config: List[Dict[str, Any]]) -> LogicCircuit:
        """Create a custom circuit from gate configuration."""
        circuit = LogicCircuit(name)
        
        for config in gate_config:
            gate_type = config["type"]
            gate_id = config["id"]
            num_inputs = config.get("num_inputs", 2)
            
            if gate_type == "AND":
                gate = ANDGate(gate_id, num_inputs)
            elif gate_type == "OR":
                gate = ORGate(gate_id, num_inputs)
            elif gate_type == "NOT":
                gate = NOTGate(gate_id)
            elif gate_type == "NAND":
                gate = NANDGate(gate_id, num_inputs)
            elif gate_type == "NOR":
                gate = NORGate(gate_id, num_inputs)
            elif gate_type == "XOR":
                gate = XORGate(gate_id, num_inputs)
            elif gate_type == "XNOR":
                gate = XNORGate(gate_id, num_inputs)
            else:
                continue
            
            circuit.add_gate(gate)
        
        # Add connections
        for config in gate_config:
            gate_id = config["id"]
            connections = config.get("connections", [])
            for target_id in connections:
                circuit.connect(gate_id, target_id)
        
        self.circuits[name] = circuit
        return circuit
    
    def set_active_circuit(self, circuit_name: str):
        """Set the active circuit."""
        if circuit_name in self.circuits:
            self.active_circuit = self.circuits[circuit_name]
    
    def process(self, inputs: Dict[str, List[int]]) -> Dict[str, Any]:
        """Process inputs through active circuit."""
        if not self.active_circuit:
            return {"error": "No active circuit"}
        
        # Set inputs for specified gates
        for gate_id, input_values in inputs.items():
            self.active_circuit.set_inputs(gate_id, input_values)
        
        # Compute circuit
        outputs = self.active_circuit.compute()
        
        return {
            "outputs": outputs,
            "circuit": self.active_circuit.name,
            "total_gates": len(self.active_circuit.gates),
            "is_integrated": self.is_integrated
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get brain statistics."""
        if not self.active_circuit:
            return {"error": "No active circuit"}
        
        gate_counts = defaultdict(int)
        for gate in self.active_circuit.gates.values():
            gate_counts[gate.gate_type] += 1
        
        return {
            "total_circuits": len(self.circuits),
            "active_circuit": self.active_circuit.name,
            "total_gates": len(self.active_circuit.gates),
            "gate_distribution": dict(gate_counts),
            "is_integrated": self.is_integrated
        }


# =============================================================================
# DEMONSTRATION
# =============================================================================

import random

def demonstrate_logic_gate_brain():
    """Demonstrate logic gate brain capabilities."""
    print("=" * 60)
    print("Logic Gate Brain System - Demonstration")
    print("=" * 60)
    
    print(f"\nUsing Real Brain System: {USING_REAL_BRAIN_SYSTEM}")
    
    # Initialize logic gate brain
    brain = LogicGateBrain(num_gates=50)
    print(f"Integration Status: {'INTEGRATED' if brain.is_integrated else 'STANDALONE'}")
    
    print("\n1. Brain Statistics:")
    print("-" * 60)
    stats = brain.get_statistics()
    print(f"   Total circuits: {stats['total_circuits']}")
    print(f"   Active circuit: {stats['active_circuit']}")
    print(f"   Total gates: {stats['total_gates']}")
    print(f"   Gate distribution: {stats['gate_distribution']}")
    
    print("\n2. Basic Logic Gates Truth Tables:")
    print("-" * 60)
    
    # Test basic gates
    and_gate = ANDGate("test_and")
    print(f"   AND Gate: {and_gate.get_truth_table()}")
    
    or_gate = ORGate("test_or")
    print(f"   OR Gate: {or_gate.get_truth_table()}")
    
    not_gate = NOTGate("test_not")
    print(f"   NOT Gate: {not_gate.get_truth_table()}")
    
    xor_gate = XORGate("test_xor")
    print(f"   XOR Gate: {xor_gate.get_truth_table()}")
    
    print("\n3. Custom Circuit - Half Adder:")
    print("-" * 60)
    
    # Create half adder circuit
    half_adder_config = [
        {"type": "XOR", "id": "xor1", "connections": []},
        {"type": "AND", "id": "and1", "connections": []}
    ]
    
    half_adder = brain.create_circuit("half_adder", half_adder_config)
    brain.set_active_circuit("half_adder")
    
    # Test half adder
    test_cases = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for a, b in test_cases:
        result = brain.process({
            "xor1": [a, b],
            "and1": [a, b]
        })
        print(f"   {a} + {b}: sum={result['outputs'].get('xor1')}, carry={result['outputs'].get('and1')}")
    
    print("\n4. Custom Circuit - Full Adder:")
    print("-" * 60)
    
    # Create full adder circuit
    full_adder_config = [
        {"type": "XOR", "id": "xor1", "connections": []},
        {"type": "XOR", "id": "xor2", "connections": ["xor1"]},
        {"type": "AND", "id": "and1", "connections": []},
        {"type": "AND", "id": "and2", "connections": ["xor1"]},
        {"type": "OR", "id": "or1", "connections": ["and1", "and2"]}
    ]
    
    full_adder = brain.create_circuit("full_adder", full_adder_config)
    brain.set_active_circuit("full_adder")
    
    # Test full adder
    test_cases = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), 
                 (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
    for a, b, cin in test_cases:
        result = brain.process({
            "xor1": [a, b],
            "and1": [a, b],
            "xor2": [cin, 0],  # Will be updated by circuit
            "and2": [cin, 0],
            "or1": [0, 0]
        })
        print(f"   {a} + {b} + {cin}: sum={result['outputs'].get('xor2')}, carry={result['outputs'].get('or1')}")
    
    print("\n5. Main Circuit Processing:")
    print("-" * 60)
    
    brain.set_active_circuit("main_circuit")
    
    # Set random inputs
    random_inputs = {}
    for i in range(5):
        gate_id = f"gate_{i}"
        random_inputs[gate_id] = [random.randint(0, 1), random.randint(0, 1)]
    
    result = brain.process(random_inputs)
    print(f"   Inputs: {len(random_inputs)} gates")
    print(f"   Outputs: {len(result['outputs'])} gates")
    print(f"   Active outputs: {sum(1 for v in result['outputs'].values() if v == 1)}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demonstrate_logic_gate_brain()
