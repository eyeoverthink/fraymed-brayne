"""
AGI Bootstrap Core Engine
First-principles intelligence construction from symbols, axioms, logic, and learning.

Four-Layer Architecture:
1. Perception Layer (Symbols) - Raw inputs only, no meaning
2. Relation Layer (Primitive Truths) - Axioms, not explanations
3. Logic Engine (Rules of Thought) - Enable reasoning from axioms
4. Learning Loop (Self-Improvement) - Learn from consistency
"""

import json
import hashlib
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import time


# =============================================================================
# LAYER 1: PERCEPTION LAYER (SYMBOLS)
# =============================================================================

class SymbolType(Enum):
    LETTER = "letter"
    NUMBER = "number"
    COLOR = "color"
    SHAPE = "shape"
    SIGNAL = "signal"
    WORD = "word"


@dataclass
class Symbol:
    """A symbol is a token without semantic interpretation."""
    value: str
    symbol_type: SymbolType
    id: str = field(default_factory=lambda: str(hashlib.sha256(str(time.time()).encode()).hexdigest())[:8])
    
    def __eq__(self, other):
        if not isinstance(other, Symbol):
            return False
        return self.value == other.value and self.symbol_type == other.symbol_type
    
    def __hash__(self):
        return hash((self.value, self.symbol_type))
    
    def __repr__(self):
        return f"Symbol({self.value}, {self.symbol_type.value})"


class SymbolSet:
    """Universe of symbols available to the system."""
    
    def __init__(self):
        self.symbols: Dict[Tuple[str, SymbolType], Symbol] = {}
        self._initialize_default_symbols()
    
    def _initialize_default_symbols(self):
        """Initialize the default symbol universe."""
        # Letters: A-Z
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            self.add_symbol(letter, SymbolType.LETTER)
        
        # Numbers: 0-9
        for number in "0123456789":
            self.add_symbol(number, SymbolType.NUMBER)
        
        # Colors
        colors = ["RED", "BLUE", "GREEN", "YELLOW", "BLACK", "WHITE"]
        for color in colors:
            self.add_symbol(color, SymbolType.COLOR)
        
        # Shapes
        shapes = ["CIRCLE", "SQUARE", "TRIANGLE", "LINE", "POINT"]
        for shape in shapes:
            self.add_symbol(shape, SymbolType.SHAPE)
        
        # Signals
        signals = ["TRUE", "FALSE"]
        for signal in signals:
            self.add_symbol(signal, SymbolType.SIGNAL)
    
    def add_symbol(self, value: str, symbol_type: SymbolType) -> Symbol:
        """Add a new symbol to the universe."""
        key = (value.upper(), symbol_type)
        if key not in self.symbols:
            symbol = Symbol(value.upper(), symbol_type)
            self.symbols[key] = symbol
        return self.symbols[key]
    
    def get_symbol(self, value: str, symbol_type: SymbolType) -> Optional[Symbol]:
        """Get a symbol by value and type."""
        key = (value.upper(), symbol_type)
        return self.symbols.get(key)
    
    def get_symbols_by_type(self, symbol_type: SymbolType) -> List[Symbol]:
        """Get all symbols of a specific type."""
        return [s for (v, t), s in self.symbols.items() if t == symbol_type]
    
    def contains(self, value: str, symbol_type: SymbolType) -> bool:
        """Check if a symbol exists in the universe."""
        return self.get_symbol(value, symbol_type) is not None


class Tokenizer:
    """Convert input to symbol sequences."""
    
    def __init__(self, symbol_set: SymbolSet):
        self.symbol_set = symbol_set
    
    def tokenize(self, input_string: str) -> List[Symbol]:
        """Convert input string to sequence of symbols."""
        tokens = []
        for char in input_string.upper():
            # Try to match as letter
            if char.isalpha() and self.symbol_set.contains(char, SymbolType.LETTER):
                tokens.append(self.symbol_set.get_symbol(char, SymbolType.LETTER))
            # Try to match as number
            elif char.isdigit() and self.symbol_set.contains(char, SymbolType.NUMBER):
                tokens.append(self.symbol_set.get_symbol(char, SymbolType.NUMBER))
            # Try to match as signal
            elif self.symbol_set.contains(char, SymbolType.SIGNAL):
                tokens.append(self.symbol_set.get_symbol(char, SymbolType.SIGNAL))
            # Otherwise create as word
            else:
                symbol = self.symbol_set.add_symbol(char, SymbolType.WORD)
                tokens.append(symbol)
        return tokens
    
    def tokenize_words(self, input_string: str) -> List[Symbol]:
        """Convert input string to word-level symbols."""
        words = input_string.upper().split()
        tokens = []
        for word in words:
            # Check if it's a known symbol
            for symbol_type in [SymbolType.COLOR, SymbolType.SHAPE, SymbolType.SIGNAL]:
                if self.symbol_set.contains(word, symbol_type):
                    tokens.append(self.symbol_set.get_symbol(word, symbol_type))
                    break
            else:
                # Create as word symbol
                symbol = self.symbol_set.add_symbol(word, SymbolType.WORD)
                tokens.append(symbol)
        return tokens


# =============================================================================
# LAYER 2: RELATION LAYER (PRIMITIVE TRUTHS)
# =============================================================================

@dataclass
class Axiom:
    """An axiom is a primitive truth, not an explanation."""
    left: Symbol
    relation: str  # "=", "!=", "<", ">", "+", "-", etc.
    right: Symbol
    confidence: float = 1.0
    id: str = field(default_factory=lambda: str(hashlib.sha256(str(time.time()).encode()).hexdigest())[:8])
    
    def __eq__(self, other):
        if not isinstance(other, Axiom):
            return False
        # Compare by symbol values and types, not object identity
        return (self.left.value == other.left.value and
                self.left.symbol_type == other.left.symbol_type and
                self.relation == other.relation and 
                self.right.value == other.right.value and
                self.right.symbol_type == other.right.symbol_type)
    
    def __hash__(self):
        return hash((self.left.value, self.left.symbol_type, self.relation, self.right.value, self.right.symbol_type))
    
    def __repr__(self):
        return f"Axiom({self.left} {self.relation} {self.right}, conf={self.confidence})"


class AxiomBase:
    """Store and manage primitive truths."""
    
    def __init__(self, symbol_set: SymbolSet):
        self.symbol_set = symbol_set
        self.axioms: Dict[str, Axiom] = {}
        self._initialize_default_axioms()
    
    def _initialize_default_axioms(self):
        """Initialize default axioms."""
        # Identity: A = A
        letters = self.symbol_set.get_symbols_by_type(SymbolType.LETTER)
        for symbol in letters:
            self.add_axiom(symbol, "=", symbol)
        
        # Distinction: A != B (for distinct letters)
        for i, a in enumerate(letters):
            for b in letters[i+1:]:
                self.add_axiom(a, "!=", b)
        
        # Arithmetic truths: 1 + 1 = 2
        one = self.symbol_set.get_symbol("1", SymbolType.NUMBER)
        if one:
            # Store the arithmetic pattern
            self.add_axiom(one, "+", one)
        
        # Category separation: RED != BLUE
        red = self.symbol_set.get_symbol("RED", SymbolType.COLOR)
        blue = self.symbol_set.get_symbol("BLUE", SymbolType.COLOR)
        if red and blue:
            self.add_axiom(red, "!=", blue)
        
        # Binary logic: TRUE != FALSE
        true_sym = self.symbol_set.get_symbol("TRUE", SymbolType.SIGNAL)
        false_sym = self.symbol_set.get_symbol("FALSE", SymbolType.SIGNAL)
        if true_sym and false_sym:
            self.add_axiom(true_sym, "!=", false_sym)
    
    def add_axiom(self, left: Symbol, relation: str, right: Symbol, result: Optional[Symbol] = None) -> Axiom:
        """Add a new axiom."""
        axiom = Axiom(left, relation, right, confidence=1.0)
        self.axioms[axiom.id] = axiom
        return axiom
    
    def get_axiom(self, left: Symbol, relation: str, right: Symbol) -> Optional[Axiom]:
        """Get an axiom if it exists."""
        for axiom in self.axioms.values():
            if (axiom.left == left and 
                axiom.relation == relation and 
                axiom.right == right):
                return axiom
        return None
    
    def check_consistency(self, axiom: Axiom) -> bool:
        """Check if an axiom is consistent with existing axioms."""
        existing = self.get_axiom(axiom.left, axiom.relation, axiom.right)
        if existing:
            return True  # Already exists, consistent
        # Check for contradictions
        if axiom.relation == "=":
            # Check if we have != for the same pair
            contradiction = self.get_axiom(axiom.left, "!=", axiom.right)
            if contradiction:
                return False
        elif axiom.relation == "!=":
            # Check if we have = for the same pair
            contradiction = self.get_axiom(axiom.left, "=", axiom.right)
            if contradiction:
                return False
        return True
    
    def discover_axioms_from_patterns(self, observations: List[Tuple[Symbol, str, Symbol]]) -> List[Axiom]:
        """Discover new axioms from observed patterns."""
        new_axioms = []
        pattern_counts = defaultdict(int)
        
        for left, relation, right in observations:
            pattern_counts[(left, relation, right)] += 1
        
        for (left, relation, right), count in pattern_counts.items():
            if count >= 2:  # Pattern appears at least twice
                axiom = Axiom(left, relation, right, confidence=min(1.0, count / 10.0))
                if self.check_consistency(axiom):
                    self.add_axiom(left, relation, right)
                    new_axioms.append(axiom)
        
        return new_axioms


# =============================================================================
# LAYER 3: LOGIC ENGINE (RULES OF THOUGHT)
# =============================================================================

class LogicGate:
    """Logic gates for reasoning."""
    
    @staticmethod
    def NOT(value: bool) -> bool:
        """NOT gate."""
        return not value
    
    @staticmethod
    def AND(a: bool, b: bool) -> bool:
        """AND gate."""
        return a and b
    
    @staticmethod
    def OR(a: bool, b: bool) -> bool:
        """OR gate."""
        return a or b
    
    @staticmethod
    def XOR(a: bool, b: bool) -> bool:
        """XOR gate."""
        return a != b
    
    @staticmethod
    def IMPLIES(a: bool, b: bool) -> bool:
        """IMPLIES gate (a → b)."""
        return not a or b


class InferenceEngine:
    """Apply rules to derive conclusions from axioms."""
    
    def __init__(self, axiom_base: AxiomBase):
        self.axiom_base = axiom_base
        self.logic_gate = LogicGate()
    
    def apply_transitivity(self, a: Symbol, b: Symbol, c: Symbol) -> Optional[Axiom]:
        """
        IF A = B AND B = C → A = C
        Transitivity inference.
        """
        axiom_ab = self.axiom_base.get_axiom(a, "=", b)
        axiom_bc = self.axiom_base.get_axiom(b, "=", c)
        
        if axiom_ab and axiom_bc:
            # Derive A = C
            if self.axiom_base.check_consistency(Axiom(a, "=", c)):
                return self.axiom_base.add_axiom(a, "=", c)
        return None
    
    def apply_negation(self, a: Symbol, b: Symbol) -> Optional[Axiom]:
        """
        IF A != B → NOT(A = B)
        Negation inference.
        """
        axiom = self.axiom_base.get_axiom(a, "!=", b)
        if axiom:
            # A = B is false
            # This is represented by the != axiom itself
            return axiom
        return None
    
    def apply_execution_rule(self, condition: bool) -> bool:
        """
        IF TRUE → action allowed
        IF FALSE → action blocked
        """
        return condition
    
    def derive_conclusions(self, premises: List[Axiom]) -> List[Axiom]:
        """Derive all possible conclusions from premises."""
        conclusions = []
        
        # Apply transitivity chains
        for i, p1 in enumerate(premises):
            for p2 in premises[i+1:]:
                if p1.relation == "=" and p2.relation == "=":
                    if p1.right == p2.left:
                        # A = B, B = C → A = C
                        conclusion = self.apply_transitivity(p1.left, p1.right, p2.right)
                        if conclusion:
                            conclusions.append(conclusion)
        
        return conclusions
    
    def check_contradiction(self, axioms: List[Axiom]) -> List[Tuple[Axiom, Axiom]]:
        """Detect contradictions in a set of axioms."""
        contradictions = []
        
        for i, a1 in enumerate(axioms):
            for a2 in axioms[i+1:]:
                # Check for direct contradictions: A = B vs A != B
                if (a1.left == a2.left and a1.right == a2.right):
                    if (a1.relation == "=" and a2.relation == "!=") or \
                       (a1.relation == "!=" and a2.relation == "="):
                        contradictions.append((a1, a2))
        
        return contradictions


# =============================================================================
# LAYER 4: LEARNING LOOP (SELF-IMPROVEMENT)
# =============================================================================

@dataclass
class Interaction:
    """A single interaction with the environment."""
    input_symbols: List[Symbol]
    applied_rules: List[str]
    result: Any
    contradiction_detected: bool
    timestamp: float = field(default_factory=time.time)
    id: str = field(default=None)
    
    def __post_init__(self):
        if self.id is None:
            # Use timestamp with nanosecond precision for unique IDs
            self.id = str(hashlib.sha256(f"{self.timestamp}{len(self.input_symbols)}{self.contradiction_detected}".encode()).hexdigest())[:8]


class MemorySystem:
    """Store all interactions for learning."""
    
    def __init__(self):
        self.interactions: Dict[str, Interaction] = {}
        self.contradiction_count = 0
        self.success_count = 0
    
    def store_interaction(self, interaction: Interaction):
        """Store an interaction."""
        # Ensure unique ID by regenerating if it exists
        if interaction.id in self.interactions:
            interaction.id = str(hashlib.sha256(str(time.time()).encode()).hexdigest())[:8]
        self.interactions[interaction.id] = interaction
        if interaction.contradiction_detected:
            self.contradiction_count += 1
        else:
            self.success_count += 1
    
    def get_interaction(self, interaction_id: str) -> Optional[Interaction]:
        """Get an interaction by ID."""
        return self.interactions.get(interaction_id)
    
    def get_recent_interactions(self, n: int = 10) -> List[Interaction]:
        """Get the n most recent interactions."""
        sorted_interactions = sorted(
            self.interactions.values(),
            key=lambda x: x.timestamp,
            reverse=True
        )
        return sorted_interactions[:n]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get memory statistics."""
        total = len(self.interactions)
        return {
            "total_interactions": total,
            "contradictions": self.contradiction_count,
            "successes": self.success_count,
            "contradiction_rate": self.contradiction_count / total if total > 0 else 0.0,
            "success_rate": self.success_count / total if total > 0 else 0.0
        }
    
    def export_to_json(self, filepath: str):
        """Export memory to JSON file."""
        data = {
            "statistics": self.get_statistics(),
            "interactions": [
                {
                    "id": i.id,
                    "input_symbols": [str(s) for s in i.input_symbols],
                    "applied_rules": i.applied_rules,
                    "result": str(i.result),
                    "contradiction_detected": i.contradiction_detected,
                    "timestamp": i.timestamp
                }
                for i in self.interactions.values()
            ]
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


class Learner:
    """Adjust rule weights based on consistency."""
    
    def __init__(self, axiom_base: AxiomBase, memory_system: MemorySystem):
        self.axiom_base = axiom_base
        self.memory_system = memory_system
        self.dopamine_level = 0.0  # Reward signal
        self.rule_weights: Dict[str, float] = defaultdict(lambda: 1.0)
    
    def set_dopamine(self, level: float):
        """Set dopamine level (reward signal)."""
        self.dopamine_level = max(0.0, min(1.0, level))
    
    def process_interaction(self, interaction: Interaction):
        """Process an interaction and adjust learning."""
        if interaction.contradiction_detected:
            # Mark error, reduce rule weights
            self._adjust_rule_weights(interaction.applied_rules, -0.1)
        else:
            # Success, increase rule weights if dopamine is high
            if self.dopamine_level > 0.5:
                self._adjust_rule_weights(interaction.applied_rules, 0.1)
    
    def _adjust_rule_weights(self, rules: List[str], delta: float):
        """Adjust weights for applied rules."""
        for rule in rules:
            self.rule_weights[rule] = max(0.1, min(2.0, self.rule_weights[rule] + delta))
    
    def get_rule_weight(self, rule: str) -> float:
        """Get weight for a specific rule."""
        return self.rule_weights.get(rule, 1.0)
    
    def discover_patterns(self, recent_interactions: List[Interaction]) -> List[Axiom]:
        """Discover new axioms from recent interactions."""
        observations = []
        
        for interaction in recent_interactions:
            # Extract patterns from input symbols
            if len(interaction.input_symbols) >= 2:
                for i in range(len(interaction.input_symbols) - 1):
                    left = interaction.input_symbols[i]
                    right = interaction.input_symbols[i + 1]
                    observations.append((left, "NEXT", right))
        
        # Use axiom base to discover new axioms
        return self.axiom_base.discover_axioms_from_patterns(observations)
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get learning statistics."""
        return {
            "dopamine_level": self.dopamine_level,
            "total_rules": len(self.rule_weights),
            "avg_rule_weight": sum(self.rule_weights.values()) / len(self.rule_weights) if self.rule_weights else 0.0,
            "strongest_rules": sorted(self.rule_weights.items(), key=lambda x: x[1], reverse=True)[:5]
        }


# =============================================================================
# BOOTSTRAP ENGINE (INTEGRATION)
# =============================================================================

class BootstrapEngine:
    """Main bootstrap engine integrating all four layers."""
    
    def __init__(self):
        # Layer 1: Perception
        self.symbol_set = SymbolSet()
        self.tokenizer = Tokenizer(self.symbol_set)
        
        # Layer 2: Relation
        self.axiom_base = AxiomBase(self.symbol_set)
        
        # Layer 3: Logic
        self.inference_engine = InferenceEngine(self.axiom_base)
        
        # Layer 4: Learning
        self.memory_system = MemorySystem()
        self.learner = Learner(self.axiom_base, self.memory_system)
    
    def observe(self, input_string: str) -> List[Symbol]:
        """Layer 1: Observe and tokenize input."""
        tokens = self.tokenizer.tokenize_words(input_string)
        return tokens
    
    def apply_rules(self, symbols: List[Symbol]) -> Tuple[List[Axiom], List[str]]:
        """Layer 3: Apply logic rules to symbols."""
        applied_rules = []
        derived_axioms = []
        
        # Apply transitivity
        for i in range(len(symbols) - 2):
            a, b, c = symbols[i], symbols[i+1], symbols[i+2]
            conclusion = self.inference_engine.apply_transitivity(a, b, c)
            if conclusion:
                derived_axioms.append(conclusion)
                applied_rules.append("transitivity")
        
        # Check for contradictions
        contradictions = self.inference_engine.check_contradiction(
            list(self.axiom_base.axioms.values()) + derived_axioms
        )
        
        return derived_axioms, applied_rules
    
    def learn(self, interaction: Interaction):
        """Layer 4: Learn from interaction."""
        self.memory_system.store_interaction(interaction)
        self.learner.process_interaction(interaction)
    
    def process(self, input_string: str, dopamine: float = 0.0) -> Dict[str, Any]:
        """Full processing pipeline through all four layers."""
        # Set dopamine level
        self.learner.set_dopamine(dopamine)
        
        # Layer 1: Observe
        symbols = self.observe(input_string)
        
        # Layer 3: Apply rules
        derived_axioms, applied_rules = self.apply_rules(symbols)
        
        # Check for contradictions
        all_axioms = list(self.axiom_base.axioms.values()) + derived_axioms
        contradictions = self.inference_engine.check_contradiction(all_axioms)
        contradiction_detected = len(contradictions) > 0
        
        # Create interaction
        interaction = Interaction(
            input_symbols=symbols,
            applied_rules=applied_rules,
            result=derived_axioms,
            contradiction_detected=contradiction_detected
        )
        
        # Layer 4: Learn
        self.learn(interaction)
        
        # Discover patterns from recent interactions
        recent = self.memory_system.get_recent_interactions(10)
        new_axioms = self.learner.discover_patterns(recent)
        
        return {
            "input": input_string,
            "symbols": [str(s) for s in symbols],
            "derived_axioms": [str(a) for a in derived_axioms],
            "new_axioms": [str(a) for a in new_axioms],
            "contradictions": [(str(c[0]), str(c[1])) for c in contradictions],
            "contradiction_detected": contradiction_detected,
            "applied_rules": applied_rules,
            "memory_stats": self.memory_system.get_statistics(),
            "learning_stats": self.learner.get_learning_statistics()
        }
    
    def get_system_state(self) -> Dict[str, Any]:
        """Get current system state."""
        return {
            "total_symbols": len(self.symbol_set.symbols),
            "total_axioms": len(self.axiom_base.axioms),
            "memory_stats": self.memory_system.get_statistics(),
            "learning_stats": self.learner.get_learning_statistics(),
            "dopamine_level": self.learner.dopamine_level
        }


# =============================================================================
# INTERACTIVE SHELL
# =============================================================================

def interactive_shell(engine: BootstrapEngine):
    """Interactive shell for teaching the bootstrap engine."""
    print("=" * 60)
    print("AGI Bootstrap Engine - Interactive Shell")
    print("=" * 60)
    print("Commands:")
    print("  <input>       Process input through bootstrap engine")
    print("  state         Show current system state")
    print("  stats         Show memory and learning statistics")
    print("  dopamine <n>  Set dopamine level (0.0 - 1.0)")
    print("  export <file> Export memory to JSON file")
    print("  quit          Exit shell")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\nbootstrap> ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "quit":
                print("Exiting bootstrap engine...")
                break
            
            elif user_input.lower() == "state":
                state = engine.get_system_state()
                print("\nSystem State:")
                for key, value in state.items():
                    print(f"  {key}: {value}")
            
            elif user_input.lower() == "stats":
                print("\nMemory Statistics:")
                for key, value in engine.memory_system.get_statistics().items():
                    print(f"  {key}: {value}")
                print("\nLearning Statistics:")
                for key, value in engine.learner.get_learning_statistics().items():
                    print(f"  {key}: {value}")
            
            elif user_input.lower().startswith("dopamine"):
                try:
                    parts = user_input.split()
                    if len(parts) == 2:
                        level = float(parts[1])
                        engine.learner.set_dopamine(level)
                        print(f"Dopamine level set to {level}")
                except ValueError:
                    print("Invalid dopamine level. Use: dopamine <0.0-1.0>")
            
            elif user_input.lower().startswith("export"):
                try:
                    parts = user_input.split()
                    if len(parts) == 2:
                        filepath = parts[1]
                        engine.memory_system.export_to_json(filepath)
                        print(f"Memory exported to {filepath}")
                except Exception as e:
                    print(f"Export failed: {e}")
            
            else:
                # Process input through bootstrap engine
                result = engine.process(user_input)
                print("\nProcessing Result:")
                print(f"  Input: {result['input']}")
                print(f"  Symbols: {result['symbols']}")
                print(f"  Derived Axioms: {result['derived_axioms']}")
                print(f"  New Axioms: {result['new_axioms']}")
                print(f"  Contradictions: {result['contradictions']}")
                print(f"  Contradiction Detected: {result['contradiction_detected']}")
                print(f"  Applied Rules: {result['applied_rules']}")
        
        except KeyboardInterrupt:
            print("\nExiting bootstrap engine...")
            break
        except Exception as e:
            print(f"Error: {e}")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    # Create bootstrap engine
    engine = BootstrapEngine()
    
    # Show initial state
    print("Initial System State:")
    state = engine.get_system_state()
    for key, value in state.items():
        print(f"  {key}: {value}")
    
    # Start interactive shell
    interactive_shell(engine)
