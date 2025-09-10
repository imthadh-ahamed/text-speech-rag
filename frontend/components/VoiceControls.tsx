'use client'

import { useState, useRef, useCallback } from 'react'
import { motion } from 'framer-motion'

interface VoiceControlsProps {
  onTranscription: (text: string) => void
  isDisabled?: boolean
}

const VoiceControls: React.FC<VoiceControlsProps> = ({ 
  onTranscription, 
  isDisabled = false 
}) => {
  const [isRecording, setIsRecording] = useState(false)
  const [isSupported, setIsSupported] = useState(true)
  const [transcript, setTranscript] = useState('')
  const [error, setError] = useState<string | null>(null)

  const recognitionRef = useRef<any>(null)

  // Initialize speech recognition
  const initializeSpeechRecognition = useCallback(() => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      setIsSupported(false)
      return null
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    const recognition = new SpeechRecognition()

    recognition.continuous = false
    recognition.interimResults = true
    recognition.lang = 'en-US'
    recognition.maxAlternatives = 1

    recognition.onstart = () => {
      setIsRecording(true)
      setError(null)
      setTranscript('')
    }

    recognition.onresult = (event) => {
      let interimTranscript = ''
      let finalTranscript = ''

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript
        if (event.results[i].isFinal) {
          finalTranscript += transcript
        } else {
          interimTranscript += transcript
        }
      }

      setTranscript(finalTranscript || interimTranscript)
    }

    recognition.onend = () => {
      setIsRecording(false)
      if (transcript.trim()) {
        onTranscription(transcript.trim())
      }
    }

    recognition.onerror = (event) => {
      setIsRecording(false)
      let errorMessage = 'Speech recognition error'
      
      switch (event.error) {
        case 'no-speech':
          errorMessage = 'No speech detected. Please try again.'
          break
        case 'audio-capture':
          errorMessage = 'No microphone found or access denied.'
          break
        case 'not-allowed':
          errorMessage = 'Microphone access denied. Please allow microphone access.'
          break
        case 'network':
          errorMessage = 'Network error occurred during recognition.'
          break
        default:
          errorMessage = `Speech recognition error: ${event.error}`
      }
      
      setError(errorMessage)
      setTimeout(() => setError(null), 5000)
    }

    return recognition
  }, [transcript, onTranscription])

  const startRecording = useCallback(() => {
    if (isDisabled || isRecording) return

    if (!recognitionRef.current) {
      recognitionRef.current = initializeSpeechRecognition()
    }

    if (recognitionRef.current) {
      try {
        recognitionRef.current.start()
      } catch (error) {
        setError('Failed to start speech recognition')
        console.error('Speech recognition error:', error)
      }
    }
  }, [isDisabled, isRecording, initializeSpeechRecognition])

  const stopRecording = useCallback(() => {
    if (recognitionRef.current && isRecording) {
      recognitionRef.current.stop()
    }
  }, [isRecording])

  if (!isSupported) {
    return (
      <div className="text-center p-4">
        <p className="text-sm text-gray-500">
          Speech recognition is not supported in your browser.
        </p>
        <p className="text-xs text-gray-400 mt-1">
          Please use a modern browser like Chrome or Edge.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Voice Input Button */}
      <div className="flex flex-col items-center space-y-3">
        <motion.button
          onClick={isRecording ? stopRecording : startRecording}
          disabled={isDisabled}
          className={`w-16 h-16 rounded-full flex items-center justify-center transition-all duration-200 ${
            isRecording
              ? 'bg-red-500 hover:bg-red-600 shadow-lg'
              : 'bg-primary-500 hover:bg-primary-600 shadow-md hover:shadow-lg'
          } ${isDisabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
          whileHover={{ scale: isDisabled ? 1 : 1.05 }}
          whileTap={{ scale: isDisabled ? 1 : 0.95 }}
          animate={isRecording ? { scale: [1, 1.1, 1] } : {}}
          transition={isRecording ? { duration: 0.5, repeat: Infinity } : {}}
        >
          {isRecording ? (
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 0.5, repeat: Infinity }}
            >
              <svg
                className="w-6 h-6 text-white"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path d="M6 6h4v12H6V6zm8 0h4v12h-4V6z" />
              </svg>
            </motion.div>
          ) : (
            <svg
              className="w-6 h-6 text-white"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path d="M12 2a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3zm1.05 9.707L13 12a1 1 0 0 1-2 0v-.293A1.002 1.002 0 0 1 10 10c0-.552.448-1 1-1s1 .448 1 1a1 1 0 0 1-1 1 .707.707 0 0 0 .707-.707z" />
            </svg>
          )}
        </motion.button>

        <div className="text-center">
          <p className="text-sm font-medium text-gray-700">
            {isRecording ? 'Recording...' : 'Press to speak'}
          </p>
          <p className="text-xs text-gray-500">
            {isRecording ? 'Release when done' : 'Ask me anything!'}
          </p>
        </div>
      </div>

      {/* Live Transcript */}
      {isRecording && transcript && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gray-50 rounded-lg p-3 border-2 border-dashed border-gray-300"
        >
          <p className="text-sm text-gray-600 mb-1">Live transcript:</p>
          <p className="text-gray-800 italic">"{transcript}"</p>
        </motion.div>
      )}

      {/* Error Message */}
      {error && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          className="bg-red-50 border border-red-200 rounded-lg p-3"
        >
          <div className="flex items-start space-x-2">
            <svg
              className="w-5 h-5 text-red-400 mt-0.5 flex-shrink-0"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clipRule="evenodd"
              />
            </svg>
            <div>
              <p className="text-sm font-medium text-red-800">
                Voice Recognition Error
              </p>
              <p className="text-sm text-red-600">
                {error}
              </p>
            </div>
          </div>
        </motion.div>
      )}

      {/* Instructions */}
      <div className="text-center">
        <details className="text-xs text-gray-500">
          <summary className="cursor-pointer hover:text-gray-700">
            Voice instructions
          </summary>
          <div className="mt-2 space-y-1 text-left">
            <p>• Click the microphone to start recording</p>
            <p>• Speak clearly and at a normal pace</p>
            <p>• Click again or wait for auto-stop</p>
            <p>• Make sure your microphone is enabled</p>
          </div>
        </details>
      </div>
    </div>
  )
}

// Extend Window interface for TypeScript
declare global {
  interface Window {
    SpeechRecognition: any
    webkitSpeechRecognition: any
  }
}

export default VoiceControls
