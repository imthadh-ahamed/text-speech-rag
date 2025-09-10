"""
Alternative AI models for when OpenAI is not available
"""
import logging
import requests
import json
from typing import Optional

logger = logging.getLogger(__name__)

class AlternativeAI:
    """Fallback AI models when OpenAI is unavailable"""
    
    def __init__(self):
        self.available_models = {
            'huggingface': self._huggingface_chat,
            'ollama': self._ollama_chat,
            'local': self._local_chat
        }
    
    async def chat(self, message: str, model_preference: str = 'huggingface') -> str:
        """Get AI response using alternative models"""
        try:
            if model_preference in self.available_models:
                return await self.available_models[model_preference](message)
            else:
                # Try all models in order
                for model_name, model_func in self.available_models.items():
                    try:
                        result = await model_func(message)
                        if result and result != "Model not available":
                            return result
                    except:
                        continue
                
                return self._intelligent_fallback(message)
                
        except Exception as e:
            logger.error(f"All alternative models failed: {str(e)}")
            return self._intelligent_fallback(message)
    
    async def _huggingface_chat(self, message: str) -> str:
        """Use Hugging Face Inference API (free tier available)"""
        try:
            # Using a free model from Hugging Face
            api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
            headers = {"Authorization": "Bearer hf_your_token_here"}  # You can get a free token
            
            payload = {
                "inputs": f"Human: {message}\nAI:",
                "parameters": {
                    "max_new_tokens": 150,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    # Extract AI response
                    if "AI:" in generated_text:
                        ai_response = generated_text.split("AI:")[-1].strip()
                        return ai_response if ai_response else "I'm here to help! Could you rephrase your question?"
            
            return "Model temporarily unavailable"
            
        except Exception as e:
            logger.error(f"Hugging Face model error: {str(e)}")
            return "Model not available"
    
    async def _ollama_chat(self, message: str) -> str:
        """Use local Ollama model if available"""
        try:
            # Check if Ollama is running locally
            ollama_url = "http://localhost:11434/api/generate"
            payload = {
                "model": "llama2",  # or any model installed in Ollama
                "prompt": f"You are a helpful AI tutor. Answer this question: {message}",
                "stream": False
            }
            
            response = requests.post(ollama_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response generated')
            
            return "Ollama not available"
            
        except Exception as e:
            logger.error(f"Ollama model error: {str(e)}")
            return "Model not available"
    
    async def _local_chat(self, message: str) -> str:
        """Use a simple local model or rule-based responses"""
        # This could integrate with transformers library for local models
        return "Local model not implemented yet"
    
    def _intelligent_fallback(self, message: str) -> str:
        """Enhanced intelligent fallback responses"""
        message_lower = message.lower()
        
        # AI/ML Questions
        if any(term in message_lower for term in ['machine learning', 'ml', 'artificial intelligence', 'ai', 'neural network', 'deep learning']):
            return """🤖 **AI & Machine Learning Fundamentals**

Machine Learning enables computers to learn patterns from data without explicit programming. Here are the key concepts:

**Types of ML:**
- **Supervised Learning**: Learning from labeled examples (classification, regression)
- **Unsupervised Learning**: Finding hidden patterns (clustering, dimensionality reduction)  
- **Reinforcement Learning**: Learning through trial and error with rewards

**Neural Networks** are the backbone of deep learning, inspired by how brain neurons work. They consist of:
- Input layers (receive data)
- Hidden layers (process information)
- Output layers (make predictions)

**Common Applications:**
- Image recognition (computer vision)
- Natural language processing (chatbots, translation)
- Recommendation systems (Netflix, Spotify)
- Autonomous vehicles

Would you like me to dive deeper into any specific aspect?"""

        # Programming Questions
        elif any(term in message_lower for term in ['programming', 'coding', 'python', 'javascript', 'algorithm', 'function', 'variable']):
            return """💻 **Programming Concepts**

Programming is the art of giving instructions to computers. Here are fundamental concepts:

**Core Building Blocks:**
- **Variables**: Store and manipulate data
- **Functions**: Reusable code blocks that perform specific tasks
- **Control Flow**: if/else statements, loops (for, while)
- **Data Structures**: Arrays, lists, dictionaries for organizing data

**Python Example:**
```python
def greet_student(name, subject):
    return f"Hello {name}! Ready to learn {subject}?"

student_name = "Alex"
result = greet_student(student_name, "AI")
print(result)
```

**Problem-Solving Approach:**
1. 📝 Understand the problem
2. 🧩 Break it into smaller parts  
3. 📋 Write pseudocode
4. 💻 Implement and test
5. 🐛 Debug and refine

What programming concept would you like to explore further?"""

        # Math Questions
        elif any(term in message_lower for term in ['math', 'mathematics', 'calculus', 'linear algebra', 'statistics', 'probability']):
            return """📐 **Mathematics for AI & Programming**

Mathematics is the foundation of computer science and AI. Key areas include:

**Linear Algebra:**
- Vectors & matrices (fundamental for AI)
- Matrix operations (used in neural networks)
- Eigenvalues & eigenvectors (dimensionality reduction)

**Calculus:**
- Derivatives (optimization algorithms)
- Chain rule (backpropagation in neural networks)
- Gradient descent (how AI models learn)

**Statistics & Probability:**
- Probability distributions
- Bayes' theorem (machine learning foundation)
- Statistical inference (data analysis)

**Real-world Applications:**
- Image processing uses linear algebra
- Neural networks use calculus for learning
- Data analysis relies on statistics

Which mathematical area interests you most?"""

        # General Help
        elif any(term in message_lower for term in ['help', 'what can you do', 'topics', 'learn']):
            return """🎓 **Welcome to Your AI Learning Companion!**

I'm here to help you master technology and computer science! Here's what we can explore together:

**🤖 Artificial Intelligence & Machine Learning**
- Neural networks and deep learning
- Supervised, unsupervised, and reinforcement learning
- Computer vision and natural language processing

**💻 Programming & Software Development**  
- Python, JavaScript, and other languages
- Algorithms and data structures
- Best practices and problem-solving

**📊 Data Science & Analytics**
- Statistics and probability
- Data visualization
- Machine learning applications

**🔢 Mathematics for Tech**
- Linear algebra for AI
- Calculus for optimization
- Discrete math for programming

**Sample questions to get started:**
- "Explain how neural networks work"
- "What's the difference between supervised and unsupervised learning?"
- "How do I start learning Python?"
- "What math do I need for machine learning?"

What would you like to dive into first? 🚀"""

        else:
            return f"""I'm experiencing some connectivity issues with my advanced AI models, but I'm still here to help! 

I noticed you asked about: "{message}"

I specialize in:
- 🤖 **Artificial Intelligence & Machine Learning**
- 💻 **Programming & Computer Science**  
- 📊 **Data Science & Mathematics**
- 🧠 **Algorithm Design & Problem Solving**

Could you rephrase your question to be more specific about one of these areas? For example:
- "How do neural networks learn?"
- "Explain Python functions"
- "What is linear algebra used for in AI?"

I'll provide detailed, educational responses to help you learn! 🎓"""

# Global instance
alternative_ai = AlternativeAI()
