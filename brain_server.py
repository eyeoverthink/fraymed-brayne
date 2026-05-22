"""
Digital Organism Brain Server
HTTP server that exposes the cognitive core for Java integration
"""

from flask import Flask, request, jsonify
from cognitive_core import OptimizedCognitiveCore
import time

app = Flask(__name__)

# Initialize the brain
brain = OptimizedCognitiveCore()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "system": "Digital Organism Brain",
        "version": "1.0"
    })

@app.route('/ask', methods=['POST'])
def ask():
    """Process a query through the cognitive core."""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({
                "error": "No query provided"
            }), 400
        
        # Process query through cognitive core
        result = brain.process_query(query)
        
        return jsonify({
            "query": query,
            "response": result['response'],
            "system": result['system'],
            "mode": result['mode'],
            "processing_time": result['processing_time'],
            "success": result.get('success', True)
        })
    
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@app.route('/stats', methods=['GET'])
def stats():
    """Get performance statistics."""
    summary = brain.get_performance_summary()
    return jsonify(summary)

if __name__ == '__main__':
    print("Digital Organism Brain Server")
    print("Starting HTTP server on port 5000...")
    print("Endpoints:")
    print("  GET  /health - Health check")
    print("  POST /ask    - Process query")
    print("  GET  /stats  - Performance statistics")
    print()
    app.run(host='localhost', port=5000, debug=False)
