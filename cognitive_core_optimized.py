"""
Phase 2: Cognitive Core - OPTIMIZED VERSION
Optimized for fast response times with timeout mechanisms
Direct Ollama API calls without LangChain overhead
"""

import time
import json
import requests
from typing import Dict, Optional, List

# Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
SYSTEM_1_MODEL = "gemma4"
SYSTEM_2_MODEL = "deepseek-r1"
SYSTEM_1_TIMEOUT = 10  # seconds (math/physics queries require more computation)
SYSTEM_2_TIMEOUT = 15  # seconds (deepseek-r1 responds in ~8.8s)

class OptimizedCognitiveCore:
    """
    Optimized dual-process cognition system with direct Ollama API calls.
    Fast response times with timeout mechanisms.
    """
    
    def __init__(self):
        self.memory = []
        self.reasoning_history = []
        self.performance_metrics = {
            "system_1_calls": 0,
            "system_2_calls": 0,
            "system_1_timeouts": 0,
            "system_2_timeouts": 0,
            "avg_system_1_time": 0,
            "avg_system_2_time": 0
        }
    
    def _call_ollama(self, model: str, prompt: str, timeout: int = 10) -> Dict:
        """Direct Ollama API call without LangChain overhead."""
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 50,  # Reduced token limit for speed
                        "temperature": 0.7,
                        "top_p": 0.9
                    }
                },
                timeout=timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                elapsed = time.time() - start_time
                return {
                    "response": data.get("response", ""),
                    "processing_time": elapsed,
                    "success": True
                }
            else:
                elapsed = time.time() - start_time
                return {
                    "error": f"Ollama API error: {response.status_code}",
                    "processing_time": elapsed,
                    "success": False
                }
        
        except requests.exceptions.Timeout:
            elapsed = time.time() - start_time
            return {
                "error": f"Request timeout after {timeout}s",
                "processing_time": elapsed,
                "success": False
            }
        
        except Exception as e:
            elapsed = time.time() - start_time
            return {
                "error": str(e),
                "processing_time": elapsed,
                "success": False
            }
    
    def _should_use_system_2(self, query: str) -> bool:
        """Determine if query requires deep reasoning."""
        reasoning_keywords = [
            "analyze", "complex", "why", "how does", "evaluate", "critique",
            "compare", "synthesize", "reason", "logic", "prove", "derive",
            "algorithm", "optimization", "strategy", "architect", "design"
        ]
        
        query_lower = query.lower()
        for keyword in reasoning_keywords:
            if keyword in query_lower:
                return True
        
        if len(query) > 200:
            return True
        
        return False
    
    def _system_1_process(self, query: str) -> Dict:
        """System 1: Fast, intuitive processing with direct API call."""
        start_time = time.time()
        
        prompt = f"""You are a digital organism with fast, intuitive cognition.

User Query: {query}

Provide a direct, concise response. Be practical and to the point."""
        
        result = self._call_ollama(SYSTEM_1_MODEL, prompt, SYSTEM_1_TIMEOUT)
        
        elapsed = time.time() - start_time
        
        if result.get("success"):
            self.performance_metrics["system_1_calls"] += 1
            self.performance_metrics["avg_system_1_time"] = (
                (self.performance_metrics["avg_system_1_time"] * 
                 (self.performance_metrics["system_1_calls"] - 1) + elapsed) / 
                self.performance_metrics["system_1_calls"]
            )
            
            return {
                "system": "System 1",
                "response": result["response"],
                "processing_time": elapsed,
                "mode": "intuitive",
                "success": True
            }
        else:
            self.performance_metrics["system_1_timeouts"] += 1
            return {
                "system": "System 1",
                "response": f"Error: {result.get('error', 'Unknown error')}",
                "processing_time": elapsed,
                "mode": "intuitive",
                "success": False
            }
    
    def _system_2_process(self, query: str) -> Dict:
        """System 2: Deep reasoning with timeout."""
        start_time = time.time()
        
        # Simplified reasoning prompt for speed
        prompt = f"""You are engaged in analytical reasoning.

Query: {query}

Provide a clear, well-structured analysis:
1. Key points
2. Analysis
3. Conclusion

Be thorough but concise."""
        
        result = self._call_ollama(SYSTEM_2_MODEL, prompt, SYSTEM_2_TIMEOUT)
        
        elapsed = time.time() - start_time
        
        if result.get("success"):
            self.performance_metrics["system_2_calls"] += 1
            self.performance_metrics["avg_system_2_time"] = (
                (self.performance_metrics["avg_system_2_time"] * 
                 (self.performance_metrics["system_2_calls"] - 1) + elapsed) / 
                self.performance_metrics["system_2_calls"]
            )
            
            return {
                "system": "System 2",
                "response": result["response"],
                "processing_time": elapsed,
                "mode": "analytical",
                "success": True
            }
        else:
            self.performance_metrics["system_2_timeouts"] += 1
            # Fallback to System 1 if System 2 fails
            print(f"System 2 failed ({result.get('error')}), falling back to System 1")
            return self._system_1_process(query)
    
    def process_query(self, query: str) -> Dict:
        """Main cognitive processing pipeline with optimization."""
        # Determine which cognitive system to use
        use_system_2 = self._should_use_system_2(query)
        
        if use_system_2:
            result = self._system_2_process(query)
        else:
            result = self._system_1_process(query)
        
        # Store interaction in memory
        interaction = {
            "query": query,
            "response": result["response"],
            "system_used": result["system"],
            "processing_time": result["processing_time"],
            "success": result.get("success", False),
            "timestamp": time.time()
        }
        
        self.memory.append(interaction)
        
        return result
    
    def get_performance_summary(self) -> Dict:
        """Return performance metrics."""
        total_calls = self.performance_metrics["system_1_calls"] + self.performance_metrics["system_2_calls"]
        total_timeouts = self.performance_metrics["system_1_timeouts"] + self.performance_metrics["system_2_timeouts"]
        
        if total_calls == 0:
            return {"status": "No queries processed yet"}
        
        return {
            "total_queries": total_calls,
            "timeouts": total_timeouts,
            "timeout_rate": f"{(total_timeouts / total_calls) * 100:.1f}%",
            "system_1_calls": self.performance_metrics["system_1_calls"],
            "system_2_calls": self.performance_metrics["system_2_calls"],
            "avg_system_1_time": f"{self.performance_metrics['avg_system_1_time']:.2f}s",
            "avg_system_2_time": f"{self.performance_metrics['avg_system_2_time']:.2f}s",
            "memory_entries": len(self.memory)
        }

# Test the optimized cognitive core
if __name__ == "__main__":
    print("Digital Organism - Phase 2: Cognitive Core (OPTIMIZED)")
    print("=" * 60)
    print("Fast response times with timeout mechanisms\n")
    
    cognitive_core = OptimizedCognitiveCore()
    
    # Test queries
    test_queries = [
        ("What is 247 * 389?", "Math - System 1"),
        ("Solve for x: 3x + 7 = 22", "Algebra - System 1"),
        ("What is the square root of 625?", "Math - System 1"),
        ("If a train travels at 60 mph for 2.5 hours, how far does it travel?", "Word problem - System 1"),
        ("What is 15% of 480?", "Percentage - System 1"),
        ("Two cars approach each other from 100 miles apart. Car A travels at 60 mph, Car B at 40 mph. How long until they collide?", "Physics - System 1"),
        ("Analyze the relationship between correlation and causation", "Analysis - System 2"),
    ]
    
    results = []
    
    for query, expected_system in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"Expected: {expected_system}")
        print(f"{'='*60}")
        
        result = cognitive_core.process_query(query)
        
        print(f"System Used: {result['system']}")
        print(f"Processing Time: {result['processing_time']:.2f}s")
        print(f"Success: {result.get('success', True)}")
        
        print(f"\nResponse: {result['response'][:200]}...")
        
        results.append({
            "query": query,
            "time": result["processing_time"],
            "success": result.get("success", True),
            "system": result["system"]
        })
    
    # Print performance summary
    print(f"\n{'='*60}")
    print("Performance Summary")
    print(f"{'='*60}")
    summary = cognitive_core.get_performance_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    # Calculate statistics
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    if successful:
        avg_time = sum(r["time"] for r in successful) / len(successful)
        max_time = max(r["time"] for r in successful)
        min_time = min(r["time"] for r in successful)
        
        print(f"\n{'='*60}")
        print("Response Time Statistics")
        print(f"{'='*60}")
        print(f"Successful queries: {len(successful)}/{len(results)}")
        print(f"Failed/Timeout queries: {len(failed)}/{len(results)}")
        print(f"Average response time: {avg_time:.2f}s")
        print(f"Min response time: {min_time:.2f}s")
        print(f"Max response time: {max_time:.2f}s")
        
        if avg_time < 5:
            print("\n[EXCELLENT] Average response time under 5 seconds")
        elif avg_time < 10:
            print("\n[GOOD] Average response time under 10 seconds")
        else:
            print(f"\n[NEEDS IMPROVEMENT] Average response time {avg_time:.2f}s")
