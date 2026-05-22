"""
Test Suite for AGI Bootstrap Brain Integration
Tests symbol-to-region mapping, axiom-to-synapse conversion, logic integration, and DNA connection.
"""

import pytest
from brain_integration import (
    BrainRegion, SymbolToRegionMapper, AxiomToSynapseConverter,
    SynapticWeight, LogicToCognitiveIntegrator, LearningToDNAConnector,
    BrainIntegrationEngine
)
from bootstrap_core import (
    Symbol, SymbolType, SymbolSet, Axiom, AxiomBase,
    InferenceEngine, Learner, BootstrapEngine
)


# =============================================================================
# SYMBOL TO REGION MAPPER TESTS
# =============================================================================

class TestSymbolToRegionMapper:
    """Test SymbolToRegionMapper class."""
    
    def test_initialization(self):
        symbol_set = SymbolSet()
        mapper = SymbolToRegionMapper(symbol_set)
        assert len(mapper.mappings) > 0
    
    def test_map_symbol_to_region(self):
        symbol_set = SymbolSet()
        mapper = SymbolToRegionMapper(symbol_set)
        
        letter_symbol = symbol_set.get_symbol("A", SymbolType.LETTER)
        region = mapper.map_symbol_to_region(letter_symbol)
        
        assert region == BrainRegion.CORTEX
    
    def test_map_color_to_visual_cortex(self):
        symbol_set = SymbolSet()
        mapper = SymbolToRegionMapper(symbol_set)
        
        color_symbol = symbol_set.get_symbol("RED", SymbolType.COLOR)
        region = mapper.map_symbol_to_region(color_symbol)
        
        assert region == BrainRegion.VISUAL_CORTEX
    
    def test_map_symbols_to_regions(self):
        symbol_set = SymbolSet()
        mapper = SymbolToRegionMapper(symbol_set)
        
        symbols = [
            symbol_set.get_symbol("A", SymbolType.LETTER),
            symbol_set.get_symbol("RED", SymbolType.COLOR)
        ]
        region_mapping = mapper.map_symbols_to_regions(symbols)
        
        assert BrainRegion.CORTEX in region_mapping
        assert BrainRegion.VISUAL_CORTEX in region_mapping


# =============================================================================
# AXIOM TO SYNAPSE CONVERTER TESTS
# =============================================================================

class TestSynapticWeight:
    """Test SynapticWeight class."""
    
    def test_synaptic_weight_creation(self):
        weight = SynapticWeight("neuron_1", "neuron_2", 0.9)
        assert weight.source_neuron_id == "neuron_1"
        assert weight.target_neuron_id == "neuron_2"
        assert weight.weight == 0.9


class TestAxiomToSynapseConverter:
    """Test AxiomToSynapseConverter class."""
    
    def test_initialization(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        converter = AxiomToSynapseConverter(axiom_base)
        assert converter.axiom_base == axiom_base
    
    def test_convert_equality_axiom(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        converter = AxiomToSynapseConverter(axiom_base)
        
        a = symbol_set.get_symbol("A", SymbolType.LETTER)
        axiom = Axiom(a, "=", a)
        
        synapses = converter.convert_axiom_to_synapse(axiom)
        assert len(synapses) == 1
        assert synapses[0].weight > 0  # Excitatory
    
    def test_convert_inequality_axiom(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        converter = AxiomToSynapseConverter(axiom_base)
        
        a = symbol_set.get_symbol("A", SymbolType.LETTER)
        b = symbol_set.get_symbol("B", SymbolType.LETTER)
        axiom = Axiom(a, "!=", b)
        
        synapses = converter.convert_axiom_to_synapse(axiom)
        assert len(synapses) == 1
        assert synapses[0].weight < 0  # Inhibitory
    
    def test_convert_all_axioms(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        converter = AxiomToSynapseConverter(axiom_base)
        
        synapses = converter.convert_all_axioms()
        assert len(synapses) > 0
    
    def test_get_synaptic_statistics(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        converter = AxiomToSynapseConverter(axiom_base)
        
        converter.convert_all_axioms()
        stats = converter.get_synaptic_statistics()
        
        assert "total_synapses" in stats
        assert "avg_weight" in stats
        assert "excitatory_count" in stats
        assert "inhibitory_count" in stats


# =============================================================================
# LOGIC TO COGNITIVE INTEGRATOR TESTS
# =============================================================================

class TestLogicToCognitiveIntegrator:
    """Test LogicToCognitiveIntegrator class."""
    
    def test_initialization(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        inference_engine = InferenceEngine(axiom_base)
        integrator = LogicToCognitiveIntegrator(inference_engine)
        assert integrator.inference_engine == inference_engine
    
    def test_apply_fast_logic(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        inference_engine = InferenceEngine(axiom_base)
        integrator = LogicToCognitiveIntegrator(inference_engine)
        
        context = {"conditions": [True, True, True]}
        result = integrator._apply_fast_logic("test", context)
        
        assert result["result"] == True
        assert result["method"] == "logic_gate_and"
    
    def test_apply_fast_logic_with_false(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        inference_engine = InferenceEngine(axiom_base)
        integrator = LogicToCognitiveIntegrator(inference_engine)
        
        context = {"conditions": [True, False, True]}
        result = integrator._apply_fast_logic("test", context)
        
        assert result["result"] == False
    
    def test_apply_logic_to_query(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        inference_engine = InferenceEngine(axiom_base)
        integrator = LogicToCognitiveIntegrator(inference_engine)
        
        context = {"axioms": [], "conditions": [True]}
        result = integrator.apply_logic_to_query("test query", context)
        
        assert "fast_reasoning" in result
        assert "deep_reasoning" in result
        assert "query" in result
    
    def test_get_reasoning_statistics(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        inference_engine = InferenceEngine(axiom_base)
        integrator = LogicToCognitiveIntegrator(inference_engine)
        
        integrator.apply_logic_to_query("test", {"axioms": [], "conditions": [True]})
        stats = integrator.get_reasoning_statistics()
        
        assert "total_reasoning_operations" in stats


# =============================================================================
# LEARNING TO DNA CONNECTOR TESTS
# =============================================================================

class TestLearningToDNAConnector:
    """Test LearningToDNAConnector class."""
    
    def test_initialization(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        memory_system = type('obj', (object,), {
            'interactions': {},
            'contradiction_count': 0,
            'success_count': 0
        })()
        learner = Learner(axiom_base, memory_system)
        connector = LearningToDNAConnector(learner)
        assert connector.learner == learner
    
    def test_extract_learning_to_dna(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        memory_system = type('obj', (object,), {
            'interactions': {},
            'contradiction_count': 0,
            'success_count': 0
        })()
        learner = Learner(axiom_base, memory_system)
        connector = LearningToDNAConnector(learner)
        
        dna_hash = connector.extract_learning_to_dna()
        assert dna_hash is not None
        assert isinstance(dna_hash, str)
    
    def test_get_dna_statistics(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        memory_system = type('obj', (object,), {
            'interactions': {},
            'contradiction_count': 0,
            'success_count': 0
        })()
        learner = Learner(axiom_base, memory_system)
        connector = LearningToDNAConnector(learner)
        
        connector.extract_learning_to_dna()
        stats = connector.get_dna_statistics()
        
        assert "dna_length" in stats
        assert "dna_hash" in stats


# =============================================================================
# BRAIN INTEGRATION ENGINE TESTS
# =============================================================================

class TestBrainIntegrationEngine:
    """Test BrainIntegrationEngine class."""
    
    def test_initialization(self):
        bootstrap_engine = BootstrapEngine()
        integration_engine = BrainIntegrationEngine(bootstrap_engine)
        
        assert integration_engine.bootstrap_engine == bootstrap_engine
        assert integration_engine.region_mapper is not None
        assert integration_engine.synapse_converter is not None
        assert integration_engine.logic_integrator is not None
        assert integration_engine.dna_connector is not None
    
    def test_integrate_symbols_to_regions(self):
        bootstrap_engine = BootstrapEngine()
        integration_engine = BrainIntegrationEngine(bootstrap_engine)
        
        symbols = bootstrap_engine.observe("RED")
        region_mapping = integration_engine.integrate_symbols_to_regions(symbols)
        
        assert isinstance(region_mapping, dict)
        assert len(region_mapping) > 0
    
    def test_integrate_axioms_to_synapses(self):
        bootstrap_engine = BootstrapEngine()
        integration_engine = BrainIntegrationEngine(bootstrap_engine)
        
        synapses = integration_engine.integrate_axioms_to_synapses()
        assert len(synapses) > 0
    
    def test_integrate_logic_to_cognitive(self):
        bootstrap_engine = BootstrapEngine()
        integration_engine = BrainIntegrationEngine(bootstrap_engine)
        
        context = {"axioms": [], "conditions": [True]}
        result = integration_engine.integrate_logic_to_cognitive("test", context)
        
        assert "fast_reasoning" in result
        assert "deep_reasoning" in result
    
    def test_integrate_learning_to_dna(self):
        bootstrap_engine = BootstrapEngine()
        integration_engine = BrainIntegrationEngine(bootstrap_engine)
        
        dna_hash = integration_engine.integrate_learning_to_dna()
        assert dna_hash is not None
    
    def test_process_query_with_brain(self):
        bootstrap_engine = BootstrapEngine()
        integration_engine = BrainIntegrationEngine(bootstrap_engine)
        
        result = integration_engine.process_query_with_brain("RED")
        
        assert "query" in result
        assert "symbols" in result
        assert "region_mapping" in result
        assert "reasoning" in result
        assert "dna_hash" in result
    
    def test_get_integration_statistics(self):
        bootstrap_engine = BootstrapEngine()
        integration_engine = BrainIntegrationEngine(bootstrap_engine)
        
        stats = integration_engine.get_integration_statistics()
        
        assert "region_mapping" in stats
        assert "synaptic_conversion" in stats
        assert "logic_integration" in stats
        assert "dna_connection" in stats


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
