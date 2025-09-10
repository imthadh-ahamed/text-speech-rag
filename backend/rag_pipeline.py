import chromadb
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader
from langchain.schema import Document
from typing import List, Optional, Dict, Any
import os
import logging
from datetime import datetime
from gemini_ai import gemini_ai

logger = logging.getLogger(__name__)

class RAGPipeline:
    """
    RAG (Retrieval-Augmented Generation) Pipeline for the AI Tutor
    """
    
    def __init__(self):
        self.embeddings = None
        self.vectorstore = None
        self.llm = None
        self.qa_chain = None
        self.text_splitter = None
        self.chroma_client = None
        
    async def initialize(self):
        """Initialize the RAG pipeline components"""
        try:
            # Initialize OpenAI components
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
            
            self.llm = ChatOpenAI(
                model_name=os.getenv("OPENAI_MODEL", "gpt-4"),
                temperature=0.7,
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
            
            # Initialize text splitter
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )
            
            # Initialize ChromaDB client
            self.chroma_client = chromadb.CloudClient(
                api_key=os.getenv("CHROMA_API_KEY"),
                tenant=os.getenv("CHROMA_TENANT"),
                database=os.getenv("CHROMA_DATABASE")
            )
            
            # Initialize vector store
            await self._setup_vectorstore()
            
            # Load initial documents if they exist
            await self._load_documents()
            
            logger.info("RAG pipeline initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG pipeline: {str(e)}")
            raise
    
    async def _setup_vectorstore(self):
        """Setup ChromaDB vector store"""
        try:
            # Create or get collection
            collection_name = "ai_tutor_knowledge"
            
            try:
                # Try to get existing collection
                collection = self.chroma_client.get_collection(collection_name)
            except:
                # Create new collection if it doesn't exist
                collection = self.chroma_client.create_collection(collection_name)
            
            # Initialize Langchain Chroma wrapper
            self.vectorstore = Chroma(
                client=self.chroma_client,
                collection_name=collection_name,
                embedding_function=self.embeddings
            )
            
        except Exception as e:
            logger.error(f"Failed to setup vector store: {str(e)}")
            raise
    
    async def _load_documents(self):
        """Load documents from the data directory"""
        try:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
            
            if not os.path.exists(data_dir):
                logger.warning(f"Data directory not found: {data_dir}")
                return
            
            # Load text files
            text_loader = DirectoryLoader(
                data_dir,
                glob="*.txt",
                loader_cls=TextLoader
            )
            
            # Load PDF files
            pdf_loader = DirectoryLoader(
                data_dir,
                glob="*.pdf",
                loader_cls=PyPDFLoader
            )
            
            documents = []
            
            # Load all documents
            try:
                text_docs = text_loader.load()
                documents.extend(text_docs)
            except Exception as e:
                logger.warning(f"No text documents found: {str(e)}")
            
            try:
                pdf_docs = pdf_loader.load()
                documents.extend(pdf_docs)
            except Exception as e:
                logger.warning(f"No PDF documents found: {str(e)}")
            
            if documents:
                # Split documents into chunks
                texts = self.text_splitter.split_documents(documents)
                
                # Add to vector store
                self.vectorstore.add_documents(texts)
            else:
                logger.info("No documents found to load")
                
        except Exception as e:
            logger.error(f"Failed to load documents: {str(e)}")
            # Don't raise here, continue without documents
    
    async def query(self, query: str) -> str:
        """
        Process a single query using RAG
        
        Args:
            query: User's question
            
        Returns:
            AI's response
        """
        try:
            if not self.vectorstore:
                # Fallback to direct LLM if no vector store
                return await self._direct_llm_query(query)
            
            # Create retrieval chain
            retriever = self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
            
            # Create memory for conversation
            memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            
            # Create conversational chain
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=retriever,
                memory=memory
            )
            
            # Get response
            result = qa_chain({"question": query})
            return result["answer"]
            
        except Exception as e:
            logger.error(f"Error in query processing: {str(e)}")
            return await self._direct_llm_query(query)
    
    async def chat(self, query: str, conversation_history: List[Dict[str, str]]) -> str:
        """
        Process a chat message with conversation context
        
        Args:
            query: User's current message
            conversation_history: List of previous messages
            
        Returns:
            AI's response
        """
        try:
            # Try Gemini with conversation context first
            gemini_response = await gemini_ai.chat(query, conversation_history)
            if gemini_response and "experiencing some technical difficulties" not in gemini_response.lower():
                return gemini_response
                
        except Exception as e:
            logger.error(f"Gemini chat failed: {str(e)}")
        
        try:
            # Fallback to RAG pipeline
            # Build context from conversation history
            context = self._build_conversation_context(conversation_history)
            
            # Combine context with current query
            full_query = f"{context}\n\nCurrent question: {query}"
            
            # Process using RAG
            return await self.query(full_query)
            
        except Exception as e:
            logger.error(f"Error in chat processing: {str(e)}")
            return await self._direct_llm_query(query)
    
    def _build_conversation_context(self, conversation_history: List[Dict[str, str]]) -> str:
        """Build context string from conversation history"""
        if not conversation_history:
            return ""
        
        context_parts = ["Previous conversation:"]
        for msg in conversation_history[-5:]:  # Keep last 5 exchanges
            context_parts.append(f"User: {msg['user']}")
            context_parts.append(f"AI: {msg['ai']}")
        
        return "\n".join(context_parts)
    
    async def _direct_llm_query(self, query: str) -> str:
        """Direct LLM query with Gemini as primary, OpenAI as fallback"""
        try:
            # First try Gemini AI (primary model)
            gemini_response = await gemini_ai.chat(query)
            if gemini_response and "experiencing some technical difficulties" not in gemini_response.lower():
                return gemini_response
            
        except Exception as e:
            logger.error(f"Gemini AI query failed: {str(e)}")
        
        try:
            # Fallback to OpenAI if available
            system_prompt = """You are an AI tutor designed to help students learn. 
            You should be helpful, encouraging, and educational in your responses. 
            If you don't know something, admit it and suggest ways the student could find the answer."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"OpenAI query failed: {str(e)}")
            
            # Final fallback to intelligent responses
            return self._get_fallback_response(query)
    
    def _get_fallback_response(self, query: str) -> str:
        """Provide intelligent fallback responses when API is unavailable"""
        query_lower = query.lower()
        
        # Machine Learning responses
        if any(term in query_lower for term in ['machine learning', 'ml', 'artificial intelligence', 'ai']):
            return """Machine Learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed for every scenario.

Key Types of Machine Learning:
1. **Supervised Learning**: Learning with labeled data (like classification and regression)
2. **Unsupervised Learning**: Finding patterns in unlabeled data (like clustering)
3. **Reinforcement Learning**: Learning through interaction and rewards

Common applications include image recognition, natural language processing, recommendation systems, and predictive analytics. Would you like to know more about any specific aspect?"""

        # Neural Networks
        elif any(term in query_lower for term in ['neural network', 'deep learning', 'neuron']):
            return """Neural Networks are computational models inspired by biological neural networks in the brain. They consist of interconnected nodes (neurons) that process and transmit information.

Key Components:
- **Input Layer**: Receives data
- **Hidden Layer(s)**: Process information
- **Output Layer**: Produces results
- **Weights & Biases**: Parameters that are learned during training

Deep Learning uses neural networks with multiple hidden layers to model complex patterns in data. It's particularly powerful for tasks like image recognition, speech processing, and natural language understanding."""

        # Programming
        elif any(term in query_lower for term in ['programming', 'coding', 'python', 'algorithm']):
            return """Programming is the process of creating instructions for computers to execute. Here are some fundamental concepts:

**Programming Basics**:
- Variables: Store data values
- Functions: Reusable blocks of code
- Control Structures: if/else, loops (for, while)
- Data Structures: Arrays, lists, dictionaries

**Python** is an excellent language for beginners because of its readable syntax and powerful libraries for AI/ML like NumPy, Pandas, and TensorFlow.

**Problem-Solving Approach**:
1. Understand the problem
2. Break it into smaller parts
3. Write pseudocode
4. Implement and test

What specific programming concept would you like to explore?"""

        # Mathematics
        elif any(term in query_lower for term in ['math', 'calculus', 'linear algebra', 'statistics']):
            return """Mathematics is fundamental to understanding AI and Machine Learning. Key areas include:

**Linear Algebra**:
- Vectors and matrices
- Matrix operations
- Eigenvalues and eigenvectors

**Calculus**:
- Derivatives for optimization
- Chain rule for backpropagation
- Gradient descent

**Statistics & Probability**:
- Probability distributions
- Bayes' theorem
- Statistical inference

**Optimization**:
- Finding minimum/maximum values
- Gradient-based methods
- Convex vs non-convex problems

These mathematical concepts help us understand how AI algorithms learn from data and make predictions."""

        # General help
        elif any(term in query_lower for term in ['help', 'what', 'how', 'explain']):
            return """I'm here to help you learn about AI, Machine Learning, Programming, and Mathematics! 

Here are some topics I can assist with:
- **AI & Machine Learning**: Concepts, algorithms, applications
- **Programming**: Python, algorithms, data structures
- **Mathematics**: Linear algebra, calculus, statistics
- **Deep Learning**: Neural networks, backpropagation, architectures

Feel free to ask specific questions like:
- "What is supervised learning?"
- "How do neural networks work?"
- "Explain gradient descent"
- "Help with Python loops"

What would you like to learn about today?"""

        else:
            return """I'm experiencing some technical difficulties connecting to my AI model right now, but I'm still here to help! 

I have knowledge about:
- **Artificial Intelligence & Machine Learning**
- **Programming and Computer Science**
- **Mathematics for AI**
- **Deep Learning and Neural Networks**

Please try rephrasing your question or ask about one of these specific topics. You can also try asking again in a few moments when my connection might be restored.

Is there a particular area of AI or programming you'd like to explore?"""
    
    async def add_documents(self, documents: List[Document]):
        """Add new documents to the knowledge base"""
        try:
            if not self.vectorstore:
                logger.error("Vector store not initialized")
                return
            
            # Split documents
            texts = self.text_splitter.split_documents(documents)
            
            # Add to vector store
            self.vectorstore.add_documents(texts)
            logger.info(f"Added {len(texts)} document chunks to knowledge base")
            
        except Exception as e:
            logger.error(f"Failed to add documents: {str(e)}")
            raise
