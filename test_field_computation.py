"""
Test Suite for AGI Bootstrap Field-Based Computation
Tests state bit system, field network, differential solver, collapse function, and coherence engine.
"""

import pytest
import numpy as np
from field_computation import (
    StateBit, StateBitRegister, FieldNode, FieldNetwork,
    DifferentialSolver, CollapseFunction, CoherenceEngine,
    FieldComputationEngine
)


# =============================================================================
# STATE BIT TESTS
# =============================================================================

class TestStateBit:
    """Test StateBit class."""
    
    def test_initialization(self):
        bit = StateBit(
            id="test_bit",
            amplitude=1.0 + 1j,
            phase=np.pi / 4,
            probability=0.5
        )
        assert bit.id == "test_bit"
        assert bit.coherence == 1.0
    
    def test_normalization(self):
        bit = StateBit(
            id="test_bit",
            amplitude=2.0 + 2j,
            phase=0.0,
            probability=0.8
        )
        bit.normalize()
        assert abs(abs(bit.amplitude) - 1.0) < 0.01
    
    def test_evolution(self):
        bit = StateBit(
            id="test_bit",
            amplitude=1.0 + 0j,
            phase=0.0,
            probability=1.0
        )
        initial_phase = bit.phase
        bit.evolve(delta_t=0.1, hamiltonian=1.0)
        assert bit.phase != initial_phase
    
    def test_collapse(self):
        bit = StateBit(
            id="test_bit",
            amplitude=1.0 + 0j,
            phase=0.0,
            probability=1.0
        )
        result = bit.collapse()
        assert isinstance(result, bool)
        assert bit.coherence < 1.0


class TestStateBitRegister:
    """Test StateBitRegister class."""
    
    def test_initialization(self):
        register = StateBitRegister(size=8)
        assert len(register.bits) == 8
        assert register.size == 8
    
    def test_evolve(self):
        register = StateBitRegister(size=4)
        initial_phases = [bit.phase for bit in register.bits]
        register.evolve(delta_t=0.1)
        new_phases = [bit.phase for bit in register.bits]
        assert initial_phases != new_phases
    
    def test_entangle_pairs(self):
        register = StateBitRegister(size=4)
        initial_phases = [bit.phase for bit in register.bits]
        register.entangle_pairs(strength=0.5)
        new_phases = [bit.phase for bit in register.bits]
        assert initial_phases != new_phases
    
    def test_measure(self):
        register = StateBitRegister(size=4)
        measurements = register.measure()
        assert len(measurements) == 4
        assert all(isinstance(m, bool) for m in measurements)
    
    def test_get_coherence(self):
        register = StateBitRegister(size=4)
        coherence = register.get_coherence()
        assert 0.0 <= coherence <= 1.0


# =============================================================================
# FIELD NODE TESTS
# =============================================================================

class TestFieldNode:
    """Test FieldNode class."""
    
    def test_initialization(self):
        node = FieldNode(
            id="test_node",
            position=(1.0, 2.0, 3.0),
            field_value=0.5,
            gradient=(0.1, 0.2, 0.3)
        )
        assert node.id == "test_node"
        assert node.position == (1.0, 2.0, 3.0)
        assert node.field_value == 0.5
    
    def test_update_field(self):
        node = FieldNode(
            id="test_node",
            position=(0.0, 0.0, 0.0),
            field_value=0.5,
            gradient=(0.0, 0.0, 0.0),
            connections=["neighbor"]
        )
        neighbors = {
            "neighbor": FieldNode(
                id="neighbor",
                position=(1.0, 1.0, 1.0),
                field_value=1.0,
                gradient=(0.0, 0.0, 0.0)
            )
        }
        initial_value = node.field_value
        node.update_field(neighbors, diffusion_rate=0.1)
        assert node.field_value != initial_value


class TestFieldNetwork:
    """Test FieldNetwork class."""
    
    def test_initialization(self):
        network = FieldNetwork(num_nodes=50)
        assert len(network.nodes) == 50
    
    def test_evolve(self):
        network = FieldNetwork(num_nodes=20)
        initial_stats = network.get_field_statistics()
        network.evolve(steps=5)
        new_stats = network.get_field_statistics()
        # Field values should change
        assert initial_stats["avg_field_value"] != new_stats["avg_field_value"]
    
    def test_get_field_statistics(self):
        network = FieldNetwork(num_nodes=30)
        stats = network.get_field_statistics()
        assert "total_nodes" in stats
        assert "avg_field_value" in stats
        assert stats["total_nodes"] == 30


# =============================================================================
# DIFFERENTIAL SOLVER TESTS
# =============================================================================

class TestDifferentialSolver:
    """Test DifferentialSolver class."""
    
    def test_initialization(self):
        solver = DifferentialSolver(dt=0.01)
        assert solver.dt == 0.01
    
    def test_solve_ode(self):
        solver = DifferentialSolver(dt=0.01)
        
        # dy/dt = -y (exponential decay)
        def decay(y, t):
            return -y
        
        initial_state = np.array([1.0])
        trajectory = solver.solve_ode(initial_state, decay, steps=10)
        
        assert len(trajectory) == 11  # Initial + 10 steps
        assert trajectory[0][0] == 1.0
        assert trajectory[-1][0] < 1.0  # Should decay
    
    def test_solve_pde(self):
        solver = DifferentialSolver(dt=0.01)
        
        # Simple laplacian (diffusion)
        def simple_laplacian(field):
            return np.roll(field, 1, axis=0) - 2 * field + np.roll(field, -1, axis=0)
        
        field = np.random.random((10, 10))
        trajectory = solver.solve_pde(field, simple_laplacian, steps=5)
        
        assert len(trajectory) == 6  # Initial + 5 steps


# =============================================================================
# COLLAPSE FUNCTION TESTS
# =============================================================================

class TestCollapseFunction:
    """Test CollapseFunction class."""
    
    def test_initialization(self):
        collapse = CollapseFunction(threshold=0.5)
        assert collapse.threshold == 0.5
    
    def test_collapse_state(self):
        collapse = CollapseFunction(threshold=0.5)
        register = StateBitRegister(size=4)
        context = {"query": "test"}
        result = collapse.collapse_state(register, context)
        
        assert "decision" in result
        assert "measurements" in result
        assert "coherence" in result
        assert isinstance(result["decision"], bool)
    
    def test_get_collapse_statistics(self):
        collapse = CollapseFunction(threshold=0.5)
        register = StateBitRegister(size=4)
        collapse.collapse_state(register, {})
        stats = collapse.get_collapse_statistics()
        
        assert "total_collapses" in stats
        assert stats["total_collapses"] == 1


# =============================================================================
# COHERENCE ENGINE TESTS
# =============================================================================

class TestCoherenceEngine:
    """Test CoherenceEngine class."""
    
    def test_initialization(self):
        engine = CoherenceEngine(tolerance=0.1)
        assert engine.tolerance == 0.1
    
    def test_synchronize(self):
        engine = CoherenceEngine(tolerance=0.1)
        network = FieldNetwork(num_nodes=20)
        result = engine.synchronize(network, target_coherence=0.9)
        
        assert isinstance(result, (bool, np.bool_))
        assert len(engine.coherence_history) > 0
    
    def test_get_coherence_history(self):
        engine = CoherenceEngine(tolerance=0.1)
        network = FieldNetwork(num_nodes=20)
        engine.synchronize(network)
        stats = engine.get_coherence_history()
        
        assert "total_measurements" in stats
        assert "avg_coherence" in stats


# =============================================================================
# FIELD COMPUTATION ENGINE TESTS
# =============================================================================

class TestFieldComputationEngine:
    """Test FieldComputationEngine class."""
    
    def test_initialization(self):
        engine = FieldComputationEngine(register_size=8, network_size=50)
        assert engine.state_register.size == 8
        assert len(engine.field_network.nodes) == 50
    
    def test_process_input(self):
        engine = FieldComputationEngine(register_size=4, network_size=20)
        input_data = {"query": "test"}
        result = engine.process_input(input_data)
        
        assert "decision" in result
        assert "synchronized" in result
        assert "field_statistics" in result
    
    def test_get_engine_statistics(self):
        engine = FieldComputationEngine(register_size=4, network_size=20)
        stats = engine.get_engine_statistics()
        
        assert "state_register" in stats
        assert "field_network" in stats
        assert "coherence_engine" in stats
        assert "collapse_function" in stats


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
