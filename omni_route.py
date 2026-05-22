"""
Phase 2: OmniRoute - Provider Resilience System
Automatic provider/model switching for 24/7 operation
"""

from langchain_ollama import OllamaLLM
from typing import Dict, List, Optional
import time
import random

class Provider:
    """Represents a model provider with health and performance metrics."""
    
    def __init__(self, name: str, model: str, base_url: str = None):
        self.name = name
        self.model = model
        self.base_url = base_url or "http://localhost:11434"
        self.health = 100.0  # 0-100 scale
        self.quota_remaining = 100.0  # percentage
        self.cost_per_token = 0.001  # default cost
        self.avg_latency = 0.5  # seconds
        self.stability_score = 95.0  # 0-100 scale
        self.task_fit_score = 85.0  # 0-100 scale
        self.success_count = 0
        self.failure_count = 0
    
    def calculate_combo_score(self) -> float:
        """
        Auto-Combo Score from NeoClaw/OmniRoute:
        Score = 0.25(Health) + 0.20(Quota) + 0.20(Cost⁻¹) + 0.15(Latency⁻¹) + 0.10(TaskFit) + 0.10(Stability)
        """
        # Normalize cost (lower is better, so invert)
        cost_score = max(0, 100 - (self.cost_per_token * 10000))
        
        # Normalize latency (lower is better, so invert)
        latency_score = max(0, 100 - (self.avg_latency * 100))
        
        score = (
            0.25 * self.health +
            0.20 * self.quota_remaining +
            0.20 * cost_score +
            0.15 * latency_score +
            0.10 * self.task_fit_score +
            0.10 * self.stability_score
        )
        
        return score
    
    def update_metrics(self, success: bool, latency: float):
        """Update provider metrics after a request."""
        if success:
            self.success_count += 1
            # Improve health slightly on success
            self.health = min(100, self.health + 0.5)
            # Update average latency
            total_requests = self.success_count + self.failure_count
            self.avg_latency = (self.avg_latency * (total_requests - 1) + latency) / total_requests
        else:
            self.failure_count += 1
            # Decrease health significantly on failure
            self.health = max(0, self.health - 10)
        
        # Decrease quota slightly with each request
        self.quota_remaining = max(0, self.quota_remaining - 0.1)

class OmniRoute:
    """
    Automatic provider routing system for resilience.
    Implements the Auto-Combo Score algorithm for provider selection.
    """
    
    def __init__(self):
        self.providers: List[Provider] = []
        self.current_provider: Optional[Provider] = None
        self.routing_history: List[Dict] = []
        self.fallback_chain: List[str] = []
    
    def add_provider(self, provider: Provider):
        """Add a provider to the routing pool."""
        self.providers.append(provider)
        if not self.current_provider:
            self.current_provider = provider
        print(f"Added provider: {provider.name} ({provider.model})")
    
    def select_provider(self, task_type: str = "general") -> Provider:
        """
        Select the best provider based on Auto-Combo Score.
        Can be influenced by task type.
        """
        if not self.providers:
            raise ValueError("No providers available")
        
        # Calculate scores for all providers
        scored_providers = []
        for provider in self.providers:
            # Adjust task fit score based on task type
            if task_type == "reasoning" and "deepseek" in provider.model.lower():
                provider.task_fit_score = 95.0
            elif task_type == "fast" and "gemma" in provider.model.lower():
                provider.task_fit_score = 95.0
            else:
                provider.task_fit_score = 85.0
            
            score = provider.calculate_combo_score()
            scored_providers.append((score, provider))
        
        # Sort by score (highest first)
        scored_providers.sort(key=lambda x: x[0], reverse=True)
        
        # Select top provider
        best_provider = scored_providers[0][1]
        
        # Log routing decision
        routing_decision = {
            "timestamp": time.time(),
            "selected_provider": best_provider.name,
            "score": scored_providers[0][0],
            "task_type": task_type,
            "all_scores": [(p.name, s) for s, p in scored_providers]
        }
        self.routing_history.append(routing_decision)
        
        # Update current provider if different
        if self.current_provider != best_provider:
            print(f"Switching provider: {self.current_provider.name} -> {best_provider.name}")
            self.current_provider = best_provider
        
        return best_provider
    
    def execute_with_routing(self, prompt: str, task_type: str = "general", max_retries: int = 3) -> Dict:
        """
        Execute a prompt with automatic routing and fallback.
        """
        attempts = 0
        last_error = None
        
        while attempts < max_retries:
            attempts += 1
            
            try:
                # Select best provider
                provider = self.select_provider(task_type)
                
                # Execute with selected provider
                start_time = time.time()
                llm = OllamaLLM(model=provider.model, base_url=provider.base_url)
                response = llm.invoke(prompt)
                latency = time.time() - start_time
                
                # Update provider metrics (success)
                provider.update_metrics(success=True, latency=latency)
                
                return {
                    "response": response,
                    "provider": provider.name,
                    "model": provider.model,
                    "latency": latency,
                    "attempts": attempts,
                    "success": True
                }
                
            except Exception as e:
                last_error = str(e)
                
                # Update provider metrics (failure)
                if self.current_provider:
                    self.current_provider.update_metrics(success=False, latency=0)
                
                # Try next provider
                if self.current_provider in self.providers:
                    idx = self.providers.index(self.current_provider)
                    if idx < len(self.providers) - 1:
                        self.current_provider = self.providers[idx + 1]
                    else:
                        self.current_provider = self.providers[0]
        
        # All attempts failed
        return {
            "response": None,
            "provider": None,
            "model": None,
            "latency": 0,
            "attempts": attempts,
            "success": False,
            "error": last_error
        }
    
    def get_provider_status(self) -> Dict:
        """Get status of all providers."""
        status = {}
        for provider in self.providers:
            status[provider.name] = {
                "model": provider.model,
                "health": f"{provider.health:.1f}%",
                "quota": f"{provider.quota_remaining:.1f}%",
                "avg_latency": f"{provider.avg_latency:.2f}s",
                "combo_score": f"{provider.calculate_combo_score():.2f}",
                "success_rate": f"{(provider.success_count / (provider.success_count + provider.failure_count) * 100) if (provider.success_count + provider.failure_count) > 0 else 0:.1f}%"
            }
        return status
    
    def simulate_load(self, num_requests: int = 10):
        """Simulate load to test routing resilience."""
        print(f"\nSimulating {num_requests} requests...")
        
        test_prompts = [
            ("What is AI?", "general"),
            ("Analyze this complex problem", "reasoning"),
            ("Quick response needed", "fast"),
            ("Generate code", "fast"),
            ("Deep philosophical analysis", "reasoning")
        ]
        
        for i in range(num_requests):
            prompt, task_type = test_prompts[i % len(test_prompts)]
            print(f"\nRequest {i+1}: {prompt[:30]}... (Task: {task_type})")
            
            result = self.execute_with_routing(prompt, task_type)
            
            if result["success"]:
                print(f"✓ Success via {result['provider']} ({result['latency']:.2f}s)")
            else:
                print(f"✗ Failed after {result['attempts']} attempts")
        
        print("\nFinal Provider Status:")
        status = self.get_provider_status()
        for name, metrics in status.items():
            print(f"{name}: {metrics}")

# Initialize OmniRoute with available Ollama models
if __name__ == "__main__":
    print("Digital Organism - Phase 2: OmniRoute")
    print("=" * 60)
    print("Provider Resilience System\n")
    
    # Create routing system
    omni_route = OmniRoute()
    
    # Add providers (simulating different Ollama models)
    provider1 = Provider(name="Gemma-4-Local", model="gemma4")
    provider1.cost_per_token = 0.001
    provider1.avg_latency = 0.3
    
    provider2 = Provider(name="DeepSeek-R1-Local", model="deepseek-r1")
    provider2.cost_per_token = 0.002
    provider2.avg_latency = 0.8
    provider2.task_fit_score = 90.0  # Better for reasoning
    
    provider3 = Provider(name="Gemma-4-Fallback", model="gemma4")
    provider3.cost_per_token = 0.0015
    provider3.avg_latency = 0.5
    provider3.quota_remaining = 50.0  # Limited quota
    
    omni_route.add_provider(provider1)
    omni_route.add_provider(provider2)
    omni_route.add_provider(provider3)
    
    # Test routing
    print("\nTesting automatic routing...\n")
    
    # Test different task types
    test_cases = [
        ("Hello, how are you?", "general"),
        ("Analyze the ethical implications of AI", "reasoning"),
        ("What is 2+2?", "fast"),
        ("Compare different machine learning approaches", "reasoning"),
        ("Quick summary of this text", "fast")
    ]
    
    for prompt, task_type in test_cases:
        print(f"\n{'='*60}")
        print(f"Task: {task_type}")
        print(f"Prompt: {prompt}")
        print(f"{'='*60}")
        
        result = omni_route.execute_with_routing(prompt, task_type)
        
        if result["success"]:
            print(f"\n✓ Provider: {result['provider']}")
            print(f"  Model: {result['model']}")
            print(f"  Latency: {result['latency']:.2f}s")
            print(f"  Attempts: {result['attempts']}")
            print(f"\nResponse: {result['response'][:200]}...")
        else:
            print(f"\n✗ Failed: {result['error']}")
    
    # Show final status
    print(f"\n{'='*60}")
    print("Final Provider Status")
    print(f"{'='*60}")
    status = omni_route.get_provider_status()
    for name, metrics in status.items():
        print(f"\n{name}:")
        for key, value in metrics.items():
            print(f"  {key}: {value}")
    
    print(f"\nRouting History: {len(omni_route.routing_history)} decisions")
