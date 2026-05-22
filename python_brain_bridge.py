"""
Python Brain Bridge Wrapper
JSON-based interface for Java-Python integration
"""

import sys
import json
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from comprehensive_brain_template import ComprehensiveBrain, BrainRegion
import numpy as np

class PythonBrainBridge:
    """Bridge interface for Java-Python integration"""
    
    def __init__(self):
        print("Initializing Python Comprehensive Brain...", file=sys.stderr)
        self.brain = ComprehensiveBrain()
        self.brain.initialize_field_attractors()
        print("Python brain initialized successfully", file=sys.stderr)
    
    def process_query(self, query_data):
        """Process query from Java"""
        try:
            system = query_data.get("system", "comprehensive_brain")
            query = query_data.get("query", {})
            mode = query.get("mode", "default")
            
            if system == "field_compute_runtime":
                return self.process_field_runtime(mode, query)
            elif system == "working_memory":
                return self.process_working_memory(mode, query)
            elif system == "motor_intent":
                return self.process_motor_intent(mode, query)
            elif system == "episodic_memory":
                return self.process_episodic_memory(mode, query)
            elif system == "semantic_memory":
                return self.process_semantic_memory(mode, query)
            elif system == "closed_loop_reward":
                return self.process_closed_loop_reward(mode, query)
            elif system == "comprehensive_brain":
                return self.process_comprehensive_brain(mode, query)
            else:
                return {"success": False, "error": f"Unknown system: {system}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def process_field_runtime(self, mode, query):
        """Process field compute runtime operations"""
        field_runtime = self.brain.systems["field_compute_runtime"]
        
        if mode == "pipeline":
            query_str = query.get("query", "")
            result = self.brain.process_field_pipeline(query_str)
            return {"success": True, "result": result}
        elif mode == "execute":
            instruction = query.get("instruction", "EXC")
            kwargs = {k: v for k, v in query.items() if k not in ["mode", "instruction"]}
            result = field_runtime.process({"mode": "execute", "instruction": instruction, **kwargs})
            return {"success": True, "result": result}
        elif mode == "update":
            input_force = query.get("input_force", None)
            result = field_runtime.process({"mode": "update", "input_force": input_force})
            return {"success": True, "result": result}
        elif mode == "attractor":
            state = np.array(query.get("state", []))
            result = field_runtime.process({"mode": "attractor", "state": state.tolist()})
            return {"success": True, "result": result}
        elif mode == "collapse":
            state = np.array(query.get("state", []))
            strength = query.get("strength", 0.5)
            result = field_runtime.process({"mode": "collapse", "state": state.tolist(), "strength": strength})
            return {"success": True, "result": result}
        elif mode == "output":
            result = field_runtime.process({"mode": "output"})
            return {"success": True, "result": result}
        elif mode == "stats":
            return {
                "success": True,
                "stats": {
                    "field_energy": field_runtime._compute_energy(field_runtime.field),
                    "instruction_count": len(field_runtime.instruction_history),
                    "attractor_count": len(field_runtime.attractors)
                }
            }
        else:
            return {"success": False, "error": f"Unknown mode: {mode}"}
    
    def process_working_memory(self, mode, query):
        """Process working memory operations"""
        wm_system = self.brain.systems["working_memory"]
        
        if mode == "add":
            content = query.get("content", "")
            activation = query.get("activation", 0.5)
            wm_system.process({"mode": "add", "content": content, "activation": activation})
            return {"success": True}
        elif mode == "get":
            threshold = query.get("threshold", 0.5)
            result = wm_system.process({"mode": "get", "threshold": threshold})
            return {"success": True, "result": result}
        else:
            return {"success": False, "error": f"Unknown mode: {mode}"}
    
    def process_motor_intent(self, mode, query):
        """Process motor intent operations"""
        motor_system = self.brain.systems["motor_intent"]
        
        if mode == "decode":
            state = np.array(query.get("state", []))
            result = motor_system.process({"mode": "decode", "state": state.tolist()})
            return {"success": True, "result": result}
        elif mode == "train":
            states = query.get("states", [])
            targets = query.get("targets", [])
            learning_rate = query.get("learning_rate", 0.01)
            motor_system.train_decoder(states, targets, learning_rate)
            return {"success": True}
        else:
            return {"success": False, "error": f"Unknown mode: {mode}"}
    
    def process_episodic_memory(self, mode, query):
        """Process episodic memory operations"""
        episodic_system = self.brain.systems["episodic_memory"]
        
        if mode == "store":
            content = query.get("content", "")
            context = query.get("context", {})
            importance = query.get("importance", 0.5)
            episodic_system.process({"mode": "store", "content": content, "context": context, "importance": importance})
            return {"success": True}
        elif mode == "recall":
            query_context = query.get("context", {})
            k = query.get("k", 5)
            result = episodic_system.process({"mode": "recall", "query_context": query_context, "k": k})
            return {"success": True, "result": result}
        else:
            return {"success": False, "error": f"Unknown mode: {mode}"}
    
    def process_semantic_memory(self, mode, query):
        """Process semantic memory operations"""
        semantic_system = self.brain.systems["semantic_memory"]
        
        if mode == "add":
            concept = query.get("concept", "")
            definition = query.get("definition", "")
            associations = query.get("associations", [])
            semantic_system.process({"mode": "add", "concept": concept, "definition": definition, "associations": associations})
            return {"success": True}
        elif mode == "strengthen":
            concept = query.get("concept", "")
            amount = query.get("amount", 0.1)
            semantic_system.process({"mode": "strengthen", "concept": concept, "amount": amount})
            return {"success": True}
        elif mode == "get_related":
            concept = query.get("concept", "")
            depth = query.get("depth", 2)
            result = semantic_system.process({"mode": "get_related", "concept": concept, "depth": depth})
            return {"success": True, "result": result}
        else:
            return {"success": False, "error": f"Unknown mode: {mode}"}
    
    def process_closed_loop_reward(self, mode, query):
        """Process closed-loop reward operations"""
        reward_system = self.brain.systems["closed_loop_reward"]
        
        if mode == "action":
            action = query.get("action", "")
            reward_system.process({"mode": "action", "action": action})
            return {"success": True}
        elif mode == "reward":
            reward = query.get("reward", 0.0)
            reward_system.process({"mode": "reward", "reward": reward})
            return {"success": True}
        elif mode == "get_dopamine":
            return {"success": True, "dopamine": reward_system.dopamine_level}
        else:
            return {"success": False, "error": f"Unknown mode: {mode}"}
    
    def process_comprehensive_brain(self, mode, query):
        """Process comprehensive brain operations"""
        
        if mode == "homeostasis":
            self.brain.apply_homeostasis()
            return {"success": True}
        elif mode == "get_homeostasis_stats":
            stats = self.brain.get_homeostasis_stats()
            return {"success": True, "stats": stats}
        elif mode == "get_continuous_state":
            state = self.brain.get_continuous_state()
            return {"success": True, "state": state.tolist()}
        elif mode == "get_system_status":
            status = self.brain.get_system_status()
            return {"success": True, "status": status}
        elif mode == "activate_region":
            region = query.get("region", "CORTEX")
            stimulus = query.get("stimulus", 0.5)
            self.brain.activate_region(BrainRegion[region], stimulus=stimulus)
            return {"success": True}
        elif mode == "apply_field_operation":
            operation = query.get("operation", "exc")
            region = query.get("region", "CORTEX")
            strength = query.get("strength", 0.5)
            self.brain.apply_field_operation(operation, BrainRegion[region], strength=strength)
            return {"success": True}
        else:
            return {"success": False, "error": f"Unknown mode: {mode}"}

def main():
    """Main bridge loop - read JSON from stdin, write JSON to stdout"""
    bridge = PythonBrainBridge()
    
    # Send initialization confirmation
    print(json.dumps({"status": "initialized", "systems": 15}))
    sys.stdout.flush()
    
    # Process queries from stdin
    for line in sys.stdin:
        if not line.strip():
            continue
        
        try:
            query_data = json.loads(line)
            response = bridge.process_query(query_data)
            print(json.dumps(response))
            sys.stdout.flush()
        except json.JSONDecodeError as e:
            error_response = {"success": False, "error": f"JSON decode error: {str(e)}"}
            print(json.dumps(error_response))
            sys.stdout.flush()
        except Exception as e:
            error_response = {"success": False, "error": f"Processing error: {str(e)}"}
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
