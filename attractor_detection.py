"""
Attractor Detection System
Implements attractor detection for continuous-state fields to identify stable states and energy minima.

Components:
- AttractorDetector: Detects attractors in state space
- EnergyLandscape: Models energy landscape of field
- BasinAnalysis: Analyzes basins of attraction
- AttractorDetectionEngine: Unified detection system
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
# ATTRACTOR DETECTOR
# =============================================================================

@dataclass
class DetectedAttractor:
    """Detected attractor in state space."""
    center: np.ndarray
    radius: float
    energy: float
    stability: float
    visit_count: int = 0
    
    def distance_to(self, state: np.ndarray) -> float:
        """Calculate distance from state to attractor."""
        return np.linalg.norm(state - self.center)
    
    def is_in_basin(self, state: np.ndarray) -> bool:
        """Check if state is in basin."""
        return self.distance_to(state) < self.radius


class AttractorDetector:
    """Detects attractors in state space."""
    
    def __init__(self, state_dim: int = 64, min_radius: float = 0.1, max_radius: float = 0.5):
        self.state_dim = state_dim
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.attractors: List[DetectedAttractor] = []
        self.visit_history: List[np.ndarray] = []
    
    def add_state_sample(self, state: np.ndarray):
        """Add state sample for analysis."""
        self.visit_history.append(state.copy())
        if len(self.visit_history) > 1000:
            self.visit_history.pop(0)
    
    def detect_attractors(self, energy_func, min_samples: int = 10) -> List[DetectedAttractor]:
        """Detect attractors from visit history."""
        if len(self.visit_history) < min_samples:
            return self.attractors.copy()
        
        # Cluster states using simple distance-based clustering
        clusters = self._cluster_states()
        
        # Convert clusters to attractors
        new_attractors = []
        for cluster_center, cluster_states in clusters.items():
            # Convert tuple to numpy array
            center_array = np.array(cluster_center)
            energy = energy_func(center_array)
            radius = self._estimate_radius(center_array, cluster_states)
            stability = self._estimate_stability(cluster_states)
            
            attractor = DetectedAttractor(
                center=center_array,
                radius=radius,
                energy=energy,
                stability=stability
            )
            new_attractors.append(attractor)
        
        self.attractors = new_attractors
        return self.attractors
    
    def _cluster_states(self, cluster_distance: float = 0.3) -> Dict[Tuple, List[np.ndarray]]:
        """Cluster states by distance."""
        clusters: Dict[Tuple, List[np.ndarray]] = {}
        
        for state in self.visit_history:
            # Round state to create key
            key = tuple(np.round(state / cluster_distance) * cluster_distance)
            
            if key not in clusters:
                clusters[key] = []
            clusters[key].append(state)
        
        # Merge nearby clusters
        merged_clusters = {}
        for key, states in clusters.items():
            center = np.mean(states, axis=0)
            merged_key = tuple(np.round(center / cluster_distance) * cluster_distance)
            
            if merged_key not in merged_clusters:
                merged_clusters[merged_key] = []
            merged_clusters[merged_key].extend(states)
        
        # Calculate actual centers
        final_clusters = {}
        for key, states in merged_clusters.items():
            center = np.mean(states, axis=0)
            final_clusters[tuple(center)] = states
        
        return final_clusters
    
    def _estimate_radius(self, center: np.ndarray, states: List[np.ndarray]) -> float:
        """Estimate basin radius from cluster."""
        distances = [np.linalg.norm(s - center) for s in states]
        max_dist = max(distances) if distances else 0
        return np.clip(max_dist, self.min_radius, self.max_radius)
    
    def _estimate_stability(self, states: List[np.ndarray]) -> float:
        """Estimate stability from cluster variance."""
        if len(states) < 2:
            return 1.0
        
        variance = np.var(states, axis=0)
        avg_variance = np.mean(variance)
        # Lower variance = higher stability
        stability = 1.0 / (1.0 + avg_variance)
        return stability
    
    def find_nearest_attractor(self, state: np.ndarray) -> Optional[DetectedAttractor]:
        """Find nearest attractor to state."""
        if not self.attractors:
            return None
        
        nearest = None
        min_distance = float('inf')
        
        for attractor in self.attractors:
            distance = attractor.distance_to(state)
            if distance < min_distance:
                min_distance = distance
                nearest = attractor
        
        return nearest


# =============================================================================
# ENERGY LANDSCAPE
# =============================================================================

class EnergyLandscape:
    """Models energy landscape of field."""
    
    def __init__(self, state_dim: int = 64):
        self.state_dim = state_dim
        self.energy_samples: List[Tuple[np.ndarray, float]] = []
        self.energy_function = None
    
    def set_energy_function(self, func):
        """Set energy function E(state)."""
        self.energy_function = func
    
    def sample_energy(self, state: np.ndarray):
        """Sample energy at state."""
        if self.energy_function:
            energy = self.energy_function(state)
        else:
            energy = -np.sum(state ** 2)
        
        self.energy_samples.append((state.copy(), energy))
        if len(self.energy_samples) > 1000:
            self.energy_samples.pop(0)
    
    def get_energy_at(self, state: np.ndarray) -> float:
        """Get energy at state."""
        if self.energy_function:
            return self.energy_function(state)
        return -np.sum(state ** 2)
    
    def find_local_minima(self, threshold: float = 0.1) -> List[np.ndarray]:
        """Find local energy minima."""
        if len(self.energy_samples) < 10:
            return []
        
        # Simple local minima detection
        minima = []
        
        for i in range(1, len(self.energy_samples) - 1):
            prev_energy = self.energy_samples[i-1][1]
            curr_energy = self.energy_samples[i][1]
            next_energy = self.energy_samples[i+1][1]
            
            if curr_energy < prev_energy and curr_energy < next_energy:
                # Local minimum
                minima.append(self.energy_samples[i][0])
        
        # Filter by energy threshold
        filtered = []
        for minimum in minima:
            energy = self.get_energy_at(minimum)
            if energy < threshold:
                filtered.append(minimum)
        
        return filtered
    
    def get_gradient(self, state: np.ndarray, epsilon: float = 0.01) -> np.ndarray:
        """Calculate energy gradient at state."""
        gradient = np.zeros(self.state_dim)
        
        for i in range(self.state_dim):
            # Finite difference
            state_plus = state.copy()
            state_plus[i] += epsilon
            energy_plus = self.get_energy_at(state_plus)
            
            state_minus = state.copy()
            state_minus[i] -= epsilon
            energy_minus = self.get_energy_at(state_minus)
            
            gradient[i] = (energy_plus - energy_minus) / (2 * epsilon)
        
        return gradient


# =============================================================================
# BASIN ANALYSIS
# =============================================================================

class BasinAnalysis:
    """Analyzes basins of attraction."""
    
    def __init__(self):
        self.basin_volumes: Dict[int, float] = {}
        self.basin_boundaries: Dict[Tuple, List[np.ndarray]] = {}
    
    def analyze_basin(self, attractor: DetectedAttractor, samples: List[np.ndarray]) -> Dict[str, Any]:
        """Analyze basin for attractor."""
        in_basin = [s for s in samples if attractor.is_in_basin(s)]
        basin_volume = len(in_basin) / len(samples) if samples else 0
        
        # Calculate basin center
        if in_basin:
            basin_center = np.mean(in_basin, axis=0)
        else:
            basin_center = attractor.center
        
        return {
            "attractor_center": attractor.center,
            "basin_volume": basin_volume,
            "basin_center": basin_center,
            "samples_in_basin": len(in_basin),
            "total_samples": len(samples)
        }
    
    def estimate_boundary(self, attractor: DetectedAttractor, samples: List[np.ndarray]) -> List[np.ndarray]:
        """Estimate basin boundary points."""
        boundary_points = []
        
        for sample in samples:
            distance = attractor.distance_to(sample)
            # Points near the boundary (within 10% of radius)
            if abs(distance - attractor.radius) < 0.1 * attractor.radius:
                boundary_points.append(sample)
        
        return boundary_points


# =============================================================================
# ATTRACTOR DETECTION ENGINE
# =============================================================================

class AttractorDetectionEngine:
    """Unified attractor detection system."""
    
    def __init__(self, state_dim: int = 64):
        self.state_dim = state_dim
        self.detector = AttractorDetector(state_dim)
        self.landscape = EnergyLandscape(state_dim)
        self.basin_analyzer = BasinAnalysis()
        self.is_integrated = USING_REAL_BRAIN_SYSTEM
        self.detection_history: List[Dict[str, Any]] = []
    
    def process_state(self, state: np.ndarray) -> Dict[str, Any]:
        """Process state through detection pipeline."""
        # Add to detector
        self.detector.add_state_sample(state)
        
        # Sample energy
        self.landscape.sample_energy(state)
        
        # Detect attractors
        attractors = self.detector.detect_attractors(self.landscape.get_energy_at)
        
        # Find nearest attractor
        nearest = self.detector.find_nearest_attractor(state)
        
        result = {
            "state": state.copy(),
            "energy": self.landscape.get_energy_at(state),
            "nearest_attractor": nearest.center.tolist() if nearest else None,
            "distance_to_attractor": nearest.distance_to(state) if nearest else float('inf'),
            "total_attractors": len(attractors),
            "is_integrated": self.is_integrated
        }
        
        self.detection_history.append(result)
        return result
    
    def analyze_attractor_dynamics(self, states: List[np.ndarray]) -> Dict[str, Any]:
        """Analyze attractor dynamics over state trajectory."""
        # Process all states
        for state in states:
            self.process_state(state)
        
        # Detect attractors
        attractors = self.detector.detect_attractors(self.landscape.get_energy_at)
        
        # Analyze basins
        basin_analyses = []
        for attractor in attractors:
            analysis = self.basin_analyzer.analyze_basin(attractor, states)
            basin_analyses.append(analysis)
        
        return {
            "attractors": attractors,
            "basin_analyses": basin_analyses,
            "total_attractors": len(attractors),
            "is_integrated": self.is_integrated
        }
    
    def get_detection_statistics(self) -> Dict[str, Any]:
        """Get detection statistics."""
        if not self.detection_history:
            return {"total_processed": 0}
        
        energies = [h["energy"] for h in self.detection_history]
        distances = [h["distance_to_attractor"] for h in self.detection_history if h["distance_to_attractor"] != float('inf')]
        
        return {
            "total_processed": len(self.detection_history),
            "avg_energy": np.mean(energies),
            "avg_distance_to_attractor": np.mean(distances) if distances else float('inf'),
            "current_attractors": len(self.detector.attractors),
            "is_integrated": self.is_integrated
        }


# =============================================================================
# DEMONSTRATION
# =============================================================================

def demonstrate_attractor_detection():
    """Demonstrate attractor detection capabilities."""
    print("=" * 60)
    print("Attractor Detection System - Demonstration")
    print("=" * 60)
    
    print(f"\nUsing Real Brain System: {USING_REAL_BRAIN_SYSTEM}")
    
    # Initialize attractor detection engine
    engine = AttractorDetectionEngine(state_dim=64)
    print(f"Integration Status: {'INTEGRATED' if engine.is_integrated else 'STANDALONE'}")
    
    print("\n1. State Processing:")
    print("-" * 60)
    
    # Generate sample states
    states = []
    for i in range(20):
        state = np.random.randn(64)
        state = np.tanh(state)
        states.append(state)
        result = engine.process_state(state)
        
        print(f"   Sample {i+1}: energy={result['energy']:.3f}, attractors={result['total_attractors']}")
    
    print("\n2. Attractor Dynamics Analysis:")
    print("-" * 60)
    
    dynamics_result = engine.analyze_attractor_dynamics(states)
    
    print(f"   Total attractors detected: {dynamics_result['total_attractors']}")
    
    for i, attractor in enumerate(dynamics_result['attractors']):
        print(f"   Attractor {i+1}: radius={attractor.radius:.3f}, energy={attractor.energy:.3f}, stability={attractor.stability:.3f}")
    
    print("\n3. Basin Analyses:")
    print("-" * 60)
    
    for i, analysis in enumerate(dynamics_result['basin_analyses']):
        print(f"   Basin {i+1}: volume={analysis['basin_volume']:.3f}, samples={analysis['samples_in_basin']}/{analysis['total_samples']}")
    
    print("\n4. Detection Statistics:")
    print("-" * 60)
    
    stats = engine.get_detection_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n5. Energy Landscape:")
    print("-" * 60)
    
    # Find local minima
    minima = engine.landscape.find_local_minima(threshold=-10.0)
    print(f"   Local minima found: {len(minima)}")
    
    print("\n6. Gradient Analysis:")
    print("-" * 60)
    
    if states:
        test_state = states[0]
        gradient = engine.landscape.get_gradient(test_state)
        print(f"   Gradient norm: {np.linalg.norm(gradient):.3f}")
        print(f"   Gradient direction: {gradient[:5]}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demonstrate_attractor_detection()
