"""
AGI Bootstrap Brain Integration
Integrates bootstrap engine with comprehensive brain system.

Components:
- SymbolToRegionMapper: Map symbols to brain regions
- AxiomToSynapseConverter: Convert axioms to synaptic weights
- LogicToCognitiveIntegrator: Integrate logic engine with cognitive core
- LearningToDNAConnector: Connect learning loop with Fractal DNA
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
import hashlib
import time

from bootstrap_core import (
    Symbol, SymbolType, SymbolSet, Axiom, AxiomBase, 
    LogicGate, InferenceEngine, Learner, BootstrapEngine
)
from bootstrap_language import Property, Entity, WordMapper
from bootstrap_math import Number, OperationEngine

# Import from actual comprehensive brain system
try:
    from comprehensive_brain_template import BrainRegion, Synapse, Neuron, ComprehensiveBrain
    USING_REAL_BRAIN_SYSTEM = True
except ImportError:
    # Fallback if comprehensive brain not available
    class BrainRegion:
        """Represents a brain region (fallback)."""
        CORTEX = "cortex"
        HIPPOCAMPUS = "hippocampus"
        THALAMUS = "thalamus"
        BASAL_GANGLIA = "basal_ganglia"
        CEREBELLUM = "cerebellum"
        BRAINSTEM = "brainstem"
        VISUAL_CORTEX = "visual_cortex"
        AUDITORY_CORTEX = "auditory_cortex"
    USING_REAL_BRAIN_SYSTEM = False


@dataclass
class RegionMapping:
    """Mapping from symbol type to brain region."""
    symbol_type: SymbolType
    region: str
    confidence: float = 1.0


class SymbolToRegionMapper:
    """Map symbols to brain regions based on their type and properties."""
    
    def __init__(self, symbol_set: SymbolSet):
        self.symbol_set = symbol_set
        self.mappings: Dict[SymbolType, str] = {}
        self._initialize_default_mappings()
    
    def _initialize_default_mappings(self):
        """Initialize default symbol-to-region mappings."""
        self.mappings[SymbolType.LETTER] = BrainRegion.CORTEX
        self.mappings[SymbolType.NUMBER] = BrainRegion.PARIETAL_LOBE if hasattr(BrainRegion, 'PARIETAL_LOBE') else BrainRegion.CORTEX
        self.mappings[SymbolType.COLOR] = BrainRegion.VISUAL_CORTEX
        self.mappings[SymbolType.SHAPE] = BrainRegion.VISUAL_CORTEX
        self.mappings[SymbolType.SIGNAL] = BrainRegion.THALAMUS
        self.mappings[SymbolType.WORD] = BrainRegion.HIPPOCAMPUS
    
    def map_symbol_to_region(self, symbol: Symbol) -> str:
        """Map a symbol to its brain region."""
        return self.mappings.get(symbol.symbol_type, BrainRegion.CORTEX)
    
    def map_symbols_to_regions(self, symbols: List[Symbol]) -> Dict[str, List[Symbol]]:
        """Map multiple symbols to their regions."""
        region_symbols = defaultdict(list)
        for symbol in symbols:
            region = self.map_symbol_to_region(symbol)
            region_symbols[region].append(symbol)
        return dict(region_symbols)
    
    def add_mapping(self, symbol_type: SymbolType, region: str):
        """Add a new symbol-to-region mapping."""
        self.mappings[symbol_type] = region
    
    def get_region_for_symbol_type(self, symbol_type: SymbolType) -> Optional[str]:
        """Get the region for a symbol type."""
        return self.mappings.get(symbol_type)


# =============================================================================
# AXIOM TO SYNAPSE CONVERTER
# =============================================================================

@dataclass
class SynapticWeight:
    """Represents a synaptic weight."""
    source_neuron_id: str
    target_neuron_id: str
    weight: float
    confidence: float = 1.0
    id: str = field(default_factory=lambda: str(hashlib.sha256(str(time.time()).encode()).hexdigest())[:8])
    
    def __repr__(self):
        return f"Synapse({self.source_neuron_id} -> {self.target_neuron_id}, w={self.weight:.2f})"


class AxiomToSynapseConverter:
    """Convert axioms to synaptic weights for the brain simulation."""
    
    def __init__(self, axiom_base: AxiomBase):
        self.axiom_base = axiom_base
        self.synaptic_weights: List[SynapticWeight] = []
        self.neuron_counter: int = 0
    
    def _generate_neuron_id(self) -> str:
        """Generate a unique neuron ID."""
        self.neuron_counter += 1
        return f"neuron_{self.neuron_counter}"
    
    def convert_axiom_to_synapse(self, axiom: Axiom) -> List[SynapticWeight]:
        """Convert an axiom to synaptic weights."""
        weights = []
        
        # Map axiom to synaptic connection
        source_id = self._generate_neuron_id()
        target_id = self._generate_neuron_id()
        
        # Determine weight based on axiom relation and confidence
        if axiom.relation == "=":
            # Equality → strong excitatory connection
            weight = 0.9 * axiom.confidence
        elif axiom.relation == "!=":
            # Inequality → inhibitory connection
            weight = -0.7 * axiom.confidence
        elif axiom.relation == "+":
            # Addition → moderate excitatory
            weight = 0.5 * axiom.confidence
        elif axiom.relation == "-":
            # Subtraction → moderate inhibitory
            weight = -0.5 * axiom.confidence
        else:
            # Other relations → weak connection
            weight = 0.3 * axiom.confidence
        
        synapse = SynapticWeight(source_id, target_id, weight, axiom.confidence)
        weights.append(synapse)
        self.synaptic_weights.append(synapse)
        
        return weights
    
    def convert_all_axioms(self) -> List[SynapticWeight]:
        """Convert all axioms in the axiom base to synaptic weights."""
        all_weights = []
        for axiom in self.axiom_base.axioms.values():
            weights = self.convert_axiom_to_synapse(axiom)
            all_weights.extend(weights)
        return all_weights
    
    def get_synaptic_statistics(self) -> Dict[str, Any]:
        """Get statistics about synaptic weights."""
        if not self.synaptic_weights:
            return {
                "total_synapses": 0,
                "avg_weight": 0.0,
                "excitatory_count": 0,
                "inhibitory_count": 0
            }
        
        weights = [s.weight for s in self.synaptic_weights]
        excitatory = sum(1 for w in weights if w > 0)
        inhibitory = sum(1 for w in weights if w < 0)
        
        return {
            "total_synapses": len(self.synaptic_weights),
            "avg_weight": sum(weights) / len(weights),
            "excitatory_count": excitatory,
            "inhibitory_count": inhibitory,
            "excitatory_ratio": excitatory / len(self.synaptic_weights),
            "inhibitory_ratio": inhibitory / len(self.synaptic_weights)
        }


# =============================================================================
# LOGIC TO COGNITIVE INTEGRATOR
# =============================================================================

class LogicToCognitiveIntegrator:
    """Integrate logic engine with cognitive core for dual-process reasoning."""
    
    def __init__(self, inference_engine: InferenceEngine):
        self.inference_engine = inference_engine
        self.logic_cache: Dict[str, Any] = {}
        self.reasoning_history: List[Dict[str, Any]] = []
    
    def apply_logic_to_query(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply logic engine reasoning to a query."""
        # Use logic gates for fast reasoning (System 1)
        fast_result = self._apply_fast_logic(query, context)
        
        # Use inference engine for deep reasoning (System 2)
        deep_result = self._apply_deep_inference(query, context)
        
        result = {
            "query": query,
            "fast_reasoning": fast_result,
            "deep_reasoning": deep_result,
            "timestamp": time.time()
        }
        
        self.reasoning_history.append(result)
        return result
    
    def _apply_fast_logic(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply fast logic gates (System 1 reasoning)."""
        # Simple logical operations using logic gates
        conditions = context.get("conditions", [])
        
        if not conditions:
            return {"result": True, "method": "default_true"}
        
        # Apply AND gate to all conditions
        result = all(conditions)
        return {
            "result": result,
            "method": "logic_gate_and",
            "conditions_count": len(conditions)
        }
    
    def _apply_deep_inference(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply deep inference (System 2 reasoning)."""
        # Extract axioms from context
        axioms = context.get("axioms", [])
        
        if not axioms:
            return {"result": None, "method": "no_axioms"}
        
        # Apply inference engine
        conclusions = self.inference_engine.derive_conclusions(axioms)
        
        return {
            "result": conclusions,
            "method": "inference_engine",
            "conclusions_count": len(conclusions)
        }
    
    def get_reasoning_statistics(self) -> Dict[str, Any]:
        """Get statistics about reasoning operations."""
        if not self.reasoning_history:
            return {
                "total_reasoning_operations": 0,
                "fast_reasoning_count": 0,
                "deep_reasoning_count": 0
            }
        
        fast_count = sum(1 for r in self.reasoning_history if r["fast_reasoning"]["method"] != "default_true")
        deep_count = sum(1 for r in self.reasoning_history if r["deep_reasoning"]["method"] == "inference_engine")
        
        return {
            "total_reasoning_operations": len(self.reasoning_history),
            "fast_reasoning_count": fast_count,
            "deep_reasoning_count": deep_count
        }


# =============================================================================
# LEARNING TO DNA CONNECTOR
# =============================================================================

class LearningToDNAConnector:
    """Connect learning loop with Fractal DNA for persistent memory."""
    
    def __init__(self, learner: Learner):
        self.learner = learner
        self.dna_sequence: List[str] = []
        self.dna_hash: Optional[str] = None
    
    def extract_learning_to_dna(self) -> str:
        """Extract learning patterns into DNA sequence."""
        # Get learning statistics
        stats = self.learner.get_learning_statistics()
        
        # Encode rule weights into DNA
        dna_segments = []
        
        for rule, weight in stats.get("strongest_rules", []):
            # Encode rule and weight as DNA segment
            segment = self._encode_rule_weight(rule, weight)
            dna_segments.append(segment)
        
        # Create DNA sequence
        self.dna_sequence = dna_segments
        self.dna_hash = self._compute_dna_hash()
        
        return self.dna_hash
    
    def _encode_rule_weight(self, rule: str, weight: float) -> str:
        """Encode a rule and its weight into a DNA segment."""
        # Simple encoding: rule name + weight value
        weight_int = int(weight * 100)
        segment = f"{rule}_{weight_int}"
        return segment
    
    def _compute_dna_hash(self) -> str:
        """Compute hash of DNA sequence."""
        if not self.dna_sequence:
            return ""
        
        dna_string = "|".join(self.dna_sequence)
        return hashlib.sha256(dna_string.encode()).hexdigest()[:16]
    
    def validate_dna_consistency(self, expected_hash: str) -> bool:
        """Validate DNA consistency against expected hash."""
        current_hash = self.extract_learning_to_dna()
        return current_hash == expected_hash
    
    def get_dna_statistics(self) -> Dict[str, Any]:
        """Get statistics about DNA sequence."""
        return {
            "dna_length": len(self.dna_sequence),
            "dna_hash": self.dna_hash,
            "learning_stats": self.learner.get_learning_statistics()
        }


# =============================================================================
# BRAIN INTEGRATION ENGINE
# =============================================================================

class BrainIntegrationEngine:
    """Main engine for integrating bootstrap with comprehensive brain."""
    
    def __init__(self, bootstrap_engine: BootstrapEngine, comprehensive_brain: Optional['ComprehensiveBrain'] = None):
        self.bootstrap_engine = bootstrap_engine
        self.comprehensive_brain = comprehensive_brain
        
        # Initialize integration components
        self.region_mapper = SymbolToRegionMapper(bootstrap_engine.symbol_set)
        self.synapse_converter = AxiomToSynapseConverter(bootstrap_engine.axiom_base)
        self.logic_integrator = LogicToCognitiveIntegrator(bootstrap_engine.inference_engine)
        self.dna_connector = LearningToDNAConnector(bootstrap_engine.learner)
        
        # Integration status
        self.is_integrated = comprehensive_brain is not None and USING_REAL_BRAIN_SYSTEM
    
    def integrate_symbols_to_regions(self, symbols: List[Symbol]) -> Dict[str, List[Symbol]]:
        """Integrate symbols to brain regions."""
        return self.region_mapper.map_symbols_to_regions(symbols)
    
    def integrate_axioms_to_synapses(self) -> List[SynapticWeight]:
        """Integrate axioms to synaptic weights."""
        weights = self.synapse_converter.convert_all_axioms()
        
        # If integrated with comprehensive brain, actually add synapses
        if self.is_integrated and self.comprehensive_brain:
            self._inject_synapses_into_brain(weights)
        
        return weights
    
    def _inject_synapses_into_brain(self, weights: List[SynapticWeight]):
        """Inject bootstrap-derived synapses into the comprehensive brain."""
        if not self.comprehensive_brain:
            return
        
        # Convert bootstrap synaptic weights to brain synapses
        for weight in weights:
            # Map to actual brain regions
            # For now, create synapses between cortex and hippocampus as a bridge
            if hasattr(self.comprehensive_brain, 'synapses'):
                # Create actual synapse in comprehensive brain
                from comprehensive_brain_template import SynapseType
                synapse = Synapse(
                    id=f"bootstrap_{weight.id}",
                    source_region=BrainRegion.CORTEX,
                    target_region=BrainRegion.HIPPOCAMPUS,
                    synapse_type=SynapseType.PLASTIC if weight.weight > 0 else SynapseType.INHIBITORY,
                    strength=abs(weight.weight),
                    plasticity=0.1  # Bootstrap synapses are highly plastic
                )
                self.comprehensive_brain.synapses.append(synapse)
    
    def integrate_logic_to_cognitive(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate logic engine with cognitive reasoning."""
        return self.logic_integrator.apply_logic_to_query(query, context)
    
    def integrate_learning_to_dna(self) -> str:
        """Integrate learning patterns to DNA sequence."""
        return self.dna_connector.extract_learning_to_dna()
    
    def get_integration_statistics(self) -> Dict[str, Any]:
        """Get comprehensive integration statistics."""
        return {
            "region_mapping": {
                "total_mappings": len(self.region_mapper.mappings)
            },
            "synaptic_conversion": self.synapse_converter.get_synaptic_statistics(),
            "logic_integration": self.logic_integrator.get_reasoning_statistics(),
            "dna_connection": self.dna_connector.get_dna_statistics()
        }
    
    def process_query_with_brain(self, query: str) -> Dict[str, Any]:
        """Process a query through the integrated brain system."""
        # Step 1: Observe and tokenize (bootstrap)
        symbols = self.bootstrap_engine.observe(query)
        
        # Step 2: Map to brain regions
        region_mapping = self.integrate_symbols_to_regions(symbols)
        
        # Step 3: Apply rules (bootstrap)
        derived_axioms, applied_rules = self.bootstrap_engine.apply_rules(symbols)
        
        # Step 4: Integrate logic with cognitive reasoning
        context = {
            "axioms": derived_axioms,
            "conditions": [True] * len(derived_axioms)  # Placeholder conditions
        }
        reasoning_result = self.integrate_logic_to_cognitive(query, context)
        
        # Step 5: Process learning
        interaction = type('obj', (object,), {
            'input_symbols': symbols,
            'applied_rules': applied_rules,
            'result': derived_axioms,
            'contradiction_detected': False,
            'id': str(hashlib.sha256(str(time.time()).encode()).hexdigest())[:8]
        })()
        self.bootstrap_engine.learner.process_interaction(interaction)
        
        # Step 6: Extract DNA
        dna_hash = self.integrate_learning_to_dna()
        
        # Step 7: If integrated with comprehensive brain, also process through it
        comprehensive_result = None
        if self.is_integrated and self.comprehensive_brain:
            comprehensive_result = self._process_through_comprehensive_brain(query, symbols)
        
        return {
            "query": query,
            "symbols": [str(s) for s in symbols],
            "region_mapping": region_mapping,
            "derived_axioms": [str(a) for a in derived_axioms],
            "reasoning": reasoning_result,
            "dna_hash": dna_hash,
            "is_integrated": self.is_integrated,
            "comprehensive_brain_result": comprehensive_result,
            "statistics": self.get_integration_statistics()
        }
    
    def _process_through_comprehensive_brain(self, query: str, symbols: List[Symbol]) -> Dict[str, Any]:
        """Process query through the actual comprehensive brain system."""
        if not self.comprehensive_brain:
            return None
        
        try:
            # Use the comprehensive brain's process_query method
            result = self.comprehensive_brain.process_query(query)
            return {
                "success": True,
                "system": "comprehensive_brain",
                "brain_regions_activated": len(self.comprehensive_brain.regions),
                "total_synapses": len(self.comprehensive_brain.synapses),
                "total_neurons": len(self.comprehensive_brain.neurons)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "system": "comprehensive_brain"
            }


# =============================================================================
# DEMONSTRATION
# =============================================================================

def demonstrate_brain_integration():
    """Demonstrate brain integration capabilities."""
    print("=" * 60)
    print("AGI Bootstrap Brain Integration - Demonstration")
    print("=" * 60)
    
    # Check if comprehensive brain is available
    print(f"\nUsing Real Brain System: {USING_REAL_BRAIN_SYSTEM}")
    
    # Initialize bootstrap engine
    bootstrap_engine = BootstrapEngine()
    
    # Try to initialize comprehensive brain
    comprehensive_brain = None
    if USING_REAL_BRAIN_SYSTEM:
        try:
            comprehensive_brain = ComprehensiveBrain()
            print("Comprehensive Brain initialized successfully")
        except Exception as e:
            print(f"Failed to initialize Comprehensive Brain: {e}")
            comprehensive_brain = None
    
    # Initialize integration engine
    integration_engine = BrainIntegrationEngine(bootstrap_engine, comprehensive_brain)
    print(f"Integration Status: {'INTEGRATED' if integration_engine.is_integrated else 'STANDALONE'}")
    
    print("\n1. Symbol to Region Mapping:")
    print("-" * 60)
    
    symbols = bootstrap_engine.observe("RED CIRCLE")
    region_mapping = integration_engine.integrate_symbols_to_regions(symbols)
    
    for region, syms in region_mapping.items():
        print(f"   {region}: {[str(s) for s in syms]}")
    
    print("\n2. Axiom to Synapse Conversion:")
    print("-" * 60)
    
    synapses = integration_engine.integrate_axioms_to_synapses()
    synapse_stats = integration_engine.synapse_converter.get_synaptic_statistics()
    
    print(f"   Total synapses: {synapse_stats['total_synapses']}")
    print(f"   Average weight: {synapse_stats['avg_weight']:.2f}")
    print(f"   Excitatory: {synapse_stats['excitatory_count']} ({synapse_stats['excitatory_ratio']:.1%})")
    print(f"   Inhibitory: {synapse_stats['inhibitory_count']} ({synapse_stats['inhibitory_ratio']:.1%})")
    
    print("\n3. Logic to Cognitive Integration:")
    print("-" * 60)
    
    query = "RED"
    context = {"axioms": [], "conditions": [True, False, True]}
    reasoning_result = integration_engine.integrate_logic_to_cognitive(query, context)
    
    print(f"   Query: {query}")
    print(f"   Fast reasoning: {reasoning_result['fast_reasoning']}")
    print(f"   Deep reasoning: {reasoning_result['deep_reasoning']}")
    
    print("\n4. Learning to DNA Connection:")
    print("-" * 60)
    
    dna_hash = integration_engine.integrate_learning_to_dna()
    dna_stats = integration_engine.dna_connector.get_dna_statistics()
    
    print(f"   DNA hash: {dna_hash}")
    print(f"   DNA length: {dna_stats['dna_length']}")
    
    print("\n5. Full Query Processing:")
    print("-" * 60)
    
    result = integration_engine.process_query_with_brain("BLUE SQUARE")
    
    print(f"   Query: {result['query']}")
    print(f"   Symbols: {result['symbols']}")
    print(f"   Regions: {list(result['region_mapping'].keys())}")
    print(f"   DNA hash: {result['dna_hash']}")
    
    print("\n6. Integration Statistics:")
    print("-" * 60)
    
    stats = integration_engine.get_integration_statistics()
    for category, data in stats.items():
        print(f"   {category}: {data}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demonstrate_brain_integration()
