from flask import Flask, request, jsonify, session
from flask_cors import CORS
from rag_pipeline import RAGPipeline
from evaluate import evaluate_rag
from dotenv import load_dotenv
import os
from flask_session import Session

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Configure Flask session (in-memory, no database)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Replace with a secure key in production
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
Session(app)

@app.route('/initialize', methods=['POST'])
def initialize():
    """Initialize the RAG pipeline with a YouTube link and API key, store in session."""
    data = request.get_json()
    youtube_url = data.get('youtube_url')
    api_key = data.get('api_key')

    if not youtube_url or not api_key:
        return jsonify({"error": "Missing YouTube URL or API key"}), 400

    os.environ["GROQ_API_KEY"] = api_key

    try:
        session['rag_initialized'] = True
        session['youtube_url'] = youtube_url
        return jsonify({"message": "RAG pipeline initialized successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat queries using the RAG pipeline."""
    if not session.get('rag_initialized'):
        return jsonify({"error": "RAG pipeline not initialized. Call /initialize first."}), 400

    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"error": "Missing question"}), 400

    try:
        rag_pipeline = RAGPipeline(session['youtube_url'])
        answer = rag_pipeline.process_query(question)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/evaluate', methods=['POST'])
def evaluate():
    """Evaluate the RAG pipeline using predefined ground truth."""
    if not session.get('rag_initialized'):
        return jsonify({"error": "RAG pipeline not initialized. Call /initialize first."}), 400

    data = request.get_json()
    ground_truth = data.get('ground_truth')

    if not ground_truth:
        return jsonify({"error": "Missing ground truth data"}), 400

    try:
        rag_pipeline = RAGPipeline(session['youtube_url'])
        evaluation_results = evaluate_rag(rag_pipeline, ground_truth)
        return jsonify(evaluation_results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/clear', methods=['POST'])
def clear():
    """Clear the session when the user exits."""
    session.clear()
    return jsonify({"message": "Session cleared successfully"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)