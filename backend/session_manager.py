from typing import Dict, List, Optional
import uuid
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class SessionManager:
    """
    Manages conversation sessions and memory for multi-turn conversations
    """
    
    def __init__(self, max_session_duration_hours: int = 24):
        self.sessions: Dict[str, Dict] = {}
        self.max_session_duration = timedelta(hours=max_session_duration_hours)
        
    def create_session(self) -> str:
        """
        Create a new conversation session
        
        Returns:
            session_id: Unique session identifier
        """
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "created_at": datetime.now(),
            "last_activity": datetime.now(),
            "conversation_history": [],
            "context": {}
        }
        
        logger.info(f"Created new session: {session_id}")
        return session_id
    
    def get_conversation_history(self, session_id: str) -> List[Dict[str, str]]:
        """
        Get conversation history for a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            List of conversation messages
        """
        if session_id not in self.sessions:
            logger.warning(f"Session not found: {session_id}")
            return []
        
        # Clean up expired sessions
        self._cleanup_expired_sessions()
        
        # Update last activity
        self.sessions[session_id]["last_activity"] = datetime.now()
        
        return self.sessions[session_id]["conversation_history"]
    
    def add_to_conversation(self, session_id: str, user_message: str, ai_response: str):
        """
        Add a message exchange to the conversation history
        
        Args:
            session_id: Session identifier
            user_message: User's message
            ai_response: AI's response
        """
        if session_id not in self.sessions:
            logger.warning(f"Session not found, creating new one: {session_id}")
            self.sessions[session_id] = {
                "created_at": datetime.now(),
                "last_activity": datetime.now(),
                "conversation_history": [],
                "context": {}
            }
        
        # Add to conversation history
        self.sessions[session_id]["conversation_history"].append({
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "ai": ai_response
        })
        
        # Update last activity
        self.sessions[session_id]["last_activity"] = datetime.now()
        
        # Keep only last 20 exchanges to prevent memory issues
        if len(self.sessions[session_id]["conversation_history"]) > 20:
            self.sessions[session_id]["conversation_history"] = \
                self.sessions[session_id]["conversation_history"][-20:]
        
        logger.info(f"Added message to session {session_id}")
    
    def clear_session(self, session_id: str):
        """
        Clear a specific session
        
        Args:
            session_id: Session identifier
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Cleared session: {session_id}")
        else:
            logger.warning(f"Attempted to clear non-existent session: {session_id}")
    
    def list_sessions(self) -> List[Dict]:
        """
        List all active sessions
        
        Returns:
            List of session information
        """
        self._cleanup_expired_sessions()
        
        session_list = []
        for session_id, session_data in self.sessions.items():
            session_list.append({
                "session_id": session_id,
                "created_at": session_data["created_at"].isoformat(),
                "last_activity": session_data["last_activity"].isoformat(),
                "message_count": len(session_data["conversation_history"])
            })
        
        return session_list
    
    def get_session_context(self, session_id: str) -> Dict:
        """
        Get session context/metadata
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session context dictionary
        """
        if session_id not in self.sessions:
            return {}
        
        return self.sessions[session_id].get("context", {})
    
    def update_session_context(self, session_id: str, context: Dict):
        """
        Update session context/metadata
        
        Args:
            session_id: Session identifier
            context: Context dictionary to update
        """
        if session_id not in self.sessions:
            logger.warning(f"Cannot update context for non-existent session: {session_id}")
            return
        
        self.sessions[session_id]["context"].update(context)
        self.sessions[session_id]["last_activity"] = datetime.now()
        
        logger.info(f"Updated context for session {session_id}")
    
    def _cleanup_expired_sessions(self):
        """Remove expired sessions"""
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session_data in self.sessions.items():
            if current_time - session_data["last_activity"] > self.max_session_duration:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
            logger.info(f"Removed expired session: {session_id}")
        
        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
    
    def get_session_stats(self) -> Dict:
        """
        Get statistics about all sessions
        
        Returns:
            Dictionary with session statistics
        """
        self._cleanup_expired_sessions()
        
        total_sessions = len(self.sessions)
        total_messages = sum(len(session["conversation_history"]) 
                           for session in self.sessions.values())
        
        if total_sessions > 0:
            avg_messages_per_session = total_messages / total_sessions
        else:
            avg_messages_per_session = 0
        
        return {
            "total_sessions": total_sessions,
            "total_messages": total_messages,
            "avg_messages_per_session": round(avg_messages_per_session, 2)
        }
