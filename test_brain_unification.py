"""
Test Suite for AGI Bootstrap Brain Unification
Tests unified orchestrator and brain unification engine.
"""

import pytest
from brain_unification import (
    BrainCapability, BrainAdapter, BootstrapAdapter, IntegrationAdapter,
    FieldAdapter, PreVerseAdapter, ComprehensiveBrainAdapter,
    UnifiedOrchestrator, BrainUnificationEngine
)


# =============================================================================
# BRAIN CAPABILITY TESTS
# =============================================================================

class TestBrainCapability:
    """Test BrainCapability class."""
    
    def test_capability_constants(self):
        assert hasattr(BrainCapability, 'SYMBOLIC_REASONING')
        assert hasattr(BrainCapability, 'LANGUAGE_PROCESSING')
        assert hasattr(BrainCapability, 'FIELD_DYNAMICS')


# =============================================================================
# BRAIN ADAPTER TESTS
# =============================================================================

class TestBrainAdapter:
    """Test BrainAdapter class."""
    
    def test_initialization(self):
        adapter = BrainAdapter(
            name="test_adapter",
            capabilities=["test_capability"]
        )
        assert adapter.name == "test_adapter"
        assert adapter.active == True
        assert adapter.priority == 1


# =============================================================================
# UNIFIED ORCHESTRATOR TESTS
# =============================================================================

class TestUnifiedOrchestrator:
    """Test UnifiedOrchestrator class."""
    
    def test_initialization(self):
        orchestrator = UnifiedOrchestrator()
        assert len(orchestrator.adapters) > 0
        assert len(orchestrator.capability_map) > 0
    
    def test_get_adapter_for_capability(self):
        orchestrator = UnifiedOrchestrator()
        adapter = orchestrator.get_adapter_for_capability(BrainCapability.SYMBOLIC_REASONING)
        assert adapter is not None
        assert adapter in orchestrator.adapters
    
    def test_orchestrate_with_capability(self):
        orchestrator = UnifiedOrchestrator()
        result = orchestrator.orchestrate(
            {"query": "test"},
            capability=BrainCapability.SYMBOLIC_REASONING
        )
        assert "success" in result
    
    def test_orchestrate_without_capability(self):
        orchestrator = UnifiedOrchestrator()
        result = orchestrator.orchestrate({"query": "test"})
        assert "success" in result
        assert "total_adapters" in result
        assert "successful_adapters" in result
    
    def test_get_orchestrator_statistics(self):
        orchestrator = UnifiedOrchestrator()
        stats = orchestrator.get_orchestrator_statistics()
        assert "total_adapters" in stats
        assert "adapter_statistics" in stats
        assert "capability_map" in stats


# =============================================================================
# BRAIN UNIFICATION ENGINE TESTS
# =============================================================================

class TestBrainUnificationEngine:
    """Test BrainUnificationEngine class."""
    
    def test_initialization(self):
        engine = BrainUnificationEngine()
        assert engine.orchestrator is not None
        assert engine.is_integrated == engine.orchestrator.is_integrated
    
    def test_process_query(self):
        engine = BrainUnificationEngine()
        result = engine.process_query("test query")
        assert "query" in result
        assert "result" in result
        assert "is_integrated" in result
    
    def test_process_query_with_capability(self):
        engine = BrainUnificationEngine()
        result = engine.process_query(
            "test query",
            capability=BrainCapability.SYMBOLIC_REASONING
        )
        assert "capability" in result
        assert result["capability"] == BrainCapability.SYMBOLIC_REASONING
    
    def test_get_system_statistics(self):
        engine = BrainUnificationEngine()
        stats = engine.get_system_statistics()
        assert "orchestrator" in stats
        assert "is_integrated" in stats


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
