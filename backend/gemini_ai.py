"""
Google Gemini AI Integration
"""
import google.generativeai as genai
import os
import logging
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class GeminiAI:
    """Google Gemini AI integration for real-time responses"""
    
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            logger.error("GEMINI_API_KEY not found in environment variables")
            self.model = None
    
    async def chat(self, message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Generate a chat response using Gemini
        
        Args:
            message: User's message
            conversation_history: Previous conversation context
            
        Returns:
            AI response
        """
        try:
            if not self.model:
                return "Gemini AI is not properly configured. Please check your API key."
            
            # Build context from conversation history
            context = self._build_context(conversation_history) if conversation_history else ""
            
            # Create the full prompt with educational context
            full_prompt = f"""You are an expert AI tutor specializing in artificial intelligence, machine learning, programming, and mathematics. Your role is to:

1. Provide clear, educational explanations
2. Use examples and analogies when helpful
3. Encourage learning and curiosity
4. Break down complex topics into understandable parts
5. Suggest follow-up questions or topics to explore

FORMATTING INSTRUCTIONS:
- Do NOT use asterisks (*) for emphasis or bullet points
- Use simple text formatting with capital letters for emphasis
- Use numbered lists (1., 2., 3.) or dashes (-) for bullet points
- Keep responses conversational and easy to read
- Avoid markdown formatting symbols like *, **, _

{context}

Student's current question: {message}

Please provide a comprehensive, educational response that helps the student learn. Remember to avoid using asterisks in your formatting:"""

            # Generate response
            response = self.model.generate_content(full_prompt)
            
            if response and response.text:
                return response.text
            else:
                return "I'm having trouble generating a response right now. Could you please rephrase your question?"
                
        except Exception as e:
            logger.error(f"Gemini AI error: {str(e)}")
            return f"I'm experiencing some technical difficulties. Error: {str(e)}"
    
    async def query(self, query: str) -> str:
        """
        Process a single query using Gemini
        
        Args:
            query: User's question
            
        Returns:
            AI response
        """
        return await self.chat(query)
    
    def _build_context(self, conversation_history: List[Dict[str, str]]) -> str:
        """Build context string from conversation history"""
        if not conversation_history:
            return ""
        
        context_parts = ["Previous conversation context:"]
        # Keep last 3 exchanges to maintain context without overwhelming the model
        for msg in conversation_history[-3:]:
            if 'user' in msg and 'ai' in msg:
                context_parts.append(f"Student: {msg['user']}")
                context_parts.append(f"AI Tutor: {msg['ai']}")
        
        return "\n".join(context_parts)
    
    def test_connection(self) -> bool:
        """Test if Gemini API is working"""
        try:
            if not self.model:
                return False
            
            response = self.model.generate_content("Hello! This is a test message.")
            return response and response.text
            
        except Exception as e:
            logger.error(f"Gemini connection test failed: {str(e)}")
            return False

# Global instance
gemini_ai = GeminiAI()
