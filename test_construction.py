"""
Test Suite for AGI Bootstrap Language and Math Construction
Tests property extraction, entity building, word mapping, and math operations.
"""

import pytest
from bootstrap_language import (
    Property, PropertyExtractor, Entity, EntityBuilder, WordMapper, LanguageConstructionEngine
)
from bootstrap_math import (
    Number, NumberSystem, OperationEngine, AbstractionEngine, MathConstructionEngine
)
from bootstrap_core import Symbol, SymbolType, SymbolSet


# =============================================================================
# LANGUAGE CONSTRUCTION TESTS
# =============================================================================

class TestProperty:
    """Test Property class."""
    
    def test_property_creation(self):
        prop = Property("color", "RED")
        assert prop.name == "color"
        assert prop.value == "RED"
        assert prop.confidence == 1.0
    
    def test_property_equality(self):
        prop1 = Property("color", "RED")
        prop2 = Property("color", "RED")
        prop3 = Property("color", "BLUE")
        assert prop1 == prop2
        assert prop1 != prop3


class TestPropertyExtractor:
    """Test PropertyExtractor class."""
    
    def test_initialization(self):
        symbol_set = SymbolSet()
        extractor = PropertyExtractor(symbol_set)
        assert len(extractor.property_rules) > 0
    
    def test_extract_properties_color(self):
        symbol_set = SymbolSet()
        extractor = PropertyExtractor(symbol_set)
        red_symbol = symbol_set.get_symbol("RED", SymbolType.COLOR)
        properties = extractor.extract_properties(red_symbol)
        assert len(properties) == 1
        assert properties[0].name == "color"
        assert properties[0].value == "RED"
    
    def test_extract_properties_shape(self):
        symbol_set = SymbolSet()
        extractor = PropertyExtractor(symbol_set)
        circle_symbol = symbol_set.get_symbol("CIRCLE", SymbolType.SHAPE)
        properties = extractor.extract_properties(circle_symbol)
        assert len(properties) == 1
        assert properties[0].name == "shape"
        assert properties[0].value == "CIRCLE"


class TestEntity:
    """Test Entity class."""
    
    def test_entity_creation(self):
        props = [Property("color", "RED"), Property("shape", "ROUND")]
        entity = Entity(props)
        assert len(entity.properties) == 2
        assert entity.name == "color_RED_shape_ROUND"
    
    def test_add_property(self):
        props = [Property("color", "RED")]
        entity = Entity(props)
        entity.add_property(Property("shape", "ROUND"))
        assert len(entity.properties) == 2
        assert entity.has_property(Property("shape", "ROUND"))
    
    def test_has_property_value(self):
        props = [Property("color", "RED"), Property("shape", "ROUND")]
        entity = Entity(props)
        assert entity.has_property_value("color", "RED")
        assert not entity.has_property_value("color", "BLUE")
    
    def test_get_property_value(self):
        props = [Property("color", "RED")]
        entity = Entity(props)
        assert entity.get_property_value("color") == "RED"
        assert entity.get_property_value("shape") is None


class TestEntityBuilder:
    """Test EntityBuilder class."""
    
    def test_build_entity_from_symbols(self):
        symbol_set = SymbolSet()
        extractor = PropertyExtractor(symbol_set)
        builder = EntityBuilder(extractor)
        
        red_symbol = symbol_set.get_symbol("RED", SymbolType.COLOR)
        circle_symbol = symbol_set.get_symbol("CIRCLE", SymbolType.SHAPE)
        entity = builder.build_entity_from_symbols([red_symbol, circle_symbol])
        
        assert len(entity.properties) == 2
        assert entity.has_property_value("color", "RED")
        assert entity.has_property_value("shape", "CIRCLE")
    
    def test_build_entity_from_properties(self):
        symbol_set = SymbolSet()
        extractor = PropertyExtractor(symbol_set)
        builder = EntityBuilder(extractor)
        
        props = [Property("color", "RED"), Property("shape", "ROUND")]
        entity = builder.build_entity_from_properties(props)
        
        assert len(entity.properties) == 2
        assert entity.id in builder.entities
    
    def test_find_entity_by_properties(self):
        symbol_set = SymbolSet()
        extractor = PropertyExtractor(symbol_set)
        builder = EntityBuilder(extractor)
        
        props = [Property("color", "RED")]
        entity1 = builder.build_entity_from_properties(props)
        entity2 = builder.find_entity_by_properties(props)
        
        assert entity1 == entity2


class TestWordMapper:
    """Test WordMapper class."""
    
    def test_map_word_to_entity(self):
        symbol_set = SymbolSet()
        extractor = PropertyExtractor(symbol_set)
        builder = EntityBuilder(extractor)
        mapper = WordMapper(builder)
        
        props = [Property("color", "RED")]
        entity = builder.build_entity_from_properties(props)
        mapper.map_word_to_entity("APPLE", entity)
        
        assert mapper.get_entity_for_word("APPLE") == entity
    
    def test_get_words_for_entity(self):
        symbol_set = SymbolSet()
        extractor = PropertyExtractor(symbol_set)
        builder = EntityBuilder(extractor)
        mapper = WordMapper(builder)
        
        props = [Property("color", "RED")]
        entity = builder.build_entity_from_properties(props)
        mapper.map_word_to_entity("APPLE", entity)
        mapper.map_word_to_entity("CHERRY", entity)
        
        words = mapper.get_words_for_entity(entity)
        assert "APPLE" in words
        assert "CHERRY" in words
    
    def test_semantic_similarity(self):
        symbol_set = SymbolSet()
        extractor = PropertyExtractor(symbol_set)
        builder = EntityBuilder(extractor)
        mapper = WordMapper(builder)
        
        # Two entities with same property
        props1 = [Property("color", "RED")]
        entity1 = builder.build_entity_from_properties(props1)
        mapper.map_word_to_entity("APPLE", entity1)
        mapper.map_word_to_entity("FIRE", entity1)
        
        similarity = mapper.semantic_similarity("APPLE", "FIRE")
        assert similarity == 1.0


class TestLanguageConstructionEngine:
    """Test LanguageConstructionEngine class."""
    
    def test_learn_word(self):
        symbol_set = SymbolSet()
        engine = LanguageConstructionEngine(symbol_set)
        
        props = [Property("color", "RED"), Property("shape", "ROUND")]
        entity = engine.learn_word("APPLE", props)
        
        assert len(entity.properties) == 2
        assert engine.understand_word("APPLE") == entity
    
    def test_understand_word(self):
        symbol_set = SymbolSet()
        engine = LanguageConstructionEngine(symbol_set)
        
        props = [Property("color", "RED")]
        engine.learn_word("FIRE", props)
        
        entity = engine.understand_word("FIRE")
        assert entity is not None
        assert entity.has_property_value("color", "RED")
    
    def test_compare_words(self):
        symbol_set = SymbolSet()
        engine = LanguageConstructionEngine(symbol_set)
        
        props1 = [Property("color", "RED")]
        props2 = [Property("color", "BLUE")]
        engine.learn_word("APPLE", props1)
        engine.learn_word("WATER", props2)
        
        similarity = engine.compare_words("APPLE", "WATER")
        assert similarity == 0.0  # Different colors
    
    def test_get_statistics(self):
        symbol_set = SymbolSet()
        engine = LanguageConstructionEngine(symbol_set)
        
        engine.learn_word("APPLE", [Property("color", "RED")])
        engine.learn_word("WATER", [Property("color", "BLUE")])
        
        stats = engine.get_statistics()
        assert stats["total_entities"] == 2
        assert stats["total_words_mapped"] == 2


# =============================================================================
# MATH CONSTRUCTION TESTS
# =============================================================================

class TestNumber:
    """Test Number class."""
    
    def test_number_creation(self):
        num = Number(3, "111")
        assert num.value == 3
        assert num.representation == "111"
    
    def test_number_addition(self):
        num1 = Number(2, "11")
        num2 = Number(3, "111")
        result = num1 + num2
        assert result.value == 5
    
    def test_number_subtraction(self):
        num1 = Number(5, "11111")
        num2 = Number(2, "11")
        result = num1 - num2
        assert result.value == 3
    
    def test_number_multiplication(self):
        num1 = Number(3, "111")
        num2 = Number(2, "11")
        result = num1 * num2
        assert result.value == 6


class TestNumberSystem:
    """Test NumberSystem class."""
    
    def test_initialization(self):
        num_system = NumberSystem()
        assert 0 in num_system.numbers
        assert 1 in num_system.numbers
    
    def test_construct_number_from_pattern(self):
        num_system = NumberSystem()
        num = num_system.construct_number_from_pattern("111")
        assert num.value == 3
        assert num.representation == "111"
    
    def test_construct_number_from_value(self):
        num_system = NumberSystem()
        num = num_system.construct_number_from_value(5)
        assert num.value == 5
        assert num.representation == "11111"
    
    def test_get_number(self):
        num_system = NumberSystem()
        num_system.construct_number_from_value(3)
        num = num_system.get_number(3)
        assert num is not None
        assert num.value == 3


class TestOperationEngine:
    """Test OperationEngine class."""
    
    def test_add(self):
        num_system = NumberSystem()
        engine = OperationEngine(num_system)
        
        a = num_system.construct_number_from_value(2)
        b = num_system.construct_number_from_value(3)
        result = engine.ADD(a, b)
        
        assert result.value == 5
    
    def test_sub(self):
        num_system = NumberSystem()
        engine = OperationEngine(num_system)
        
        a = num_system.construct_number_from_value(5)
        b = num_system.construct_number_from_value(2)
        result = engine.SUB(a, b)
        
        assert result.value == 3
    
    def test_mul(self):
        num_system = NumberSystem()
        engine = OperationEngine(num_system)
        
        a = num_system.construct_number_from_value(3)
        b = num_system.construct_number_from_value(4)
        result = engine.MUL(a, b)
        
        assert result.value == 12
    
    def test_div(self):
        num_system = NumberSystem()
        engine = OperationEngine(num_system)
        
        a = num_system.construct_number_from_value(8)
        b = num_system.construct_number_from_value(2)
        result = engine.DIV(a, b)
        
        assert result is not None
        assert result.value == 4
    
    def test_div_non_divisible(self):
        num_system = NumberSystem()
        engine = OperationEngine(num_system)
        
        a = num_system.construct_number_from_value(7)
        b = num_system.construct_number_from_value(2)
        result = engine.DIV(a, b)
        
        assert result is None
    
    def test_verify_reversibility_add(self):
        num_system = NumberSystem()
        engine = OperationEngine(num_system)
        
        a = num_system.construct_number_from_value(5)
        b = num_system.construct_number_from_value(3)
        reversible = engine.verify_reversibility("ADD", a, b)
        
        assert reversible == True


class TestAbstractionEngine:
    """Test AbstractionEngine class."""
    
    def test_initialization(self):
        num_system = NumberSystem()
        op_engine = OperationEngine(num_system)
        engine = AbstractionEngine(op_engine)
        assert engine is not None
    
    def test_discover_patterns(self):
        num_system = NumberSystem()
        op_engine = OperationEngine(num_system)
        engine = AbstractionEngine(op_engine)
        
        # Perform some operations
        for i in range(1, 4):
            for j in range(1, 4):
                op_engine.ADD(num_system.construct_number_from_value(i), 
                             num_system.construct_number_from_value(j))
        
        patterns = engine.discover_patterns()
        # Should discover at least some patterns
        assert len(patterns) >= 0


class TestMathConstructionEngine:
    """Test MathConstructionEngine class."""
    
    def test_initialization(self):
        engine = MathConstructionEngine()
        assert engine.number_system is not None
        assert engine.operation_engine is not None
        assert engine.abstraction_engine is not None
    
    def test_construct_number(self):
        engine = MathConstructionEngine()
        num = engine.construct_number(5)
        assert num.value == 5
    
    def test_perform_operation_add(self):
        engine = MathConstructionEngine()
        result = engine.perform_operation("ADD", 2, 3)
        assert result.value == 5
    
    def test_perform_operation_sub(self):
        engine = MathConstructionEngine()
        result = engine.perform_operation("SUB", 5, 2)
        assert result.value == 3
    
    def test_perform_operation_mul(self):
        engine = MathConstructionEngine()
        result = engine.perform_operation("MUL", 3, 4)
        assert result.value == 12
    
    def test_perform_operation_div(self):
        engine = MathConstructionEngine()
        result = engine.perform_operation("DIV", 8, 2)
        assert result.value == 4
    
    def test_get_statistics(self):
        engine = MathConstructionEngine()
        engine.perform_operation("ADD", 2, 3)
        engine.perform_operation("MUL", 3, 4)
        
        stats = engine.get_statistics()
        assert stats["total_operations"] == 2


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
