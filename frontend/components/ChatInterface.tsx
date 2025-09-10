'use client'

import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

interface Message {
  type: 'user' | 'ai'
  content: string
  timestamp: Date
  emotion?: string
}

interface ChatInterfaceProps {
  messages: Message[]
  onSendMessage: (message: string) => void
  isLoading: boolean
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ 
  messages, 
  onSendMessage, 
  isLoading 
}) => {
  const [inputValue, setInputValue] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  // Auto-scroll to bottom when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue.trim())
      setInputValue('')
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const formatTimestamp = (timestamp: Date) => {
    return timestamp.toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  const getEmotionColor = (emotion?: string) => {
    switch (emotion) {
      case 'happy': return 'border-l-green-400'
      case 'thinking': return 'border-l-purple-400'
      case 'explaining': return 'border-l-blue-400'
      case 'encouraging': return 'border-l-yellow-400'
      case 'questioning': return 'border-l-pink-400'
      default: return 'border-l-gray-400'
    }
  }

  return (
    <div className="card flex flex-col h-[600px]">
      {/* Chat Header */}
      <div className="border-b border-gray-200 pb-4 mb-4">
        <h2 className="text-lg font-semibold text-gray-800">
          Chat with AI Tutor
        </h2>
        <p className="text-sm text-gray-600">
          Ask questions about AI, ML, programming, or mathematics
        </p>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto space-y-4 mb-4">
        <AnimatePresence initial={false}>
          {messages.map((message, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] p-3 rounded-lg ${
                  message.type === 'user'
                    ? 'bg-primary-500 text-white ml-4'
                    : `bg-gray-50 text-gray-800 mr-4 border-l-4 ${getEmotionColor(message.emotion)}`
                }`}
              >
                {/* Message Content */}
                <div className="whitespace-pre-wrap break-words">
                  {message.content}
                </div>
                
                {/* Message Metadata */}
                <div className={`text-xs mt-2 ${
                  message.type === 'user' 
                    ? 'text-primary-100' 
                    : 'text-gray-500'
                }`}>
                  <div className="flex items-center justify-between">
                    <span>{formatTimestamp(message.timestamp)}</span>
                    {message.type === 'ai' && message.emotion && (
                      <span className="capitalize">
                        {message.emotion}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Loading Indicator */}
        {isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex justify-start"
          >
            <div className="bg-gray-50 text-gray-800 p-3 rounded-lg mr-4 border-l-4 border-l-gray-400">
              <div className="flex items-center space-x-2">
                <div className="flex space-x-1">
                  {[0, 1, 2].map((i) => (
                    <motion.div
                      key={i}
                      className="w-2 h-2 bg-gray-400 rounded-full"
                      animate={{ y: [0, -5, 0] }}
                      transition={{
                        duration: 0.6,
                        repeat: Infinity,
                        delay: i * 0.1,
                      }}
                    />
                  ))}
                </div>
                <span className="text-sm">AI is thinking...</span>
              </div>
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="flex space-x-3">
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your question here..."
            className="flex-1 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !inputValue.trim()}
            className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? (
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
              />
            ) : (
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                />
              </svg>
            )}
          </button>
        </div>

        {/* Quick Actions */}
        <div className="flex flex-wrap gap-2">
          {[
            "Explain machine learning",
            "What is a neural network?",
            "Help with Python programming",
            "Mathematics for AI"
          ].map((suggestion, index) => (
            <button
              key={index}
              onClick={() => !isLoading && onSendMessage(suggestion)}
              disabled={isLoading}
              className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {suggestion}
            </button>
          ))}
        </div>
      </form>
    </div>
  )
}

export default ChatInterface
