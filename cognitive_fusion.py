"""
Cognitive Fusion Component
Implements role-fused dynamical inference with role brains, weighted synthesis, and confidence arbitration.

Components:
- RoleBrain: Specialized brain for specific cognitive role
- WeightedSynthesizer: Combines outputs from multiple brains
- ConfidenceArbiter: Arbitrates between conflicting outputs
- CognitiveFusionEngine: Unified fusion engine
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
# ROLE BRAIN
# =============================================================================

@dataclass
class RoleBrain:
    """Specialized brain for specific cognitive role."""
    name: str
    role: str
    state_dim: int = 64
    confidence: float = 0.5
    weights: np.ndarray = field(default_factory=lambda: np.zeros(64))
    active: bool = True
    
    def __post_init__(self):
        """Initialize random weights."""
        self.weights = np.random.randn(self.state_dim)
        self.weights = self.weights / np.linalg.norm(self.weights)
    
    def process(self, input_state: np.ndarray) -> Dict[str, Any]:
        """Process input through role brain."""
        if not self.active:
            return {
                "output": np.zeros_like(input_state),
                "confidence": 0.0,
                "role": self.role
            }
        
        # Apply role-specific transformation
        transformed = np.dot(self.weights, input_state)
        
        # Ensure output is array (not scalar)
        if np.isscalar(transformed):
            transformed = np.array([transformed])
        
        # Normalize
        transformed = np.tanh(transformed)
        
        return {
            "output": transformed,
            "confidence": self.confidence,
            "role": self.role
        }
    
    def update_confidence(self, performance: float):
        """Update confidence based on performance."""
        # Smooth confidence update
        self.confidence = 0.9 * self.confidence + 0.1 * performance
        self.confidence = np.clip(self.confidence, 0.0, 1.0)


# =============================================================================
# WEIGHTED SYNTHESIZER
# =============================================================================

class WeightedSynthesizer:
    """Combines outputs from multiple brains using weighted synthesis."""
    
    def __init__(self):
        self.synthesis_weights: Dict[str, float] = {}
        self.adaptation_rate = 0.1
    
    def set_weight(self, brain_name: str, weight: float):
        """Set synthesis weight for a brain."""
        self.synthesis_weights[brain_name] = np.clip(weight, 0.0, 1.0)
    
    def synthesize(self, brain_outputs: Dict[str, np.ndarray]) -> np.ndarray:
        """Synthesize outputs from multiple brains."""
        if not brain_outputs:
            return np.zeros(64)
        
        # Get output dimensions
        first_output = list(brain_outputs.values())[0]
        output_dim = len(first_output)
        
        # Initialize synthesis
        synthesized = np.zeros(output_dim)
        total_weight = 0.0
        
        for brain_name, output in brain_outputs.items():
            weight = self.synthesis_weights.get(brain_name, 1.0)
            synthesized += weight * output
            total_weight += weight
        
        if total_weight > 0:
            synthesized /= total_weight
        
        return synthesized
    
    def adapt_weights(self, performance_metrics: Dict[str, float]):
        """Adapt weights based on performance metrics."""
        for brain_name, performance in performance_metrics.items():
            current_weight = self.synthesis_weights.get(brain_name, 0.5)
            # Move weight toward performance
            new_weight = current_weight + self.adaptation_rate * (performance - current_weight)
            self.set_weight(brain_name, new_weight)


# =============================================================================
# CONFIDENCE ARBITRATOR
# =============================================================================

class ConfidenceArbiter:
    """Arbitrates between conflicting outputs based on confidence."""
    
    def __init__(self):
        self.arbitration_history: List[Dict[str, Any]] = []
    
    def arbitrate(self, brain_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Arbitrate between multiple brain results."""
        if not brain_results:
            return {
                "selected_output": np.zeros(64),
                "selected_brain": None,
                "confidence": 0.0
            }
        
        # Sort by confidence
        sorted_results = sorted(brain_results, key=lambda x: x.get("confidence", 0.0), reverse=True)
        
        # Select highest confidence
        selected = sorted_results[0]
        
        # Record arbitration
        self.arbitration_history.append({
            "timestamp": time.time(),
            "selected_role": selected.get("role"),
            "confidence": selected.get("confidence"),
            "num_candidates": len(brain_results)
        })
        
        return {
            "selected_output": selected["output"],
            "selected_brain": selected["role"],
            "confidence": selected["confidence"],
            "num_candidates": len(brain_results)
        }
    
    def get_arbitration_statistics(self) -> Dict[str, Any]:
        """Get arbitration statistics."""
        if not self.arbitration_history:
            return {"total_arbitrations": 0}
        
        role_counts = defaultdict(int)
        for record in self.arbitration_history:
            role_counts[record["selected_role"]] += 1
        
        return {
            "total_arbitrations": len(self.arbitration_history),
            "role_selection_counts": dict(role_counts),
            "avg_confidence": np.mean([r["confidence"] for r in self.arbitration_history])
        }


# =============================================================================
# COGNITIVE FUSION ENGINE
# =============================================================================

class CognitiveFusionEngine:
    """Unified cognitive fusion engine."""
    
    def __init__(self):
        self.role_brains: Dict[str, RoleBrain] = {}
        self.synthesizer = WeightedSynthesizer()
        self.arbiter = ConfidenceArbiter()
        self.is_integrated = USING_REAL_BRAIN_SYSTEM
        self._initialize_role_brains()
    
    def _initialize_role_brains(self):
        """Initialize role brains for different cognitive functions."""
        roles = [
            ("reasoning", "reasoning_brain"),
            ("memory", "memory_brain"),
            ("perception", "perception_brain"),
            ("attention", "attention_brain"),
            ("language", "language_brain"),
            ("motor", "motor_brain"),
            ("emotion", "emotion_brain")
        ]
        
        for role, name in roles:
            brain = RoleBrain(name=name, role=role, state_dim=64)
            self.role_brains[name] = brain
            self.synthesizer.set_weight(name, 1.0 / len(roles))
    
    def process(self, input_state: np.ndarray) -> Dict[str, Any]:
        """Process input through cognitive fusion engine."""
        # Process through all role brains
        brain_outputs = {}
        brain_results = []
        
        for brain_name, brain in self.role_brains.items():
            result = brain.process(input_state)
            brain_outputs[brain_name] = result["output"]
            brain_results.append(result)
        
        # Synthesize outputs
        synthesized_output = self.synthesizer.synthesize(brain_outputs)
        
        # Arbitrate for final decision
        arbitration_result = self.arbiter.arbitrate(brain_results)
        
        # Calculate ensemble confidence
        ensemble_confidence = np.mean([r["confidence"] for r in brain_results])
        
        return {
            "synthesized_output": synthesized_output,
            "arbitrated_output": arbitration_result["selected_output"],
            "selected_brain": arbitration_result["selected_brain"],
            "arbitration_confidence": arbitration_result["confidence"],
            "ensemble_confidence": ensemble_confidence,
            "all_outputs": brain_outputs,
            "is_integrated": self.is_integrated
        }
    
    def update_brain_confidences(self, performance_metrics: Dict[str, float]):
        """Update brain confidences based on performance."""
        for brain_name, performance in performance_metrics.items():
            if brain_name in self.role_brains:
                self.role_brains[brain_name].update_confidence(performance)
    
    def adapt_synthesis_weights(self, performance_metrics: Dict[str, float]):
        """Adapt synthesis weights based on performance."""
        self.synthesizer.adapt_weights(performance_metrics)
    
    def get_fusion_statistics(self) -> Dict[str, Any]:
        """Get fusion engine statistics."""
        brain_stats = {}
        for name, brain in self.role_brains.items():
            brain_stats[name] = {
                "role": brain.role,
                "confidence": brain.confidence,
                "active": brain.active
            }
        
        synthesis_weights = self.synthesizer.synthesis_weights.copy()
        arbitration_stats = self.arbiter.get_arbitration_statistics()
        
        return {
            "total_role_brains": len(self.role_brains),
            "brain_statistics": brain_stats,
            "synthesis_weights": synthesis_weights,
            "arbitration_statistics": arbitration_stats,
            "is_integrated": self.is_integrated
        }


# =============================================================================
# DEMONSTRATION
# =============================================================================

def demonstrate_cognitive_fusion():
    """Demonstrate cognitive fusion capabilities."""
    print("=" * 60)
    print("Cognitive Fusion - Demonstration")
    print("=" * 60)
    
    print(f"\nUsing Real Brain System: {USING_REAL_BRAIN_SYSTEM}")
    
    # Initialize cognitive fusion engine
    engine = CognitiveFusionEngine()
    print(f"Integration Status: {'INTEGRATED' if engine.is_integrated else 'STANDALONE'}")
    
    print("\n1. Engine Statistics:")
    print("-" * 60)
    stats = engine.get_fusion_statistics()
    print(f"   Total role brains: {stats['total_role_brains']}")
    
    for name, brain_stat in stats['brain_statistics'].items():
        print(f"   {name}: role={brain_stat['role']}, confidence={brain_stat['confidence']:.3f}")
    
    print("\n2. Synthesis Weights:")
    print("-" * 60)
    for brain_name, weight in stats['synthesis_weights'].items():
        print(f"   {brain_name}: {weight:.3f}")
    
    print("\n3. Input Processing:")
    print("-" * 60)
    
    # Create random input state
    input_state = np.random.randn(64)
    input_state = np.tanh(input_state)
    
    result = engine.process(input_state)
    
    print(f"   Input state norm: {np.linalg.norm(input_state):.3f}")
    print(f"   Synthesized output norm: {np.linalg.norm(result['synthesized_output']):.3f}")
    print(f"   Arbitrated output norm: {np.linalg.norm(result['arbitrated_output']):.3f}")
    print(f"   Selected brain: {result['selected_brain']}")
    print(f"   Arbitration confidence: {result['arbitration_confidence']:.3f}")
    print(f"   Ensemble confidence: {result['ensemble_confidence']:.3f}")
    
    print("\n4. Multiple Processing Iterations:")
    print("-" * 60)
    
    for i in range(5):
        input_state = np.random.randn(64)
        input_state = np.tanh(input_state)
        result = engine.process(input_state)
        
        print(f"   Iteration {i+1}: selected={result['selected_brain']}, confidence={result['arbitration_confidence']:.3f}")
    
    print("\n5. Confidence Adaptation:")
    print("-" * 60)
    
    # Simulate performance feedback
    performance_metrics = {
        "reasoning_brain": 0.8,
        "memory_brain": 0.7,
        "perception_brain": 0.9,
        "attention_brain": 0.6,
        "language_brain": 0.85,
        "motor_brain": 0.5,
        "emotion_brain": 0.75
    }
    
    engine.update_brain_confidences(performance_metrics)
    engine.adapt_synthesis_weights(performance_metrics)
    
    new_stats = engine.get_fusion_statistics()
    print("   Updated brain confidences:")
    for name, brain_stat in new_stats['brain_statistics'].items():
        print(f"   {name}: {brain_stat['confidence']:.3f}")
    
    print("\n6. Final Statistics:")
    print("-" * 60)
    
    for key, value in new_stats.items():
        if key != "brain_statistics":
            print(f"   {key}: {value}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demonstrate_cognitive_fusion()
