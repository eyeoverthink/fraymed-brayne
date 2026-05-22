"""
AGI Bootstrap Language Construction
Property-based semantic mapping for building language from symbols and patterns.

Components:
- PropertyExtractor: Extract properties from symbols
- EntityBuilder: Build entities from property combinations
- WordMapper: Map words to property sets
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
import hashlib
import time

from bootstrap_core import Symbol, SymbolType, SymbolSet, AxiomBase


# =============================================================================
# PROPERTY SYSTEM
# =============================================================================

@dataclass
class Property:
    """A property describes a characteristic of an entity."""
    name: str
    value: str
    confidence: float = 1.0
    id: str = field(default_factory=lambda: str(hashlib.sha256(str(time.time()).encode()).hexdigest())[:8])
    
    def __eq__(self, other):
        if not isinstance(other, Property):
            return False
        return self.name == other.name and self.value == other.value
    
    def __hash__(self):
        return hash((self.name, self.value))
    
    def __repr__(self):
        return f"Property({self.name}={self.value}, conf={self.confidence})"


class PropertyExtractor:
    """Extract properties from symbols."""
    
    def __init__(self, symbol_set: SymbolSet):
        self.symbol_set = symbol_set
        self.property_rules: Dict[SymbolType, List[Property]] = {}
        self._initialize_property_rules()
    
    def _initialize_property_rules(self):
        """Initialize default property extraction rules."""
        # Color properties
        color_properties = [
            Property("color", "RED"),
            Property("color", "BLUE"),
            Property("color", "GREEN"),
            Property("color", "YELLOW"),
            Property("color", "BLACK"),
            Property("color", "WHITE")
        ]
        self.property_rules[SymbolType.COLOR] = color_properties
        
        # Shape properties
        shape_properties = [
            Property("shape", "CIRCLE"),
            Property("shape", "SQUARE"),
            Property("shape", "TRIANGLE"),
            Property("shape", "LINE"),
            Property("shape", "POINT")
        ]
        self.property_rules[SymbolType.SHAPE] = shape_properties
        
        # Signal properties
        signal_properties = [
            Property("truth", "TRUE"),
            Property("truth", "FALSE")
        ]
        self.property_rules[SymbolType.SIGNAL] = signal_properties
    
    def extract_properties(self, symbol: Symbol) -> List[Property]:
        """Extract properties from a symbol based on its type."""
        if symbol.symbol_type in self.property_rules:
            # Find matching property by value
            for prop in self.property_rules[symbol.symbol_type]:
                if prop.value == symbol.value:
                    return [prop]
        # If no rule matches, return empty list
        return []
    
    def extract_properties_from_symbols(self, symbols: List[Symbol]) -> List[Property]:
        """Extract properties from a sequence of symbols."""
        properties = []
        for symbol in symbols:
            properties.extend(self.extract_properties(symbol))
        return properties
    
    def add_property_rule(self, symbol_type: SymbolType, property: Property):
        """Add a new property extraction rule."""
        if symbol_type not in self.property_rules:
            self.property_rules[symbol_type] = []
        self.property_rules[symbol_type].append(property)


class Entity:
    """An entity is a collection of properties."""
    
    def __init__(self, properties: List[Property], name: Optional[str] = None):
        self.properties: Set[Property] = set(properties)
        self.name = name if name else self._generate_name()
        self.id = str(hashlib.sha256(str(time.time()).encode()).hexdigest())[:8]
    
    def _generate_name(self) -> str:
        """Generate a name from properties."""
        if not self.properties:
            return "UNKNOWN"
        # Sort properties by name for consistent naming
        sorted_props = sorted(self.properties, key=lambda p: p.name)
        parts = [f"{p.name}_{p.value}" for p in sorted_props]
        return "_".join(parts)
    
    def add_property(self, property: Property):
        """Add a property to the entity."""
        self.properties.add(property)
        self.name = self._generate_name()
    
    def has_property(self, property: Property) -> bool:
        """Check if entity has a specific property."""
        return property in self.properties
    
    def has_property_value(self, property_name: str, property_value: str) -> bool:
        """Check if entity has a property with specific value."""
        for prop in self.properties:
            if prop.name == property_name and prop.value == property_value:
                return True
        return False
    
    def get_property_value(self, property_name: str) -> Optional[str]:
        """Get the value of a specific property."""
        for prop in self.properties:
            if prop.name == property_name:
                return prop.value
        return None
    
    def __eq__(self, other):
        if not isinstance(other, Entity):
            return False
        return self.properties == other.properties
    
    def __hash__(self):
        return hash(frozenset(self.properties))
    
    def __repr__(self):
        return f"Entity({self.name}, props={len(self.properties)})"


class EntityBuilder:
    """Build entities from property combinations."""
    
    def __init__(self, property_extractor: PropertyExtractor):
        self.property_extractor = property_extractor
        self.entities: Dict[str, Entity] = {}
        self.entity_patterns: Dict[Tuple[str, ...], Entity] = {}
    
    def build_entity_from_symbols(self, symbols: List[Symbol]) -> Entity:
        """Build an entity from a sequence of symbols."""
        properties = self.property_extractor.extract_properties_from_symbols(symbols)
        if not properties:
            # Create empty entity
            return Entity([])
        
        entity = Entity(properties)
        self.entities[entity.id] = entity
        
        # Store pattern for future reference
        pattern_key = tuple(sorted([f"{p.name}:{p.value}" for p in properties]))
        self.entity_patterns[pattern_key] = entity
        
        return entity
    
    def build_entity_from_properties(self, properties: List[Property]) -> Entity:
        """Build an entity directly from properties."""
        entity = Entity(properties)
        self.entities[entity.id] = entity
        return entity
    
    def find_entity_by_properties(self, properties: List[Property]) -> Optional[Entity]:
        """Find an entity that matches the given properties."""
        pattern_key = tuple(sorted([f"{p.name}:{p.value}" for p in properties]))
        return self.entity_patterns.get(pattern_key)
    
    def find_similar_entities(self, entity: Entity, min_overlap: float = 0.5) -> List[Entity]:
        """Find entities with similar properties."""
        similar = []
        for other in self.entities.values():
            if other.id == entity.id:
                continue
            
            # Calculate overlap
            intersection = len(entity.properties & other.properties)
            union = len(entity.properties | other.properties)
            overlap = intersection / union if union > 0 else 0.0
            
            if overlap >= min_overlap:
                similar.append((other, overlap))
        
        # Sort by overlap score
        similar.sort(key=lambda x: x[1], reverse=True)
        return [e for e, _ in similar]


class WordMapper:
    """Map words to property sets for semantic understanding."""
    
    def __init__(self, entity_builder: EntityBuilder):
        self.entity_builder = entity_builder
        self.word_to_entity: Dict[str, Entity] = {}
        self.entity_to_words: Dict[Entity, Set[str]] = defaultdict(set)
    
    def map_word_to_entity(self, word: str, entity: Entity):
        """Map a word to an entity."""
        self.word_to_entity[word.upper()] = entity
        self.entity_to_words[entity].add(word.upper())
    
    def get_entity_for_word(self, word: str) -> Optional[Entity]:
        """Get the entity associated with a word."""
        return self.word_to_entity.get(word.upper())
    
    def get_words_for_entity(self, entity: Entity) -> Set[str]:
        """Get all words associated with an entity."""
        return self.entity_to_words.get(entity, set())
    
    def discover_word_entity_mapping(self, word: str, symbols: List[Symbol]):
        """Discover word-entity mapping from symbol patterns."""
        # Build entity from symbols
        entity = self.entity_builder.build_entity_from_symbols(symbols)
        
        # Map word to entity
        self.map_word_to_entity(word, entity)
        
        return entity
    
    def infer_entity_from_word(self, word: str, symbol_set: SymbolSet) -> Optional[Entity]:
        """Infer entity properties from a word using symbol mapping."""
        # Try to find symbols that match the word
        for symbol_type in [SymbolType.COLOR, SymbolType.SHAPE, SymbolType.SIGNAL]:
            symbol = symbol_set.get_symbol(word, symbol_type)
            if symbol:
                # Create entity from symbol
                entity = self.entity_builder.build_entity_from_symbols([symbol])
                return entity
        
        return None
    
    def semantic_similarity(self, word1: str, word2: str) -> float:
        """Calculate semantic similarity between two words based on their entities."""
        entity1 = self.get_entity_for_word(word1)
        entity2 = self.get_entity_for_word(word2)
        
        if not entity1 or not entity2:
            return 0.0
        
        # Calculate property overlap
        intersection = len(entity1.properties & entity2.properties)
        union = len(entity1.properties | entity2.properties)
        similarity = intersection / union if union > 0 else 0.0
        
        return similarity


# =============================================================================
# LANGUAGE CONSTRUCTION ENGINE
# =============================================================================

class LanguageConstructionEngine:
    """Main engine for language construction from properties."""
    
    def __init__(self, symbol_set: SymbolSet):
        self.symbol_set = symbol_set
        self.property_extractor = PropertyExtractor(symbol_set)
        self.entity_builder = EntityBuilder(self.property_extractor)
        self.word_mapper = WordMapper(self.entity_builder)
    
    def learn_word(self, word: str, properties: List[Property]) -> Entity:
        """Learn a word with its associated properties."""
        entity = self.entity_builder.build_entity_from_properties(properties)
        self.word_mapper.map_word_to_entity(word, entity)
        return entity
    
    def understand_word(self, word: str) -> Optional[Entity]:
        """Understand a word by retrieving its entity."""
        return self.word_mapper.get_entity_for_word(word)
    
    def discover_word_from_symbols(self, word: str, symbols: List[Symbol]) -> Entity:
        """Discover word meaning from symbol patterns."""
        return self.word_mapper.discover_word_entity_mapping(word, symbols)
    
    def compare_words(self, word1: str, word2: str) -> float:
        """Compare two words semantically."""
        return self.word_mapper.semantic_similarity(word1, word2)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get language construction statistics."""
        return {
            "total_entities": len(self.entity_builder.entities),
            "total_words_mapped": len(self.word_mapper.word_to_entity),
            "avg_properties_per_entity": sum(
                len(e.properties) for e in self.entity_builder.entities.values()
            ) / len(self.entity_builder.entities) if self.entity_builder.entities else 0.0
        }


# =============================================================================
# DEMONSTRATION
# =============================================================================

def demonstrate_language_construction():
    """Demonstrate language construction capabilities."""
    print("=" * 60)
    print("AGI Bootstrap Language Construction - Demonstration")
    print("=" * 60)
    
    # Initialize engine
    symbol_set = SymbolSet()
    engine = LanguageConstructionEngine(symbol_set)
    
    print("\n1. Learning words from properties:")
    print("-" * 60)
    
    # Learn APPLE: RED + ROUND + OBJECT
    apple_props = [
        Property("color", "RED"),
        Property("shape", "ROUND"),
        Property("type", "OBJECT")
    ]
    apple_entity = engine.learn_word("APPLE", apple_props)
    print(f"   APPLE -> {apple_entity}")
    
    # Learn FIRE: RED + HOT + DANGER
    fire_props = [
        Property("color", "RED"),
        Property("temperature", "HOT"),
        Property("type", "DANGER")
    ]
    fire_entity = engine.learn_word("FIRE", fire_props)
    print(f"   FIRE -> {fire_entity}")
    
    # Learn WATER: BLUE + LIQUID + ESSENTIAL
    water_props = [
        Property("color", "BLUE"),
        Property("state", "LIQUID"),
        Property("type", "ESSENTIAL")
    ]
    water_entity = engine.learn_word("WATER", water_props)
    print(f"   WATER -> {water_entity}")
    
    print("\n2. Understanding words:")
    print("-" * 60)
    
    apple_understood = engine.understand_word("APPLE")
    print(f"   APPLE understood: {apple_understood}")
    
    print("\n3. Semantic similarity:")
    print("-" * 60)
    
    apple_fire_sim = engine.compare_words("APPLE", "FIRE")
    print(f"   APPLE vs FIRE: {apple_fire_sim:.2f} (both RED)")
    
    apple_water_sim = engine.compare_words("APPLE", "WATER")
    print(f"   APPLE vs WATER: {apple_water_sim:.2f} (different colors)")
    
    fire_water_sim = engine.compare_words("FIRE", "WATER")
    print(f"   FIRE vs WATER: {fire_water_sim:.2f} (different colors)")
    
    print("\n4. Statistics:")
    print("-" * 60)
    stats = engine.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demonstrate_language_construction()
