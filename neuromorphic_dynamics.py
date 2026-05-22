"""
Neuromorphic Dynamics Component
Implements spiking neurons, chemistry, and plasticity for continuous-state neuromorphic reasoning.

Components:
- SpikingNeuron: Izhikevich-style spiking neuron
- ChemicalSynapse: Synapse with neurotransmitter dynamics
- PlasticityRule: STDP and dopamine-gated learning
- NeuromorphicEngine: Core dynamics engine
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
import numpy as np
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
# SPIKING NEURON
# =============================================================================

@dataclass
class SpikingNeuron:
    """Izhikevich-style spiking neuron."""
    id: str
    v: float = -65.0  # Membrane potential (mV)
    u: float = -13.0  # Recovery variable
    a: float = 0.02  # Time scale of recovery
    b: float = 0.2  # Sensitivity of recovery
    c: float = -65.0  # After-spike reset of v
    d: float = 2.0  # After-spike reset of u
    region: str = BrainRegion.CORTEX
    last_spike: float = 0.0
    spike_history: List[float] = field(default_factory=list)
    
    def update(self, I: float, dt: float = 0.1) -> Tuple[float, bool]:
        """Update neuron state using Izhikevich model."""
        # Izhikevich equations
        dv = (0.04 * self.v**2 + 5 * self.v + 140 - self.u + I) * dt
        du = (self.a * (self.b * self.v - self.u)) * dt
        
        self.v += dv
        self.u += du
        
        # Spike detection
        spiked = False
        if self.v >= 30.0:
            self.v = self.c
            self.u += self.d
            spiked = True
            self.last_spike = time.time()
            self.spike_history.append(self.last_spike)
            # Keep only recent spikes
            if len(self.spike_history) > 100:
                self.spike_history.pop(0)
        
        return self.v, spiked
    
    def get_firing_rate(self, window: float = 1.0) -> float:
        """Calculate firing rate over time window."""
        now = time.time()
        recent_spikes = [t for t in self.spike_history if now - t < window]
        return len(recent_spikes) / window


# =============================================================================
# CHEMICAL SYNAPSE
# =============================================================================

@dataclass
class ChemicalSynapse:
    """Synapse with neurotransmitter dynamics."""
    id: str
    source_id: str
    target_id: str
    weight: float = 0.5  # Synaptic weight
    delay: float = 1.0  # Transmission delay (ms)
    neurotransmitter: str = "AMPA"  # AMPA, GABA, Dopamine
    concentration: float = 0.0  # Neurotransmitter concentration
    decay_rate: float = 0.1  # Decay rate of concentration
    
    def release(self, spiked: bool):
        """Release neurotransmitter on spike."""
        if spiked:
            self.concentration += self.weight
    
    def update(self, dt: float = 0.1) -> float:
        """Update neurotransmitter concentration."""
        # Decay
        self.concentration *= (1 - self.decay_rate * dt)
        return self.concentration
    
    def get_effective_weight(self) -> float:
        """Get effective weight based on neurotransmitter type."""
        if self.neurotransmitter == "GABA":
            return -self.concentration  # Inhibitory
        elif self.neurotransmitter == "Dopamine":
            return self.concentration * 1.5  # Modulatory
        else:  # AMPA
            return self.concentration  # Excitatory


# =============================================================================
# PLASTICITY RULES
# =============================================================================

class PlasticityRule:
    """Base class for plasticity rules."""
    
    def __init__(self, learning_rate: float = 0.01):
        self.learning_rate = learning_rate
    
    def update_weight(self, synapse: ChemicalSynapse, pre_spike: bool, post_spike: bool):
        """Update synaptic weight (to be overridden)."""
        raise NotImplementedError


class STDPRule(PlasticityRule):
    """Spike Timing Dependent Plasticity."""
    
    def __init__(self, learning_rate: float = 0.01, tau_plus: float = 20.0, tau_minus: float = 20.0):
        super().__init__(learning_rate)
        self.tau_plus = tau_plus
        self.tau_minus = tau_minus
        self.pre_trace = 0.0
        self.post_trace = 0.0
    
    def update_weight(self, synapse: ChemicalSynapse, pre_spike: bool, post_spike: bool):
        """Update weight using STDP."""
        # Update traces
        self.pre_trace *= 0.95  # Decay
        self.post_trace *= 0.95  # Decay
        
        if pre_spike:
            self.pre_trace += 1.0
            # Post-pre depression
            delta_w = -self.learning_rate * self.post_trace
            synapse.weight = np.clip(synapse.weight + delta_w, 0, 1)
        
        if post_spike:
            self.post_trace += 1.0
            # Pre-post potentiation
            delta_w = self.learning_rate * self.pre_trace
            synapse.weight = np.clip(synapse.weight + delta_w, 0, 1)


class DopamineGatedRule(PlasticityRule):
    """Dopamine-gated plasticity (three-factor learning)."""
    
    def __init__(self, learning_rate: float = 0.01, dopamine_level: float = 0.0):
        super().__init__(learning_rate)
        self.dopamine_level = dopamine_level
    
    def set_dopamine(self, level: float):
        """Set dopamine level (reward signal)."""
        self.dopamine_level = level
    
    def update_weight(self, synapse: ChemicalSynapse, pre_spike: bool, post_spike: bool):
        """Update weight with dopamine modulation."""
        if pre_spike and post_spike:
            # Co-activated synapse modulated by dopamine
            delta_w = self.learning_rate * self.dopamine_level
            synapse.weight = np.clip(synapse.weight + delta_w, 0, 1)


# =============================================================================
# NEUROMORPHIC ENGINE
# =============================================================================

class NeuromorphicEngine:
    """Core neuromorphic dynamics engine."""
    
    def __init__(self, num_neurons: int = 100, connection_density: float = 0.1):
        self.num_neurons = num_neurons
        self.connection_density = connection_density
        self.neurons: Dict[str, SpikingNeuron] = {}
        self.synapses: Dict[str, ChemicalSynapse] = {}
        self.adjacency: Dict[str, List[str]] = defaultdict(list)
        self.plasticity_rules: Dict[str, PlasticityRule] = {}
        self.is_integrated = USING_REAL_BRAIN_SYSTEM
        self.dt = 0.1  # Time step (ms)
        self._initialize_network()
    
    def _initialize_network(self):
        """Initialize spiking neural network."""
        # Create neurons
        for i in range(self.num_neurons):
            neuron = SpikingNeuron(
                id=f"neuron_{i}",
                v=-65.0 + np.random.random() * 5,  # Random initialization
                u=-13.0 + np.random.random() * 2,
                region=BrainRegion.CORTEX
            )
            self.neurons[neuron.id] = neuron
        
        # Create synapses
        num_synapses = int(self.num_neurons * self.num_neurons * self.connection_density)
        synapse_count = 0
        attempts = 0
        
        while synapse_count < num_synapses and attempts < num_synapses * 10:
            source_id = f"neuron_{np.random.randint(0, self.num_neurons)}"
            target_id = f"neuron_{np.random.randint(0, self.num_neurons)}"
            
            if source_id != target_id and target_id not in self.adjacency[source_id]:
                neurotransmitter = np.random.choice(["AMPA", "GABA", "Dopamine"])
                synapse = ChemicalSynapse(
                    id=f"synapse_{synapse_count}",
                    source_id=source_id,
                    target_id=target_id,
                    weight=np.random.random(),
                    neurotransmitter=neurotransmitter
                )
                self.synapses[synapse.id] = synapse
                self.adjacency[source_id].append(target_id)
                
                # Add plasticity rule
                if neurotransmitter == "Dopamine":
                    self.plasticity_rules[synapse.id] = DopamineGatedRule()
                else:
                    self.plasticity_rules[synapse.id] = STDPRule()
                
                synapse_count += 1
            
            attempts += 1
    
    def step(self, external_input: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """Execute one time step."""
        if external_input is None:
            external_input = {}
        
        # Collect synaptic currents
        currents = defaultdict(float)
        
        for synapse in self.synapses.values():
            source_neuron = self.neurons[synapse.source_id]
            target_id = synapse.target_id
            
            # Check if source spiked recently
            recent_spike = (time.time() - source_neuron.last_spike) < synapse.delay
            
            synapse.release(recent_spike)
            concentration = synapse.update(self.dt)
            effective_weight = synapse.get_effective_weight()
            
            currents[target_id] += effective_weight * concentration
        
        # Add external input
        for neuron_id, input_current in external_input.items():
            currents[neuron_id] += input_current
        
        # Update neurons
        spikes = []
        for neuron_id, neuron in self.neurons.items():
            v, spiked = neuron.update(currents[neuron_id], self.dt)
            if spiked:
                spikes.append(neuron_id)
        
        # Apply plasticity
        for synapse_id, synapse in self.synapses.items():
            source_neuron = self.neurons[synapse.source_id]
            target_neuron = self.neurons[synapse.target_id]
            source_spiked = source_neuron.id in spikes
            target_spiked = target_neuron.id in spikes
            
            if synapse_id in self.plasticity_rules:
                self.plasticity_rules[synapse_id].update_weight(synapse, source_spiked, target_spiked)
        
        # Calculate statistics
        firing_rates = {nid: n.get_firing_rate() for nid, n in self.neurons.items()}
        avg_firing_rate = np.mean(list(firing_rates.values())) if firing_rates else 0.0
        
        return {
            "spikes": spikes,
            "num_spikes": len(spikes),
            "avg_firing_rate": avg_firing_rate,
            "avg_voltage": np.mean([n.v for n in self.neurons.values()]),
            "total_synapses": len(self.synapses),
            "is_integrated": self.is_integrated
        }
    
    def set_dopamine(self, level: float):
        """Set dopamine level for reward-modulated learning."""
        for rule in self.plasticity_rules.values():
            if isinstance(rule, DopamineGatedRule):
                rule.set_dopamine(level)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get engine statistics."""
        active_synapses = sum(1 for s in self.synapses.values() if s.weight > 0.5)
        avg_weight = np.mean([s.weight for s in self.synapses.values()]) if self.synapses else 0.0
        
        return {
            "total_neurons": len(self.neurons),
            "total_synapses": len(self.synapses),
            "active_synapses": active_synapses,
            "avg_weight": avg_weight,
            "is_integrated": self.is_integrated
        }


# =============================================================================
# DEMONSTRATION
# =============================================================================

def demonstrate_neuromorphic_dynamics():
    """Demonstrate neuromorphic dynamics capabilities."""
    print("=" * 60)
    print("Neuromorphic Dynamics - Demonstration")
    print("=" * 60)
    
    print(f"\nUsing Real Brain System: {USING_REAL_BRAIN_SYSTEM}")
    
    # Initialize neuromorphic engine
    engine = NeuromorphicEngine(num_neurons=50, connection_density=0.15)
    print(f"Integration Status: {'INTEGRATED' if engine.is_integrated else 'STANDALONE'}")
    
    print("\n1. Engine Statistics:")
    print("-" * 60)
    stats = engine.get_statistics()
    print(f"   Total neurons: {stats['total_neurons']}")
    print(f"   Total synapses: {stats['total_synapses']}")
    print(f"   Active synapses: {stats['active_synapses']}")
    print(f"   Avg weight: {stats['avg_weight']:.3f}")
    
    print("\n2. Simulation Steps:")
    print("-" * 60)
    
    # Set external input to stimulate some neurons
    external_input = {f"neuron_{i}": 10.0 for i in range(5)}
    
    for i in range(20):
        result = engine.step(external_input)
        print(f"   Step {i+1}: {result['num_spikes']} spikes, firing rate: {result['avg_firing_rate']:.2f} Hz")
        
        # Apply dopamine reward at step 10
        if i == 10:
            engine.set_dopamine(1.0)
            print(f"   Dopamine reward applied at step {i+1}")
    
    print("\n3. Final Statistics:")
    print("-" * 60)
    
    final_stats = engine.get_statistics()
    for key, value in final_stats.items():
        print(f"   {key}: {value}")
    
    print("\n4. Plasticity Effects:")
    print("-" * 60)
    
    avg_weight_after = np.mean([s.weight for s in engine.synapses.values()])
    print(f"   Average synapse weight after learning: {avg_weight_after:.3f}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demonstrate_neuromorphic_dynamics()
