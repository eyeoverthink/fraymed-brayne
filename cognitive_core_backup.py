"""
Phase 2: Cognitive Core
Dual-process cognition with DeepSeek-R1 reasoning engine
"""

import chromadb
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
import time
import json
from typing import Dict, Optional, List

# Initialize ChromaDB vector store
chroma_client = chromadb.Client()
embeddings = OllamaEmbeddings(model="nomic-embed-text")

vectorstore = Chroma(
    client=chroma_client,
    collection_name="digital_organism_cognitive_core",
    embedding_function=embeddings,
)

# Initialize LLMs
system_1_llm = OllamaLLM(model="gemma4")  # Fast, intuitive responses
system_2_llm = OllamaLLM(model="deepseek-r1")  # Deep, deliberate reasoning

class CognitiveCore:
    """
    Dual-process cognition system implementing System 1 (fast/intuitive) 
    and System 2 (slow/deliberate) thinking modes.
    """
    
    def __init__(self):
        self.memory = []
        self.reasoning_history = []
        self.performance_metrics = {
            "system_1_calls": 0,
            "system_2_calls": 0,
            "avg_system_1_time": 0,
            "avg_system_2_time": 0
        }
    
    def _should_use_system_2(self, query: str, context: str) -> bool:
        """
        Determine if query requires deep reasoning (System 2) or can use 
        fast intuitive response (System 1).
        """
        # Keywords that trigger deep reasoning
        reasoning_keywords = [
            "analyze", "complex", "why", "how does", "evaluate", "critique",
            "compare", "synthesize", "reason", "logic", "prove", "derive",
            "algorithm", "optimization", "strategy", "architect", "design"
        ]
        
        # Check for reasoning keywords
        query_lower = query.lower()
        for keyword in reasoning_keywords:
            if keyword in query_lower:
                return True
        
        # Check query complexity (length and structure)
        if len(query) > 200:
            return True
        
        # Check if context is complex
        if len(context) > 1000:
            return True
        
        return False
    
    def _system_1_process(self, query: str, context: str) -> Dict:
        """
        System 1: Fast, intuitive, automatic processing.
        Good for quick responses, pattern recognition, routine tasks.
        """
        start_time = time.time()
        
        prompt = f"""You are a digital organism with fast, intuitive cognition.

Context from memory:
{context}

User Query: {query}

Provide a direct, intuitive response without overthinking. Be concise and practical."""
        
        response = system_1_llm.invoke(prompt)
        elapsed = time.time() - start_time
        
        self.performance_metrics["system_1_calls"] += 1
        self.performance_metrics["avg_system_1_time"] = (
            (self.performance_metrics["avg_system_1_time"] * 
             (self.performance_metrics["system_1_calls"] - 1) + elapsed) / 
            self.performance_metrics["system_1_calls"]
        )
        
        return {
            "system": "System 1",
            "response": response,
            "reasoning": None,
            "processing_time": elapsed,
            "mode": "intuitive"
        }
    
    def _system_2_process(self, query: str, context: str) -> Dict:
        """
        System 2: Slow, deliberate, analytical processing.
        Good for complex reasoning, problem-solving, strategic thinking.
        """
        start_time = time.time()
        
        # First, get initial intuitive response
        initial_prompt = f"""Provide a quick initial thought on this query:
        
Query: {query}
Context: {context}

Just give your immediate intuition (1-2 sentences)."""
        
        initial_thought = system_1_llm.invoke(initial_prompt)
        
        # Then, engage deep reasoning
        reasoning_prompt = f"""You are engaged in deep, analytical reasoning.

Query: {query}
Context from memory:
{context}
Initial intuition: {initial_thought}

Provide a detailed step-by-step analysis:
1. Deconstruct the problem into components
2. Analyze each component systematically
3. Identify relationships and dependencies
4. Evaluate multiple perspectives
5. Synthesize conclusions with supporting evidence

Be thorough and methodical."""
        
        reasoning = system_2_llm.invoke(reasoning_prompt)
        elapsed = time.time() - start_time
        
        # Generate final response based on reasoning
        final_prompt = f"""Based on your deep reasoning, provide a clear, well-structured response:

Query: {query}
Reasoning analysis: {reasoning}

Synthesize a final response that incorporates your analytical insights."""
        
        final_response = system_1_llm.invoke(final_prompt)
        total_elapsed = time.time() - start_time
        
        self.performance_metrics["system_2_calls"] += 1
        self.performance_metrics["avg_system_2_time"] = (
            (self.performance_metrics["avg_system_2_time"] * 
             (self.performance_metrics["system_2_calls"] - 1) + total_elapsed) / 
            self.performance_metrics["system_2_calls"]
        )
        
        self.reasoning_history.append({
            "query": query,
            "initial_thought": initial_thought,
            "reasoning": reasoning,
            "final_response": final_response,
            "timestamp": time.time()
        })
        
        return {
            "system": "System 2",
            "response": final_response,
            "reasoning": reasoning,
            "initial_thought": initial_thought,
            "processing_time": total_elapsed,
            "mode": "analytical"
        }
    
    def process_query(self, query: str) -> Dict:
        """
        Main cognitive processing pipeline.
        Determines which cognitive system to use based on query complexity.
        """
        # Retrieve relevant memories
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        docs = retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in docs]) if docs else "No relevant memories found."
        
        # Determine which cognitive system to use
        use_system_2 = self._should_use_system_2(query, context)
        
        if use_system_2:
            result = self._system_2_process(query, context)
        else:
            result = self._system_1_process(query, context)
        
        # Store interaction in memory
        interaction = {
            "query": query,
            "response": result["response"],
            "system_used": result["system"],
            "processing_time": result["processing_time"],
            "timestamp": time.time()
        }
        
        self.memory.append(interaction)
        
        # Store in vector store
        vectorstore.add_texts(
            texts=[f"Query: {query}\nResponse: {result['response']}\nSystem: {result['system']}"],
            metadatas=[{
                "type": "cognitive_interaction",
                "system": result["system"],
                "timestamp": str(time.time())
            }]
        )
        
        result["context"] = context
        return result
    
    def get_performance_summary(self) -> Dict:
        """Return performance metrics and cognitive statistics."""
        total_calls = self.performance_metrics["system_1_calls"] + self.performance_metrics["system_2_calls"]
        
        if total_calls == 0:
            return {"status": "No queries processed yet"}
        
        return {
            "total_queries": total_calls,
            "system_1_usage": f"{(self.performance_metrics['system_1_calls'] / total_calls) * 100:.1f}%",
            "system_2_usage": f"{(self.performance_metrics['system_2_calls'] / total_calls) * 100:.1f}%",
            "avg_system_1_time": f"{self.performance_metrics['avg_system_1_time']:.2f}s",
            "avg_system_2_time": f"{self.performance_metrics['avg_system_2_time']:.2f}s",
            "reasoning_history_entries": len(self.reasoning_history)
        }

# Test the cognitive core
if __name__ == "__main__":
    print("Digital Organism - Phase 2: Cognitive Core")
    print("=" * 60)
    print("Dual-Process Cognition with DeepSeek-R1\n")
    
    cognitive_core = CognitiveCore()
    
    # Test queries that should trigger different systems
    test_queries = [
        ("Hello, how are you?", "System 1 - Simple greeting"),
        ("What is 2 + 2?", "System 1 - Simple fact"),
        ("Analyze the ethical implications of AI consciousness", "System 2 - Complex analysis"),
        ("Design an architecture for a scalable microservices system", "System 2 - Complex design"),
        ("Compare different approaches to reinforcement learning", "System 2 - Comparative analysis"),
        ("What's the weather like?", "System 1 - Simple query")
    ]
    
    for query, expected_system in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"Expected: {expected_system}")
        print(f"{'='*60}")
        
        result = cognitive_core.process_query(query)
        
        print(f"\nSystem Used: {result['system']}")
        print(f"Mode: {result['mode']}")
        print(f"Processing Time: {result['processing_time']:.2f}s")
        
        if result['reasoning']:
            print(f"\n--- Reasoning ---")
            print(result['reasoning'][:500] + "..." if len(result['reasoning']) > 500 else result['reasoning'])
        
        print(f"\n--- Response ---")
        print(result['response'][:800] + "..." if len(result['response']) > 800 else result['response'])
    
    # Print performance summary
    print(f"\n{'='*60}")
    print("Performance Summary")
    print(f"{'='*60}")
    summary = cognitive_core.get_performance_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")
