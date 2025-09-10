from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Import our modules
from rag_pipeline import RAGPipeline
from session_manager import SessionManager
from emotion_classifier import EmotionClassifier

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Conversational AI Tutor API",
    description="A RAG-powered conversational AI tutor with emotion detection",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class QueryRequest(BaseModel):
    query: str

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

class AIResponse(BaseModel):
    text: str
    emotion: str
    session_id: Optional[str] = None

# Initialize components
rag_pipeline = None
session_manager = None
emotion_classifier = None

@app.on_event("startup")
async def startup_event():
    """Initialize RAG pipeline and other components on startup"""
    global rag_pipeline, session_manager, emotion_classifier
    
    try:
        rag_pipeline = RAGPipeline()
        await rag_pipeline.initialize()
        
        session_manager = SessionManager()
        emotion_classifier = EmotionClassifier()
        
        logger.info("All components initialized successfully!")
        
    except Exception as e:
        logger.error(f"Failed to initialize components: {str(e)}")
        raise

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Conversational AI Tutor API is running!"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "rag_pipeline": rag_pipeline is not None,
        "session_manager": session_manager is not None,
        "emotion_classifier": emotion_classifier is not None
    }

@app.post("/query", response_model=AIResponse)
async def query_endpoint(request: QueryRequest):
    """
    Single query endpoint - stateless interaction
    
    Args:
        request: QueryRequest containing the user's query
        
    Returns:
        AIResponse with text response and emotion
    """
    try:
        if not rag_pipeline:
            raise HTTPException(status_code=500, detail="RAG pipeline not initialized")
        
        # Get response from RAG pipeline
        response_text = await rag_pipeline.query(request.query)
        
        # Classify emotion
        emotion = emotion_classifier.classify_emotion(response_text, request.query)
        
        return AIResponse(
            text=response_text,
            emotion=emotion
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")

@app.post("/chat", response_model=AIResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Multi-turn conversation endpoint with session memory
    
    Args:
        request: ChatRequest containing query and optional session_id
        
    Returns:
        AIResponse with text response, emotion, and session_id
    """
    try:
        if not rag_pipeline or not session_manager:
            raise HTTPException(status_code=500, detail="Components not initialized")
        
        # Get or create session
        session_id = request.session_id
        if not session_id:
            session_id = session_manager.create_session()
        
        # Get conversation history
        conversation_history = session_manager.get_conversation_history(session_id)
        
        # Get response from RAG pipeline with context
        response_text = await rag_pipeline.chat(
            query=request.query,
            conversation_history=conversation_history
        )
        
        # Update conversation history
        session_manager.add_to_conversation(
            session_id=session_id,
            user_message=request.query,
            ai_response=response_text
        )
        
        # Classify emotion
        emotion = emotion_classifier.classify_emotion(response_text, request.query)
        
        return AIResponse(
            text=response_text,
            emotion=emotion,
            session_id=session_id
        )
        
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process chat: {str(e)}")

@app.delete("/chat/{session_id}")
async def clear_session(session_id: str):
    """Clear a specific chat session"""
    try:
        if not session_manager:
            raise HTTPException(status_code=500, detail="Session manager not initialized")
        
        session_manager.clear_session(session_id)
        return {"message": f"Session {session_id} cleared successfully"}
        
    except Exception as e:
        logger.error(f"Error clearing session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to clear session: {str(e)}")

@app.get("/sessions")
async def list_sessions():
    """List all active sessions"""
    try:
        if not session_manager:
            raise HTTPException(status_code=500, detail="Session manager not initialized")
        
        sessions = session_manager.list_sessions()
        return {"sessions": sessions}
        
    except Exception as e:
        logger.error(f"Error listing sessions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list sessions: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
