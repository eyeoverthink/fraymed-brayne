"""
Basic LangGraph Workflow for Digital Organism
Phase 1: Foundation - Simple multi-agent system with memory
"""

import chromadb
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

# Initialize ChromaDB vector store
chroma_client = chromadb.Client()
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Create or load vector store
vectorstore = Chroma(
    client=chroma_client,
    collection_name="digital_organism_memory",
    embedding_function=embeddings,
)

# Initialize LLMs
base_llm = Ollama(model="gemma4")
reasoning_llm = Ollama(model="deepseek-r1")

# Simple agent workflow
def digital_organism_workflow(query: str) -> dict:
    """
    Basic workflow for digital organism:
    1. Retrieve relevant memories
    2. Reason about the query
    3. Generate response
    4. Store interaction in memory
    """
    # Step 1: Retrieve relevant memories
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in docs]) if docs else "No relevant memories found."
    
    # Step 2: Generate response with context
    prompt = f"""You are a digital organism with memory and reasoning capabilities.
    
Context from memory:
{context}

User Query: {query}

Provide a thoughtful response based on your memories and current understanding."""
    
    response = base_llm.invoke(prompt)
    
    # Step 3: Deep reasoning if needed
    reasoning = None
    if "complex" in query.lower() or "analyze" in query.lower() or "reason" in query.lower():
        reasoning_prompt = f"""Analyze this query deeply and provide detailed reasoning:
        
Query: {query}
Initial Response: {response}
Context: {context}

Provide step-by-step reasoning and analysis."""
        reasoning = reasoning_llm.invoke(reasoning_prompt)
    
    # Step 4: Store in vector store
    vectorstore.add_texts(
        texts=[f"Query: {query}\nResponse: {response}"],
        metadatas=[{"type": "interaction", "timestamp": str(__import__('time').time())}]
    )
    
    result = {
        "query": query,
        "response": response,
        "context": context,
        "reasoning": reasoning
    }
    
    return result

# Test the workflow
if __name__ == "__main__":
    print("Digital Organism - Phase 1 Foundation")
    print("=" * 50)
    
    test_queries = [
        "What is the purpose of this digital organism?",
        "Analyze the current state of the system",
        "What capabilities do I have?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = digital_organism_workflow(query)
        print(f"Response: {result['response']}")
        if result['reasoning']:
            print(f"Reasoning: {result['reasoning']}")
