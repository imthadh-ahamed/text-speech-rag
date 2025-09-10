# 🤖 Conversational AI Tutor

A production-ready Conversational AI Tutor application featuring Google Gemini AI, speech-to-text, text-to-speech, animated mascot, and RAG-powered responses for AI, ML, programming, and mathematics education.

## ✨ Features

### 🎯 Core Functionality
- **Google Gemini AI Integration**: Primary AI model for real-time, intelligent educational responses
- **Multi-Layer AI Fallback**: Gemini → OpenAI → Intelligent offline responses
- **RAG-Powered Knowledge**: Enhanced responses using LangChain and ChromaDB vector database
- **Speech-to-Text**: Real-time voice input using Web Speech API
- **Text-to-Speech**: Natural voice output using ElevenLabs API with Web Speech fallback
- **Animated Mascot**: Emotion-aware 3D mascot with facial expressions and animations
- **Session Management**: Multi-turn conversations with memory and context awareness
- **Emotion Detection**: Context-aware emotional responses with 5 distinct states

### 🛠 Technical Features
- **FastAPI Backend**: High-performance Python API with async support and clean architecture
- **Next.js Frontend**: Modern React-based UI with TypeScript and Tailwind CSS
- **Google Gemini 1.5 Flash**: Fast, capable AI model for educational responses
- **Vector Database**: ChromaDB cloud integration for knowledge retrieval and RAG
- **Robust Error Handling**: Multiple fallback layers and graceful degradation
- **Clean Production Code**: Optimized logging, removed debugging code, production-ready
- **Docker Support**: Full containerization for easy deployment
- **Educational Focus**: Specialized AI tutor for AI, ML, programming, and mathematics

## 🏗 Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Vector DB     │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (ChromaDB)    │
│                 │    │                 │    │                 │
│ • Animated UI   │    │ • RAG Pipeline  │    │ • Knowledge     │
│ • Voice I/O     │    │ • LangChain     │    │   Storage       │
│ • Chat Interface│    │ • Session Mgmt  │    │ • Embeddings    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         │                   ┌───▼───┐
    ┌────▼────┐             │Gemini │ (Primary)
    │ Speech  │             │  AI   │
    │ APIs    │             └───┬───┘
    └─────────┘                 │
         │                   ┌──▼──┐
    ┌────▼────┐             │OpenAI│ (Fallback)
    │ElevenLabs│             │GPT  │
    │   TTS   │             └──┬──┘
    └─────────┘                │
         │                 ┌───▼────┐
    ┌────▼────┐           │Smart   │ (Offline)
    │Web Speech│          │Fallback│
    │ Fallback │          │Responses│
    └─────────┘           └────────┘
```

## 🎯 What Makes This Special

### 🧠 **Intelligent AI Integration**
- **Google Gemini 1.5 Flash** as primary AI for fast, educational responses
- **Multi-layer fallback system** ensures reliability even when APIs are down
- **Educational specialization** with custom prompts for AI/ML, programming, and mathematics
- **Clean response formatting** optimized for chat interfaces (no markdown artifacts)

### 🏗️ **Production-Ready Architecture**
- **Optimized codebase** with cleaned logging and removed debugging code
- **Robust error handling** with graceful degradation
- **Real-time responses** with conversation context and memory
- **Scalable design** ready for production deployment

### 🎨 **Enhanced User Experience** 
- **Animated mascot** with emotion-aware expressions
- **Voice interaction** with speech-to-text and text-to-speech
- **Clean, modern UI** built with Next.js and Tailwind CSS
- **Responsive design** that works on desktop and mobile

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Docker and Docker Compose (optional)
- **Required API Keys**: Google Gemini, ChromaDB
- **Optional API Keys**: OpenAI (fallback), ElevenLabs (TTS)

### 🔑 Getting API Keys
1. **Google Gemini API**: Get free API key at [Google AI Studio](https://makersuite.google.com/)
2. **ChromaDB**: Sign up at [ChromaDB Cloud](https://www.trychroma.com/) for vector database
3. **OpenAI** (Optional): Get API key at [OpenAI Platform](https://platform.openai.com/) for fallback
4. **ElevenLabs** (Optional): Get TTS API key at [ElevenLabs](https://elevenlabs.io/) for voice

### 1. Clone and Setup Environment
```bash
git clone <your-repo-url>
cd text-speech-rag
cp .env.example .env
# Edit .env with your API keys
```

### 2. Option A: Docker Deployment (Recommended)
```bash
# Start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

### 2. Option B: Local Development
```bash
# Backend setup
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend setup (new terminal)
cd frontend
npm install
npm run dev

# Access at http://localhost:3000
```

## 📁 Project Structure

```
text-speech-rag/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main FastAPI application
│   ├── rag_pipeline.py     # RAG implementation with LangChain
│   ├── gemini_ai.py        # Google Gemini AI integration
│   ├── session_manager.py  # Session & memory management
│   ├── emotion_classifier.py # Emotion detection logic
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend container
├── frontend/               # Next.js frontend
│   ├── app/               # Next.js 13+ app directory
│   ├── components/        # React components
│   │   ├── AIMascot.tsx   # Animated mascot component
│   │   ├── ChatInterface.tsx # Chat UI component
│   │   └── VoiceControls.tsx # Voice input component
│   ├── lib/               # Utility libraries
│   │   ├── aiService.ts   # API client
│   │   └── ttsService.ts  # Text-to-speech service
│   ├── styles/            # CSS styles
│   └── Dockerfile         # Frontend container
├── data/                  # Knowledge base files
│   ├── ai_fundamentals.txt
│   ├── mathematics_for_ml.txt
│   └── programming_fundamentals.txt
├── docker-compose.yml     # Container orchestration
├── .env.example          # Environment template
└── README.md            # This file
```

## 🎮 Usage Guide

### 🗣 Voice Interaction
1. Click the microphone button
2. Speak your question clearly
3. The mascot will show "thinking" emotion
4. Listen to the AI's spoken response
5. Watch the mascot's expressions change based on context

### 💬 Text Chat
1. Type questions in the chat interface
2. Use quick-action buttons for common topics
3. View conversation history with timestamps
4. Clear chat to start fresh sessions

### 🎭 Mascot Emotions
- **Happy**: Celebrating correct answers or positive interactions
- **Thinking**: Processing complex questions or analyzing
- **Explaining**: Teaching mode with detailed explanations
- **Encouraging**: Supporting learning and motivation
- **Questioning**: Asking clarifying questions

## 🔧 API Endpoints

### Core Endpoints
- `POST /query` - Single stateless question
- `POST /chat` - Multi-turn conversation with memory
- `GET /health` - Health check and system status
- `DELETE /chat/{session_id}` - Clear specific session
- `GET /sessions` - List active sessions

### Request/Response Format
```json
// Request
{
  "query": "What is machine learning?",
  "session_id": "optional-session-id"
}

// Response
{
  "text": "Machine learning is a subset of artificial intelligence...",
  "emotion": "explaining",
  "session_id": "uuid-session-id"
}
```

## 🎯 Key Features Explained

### AI Response System
- **Primary AI**: Google Gemini 1.5 Flash for fast, educational responses
- **Intelligent Fallback**: Multi-layer system (Gemini → OpenAI → Smart Offline)
- **RAG Integration**: Document-enhanced responses using ChromaDB
- **Educational Focus**: Specialized prompts for AI, ML, programming, math
- **Clean Formatting**: Optimized responses without markdown artifacts
- **Context Awareness**: Conversation history and session management

### Emotion Detection
- **Rule-Based Classification**: Pattern matching and keyword analysis
- **Context Awareness**: Considers user query and response content
- **Visual Feedback**: Mascot expressions and animations
- **5 Emotion States**: Happy, Thinking, Explaining, Encouraging, Questioning

### Voice Features
- **Speech Recognition**: Browser-based Web Speech API
- **Text-to-Speech**: ElevenLabs API with natural voices
- **Fallback Support**: Web Speech API if ElevenLabs unavailable
- **Real-time Feedback**: Live transcription display

## 🔒 Environment Variables

```bash
# Required API Keys
GEMINI_API_KEY=your_gemini_api_key              # Google Gemini AI (Primary)
CHROMA_API_KEY=your_chroma_api_key              # ChromaDB Vector Database

# Optional API Keys (Fallbacks)
OPENAI_API_KEY=your_openai_api_key              # OpenAI GPT (Fallback)
ELEVENLABS_API_KEY=your_elevenlabs_api_key      # ElevenLabs TTS (Optional)

# Configuration
OPENAI_MODEL=gpt-3.5-turbo                      # OpenAI model for fallback
CHROMA_TENANT=your_tenant_id                    # ChromaDB tenant
CHROMA_DATABASE=your_database_name              # ChromaDB database
NEXT_PUBLIC_API_URL=http://localhost:8000       # Backend URL for frontend
```

## 🚀 Deployment

### Production Deployment
1. **Environment Setup**: Configure all API keys
2. **Build Images**: `docker-compose build`
3. **Deploy**: `docker-compose up -d`
4. **Monitor**: Check logs with `docker-compose logs -f`

### Cloud Deployment Options
- **AWS**: ECS with Fargate or EC2
- **Google Cloud**: Cloud Run or GKE
- **Azure**: Container Instances or AKS
- **Vercel**: Frontend deployment
- **Railway/Render**: Full-stack deployment

## 📊 Monitoring & Logging

### Health Checks
- Backend: `GET /health`
- Frontend: Browser console for errors
- Docker: Built-in healthcheck endpoints

### Logging
- Structured logging with timestamps
- Error tracking and stack traces
- API request/response logging
- Session activity monitoring

## 🛠 Development

### Adding Knowledge
1. Place documents in `/data` directory
2. Restart backend to reindex
3. Supports: `.txt`, `.pdf`, `.docx`

### Customizing Emotions
1. Edit `emotion_classifier.py`
2. Add new patterns and keywords
3. Update frontend emotion mappings
4. Modify mascot animations

### Extending API
1. Add new endpoints in `main.py`
2. Implement business logic in separate modules
3. Update frontend service clients
4. Add comprehensive error handling

## 🤝 Contributing

1. Fork the repository
2. Create feature branches
3. Follow existing code style
4. Add comprehensive tests
5. Update documentation
6. Submit pull requests

## 📝 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🙏 Acknowledgments

- **Google Gemini**: Primary AI model for educational responses
- **OpenAI**: GPT models for fallback support
- **ElevenLabs**: High-quality text-to-speech
- **LangChain**: RAG framework and tools
- **ChromaDB**: Vector database platform
- **Framer Motion**: React animations
- **Next.js**: React framework
- **FastAPI**: Python web framework

## 🆕 Recent Updates

### ✅ **Latest Improvements (Sept 2025)**
- **Gemini AI Integration**: Switched to Google Gemini 1.5 Flash for primary AI responses
- **Code Optimization**: Removed debugging code and optimized for production
- **Enhanced Formatting**: Fixed response formatting to avoid markdown artifacts
- **Robust Fallback**: Multi-layer AI fallback system for reliability
- **Clean Architecture**: Streamlined codebase with better error handling
- **Educational Focus**: Specialized prompts for AI, ML, programming, and math education

### 🎯 **Current Status**
- ✅ **Fully Functional**: Real-time AI responses with Gemini integration
- ✅ **Production Ready**: Optimized code with clean logging
- ✅ **Voice Features**: Working speech-to-text and text-to-speech
- ✅ **Animated UI**: Emotion-aware mascot with expressions
- ✅ **Docker Support**: Full containerization available
- ✅ **Comprehensive Docs**: Updated documentation and setup guides

## 📞 Support

For issues, questions, or contributions:
- Create GitHub issues for bugs
- Submit feature requests via discussions  
- Check existing documentation first
- Provide detailed reproduction steps

### 🚀 **Ready to Deploy**
The application is production-ready with Google Gemini AI providing intelligent, educational responses specialized for AI, machine learning, programming, and mathematics topics.

---

**Built with ❤️ for AI-powered education using Google Gemini**