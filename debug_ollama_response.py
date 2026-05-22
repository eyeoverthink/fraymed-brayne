"""
Debug Ollama response to see what's being returned
"""

import requests
import json

OLLAMA_BASE_URL = "http://localhost:11434"
MODEL = "gemma4"

def test_ollama_response():
    print("Testing Ollama response...")
    
    prompt = "What is 2+2?"
    
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 50,
                "temperature": 0.7,
                "top_p": 0.9
            }
        },
        timeout=15
    )
    
    print(f"Status code: {response.status_code}")
    print(f"Response text: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"JSON data: {json.dumps(data, indent=2)}")
        print(f"Response field: {data.get('response', 'NOT FOUND')}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_ollama_response()
