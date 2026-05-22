"""
Attractor Semantics Component
Implements continuous state fields, attractor words, and controlled collapse for reward-modulated attractor cognition.

Components:
- ContinuousField: Continuous state field in [-1, 1] space
- AttractorWord: Stable energy minima representing concepts
- ControlledCollapse: Quantum-like collapse with confidence
- AttractorSemanticsEngine: Unified semantics engine
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
# CONTINUOUS FIELD
# =============================================================================

class ContinuousField:
    """Continuous state field in [-1, 1] space."""
    
    def __init__(self, dimension: int = 64):
        self.dimension = dimension
        self.state = np.zeros(dimension)
        self.velocity = np.zeros(dimension)
        self.energy_history: List[float] = []
    
    def set_state(self, new_state: np.ndarray):
        """Set field state."""
        if len(new_state) == self.dimension:
            self.state = np.clip(new_state, -1.0, 1.0)
    
    def get_energy(self) -> float:
        """Calculate field energy (negative of norm squared)."""
        return -np.sum(self.state ** 2)
    
    def evolve(self, force: np.ndarray, dt: float = 0.1):
        """Evolve field under force."""
        # Update velocity (F = ma, assume m=1)
        self.velocity += force * dt
        # Damping
        self.velocity *= 0.9
        # Update position
        self.state += self.velocity * dt
        # Clip to [-1, 1]
        self.state = np.clip(self.state, -1.0, 1.0)
        
        # Record energy
        self.energy_history.append(self.get_energy())
        if len(self.energy_history) > 1000:
            self.energy_history.pop(0)
    
    def is_stable(self, threshold: float = 0.01) -> bool:
        """Check if field is stable (low velocity)."""
        return np.linalg.norm(self.velocity) < threshold


# =============================================================================
# ATTRACTOR WORD
# =============================================================================

@dataclass
class AttractorWord:
    """Stable energy minimum representing a concept."""
    word: str
    center: np.ndarray  # Center point in state space
    radius: float  # Basin of attraction radius
    strength: float = 1.0  # Attractor strength
    
    def distance_to(self, state: np.ndarray) -> float:
        """Calculate distance from state to attractor center."""
        return np.linalg.norm(state - self.center)
    
    def is_in_basin(self, state: np.ndarray) -> bool:
        """Check if state is in attractor basin."""
        return self.distance_to(state) < self.radius
    
    def attraction_force(self, state: np.ndarray) -> np.ndarray:
        """Calculate attraction force toward attractor."""
        direction = self.center - state
        distance = np.linalg.norm(direction)
        if distance == 0:
            return np.zeros_like(state)
        # Force proportional to distance (spring-like)
        return (direction / distance) * self.strength * distance


# =============================================================================
# CONTROLLED COLLAPSE
# =============================================================================

class ControlledCollapse:
    """Quantum-like collapse with confidence-based decision."""
    
    def __init__(self):
        self.collapse_history: List[Dict[str, Any]] = []
    
    def collapse_to_attractor(self, field: ContinuousField, attractors: List[AttractorWord], confidence: float = 0.5) -> Dict[str, Any]:
        """Collapse field state to nearest attractor."""
        # Find nearest attractor
        nearest_attractor = None
        min_distance = float('inf')
        
        for attractor in attractors:
            distance = attractor.distance_to(field.state)
            if distance < min_distance:
                min_distance = distance
                nearest_attractor = attractor
        
        # Collapse probability based on confidence and distance
        if nearest_attractor:
            collapse_prob = confidence * np.exp(-min_distance)
            
            # Decide whether to collapse
            if np.random.random() < collapse_prob:
                # Collapse to attractor
                field.set_state(nearest_attractor.center)
                field.velocity *= 0.1  # Reduce velocity on collapse
                
                result = {
                    "collapsed": True,
                    "attractor": nearest_attractor.word,
                    "confidence": confidence,
                    "distance": min_distance
                }
            else:
                result = {
                    "collapsed": False,
                    "attractor": None,
                    "confidence": confidence,
                    "distance": min_distance
                }
        else:
            result = {
                "collapsed": False,
                "attractor": None,
                "confidence": confidence,
                "distance": float('inf')
            }
        
        self.collapse_history.append(result)
        return result
    
    def get_collapse_statistics(self) -> Dict[str, Any]:
        """Get collapse statistics."""
        if not self.collapse_history:
            return {"total_collapses": 0}
        
        collapsed_count = sum(1 for c in self.collapse_history if c["collapsed"])
        attractor_counts = defaultdict(int)
        
        for record in self.collapse_history:
            if record["attractor"]:
                attractor_counts[record["attractor"]] += 1
        
        return {
            "total_collapses": len(self.collapse_history),
            "successful_collapses": collapsed_count,
            "collapse_rate": collapsed_count / len(self.collapse_history),
            "attractor_frequencies": dict(attractor_counts)
        }


# =============================================================================
# ATTRACTOR SEMANTICS ENGINE
# =============================================================================

class AttractorSemanticsEngine:
    """Unified attractor semantics engine."""
    
    def __init__(self, state_dim: int = 64):
        self.state_dim = state_dim
        self.field = ContinuousField(state_dim)
        self.attractors: Dict[str, AttractorWord] = {}
        self.collapse_controller = ControlledCollapse()
        self.is_integrated = USING_REAL_BRAIN_SYSTEM
        self._initialize_attractors()
    
    def _initialize_attractors(self):
        """Initialize basic attractor words."""
        # Create attractors for basic concepts
        concepts = [
            ("apple", np.array([0.8, 0.1, 0.2, 0.3, 0.1])),
            ("red", np.array([0.9, 0.1, 0.1, 0.1, 0.1])),
            ("fruit", np.array([0.7, 0.2, 0.3, 0.2, 0.1])),
            ("round", np.array([0.1, 0.1, 0.8, 0.2, 0.1])),
            ("sweet", np.array([0.2, 0.8, 0.1, 0.1, 0.1]))
        ]
        
        for word, center in concepts:
            # Pad to state_dim
            if len(center) < self.state_dim:
                padded = np.zeros(self.state_dim)
                padded[:len(center)] = center
                center = padded
            
            attractor = AttractorWord(
                word=word,
                center=center,
                radius=0.5,
                strength=1.0
            )
            self.attractors[word] = attractor
    
    def add_attractor(self, word: str, center: np.ndarray, radius: float = 0.5):
        """Add new attractor word."""
        if len(center) < self.state_dim:
            padded = np.zeros(self.state_dim)
            padded[:len(center)] = center
            center = padded
        
        attractor = AttractorWord(word=word, center=center, radius=radius)
        self.attractors[word] = attractor
    
    def process(self, input_state: np.ndarray, confidence: float = 0.5, dt: float = 0.1) -> Dict[str, Any]:
        """Process input through attractor semantics."""
        # Set field state
        self.field.set_state(input_state)
        
        # Calculate attraction forces
        total_force = np.zeros(self.state_dim)
        active_attractors = []
        
        for attractor in self.attractors.values():
            if attractor.is_in_basin(self.field.state):
                force = attractor.attraction_force(self.field.state)
                total_force += force
                active_attractors.append(attractor.word)
        
        # Evolve field
        self.field.evolve(total_force, dt)
        
        # Attempt collapse
        collapse_result = self.collapse_controller.collapse_to_attractor(
            self.field,
            list(self.attractors.values()),
            confidence
        )
        
        return {
            "field_state": self.field.state.copy(),
            "field_energy": self.field.get_energy(),
            "field_stable": self.field.is_stable(),
            "active_attractors": active_attractors,
            "collapse_result": collapse_result,
            "is_integrated": self.is_integrated
        }
    
    def get_semantics_statistics(self) -> Dict[str, Any]:
        """Get semantics engine statistics."""
        collapse_stats = self.collapse_controller.get_collapse_statistics()
        
        return {
            "state_dimension": self.state_dim,
            "total_attractors": len(self.attractors),
            "field_energy": self.field.get_energy(),
            "field_stable": self.field.is_stable(),
            "collapse_statistics": collapse_stats,
            "is_integrated": self.is_integrated
        }


# =============================================================================
# DEMONSTRATION
# =============================================================================

def demonstrate_attractor_semantics():
    """Demonstrate attractor semantics capabilities."""
    print("=" * 60)
    print("Attractor Semantics - Demonstration")
    print("=" * 60)
    
    print(f"\nUsing Real Brain System: {USING_REAL_BRAIN_SYSTEM}")
    
    # Initialize attractor semantics engine
    engine = AttractorSemanticsEngine(state_dim=64)
    print(f"Integration Status: {'INTEGRATED' if engine.is_integrated else 'STANDALONE'}")
    
    print("\n1. Engine Statistics:")
    print("-" * 60)
    stats = engine.get_semantics_statistics()
    print(f"   State dimension: {stats['state_dimension']}")
    print(f"   Total attractors: {stats['total_attractors']}")
    print(f"   Field energy: {stats['field_energy']:.3f}")
    print(f"   Field stable: {stats['field_stable']}")
    
    print("\n2. Attractor Words:")
    print("-" * 60)
    
    for word, attractor in engine.attractors.items():
        print(f"   {word}: radius={attractor.radius:.2f}, strength={attractor.strength:.2f}")
    
    print("\n3. Input Processing:")
    print("-" * 60)
    
    # Create input similar to "apple"
    input_state = np.zeros(64)
    input_state[0] = 0.7
    input_state[1] = 0.2
    input_state[2] = 0.3
    input_state[3] = 0.1
    input_state = np.tanh(input_state)
    
    result = engine.process(input_state, confidence=0.8)
    
    print(f"   Input energy: {result['field_energy']:.3f}")
    print(f"   Active attractors: {result['active_attractors']}")
    print(f"   Collapse: {result['collapse_result']['collapsed']}")
    print(f"   Collapsed to: {result['collapse_result'].get('attractor', 'None')}")
    
    print("\n4. Multiple Processing Iterations:")
    print("-" * 60)
    
    for i in range(10):
        input_state = np.random.randn(64)
        input_state = np.tanh(input_state)
        result = engine.process(input_state, confidence=0.7)
        
        print(f"   Iteration {i+1}: energy={result['field_energy']:.3f}, stable={result['field_stable']}, collapsed={result['collapse_result']['collapsed']}")
    
    print("\n5. Collapse Statistics:")
    print("-" * 60)
    
    collapse_stats = engine.collapse_controller.get_collapse_statistics()
    print(f"   Total collapses: {collapse_stats['total_collapses']}")
    print(f"   Successful collapses: {collapse_stats['successful_collapses']}")
    print(f"   Collapse rate: {collapse_stats['collapse_rate']:.3f}")
    print(f"   Attractor frequencies: {collapse_stats['attractor_frequencies']}")
    
    print("\n6. Final Statistics:")
    print("-" * 60)
    
    final_stats = engine.get_semantics_statistics()
    for key, value in final_stats.items():
        if key != "collapse_statistics":
            print(f"   {key}: {value}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demonstrate_attractor_semantics()
