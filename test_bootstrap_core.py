"""
Test Suite for AGI Bootstrap Core Engine
Tests all four layers: Perception, Relation, Logic, Learning
"""

import pytest
from bootstrap_core import (
    Symbol, SymbolType, SymbolSet, Tokenizer,
    Axiom, AxiomBase, LogicGate, InferenceEngine,
    Interaction, MemorySystem, Learner, BootstrapEngine
)


# =============================================================================
# LAYER 1: PERCEPTION LAYER TESTS
# =============================================================================

class TestSymbol:
    """Test Symbol class."""
    
    def test_symbol_creation(self):
        symbol = Symbol("A", SymbolType.LETTER)
        assert symbol.value == "A"
        assert symbol.symbol_type == SymbolType.LETTER
        assert symbol.id is not None
    
    def test_symbol_equality(self):
        s1 = Symbol("A", SymbolType.LETTER)
        s2 = Symbol("A", SymbolType.LETTER)
        s3 = Symbol("B", SymbolType.LETTER)
        s4 = Symbol("A", SymbolType.NUMBER)
        
        assert s1 == s2
        assert s1 != s3
        assert s1 != s4
    
    def test_symbol_hash(self):
        s1 = Symbol("A", SymbolType.LETTER)
        s2 = Symbol("A", SymbolType.LETTER)
        assert hash(s1) == hash(s2)


class TestSymbolSet:
    """Test SymbolSet class."""
    
    def test_initialization(self):
        symbol_set = SymbolSet()
        # Should have default symbols
        assert len(symbol_set.symbols) > 0
    
    def test_add_symbol(self):
        symbol_set = SymbolSet()
        new_symbol = symbol_set.add_symbol("TEST", SymbolType.WORD)
        assert new_symbol.value == "TEST"
        assert new_symbol.symbol_type == SymbolType.WORD
        assert (new_symbol.value, new_symbol.symbol_type) in symbol_set.symbols
    
    def test_get_symbol(self):
        symbol_set = SymbolSet()
        symbol = symbol_set.get_symbol("A", SymbolType.LETTER)
        assert symbol is not None
        assert symbol.value == "A"
    
    def test_get_symbols_by_type(self):
        symbol_set = SymbolSet()
        letters = symbol_set.get_symbols_by_type(SymbolType.LETTER)
        assert len(letters) == 26  # A-Z
        colors = symbol_set.get_symbols_by_type(SymbolType.COLOR)
        assert len(colors) >= 6  # RED, BLUE, GREEN, YELLOW, BLACK, WHITE
    
    def test_contains(self):
        symbol_set = SymbolSet()
        assert symbol_set.contains("A", SymbolType.LETTER)
        assert symbol_set.contains("RED", SymbolType.COLOR)
        assert not symbol_set.contains("XYZ", SymbolType.WORD)


class TestTokenizer:
    """Test Tokenizer class."""
    
    def test_tokenize_letters(self):
        symbol_set = SymbolSet()
        tokenizer = Tokenizer(symbol_set)
        tokens = tokenizer.tokenize("ABC")
        assert len(tokens) == 3
        assert all(t.symbol_type == SymbolType.LETTER for t in tokens)
    
    def test_tokenize_numbers(self):
        symbol_set = SymbolSet()
        tokenizer = Tokenizer(symbol_set)
        tokens = tokenizer.tokenize("123")
        assert len(tokens) == 3
        assert all(t.symbol_type == SymbolType.NUMBER for t in tokens)
    
    def test_tokenize_mixed(self):
        symbol_set = SymbolSet()
        tokenizer = Tokenizer(symbol_set)
        tokens = tokenizer.tokenize("A1B2")
        assert len(tokens) == 4
    
    def test_tokenize_words(self):
        symbol_set = SymbolSet()
        tokenizer = Tokenizer(symbol_set)
        tokens = tokenizer.tokenize_words("RED CIRCLE")
        assert len(tokens) == 2
        assert tokens[0].value == "RED"
        assert tokens[0].symbol_type == SymbolType.COLOR


# =============================================================================
# LAYER 2: RELATION LAYER TESTS
# =============================================================================

class TestAxiom:
    """Test Axiom class."""
    
    def test_axiom_creation(self):
        symbol_set = SymbolSet()
        a = symbol_set.get_symbol("A", SymbolType.LETTER)
        b = symbol_set.get_symbol("B", SymbolType.LETTER)
        axiom = Axiom(a, "!=", b)
        assert axiom.left == a
        assert axiom.relation == "!="
        assert axiom.right == b
        assert axiom.confidence == 1.0
    
    def test_axiom_equality(self):
        symbol_set = SymbolSet()
        a = symbol_set.get_symbol("A", SymbolType.LETTER)
        b = symbol_set.get_symbol("B", SymbolType.LETTER)
        axiom1 = Axiom(a, "!=", b)
        axiom2 = Axiom(a, "!=", b)
        assert axiom1 == axiom2


class TestAxiomBase:
    """Test AxiomBase class."""
    
    def test_initialization(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        # Should have default axioms
        assert len(axiom_base.axioms) > 0
    
    def test_identity_axioms(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        # Check that A = A exists for letters
        a = symbol_set.get_symbol("A", SymbolType.LETTER)
        axiom = axiom_base.get_axiom(a, "=", a)
        assert axiom is not None
    
    def test_distinction_axioms(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        # Check that A != B exists for distinct letters
        a = symbol_set.get_symbol("A", SymbolType.LETTER)
        b = symbol_set.get_symbol("B", SymbolType.LETTER)
        axiom = axiom_base.get_axiom(a, "!=", b)
        assert axiom is not None
    
    def test_add_axiom(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        a = symbol_set.get_symbol("A", SymbolType.LETTER)
        new_symbol = symbol_set.add_symbol("X", SymbolType.WORD)
        axiom = axiom_base.add_axiom(a, "=", new_symbol)
        assert axiom.id in axiom_base.axioms
    
    def test_check_consistency(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        a = symbol_set.get_symbol("A", SymbolType.LETTER)
        b = symbol_set.get_symbol("B", SymbolType.LETTER)
        
        # Check consistent axiom
        axiom1 = Axiom(a, "!=", b)
        assert axiom_base.check_consistency(axiom1) == True
        
        # Check inconsistent axiom (contradicts existing)
        axiom2 = Axiom(a, "=", b)
        assert axiom_base.check_consistency(axiom2) == False
    
    def test_discover_axioms_from_patterns(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        
        # Create repeated pattern
        a = symbol_set.get_symbol("A", SymbolType.LETTER)
        b = symbol_set.get_symbol("B", SymbolType.LETTER)
        observations = [(a, "NEXT", b)] * 3
        
        new_axioms = axiom_base.discover_axioms_from_patterns(observations)
        assert len(new_axioms) > 0


# =============================================================================
# LAYER 3: LOGIC ENGINE TESTS
# =============================================================================

class TestLogicGate:
    """Test LogicGate class."""
    
    def test_not_gate(self):
        assert LogicGate.NOT(True) == False
        assert LogicGate.NOT(False) == True
    
    def test_and_gate(self):
        assert LogicGate.AND(True, True) == True
        assert LogicGate.AND(True, False) == False
        assert LogicGate.AND(False, True) == False
        assert LogicGate.AND(False, False) == False
    
    def test_or_gate(self):
        assert LogicGate.OR(True, True) == True
        assert LogicGate.OR(True, False) == True
        assert LogicGate.OR(False, True) == True
        assert LogicGate.OR(False, False) == False
    
    def test_xor_gate(self):
        assert LogicGate.XOR(True, True) == False
        assert LogicGate.XOR(True, False) == True
        assert LogicGate.XOR(False, True) == True
        assert LogicGate.XOR(False, False) == False
    
    def test_implies_gate(self):
        assert LogicGate.IMPLIES(True, True) == True
        assert LogicGate.IMPLIES(True, False) == False
        assert LogicGate.IMPLIES(False, True) == True
        assert LogicGate.IMPLIES(False, False) == True


class TestInferenceEngine:
    """Test InferenceEngine class."""
    
    def test_apply_transitivity(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        engine = InferenceEngine(axiom_base)
        
        a = symbol_set.get_symbol("A", SymbolType.LETTER)
        b = symbol_set.get_symbol("B", SymbolType.LETTER)
        c = symbol_set.get_symbol("C", SymbolType.LETTER)
        
        # Add A = B and B = C
        axiom_base.add_axiom(a, "=", b)
        axiom_base.add_axiom(b, "=", c)
        
        # Should derive A = C
        conclusion = engine.apply_transitivity(a, b, c)
        assert conclusion is not None
        assert conclusion.left == a
        assert conclusion.right == c
    
    def test_check_contradiction(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        engine = InferenceEngine(axiom_base)
        
        a = symbol_set.get_symbol("A", SymbolType.LETTER)
        b = symbol_set.get_symbol("B", SymbolType.LETTER)
        
        axiom1 = Axiom(a, "=", b)
        axiom2 = Axiom(a, "!=", b)
        
        contradictions = engine.check_contradiction([axiom1, axiom2])
        assert len(contradictions) == 1


# =============================================================================
# LAYER 4: LEARNING LOOP TESTS
# =============================================================================

class TestInteraction:
    """Test Interaction class."""
    
    def test_interaction_creation(self):
        symbol_set = SymbolSet()
        symbols = [symbol_set.get_symbol("A", SymbolType.LETTER)]
        interaction = Interaction(
            input_symbols=symbols,
            applied_rules=["test"],
            result=None,
            contradiction_detected=False
        )
        assert interaction.id is not None
        assert interaction.contradiction_detected == False


class TestMemorySystem:
    """Test MemorySystem class."""
    
    def test_store_interaction(self):
        memory = MemorySystem()
        symbol_set = SymbolSet()
        symbols = [symbol_set.get_symbol("A", SymbolType.LETTER)]
        interaction = Interaction(
            input_symbols=symbols,
            applied_rules=["test"],
            result=None,
            contradiction_detected=False
        )
        memory.store_interaction(interaction)
        assert interaction.id in memory.interactions
        assert memory.success_count == 1
    
    def test_get_statistics(self):
        memory = MemorySystem()
        symbol_set = SymbolSet()
        
        # Add successful interaction
        symbols = [symbol_set.get_symbol("A", SymbolType.LETTER)]
        interaction1 = Interaction(
            input_symbols=symbols,
            applied_rules=["test"],
            result=None,
            contradiction_detected=False
        )
        memory.store_interaction(interaction1)
        
        # Add contradictory interaction
        interaction2 = Interaction(
            input_symbols=symbols,
            applied_rules=["test"],
            result=None,
            contradiction_detected=True
        )
        memory.store_interaction(interaction2)
        
        stats = memory.get_statistics()
        assert stats["total_interactions"] == 2
        assert stats["successes"] == 1
        assert stats["contradictions"] == 1


class TestLearner:
    """Test Learner class."""
    
    def test_set_dopamine(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        memory = MemorySystem()
        learner = Learner(axiom_base, memory)
        
        learner.set_dopamine(0.8)
        assert learner.dopamine_level == 0.8
        
        learner.set_dopamine(1.5)  # Should cap at 1.0
        assert learner.dopamine_level == 1.0
    
    def test_adjust_rule_weights(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        memory = MemorySystem()
        learner = Learner(axiom_base, memory)
        
        learner._adjust_rule_weights(["test_rule"], 0.5)
        assert learner.get_rule_weight("test_rule") == 1.5
    
    def test_process_interaction(self):
        symbol_set = SymbolSet()
        axiom_base = AxiomBase(symbol_set)
        memory = MemorySystem()
        learner = Learner(axiom_base, memory)
        
        symbols = [symbol_set.get_symbol("A", SymbolType.LETTER)]
        interaction = Interaction(
            input_symbols=symbols,
            applied_rules=["test_rule"],
            result=None,
            contradiction_detected=True
        )
        
        learner.process_interaction(interaction)
        assert learner.get_rule_weight("test_rule") < 1.0  # Should decrease


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestBootstrapEngine:
    """Test BootstrapEngine integration."""
    
    def test_initialization(self):
        engine = BootstrapEngine()
        assert engine.symbol_set is not None
        assert engine.tokenizer is not None
        assert engine.axiom_base is not None
        assert engine.inference_engine is not None
        assert engine.memory_system is not None
        assert engine.learner is not None
    
    def test_observe(self):
        engine = BootstrapEngine()
        symbols = engine.observe("RED CIRCLE")
        assert len(symbols) == 2
        assert symbols[0].value == "RED"
    
    def test_process_basic_input(self):
        engine = BootstrapEngine()
        result = engine.process("RED")
        assert "input" in result
        assert "symbols" in result
        assert "contradiction_detected" in result
        assert result["input"] == "RED"
    
    def test_process_with_dopamine(self):
        engine = BootstrapEngine()
        result = engine.process("RED", dopamine=0.8)
        assert engine.learner.dopamine_level == 0.8
    
    def test_get_system_state(self):
        engine = BootstrapEngine()
        state = engine.get_system_state()
        assert "total_symbols" in state
        assert "total_axioms" in state
        assert "memory_stats" in state
        assert "learning_stats" in state
        assert state["total_symbols"] > 0
        assert state["total_axioms"] > 0
    
    def test_learning_from_interactions(self):
        engine = BootstrapEngine()
        
        # Process multiple inputs to build up memory
        engine.process("RED")
        engine.process("BLUE")
        engine.process("GREEN")
        
        # Check memory has grown
        stats = engine.memory_system.get_statistics()
        assert stats["total_interactions"] == 3
    
    def test_contradiction_detection(self):
        engine = BootstrapEngine()
        
        # Manually add contradictory axioms
        symbol_set = engine.symbol_set
        a = symbol_set.get_symbol("A", SymbolType.LETTER)
        b = symbol_set.get_symbol("B", SymbolType.LETTER)
        
        engine.axiom_base.add_axiom(a, "=", b)
        engine.axiom_base.add_axiom(a, "!=", b)
        
        # Check for contradictions
        all_axioms = list(engine.axiom_base.axioms.values())
        contradictions = engine.inference_engine.check_contradiction(all_axioms)
        assert len(contradictions) > 0


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
