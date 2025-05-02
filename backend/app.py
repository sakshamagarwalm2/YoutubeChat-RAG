"""
Flask backend for YouTube RAG Chat application
This module provides API endpoints for initializing the RAG pipeline,
answering questions about YouTube videos, and managing session state.
"""

import os
import logging
import tempfile
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
from rag_pipeline import RAGPipeline
from werkzeug.exceptions import BadRequest, InternalServerError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure session
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = os.path.join(tempfile.gettempdir(), "flask_session")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SECRET_KEY"] = os.urandom(24)  # Generate a random secret key
Session(app)

# Configure CORS
CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Global pipeline instance (will be initialized per session)
pipeline = None


@app.route("/initialize", methods=["POST"])
def initialize():
    """
    Initialize the RAG pipeline with a YouTube video.
    
    Request format:
    {
        "youtube_url": string,
        "api_key": string
    }
    """
    global pipeline
    
    try:
        data = request.get_json()
        
        if not data:
            raise BadRequest("Missing request body")
        
        youtube_url = data.get("youtube_url")
        api_key = data.get("api_key")
        
        if not youtube_url:
            raise BadRequest("Missing 'youtube_url' parameter")
        
        if not api_key:
            raise BadRequest("Missing 'api_key' parameter")
        
        # Create and initialize the pipeline
        pipeline = RAGPipeline(api_key=api_key)
        
        result = pipeline.initialize(youtube_url)
        
        # Store in session
        session["initialized"] = True
        session["youtube_url"] = youtube_url
        session["video_id"] = result["video_id"]
        
        return jsonify({
            "status": "success",
            "message": "RAG pipeline initialized successfully",
            "video_id": result["video_id"]
        })
    
    except BadRequest as e:
        logger.error(f"Bad request: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
    
    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
    
    except Exception as e:
        logger.error(f"Initialization error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Failed to initialize: {str(e)}"
        }), 500


@app.route("/chat", methods=["POST"])
def chat():
    """
    Answer a question about the YouTube video.
    
    Request format:
    {
        "question": string
    }
    """
    global pipeline
    
    try:
        # Check if initialized
        if not session.get("initialized") or not pipeline:
            raise BadRequest("Pipeline not initialized. Call /initialize first.")
        
        data = request.get_json()
        
        if not data:
            raise BadRequest("Missing request body")
        
        question = data.get("question")
        
        if not question:
            raise BadRequest("Missing 'question' parameter")
        
        # Answer the question
        answer = pipeline.answer_question(question)
        
        return jsonify({
            "status": "success",
            "answer": answer
        })
    
    except BadRequest as e:
        logger.error(f"Bad request: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
    
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Failed to answer question: {str(e)}"
        }), 500


@app.route("/clear", methods=["POST"])
def clear():
    """Clear the session data and reset the pipeline."""
    global pipeline
    
    try:
        # Clear session
        session.clear()
        
        # Reset pipeline
        pipeline = None
        
        return jsonify({
            "status": "success",
            "message": "Session cleared successfully"
        })
    
    except Exception as e:
        logger.error(f"Error clearing session: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Failed to clear session: {str(e)}"
        }), 500


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "success",
        "message": "Service is running"
    })


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(e):
    """Handle 405 errors."""
    return jsonify({
        "status": "error",
        "message": "Method not allowed"
    }), 405


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    logger.error(f"Server error: {str(e)}")
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500


if __name__ == "__main__":
    # Create session directory if it doesn't exist
    os.makedirs(app.config["SESSION_FILE_DIR"], exist_ok=True)
    
    # Run the app
    app.run(debug=True, host="0.0.0.0", port=5000)