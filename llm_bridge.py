"""
LLM Bridge for Integration
Bridges the field-based cognitive system with LLM capabilities for natural language processing and reasoning.

Components:
- StateEncoder: Encodes field states to LLM prompts
- StateDecoder: Decodes LLM responses to field states
- LLMInterface: Interface to Ollama LLM models
- LLMBridge: Unified bridge layer
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
# STATE ENCODER
# =============================================================================

class StateEncoder:
    """Encodes field states to LLM prompts."""
    
    def __init__(self, state_dim: int = 64):
        self.state_dim = state_dim
        self.token_mapping = {}
        self._initialize_mapping()
    
    def _initialize_mapping(self):
        """Initialize state to token mapping."""
        # Map state regions to conceptual tokens
        self.token_mapping = {
            "high_positive": "excited",
            "high_negative": "inhibited",
            "low_magnitude": "neutral",
            "oscillating": "dynamic"
        }
    
    def encode_state(self, state: np.ndarray) -> str:
        """Encode state to natural language description."""
        # Calculate statistics
        mean = np.mean(state)
        std = np.std(state)
        max_val = np.max(state)
        min_val = np.min(state)
        
        # Generate description
        description = f"Current cognitive state: "
        
        if mean > 0.3:
            description += "highly activated"
        elif mean < -0.3:
            description += "strongly inhibited"
        else:
            description += "neutral"
        
        description += f" (mean={mean:.3f}, std={std:.3f}). "
        
        if std > 0.5:
            description += "State is highly variable and dynamic. "
        elif std < 0.2:
            description += "State is stable and consistent. "
        
        # Identify active regions
        active_indices = np.where(np.abs(state) > 0.5)[0]
        if len(active_indices) > 0:
            description += f"Active regions: {len(active_indices)} out of {self.state_dim}. "
        
        return description
    
    def encode_attractor(self, attractor_name: str, confidence: float) -> str:
        """Encode attractor state to description."""
        return f"System state collapsed to attractor '{attractor_name}' with confidence {confidence:.3f}."
    
    def encode_dynamics(self, energy: float, stability: float) -> str:
        """Encode dynamics information."""
        return f"Energy: {energy:.3f}, Stability: {stability:.3f}."


# =============================================================================
# STATE DECODER
# =============================================================================

class StateDecoder:
    """Decodes LLM responses to field states."""
    
    def __init__(self, state_dim: int = 64):
        self.state_dim = state_dim
        self.semantic_mapping = {}
        self._initialize_mapping()
    
    def _initialize_mapping(self):
        """Initialize semantic to state mapping."""
        self.semantic_mapping = {
            "excite": 0.8,
            "activate": 0.7,
            "enhance": 0.6,
            "inhibit": -0.8,
            "suppress": -0.7,
            "reduce": -0.6,
            "neutral": 0.0,
            "maintain": 0.0
        }
    
    def decode_instruction(self, text: str) -> Tuple[str, Dict[str, Any]]:
        """Decode text to SIMD instruction."""
        text_lower = text.lower()
        
        if "excite" in text_lower or "activate" in text_lower or "enhance" in text_lower:
            return "EXC", {"strength": 1.0}
        elif "inhibit" in text_lower or "suppress" in text_lower or "reduce" in text_lower:
            return "INH", {"strength": 1.0}
        elif "support" in text_lower or "merge" in text_lower or "average" in text_lower:
            return "SUP", {}
        elif "collapse" in text_lower or "decide" in text_lower or "choose" in text_lower:
            return "CLP", {"threshold": 0.5}
        else:
            return "SUP", {}  # Default to support
    
    def decode_to_state(self, text: str, base_state: np.ndarray) -> np.ndarray:
        """Decode text to state modification."""
        instruction, kwargs = self.decode_instruction(text)
        
        # Apply instruction to base state
        if instruction == "EXC":
            return np.clip(base_state + 0.1, -1.0, 1.0)
        elif instruction == "INH":
            return np.clip(base_state - 0.1, -1.0, 1.0)
        elif instruction == "SUP":
            avg = np.mean(base_state)
            return 0.5 * base_state + 0.5 * avg
        elif instruction == "CLP":
            return np.where(base_state > 0.5, 1.0, np.where(base_state < -0.5, -1.0, base_state))
        else:
            return base_state.copy()


# =============================================================================
# LLM INTERFACE
# =============================================================================

class LLMInterface:
    """Interface to Ollama LLM models."""
    
    def __init__(self, model: str = "gemma4"):
        self.model = model
        self.available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """Check if Ollama is available."""
        try:
            import ollama
            return True
        except ImportError:
            return False
    
    def generate(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate response from LLM."""
        if not self.available:
            return f"LLM not available. Simulated response for: {prompt[:50]}..."
        
        try:
            import ollama
            
            full_prompt = prompt
            if context:
                full_prompt = f"Context: {context}\n\nQuery: {prompt}"
            
            response = ollama.generate(model=self.model, prompt=full_prompt)
            return response.get("response", "")
        except Exception as e:
            return f"LLM error: {str(e)}"
    
    def generate_with_state(self, prompt: str, state_description: str) -> str:
        """Generate response with state context."""
        context = f"Cognitive State: {state_description}"
        return self.generate(prompt, context)


# =============================================================================
# LLM BRIDGE
# =============================================================================

class LLMBridge:
    """Unified LLM bridge layer."""
    
    def __init__(self, state_dim: int = 64, model: str = "gemma4"):
        self.state_dim = state_dim
        self.encoder = StateEncoder(state_dim)
        self.decoder = StateDecoder(state_dim)
        self.llm_interface = LLMInterface(model)
        self.is_integrated = USING_REAL_BRAIN_SYSTEM
        self.bridge_history: List[Dict[str, Any]] = []
    
    def query_with_state(self, query: str, state: np.ndarray) -> Dict[str, Any]:
        """Query LLM with current cognitive state."""
        # Encode state
        state_description = self.encoder.encode_state(state)
        
        # Generate response
        response = self.llm_interface.generate_with_state(query, state_description)
        
        # Decode response to instruction
        instruction, kwargs = self.decoder.decode_instruction(response)
        
        # Apply instruction to state
        new_state = self.decoder.decode_to_state(response, state)
        
        result = {
            "query": query,
            "state_description": state_description,
            "llm_response": response,
            "decoded_instruction": instruction,
            "new_state": new_state,
            "is_integrated": self.is_integrated
        }
        
        self.bridge_history.append(result)
        return result
    
    def query_attractor_guidance(self, query: str, attractor_name: str, confidence: float) -> Dict[str, Any]:
        """Query LLM with attractor context."""
        attractor_description = self.encoder.encode_attractor(attractor_name, confidence)
        
        response = self.llm_interface.generate_with_state(query, attractor_description)
        instruction, kwargs = self.decoder.decode_instruction(response)
        
        return {
            "query": query,
            "attractor_context": attractor_description,
            "llm_response": response,
            "decoded_instruction": instruction,
            "is_integrated": self.is_integrated
        }
    
    def query_dynamics_guidance(self, query: str, energy: float, stability: float) -> Dict[str, Any]:
        """Query LLM with dynamics context."""
        dynamics_description = self.encoder.encode_dynamics(energy, stability)
        
        response = self.llm_interface.generate_with_state(query, dynamics_description)
        instruction, kwargs = self.decoder.decode_instruction(response)
        
        return {
            "query": query,
            "dynamics_context": dynamics_description,
            "llm_response": response,
            "decoded_instruction": instruction,
            "is_integrated": self.is_integrated
        }
    
    def get_bridge_statistics(self) -> Dict[str, Any]:
        """Get bridge statistics."""
        instruction_counts = defaultdict(int)
        for record in self.bridge_history:
            instruction_counts[record["decoded_instruction"]] += 1
        
        return {
            "total_queries": len(self.bridge_history),
            "llm_available": self.llm_interface.available,
            "instruction_distribution": dict(instruction_counts),
            "is_integrated": self.is_integrated
        }


# =============================================================================
# DEMONSTRATION
# =============================================================================

def demonstrate_llm_bridge():
    """Demonstrate LLM bridge capabilities."""
    print("=" * 60)
    print("LLM Bridge - Demonstration")
    print("=" * 60)
    
    print(f"\nUsing Real Brain System: {USING_REAL_BRAIN_SYSTEM}")
    
    # Initialize LLM bridge
    bridge = LLMBridge(state_dim=64, model="gemma4")
    print(f"Integration Status: {'INTEGRATED' if bridge.is_integrated else 'STANDALONE'}")
    
    print("\n1. Bridge Statistics:")
    print("-" * 60)
    stats = bridge.get_bridge_statistics()
    print(f"   Total queries: {stats['total_queries']}")
    print(f"   LLM available: {stats['llm_available']}")
    
    print("\n2. State Encoding:")
    print("-" * 60)
    
    # Create sample state
    state = np.random.randn(64)
    state = np.tanh(state)
    
    state_description = bridge.encoder.encode_state(state)
    print(f"   {state_description}")
    
    print("\n3. Query with State:")
    print("-" * 60)
    
    query = "What should I do next?"
    result = bridge.query_with_state(query, state)
    
    print(f"   Query: {result['query']}")
    print(f"   State description: {result['state_description'][:80]}...")
    print(f"   LLM response: {result['llm_response'][:80]}...")
    print(f"   Decoded instruction: {result['decoded_instruction']}")
    
    print("\n4. Attractor Guidance:")
    print("-" * 60)
    
    attractor_query = "How should I interpret this attractor?"
    result = bridge.query_attractor_guidance(attractor_query, "apple", 0.85)
    
    print(f"   Query: {result['query']}")
    print(f"   Attractor context: {result['attractor_context']}")
    print(f"   LLM response: {result['llm_response'][:80]}...")
    print(f"   Decoded instruction: {result['decoded_instruction']}")
    
    print("\n5. Dynamics Guidance:")
    print("-" * 60)
    
    dynamics_query = "Is the system stable?"
    result = bridge.query_dynamics_guidance(dynamics_query, -15.5, 0.92)
    
    print(f"   Query: {result['query']}")
    print(f"   Dynamics context: {result['dynamics_context']}")
    print(f"   LLM response: {result['llm_response'][:80]}...")
    print(f"   Decoded instruction: {result['decoded_instruction']}")
    
    print("\n6. Multiple Queries:")
    print("-" * 60)
    
    queries = [
        "What is the best action?",
        "Should I continue?",
        "How to improve stability?"
    ]
    
    for i, query in enumerate(queries):
        state = np.random.randn(64)
        state = np.tanh(state)
        result = bridge.query_with_state(query, state)
        print(f"   Query {i+1}: {result['decoded_instruction']}")
    
    print("\n7. Final Statistics:")
    print("-" * 60)
    
    final_stats = bridge.get_bridge_statistics()
    for key, value in final_stats.items():
        if key != "instruction_distribution":
            print(f"   {key}: {value}")
    
    print(f"   Instruction distribution: {final_stats['instruction_distribution']}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demonstrate_llm_bridge()
