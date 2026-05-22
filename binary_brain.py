"""
Binary Brain System
A fully binary neural network with binary neurons and synapses.
All values are 0 or 1, simulating digital logic circuits.

Components:
- BinaryNeuron: Binary neuron (0 or 1)
- BinarySynapse: Binary synaptic connection (0 or 1)
- BinaryBrain: Network of binary neurons and synapses
- BinaryLearning: Learning rules for binary networks
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
import time
import random

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
# BINARY NEURON
# =============================================================================

@dataclass
class BinaryNeuron:
    """Binary neuron with state 0 or 1."""
    id: str
    state: int = 0  # Binary state: 0 or 1
    threshold: int = 1  # Firing threshold
    refractory_period: int = 0  # Refractory counter
    region: str = BrainRegion.CORTEX
    
    def __post_init__(self):
        """Ensure state is binary."""
        self.state = int(bool(self.state))
    
    def activate(self, inputs: List[int]) -> int:
        """Activate neuron based on binary inputs."""
        if self.refractory_period > 0:
            self.refractory_period -= 1
            return 0
        
        # Binary summation: count of 1s
        total = sum(inputs)
        
        # Binary threshold activation
        if total >= self.threshold:
            self.state = 1
            self.refractory_period = 1  # Set refractory period
            return 1
        else:
            self.state = 0
            return 0
    
    def reset(self):
        """Reset neuron state."""
        self.state = 0
        self.refractory_period = 0


# =============================================================================
# BINARY SYNAPSE
# =============================================================================

@dataclass
class BinarySynapse:
    """Binary synaptic connection (0 or 1 weight)."""
    id: str
    source_id: str
    target_id: str
    weight: int = 1  # Binary weight: 0 or 1
    delay: int = 0  # Transmission delay
    
    def __post_init__(self):
        """Ensure weight is binary."""
        self.weight = int(bool(self.weight))
    
    def transmit(self, signal: int) -> int:
        """Transmit signal through synapse."""
        if self.delay > 0:
            self.delay -= 1
            return 0
        return signal * self.weight
    
    def flip(self):
        """Flip binary weight (0 -> 1, 1 -> 0)."""
        self.weight = 1 - self.weight


# =============================================================================
# BINARY BRAIN
# =============================================================================

class BinaryBrain:
    """Network of binary neurons and synapses."""
    
    def __init__(self, num_neurons: int = 100, connection_density: float = 0.1):
        self.num_neurons = num_neurons
        self.connection_density = connection_density
        self.neurons: Dict[str, BinaryNeuron] = {}
        self.synapses: Dict[str, BinarySynapse] = {}
        self.adjacency: Dict[str, List[str]] = defaultdict(list)
        self.is_integrated = USING_REAL_BRAIN_SYSTEM
        self._initialize_network()
    
    def _initialize_network(self):
        """Initialize binary neural network."""
        # Create neurons
        for i in range(self.num_neurons):
            neuron = BinaryNeuron(
                id=f"neuron_{i}",
                state=random.randint(0, 1),
                threshold=random.randint(1, 3)
            )
            self.neurons[neuron.id] = neuron
        
        # Create synapses
        num_synapses = int(self.num_neurons * self.num_neurons * self.connection_density)
        synapse_count = 0
        attempts = 0
        
        while synapse_count < num_synapses and attempts < num_synapses * 10:
            source_id = f"neuron_{random.randint(0, self.num_neurons - 1)}"
            target_id = f"neuron_{random.randint(0, self.num_neurons - 1)}"
            
            if source_id != target_id and target_id not in self.adjacency[source_id]:
                synapse = BinarySynapse(
                    id=f"synapse_{synapse_count}",
                    source_id=source_id,
                    target_id=target_id,
                    weight=random.randint(0, 1)
                )
                self.synapses[synapse.id] = synapse
                self.adjacency[source_id].append(target_id)
                synapse_count += 1
            
            attempts += 1
    
    def step(self) -> Dict[str, Any]:
        """Execute one time step of binary brain."""
        # Collect signals
        signals = defaultdict(list)
        
        for synapse in self.synapses.values():
            source_neuron = self.neurons[synapse.source_id]
            signal = synapse.transmit(source_neuron.state)
            if signal == 1:
                signals[synapse.target_id].append(signal)
        
        # Activate neurons
        activations = {}
        for neuron_id, neuron in self.neurons.items():
            new_state = neuron.activate(signals[neuron_id])
            activations[neuron_id] = new_state
        
        # Calculate statistics
        active_neurons = sum(1 for n in self.neurons.values() if n.state == 1)
        active_synapses = sum(1 for s in self.synapses.values() if s.weight == 1)
        
        return {
            "activations": activations,
            "active_neurons": active_neurons,
            "total_neurons": len(self.neurons),
            "active_synapses": active_synapses,
            "total_synapses": len(self.synapses),
            "is_integrated": self.is_integrated
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get brain statistics."""
        active_neurons = sum(1 for n in self.neurons.values() if n.state == 1)
        active_synapses = sum(1 for s in self.synapses.values() if s.weight == 1)
        
        # Calculate network properties
        in_degrees = [len(self.adjacency[nid]) for nid in self.neurons]
        out_degrees = []
        for nid in self.neurons:
            out_deg = sum(1 for s in self.synapses.values() if s.source_id == nid)
            out_degrees.append(out_deg)
        
        return {
            "total_neurons": len(self.neurons),
            "active_neurons": active_neurons,
            "total_synapses": len(self.synapses),
            "active_synapses": active_synapses,
            "avg_in_degree": sum(in_degrees) / len(in_degrees) if in_degrees else 0,
            "avg_out_degree": sum(out_degrees) / len(out_degrees) if out_degrees else 0,
            "is_integrated": self.is_integrated
        }
    
    def set_input(self, neuron_ids: List[str], states: List[int]):
        """Set input neurons to specific states."""
        for neuron_id, state in zip(neuron_ids, states):
            if neuron_id in self.neurons:
                self.neurons[neuron_id].state = int(bool(state))
    
    def get_output(self, neuron_ids: List[str]) -> List[int]:
        """Get output from specific neurons."""
        return [self.neurons[nid].state if nid in self.neurons else 0 for nid in neuron_ids]


# =============================================================================
# BINARY LEARNING
# =============================================================================

class BinaryLearning:
    """Learning rules for binary networks."""
    
    def __init__(self, binary_brain: BinaryBrain):
        self.binary_brain = binary_brain
        self.learning_rate = 0.1
    
    def hebbian_learning(self, source_id: str, target_id: str):
        """Hebbian learning: strengthen co-activated connections."""
        source = self.binary_brain.neurons.get(source_id)
        target = self.binary_brain.neurons.get(target_id)
        
        if not source or not target:
            return
        
        # Find synapse
        for synapse in self.binary_brain.synapses.values():
            if synapse.source_id == source_id and synapse.target_id == target_id:
                # Binary Hebbian: if both active, set weight to 1
                if source.state == 1 and target.state == 1:
                    synapse.weight = 1
                elif source.state == 0 or target.state == 0:
                    # With probability, weaken
                    if random.random() < self.learning_rate:
                        synapse.weight = 0
                break
    
    def anti_hebbian_learning(self, source_id: str, target_id: str):
        """Anti-Hebbian learning: weaken co-activated connections."""
        source = self.binary_brain.neurons.get(source_id)
        target = self.binary_brain.neurons.get(target_id)
        
        if not source or not target:
            return
        
        for synapse in self.binary_brain.synapses.values():
            if synapse.source_id == source_id and synapse.target_id == target_id:
                # Anti-Hebbian: if both active, set weight to 0
                if source.state == 1 and target.state == 1:
                    synapse.weight = 0
                elif source.state == 0 or target.state == 0:
                    # With probability, strengthen
                    if random.random() < self.learning_rate:
                        synapse.weight = 1
                break
    
    def random_flip(self, flip_probability: float = 0.01):
        """Randomly flip synapse weights."""
        for synapse in self.binary_brain.synapses.values():
            if random.random() < flip_probability:
                synapse.flip()


# =============================================================================
# DEMONSTRATION
# =============================================================================

def demonstrate_binary_brain():
    """Demonstrate binary brain capabilities."""
    print("=" * 60)
    print("Binary Brain System - Demonstration")
    print("=" * 60)
    
    print(f"\nUsing Real Brain System: {USING_REAL_BRAIN_SYSTEM}")
    
    # Initialize binary brain
    brain = BinaryBrain(num_neurons=50, connection_density=0.15)
    print(f"Integration Status: {'INTEGRATED' if brain.is_integrated else 'STANDALONE'}")
    
    print("\n1. Brain Statistics:")
    print("-" * 60)
    stats = brain.get_statistics()
    print(f"   Total neurons: {stats['total_neurons']}")
    print(f"   Active neurons: {stats['active_neurons']}")
    print(f"   Total synapses: {stats['total_synapses']}")
    print(f"   Active synapses: {stats['active_synapses']}")
    print(f"   Avg in-degree: {stats['avg_in_degree']:.2f}")
    print(f"   Avg out-degree: {stats['avg_out_degree']:.2f}")
    
    print("\n2. Simulation Steps:")
    print("-" * 60)
    
    for i in range(10):
        result = brain.step()
        print(f"   Step {i+1}: {result['active_neurons']} active neurons, {result['active_synapses']} active synapses")
    
    print("\n3. Learning Demonstration:")
    print("-" * 60)
    
    learning = BinaryLearning(brain)
    
    # Set input
    input_neurons = [f"neuron_{i}" for i in range(5)]
    input_states = [1, 1, 0, 1, 0]
    brain.set_input(input_neurons, input_states)
    
    print(f"   Input set: {input_states}")
    
    # Run step
    result = brain.step()
    print(f"   After step: {result['active_neurons']} active neurons")
    
    # Apply Hebbian learning
    learning.hebbian_learning("neuron_0", "neuron_1")
    print(f"   Applied Hebbian learning")
    
    # Check statistics
    new_stats = brain.get_statistics()
    print(f"   After learning: {new_stats['active_synapses']} active synapses")
    
    print("\n4. Final Statistics:")
    print("-" * 60)
    
    final_stats = brain.get_statistics()
    for key, value in final_stats.items():
        print(f"   {key}: {value}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demonstrate_binary_brain()
