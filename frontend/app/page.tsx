'use client'

import { useState, useEffect } from 'react'
import AIMascot from '../components/AIMascot'
import ChatInterface from '../components/ChatInterface'
import VoiceControls from '../components/VoiceControls'
import { AIService } from '../lib/aiService'
import { TTSService } from '../lib/ttsService'

export default function Home() {
  const [isLoading, setIsLoading] = useState(false)
  const [currentEmotion, setCurrentEmotion] = useState('happy')
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Array<{
    type: 'user' | 'ai'
    content: string
    timestamp: Date
    emotion?: string
  }>>([
    {
      type: 'ai',
      content: 'Hello! I\'m your AI tutor. I\'m here to help you learn about AI, machine learning, programming, and mathematics. Feel free to ask me anything, or use the microphone to speak with me!',
      timestamp: new Date(),
      emotion: 'happy'
    }
  ])

  const aiService = new AIService()
  const ttsService = new TTSService()

  const handleTextQuery = async (query: string) => {
    if (!query.trim()) return

    setIsLoading(true)
    
    // Add user message
    const userMessage = {
      type: 'user' as const,
      content: query,
      timestamp: new Date()
    }
    setMessages(prev => [...prev, userMessage])

    try {
      // Get AI response
      const response = await aiService.chat(query, sessionId)
      
      // Update session ID if new
      if (response.session_id && !sessionId) {
        setSessionId(response.session_id)
      }

      // Add AI message
      const aiMessage = {
        type: 'ai' as const,
        content: response.text,
        timestamp: new Date(),
        emotion: response.emotion
      }
      setMessages(prev => [...prev, aiMessage])

      // Update mascot emotion
      setCurrentEmotion(response.emotion)

      // Generate and play TTS
      await playTTS(response.text)

    } catch (error) {
      console.error('Error getting AI response:', error)
      
      const errorMessage = {
        type: 'ai' as const,
        content: 'I apologize, but I\'m having trouble connecting right now. Please try again in a moment.',
        timestamp: new Date(),
        emotion: 'thinking'
      }
      setMessages(prev => [...prev, errorMessage])
      setCurrentEmotion('thinking')
    } finally {
      setIsLoading(false)
    }
  }

  const handleVoiceQuery = async (transcript: string) => {
    await handleTextQuery(transcript)
  }

  const playTTS = async (text: string) => {
    try {
      setIsSpeaking(true)
      await ttsService.speak(text)
    } catch (error) {
      console.error('TTS Error:', error)
    } finally {
      setIsSpeaking(false)
    }
  }

  const clearChat = () => {
    setMessages([{
      type: 'ai',
      content: 'Chat cleared! How can I help you today?',
      timestamp: new Date(),
      emotion: 'happy'
    }])
    setSessionId(null)
    setCurrentEmotion('happy')
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">
              🤖 AI Tutor
            </h1>
            <button
              onClick={clearChat}
              className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-800 hover:bg-gray-50 rounded-lg transition-colors"
            >
              Clear Chat
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col lg:flex-row max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-6 gap-6">
        {/* Left Panel - Mascot */}
        <div className="lg:w-1/3 flex flex-col">
          <div className="card flex-1 min-h-[400px] flex flex-col items-center justify-center">
            <AIMascot 
              emotion={currentEmotion}
              isSpeaking={isSpeaking}
              isLoading={isLoading}
            />
            
            {/* Voice Controls */}
            <div className="mt-6 w-full">
              <VoiceControls 
                onTranscription={handleVoiceQuery}
                isDisabled={isLoading}
              />
            </div>

            {/* Status */}
            <div className="mt-4 text-center">
              <p className="text-sm text-gray-600">
                Status: <span className="font-medium">
                  {isLoading ? 'Thinking...' : 
                   isSpeaking ? 'Speaking...' : 
                   'Ready to help!'}
                </span>
              </p>
              <p className="text-xs text-gray-400 mt-1">
                Emotion: {currentEmotion}
              </p>
            </div>
          </div>
        </div>

        {/* Right Panel - Chat Interface */}
        <div className="lg:w-2/3 flex flex-col">
          <ChatInterface
            messages={messages}
            onSendMessage={handleTextQuery}
            isLoading={isLoading}
          />
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-center text-sm text-gray-500">
            AI Tutor - Powered by OpenAI GPT-4 and ElevenLabs TTS
          </p>
        </div>
      </footer>
    </div>
  )
}
