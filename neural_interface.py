"""
Neural Interface Component
Implements spike decoding, continuous projection, and lobe mapping for hybrid spike-decoded cognitive field architecture.

Components:
- SpikeDecoder: Decodes spike trains into continuous vectors
- ContinuousProjector: Projects spikes to continuous state space
- LobeMapper: Maps neural activity to brain lobes/regions
- NeuralInterface: Unified interface layer
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
        THALAMUS = "thalamus"
        BASAL_GANGLIA = "basal_ganglia"
        CEREBELLUM = "cerebellum"
        VISUAL_CORTEX = "visual_cortex"
        AUDITORY_CORTEX = "auditory_cortex"
    USING_REAL_BRAIN_SYSTEM = False


# =============================================================================
# SPIKE DECODER
# =============================================================================

@dataclass
class SpikeTrain:
    """Spike train data structure."""
    neuron_id: str
    spike_times: List[float] = field(default_factory=list)
    
    def add_spike(self, timestamp: float):
        """Add a spike at given timestamp."""
        self.spike_times.append(timestamp)
        self.spike_times.sort()
    
    def get_rate(self, window: float = 1.0) -> float:
        """Calculate firing rate over time window."""
        now = time.time()
        recent = [t for t in self.spike_times if now - t < window]
        return len(recent) / window
    
    def get_isi(self) -> List[float]:
        """Get inter-spike intervals."""
        if len(self.spike_times) < 2:
            return []
        return [self.spike_times[i+1] - self.spike_times[i] for i in range(len(self.spike_times)-1)]


class SpikeDecoder:
    """Decodes spike trains into continuous vectors."""
    
    def __init__(self, num_neurons: int, decoding_window: float = 0.1):
        self.num_neurons = num_neurons
        self.decoding_window = decoding_window
        self.spike_trains: Dict[str, SpikeTrain] = {}
        self._initialize_trains()
    
    def _initialize_trains(self):
        """Initialize spike trains for all neurons."""
        for i in range(self.num_neurons):
            self.spike_trains[f"neuron_{i}"] = SpikeTrain(f"neuron_{i}")
    
    def add_spike(self, neuron_id: str, timestamp: Optional[float] = None):
        """Add a spike to the train."""
        if timestamp is None:
            timestamp = time.time()
        if neuron_id in self.spike_trains:
            self.spike_trains[neuron_id].add_spike(timestamp)
    
    def decode_to_rate_vector(self) -> np.ndarray:
        """Decode spike trains to firing rate vector."""
        rates = []
        for train in self.spike_trains.values():
            rate = train.get_rate(self.decoding_window)
            rates.append(rate)
        return np.array(rates)
    
    def decode_to_temporal_pattern(self, bins: int = 10) -> np.ndarray:
        """Decode spike trains to temporal pattern matrix."""
        now = time.time()
        pattern = np.zeros((self.num_neurons, bins))
        
        for i, train in enumerate(self.spike_trains.values()):
            for spike_time in train.spike_times:
                if now - spike_time < self.decoding_window:
                    bin_idx = int((now - spike_time) / self.decoding_window * bins)
                    if 0 <= bin_idx < bins:
                        pattern[i, bin_idx] = 1
        
        return pattern
    
    def decode_to_phase_vector(self) -> np.ndarray:
        """Decode spike trains to phase vector (oscillatory component)."""
        phases = []
        for train in self.spike_trains.values():
            isi = train.get_isi()
            if len(isi) > 0:
                # Phase based on time since last spike
                time_since = time.time() - train.spike_times[-1]
                avg_isi = np.mean(isi)
                if avg_isi > 0:
                    phase = (time_since / avg_isi) * 2 * np.pi
                    phases.append(phase)
                else:
                    phases.append(0.0)
            else:
                phases.append(0.0)
        return np.array(phases)


# =============================================================================
# CONTINUOUS PROJECTOR
# =============================================================================

class ContinuousProjector:
    """Projects spike patterns to continuous state space."""
    
    def __init__(self, state_dim: int = 64):
        self.state_dim = state_dim
        self.projection_matrix = None
        self._initialize_projection()
    
    def _initialize_projection(self):
        """Initialize random projection matrix."""
        # Random projection from spike space to continuous state
        self.projection_matrix = np.random.randn(self.state_dim, self.state_dim)
        # Normalize
        self.projection_matrix = self.projection_matrix / np.linalg.norm(self.projection_matrix, axis=1, keepdims=True)
    
    def project_rate_vector(self, rate_vector: np.ndarray) -> np.ndarray:
        """Project rate vector to continuous state."""
        if len(rate_vector) < self.state_dim:
            # Pad with zeros
            padded = np.zeros(self.state_dim)
            padded[:len(rate_vector)] = rate_vector
            rate_vector = padded
        elif len(rate_vector) > self.state_dim:
            # Truncate
            rate_vector = rate_vector[:self.state_dim]
        
        # Apply projection
        continuous_state = np.dot(self.projection_matrix, rate_vector)
        
        # Normalize to [-1, 1]
        continuous_state = np.tanh(continuous_state)
        
        return continuous_state
    
    def project_temporal_pattern(self, pattern: np.ndarray) -> np.ndarray:
        """Project temporal pattern to continuous state."""
        # Flatten pattern
        flat = pattern.flatten()
        
        if len(flat) < self.state_dim:
            padded = np.zeros(self.state_dim)
            padded[:len(flat)] = flat
            flat = padded
        
        # Apply projection
        continuous_state = np.dot(self.projection_matrix[:self.state_dim, :len(flat)], flat)
        
        return np.tanh(continuous_state)
    
    def project_phase_vector(self, phase_vector: np.ndarray) -> np.ndarray:
        """Project phase vector to continuous state."""
        # Convert phase to sin/cos components
        sin_comp = np.sin(phase_vector)
        cos_comp = np.cos(phase_vector)
        combined = np.concatenate([sin_comp, cos_comp])
        
        if len(combined) < self.state_dim:
            padded = np.zeros(self.state_dim)
            padded[:len(combined)] = combined
            combined = padded
        
        return np.tanh(np.dot(self.projection_matrix[:self.state_dim, :len(combined)], combined))


# =============================================================================
# LOBE MAPPER
# =============================================================================

class LobeMapper:
    """Maps neural activity to brain lobes/regions."""
    
    def __init__(self, num_neurons: int):
        self.num_neurons = num_neurons
        self.neuron_to_lobe: Dict[str, str] = {}
        self.lobe_to_neurons: Dict[str, List[str]] = defaultdict(list)
        self._initialize_mapping()
    
    def _initialize_mapping(self):
        """Initialize neuron to lobe mapping."""
        regions = [
            BrainRegion.CORTEX,
            BrainRegion.HIPPOCAMPUS,
            BrainRegion.THALAMUS,
            BrainRegion.BASAL_GANGLIA,
            BrainRegion.CEREBELLUM,
            BrainRegion.VISUAL_CORTEX,
            BrainRegion.AUDITORY_CORTEX
        ]
        
        for i in range(self.num_neurons):
            # Distribute neurons across regions
            region = regions[i % len(regions)]
            neuron_id = f"neuron_{i}"
            self.neuron_to_lobe[neuron_id] = region
            self.lobe_to_neurons[region].append(neuron_id)
    
    def get_lobe_activity(self, spike_vector: np.ndarray) -> Dict[str, float]:
        """Get activity level for each lobe."""
        lobe_activity = {}
        
        for region, neuron_ids in self.lobe_to_neurons.items():
            activity = 0.0
            for neuron_id in neuron_ids:
                idx = int(neuron_id.split('_')[1])
                if idx < len(spike_vector):
                    activity += spike_vector[idx]
            lobe_activity[region] = activity / len(neuron_ids)
        
        return lobe_activity
    
    def get_continuous_state_by_lobe(self, continuous_state: np.ndarray) -> Dict[str, np.ndarray]:
        """Get continuous state vectors for each lobe."""
        lobe_states = {}
        
        for region, neuron_ids in self.lobe_to_neurons.items():
            state_vector = []
            for neuron_id in neuron_ids:
                idx = int(neuron_id.split('_')[1])
                if idx < len(continuous_state):
                    state_vector.append(continuous_state[idx])
            lobe_states[region] = np.array(state_vector)
        
        return lobe_states
    
    def map_input_to_lobe(self, input_type: str) -> str:
        """Map input type to appropriate brain lobe."""
        mapping = {
            "text": BrainRegion.CORTEX,
            "visual": BrainRegion.VISUAL_CORTEX,
            "audio": BrainRegion.AUDITORY_CORTEX,
            "memory": BrainRegion.HIPPOCAMPUS,
            "motor": BrainRegion.CEREBELLUM,
            "emotion": BrainRegion.BASAL_GANGLIA,
            "attention": BrainRegion.THALAMUS
        }
        return mapping.get(input_type, BrainRegion.CORTEX)


# =============================================================================
# NEURAL INTERFACE
# =============================================================================

class NeuralInterface:
    """Unified neural interface layer."""
    
    def __init__(self, num_neurons: int = 100, state_dim: int = 64):
        self.num_neurons = num_neurons
        self.spike_decoder = SpikeDecoder(num_neurons)
        self.continuous_projector = ContinuousProjector(state_dim)
        self.lobe_mapper = LobeMapper(num_neurons)
        self.is_integrated = USING_REAL_BRAIN_SYSTEM
        self.continuous_state = np.zeros(state_dim)
    
    def process_spikes(self, spikes: List[str]) -> Dict[str, Any]:
        """Process spike list through interface pipeline."""
        timestamp = time.time()
        
        # Add spikes to decoder
        for neuron_id in spikes:
            self.spike_decoder.add_spike(neuron_id, timestamp)
        
        # Decode to rate vector
        rate_vector = self.spike_decoder.decode_to_rate_vector()
        
        # Project to continuous state
        self.continuous_state = self.continuous_projector.project_rate_vector(rate_vector)
        
        # Map to lobes
        lobe_activity = self.lobe_mapper.get_lobe_activity(rate_vector)
        lobe_states = self.lobe_mapper.get_continuous_state_by_lobe(self.continuous_state)
        
        return {
            "continuous_state": self.continuous_state,
            "lobe_activity": lobe_activity,
            "lobe_states": lobe_states,
            "firing_rates": rate_vector,
            "is_integrated": self.is_integrated
        }
    
    def get_continuous_state(self) -> np.ndarray:
        """Get current continuous state."""
        return self.continuous_state.copy()
    
    def get_interface_statistics(self) -> Dict[str, Any]:
        """Get interface statistics."""
        total_spikes = sum(len(train.spike_times) for train in self.spike_decoder.spike_trains.values())
        
        return {
            "total_neurons": self.num_neurons,
            "total_spikes": total_spikes,
            "state_dimension": self.continuous_projector.state_dim,
            "num_lobes": len(self.lobe_mapper.lobe_to_neurons),
            "is_integrated": self.is_integrated
        }


# =============================================================================
# DEMONSTRATION
# =============================================================================

def demonstrate_neural_interface():
    """Demonstrate neural interface capabilities."""
    print("=" * 60)
    print("Neural Interface - Demonstration")
    print("=" * 60)
    
    print(f"\nUsing Real Brain System: {USING_REAL_BRAIN_SYSTEM}")
    
    # Initialize neural interface
    interface = NeuralInterface(num_neurons=50, state_dim=64)
    print(f"Integration Status: {'INTEGRATED' if interface.is_integrated else 'STANDALONE'}")
    
    print("\n1. Interface Statistics:")
    print("-" * 60)
    stats = interface.get_interface_statistics()
    print(f"   Total neurons: {stats['total_neurons']}")
    print(f"   State dimension: {stats['state_dimension']}")
    print(f"   Number of lobes: {stats['num_lobes']}")
    
    print("\n2. Spike Processing:")
    print("-" * 60)
    
    # Simulate some spikes
    spikes = [f"neuron_{i}" for i in range(0, 10, 2)]
    result = interface.process_spikes(spikes)
    
    print(f"   Input spikes: {len(spikes)}")
    print(f"   Continuous state shape: {result['continuous_state'].shape}")
    print(f"   Continuous state range: [{result['continuous_state'].min():.3f}, {result['continuous_state'].max():.3f}]")
    
    print("\n3. Lobe Activity:")
    print("-" * 60)
    
    for lobe, activity in result['lobe_activity'].items():
        print(f"   {lobe}: {activity:.3f}")
    
    print("\n4. Lobe States:")
    print("-" * 60)
    
    for lobe, state in result['lobe_states'].items():
        if len(state) > 0:
            print(f"   {lobe}: shape={state.shape}, mean={state.mean():.3f}")
    
    print("\n5. Multiple Spike Batches:")
    print("-" * 60)
    
    for i in range(5):
        # Generate random spikes
        batch_spikes = [f"neuron_{np.random.randint(0, 50)}" for _ in range(np.random.randint(5, 15))]
        result = interface.process_spikes(batch_spikes)
        print(f"   Batch {i+1}: {len(batch_spikes)} spikes -> state norm: {np.linalg.norm(result['continuous_state']):.3f}")
    
    print("\n6. Final Continuous State:")
    print("-" * 60)
    
    final_state = interface.get_continuous_state()
    print(f"   State norm: {np.linalg.norm(final_state):.3f}")
    print(f"   State mean: {final_state.mean():.3f}")
    print(f"   State std: {final_state.std():.3f}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demonstrate_neural_interface()
