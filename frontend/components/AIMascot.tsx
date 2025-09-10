'use client'

import { motion, AnimatePresence } from 'framer-motion'
import { useEffect, useState } from 'react'

interface AIMascotProps {
  emotion: string
  isSpeaking: boolean
  isLoading: boolean
}

const AIMascot: React.FC<AIMascotProps> = ({ emotion, isSpeaking, isLoading }) => {
  const [eyeBlinkState, setEyeBlinkState] = useState(false)

  // Auto blink animation
  useEffect(() => {
    const blinkInterval = setInterval(() => {
      setEyeBlinkState(true)
      setTimeout(() => setEyeBlinkState(false), 150)
    }, 2000 + Math.random() * 3000)

    return () => clearInterval(blinkInterval)
  }, [])

  const getMascotColor = () => {
    switch (emotion) {
      case 'happy': return 'from-green-400 to-blue-500'
      case 'thinking': return 'from-purple-400 to-indigo-500'
      case 'explaining': return 'from-blue-400 to-cyan-500'
      case 'encouraging': return 'from-yellow-400 to-orange-500'
      case 'questioning': return 'from-pink-400 to-red-500'
      default: return 'from-blue-400 to-indigo-500'
    }
  }

  const getMascotAnimation = () => {
    if (isLoading) return 'thinking'
    if (isSpeaking) return 'speaking'
    return emotion
  }

  const animationVariants = {
    happy: {
      scale: [1, 1.1, 1],
      rotate: [0, 5, -5, 0],
      transition: { duration: 0.6, ease: 'easeInOut' }
    },
    thinking: {
      x: [0, -10, 10, 0],
      transition: { duration: 2, repeat: Infinity, ease: 'easeInOut' }
    },
    explaining: {
      y: [0, -5, 0],
      transition: { duration: 1.5, repeat: Infinity, ease: 'easeInOut' }
    },
    encouraging: {
      scale: [1, 1.05, 1],
      transition: { duration: 1, repeat: Infinity, ease: 'easeInOut' }
    },
    questioning: {
      rotate: [0, 3, -3, 0],
      transition: { duration: 0.8, repeat: Infinity, ease: 'easeInOut' }
    },
    speaking: {
      scale: [1, 1.02, 1],
      transition: { duration: 0.3, repeat: Infinity, ease: 'easeInOut' }
    }
  }

  const currentAnimation = getMascotAnimation()

  return (
    <div className="flex flex-col items-center space-y-4">
      {/* Main Mascot */}
      <motion.div
        className="relative"
        variants={animationVariants}
        animate={currentAnimation}
      >
        {/* Mascot Body */}
        <div className={`w-32 h-32 rounded-full bg-gradient-to-br ${getMascotColor()} shadow-lg relative overflow-hidden`}>
          {/* Eyes */}
          <div className="absolute top-8 left-1/2 transform -translate-x-1/2 flex space-x-3">
            <motion.div
              className="w-4 h-4 bg-white rounded-full flex items-center justify-center"
              animate={{ scaleY: eyeBlinkState ? 0.1 : 1 }}
              transition={{ duration: 0.1 }}
            >
              <div className="w-2 h-2 bg-gray-800 rounded-full"></div>
            </motion.div>
            <motion.div
              className="w-4 h-4 bg-white rounded-full flex items-center justify-center"
              animate={{ scaleY: eyeBlinkState ? 0.1 : 1 }}
              transition={{ duration: 0.1 }}
            >
              <div className="w-2 h-2 bg-gray-800 rounded-full"></div>
            </motion.div>
          </div>

          {/* Mouth */}
          <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2">
            <AnimatePresence mode="wait">
              {isSpeaking ? (
                <motion.div
                  key="speaking"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="w-6 h-3 bg-gray-800 rounded-full"
                />
              ) : emotion === 'happy' ? (
                <motion.div
                  key="happy"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="w-6 h-3 bg-gray-800 rounded-b-full"
                />
              ) : emotion === 'thinking' ? (
                <motion.div
                  key="thinking"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="w-4 h-1 bg-gray-800 rounded-full"
                />
              ) : (
                <motion.div
                  key="neutral"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="w-5 h-2 bg-gray-800 rounded-full"
                />
              )}
            </AnimatePresence>
          </div>

          {/* Loading indicator */}
          {isLoading && (
            <div className="absolute top-2 right-2">
              <div className="w-3 h-3 bg-white rounded-full animate-pulse"></div>
            </div>
          )}

          {/* Speaking indicator */}
          {isSpeaking && (
            <motion.div
              className="absolute -top-2 -right-2 w-6 h-6"
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 0.5, repeat: Infinity }}
            >
              <div className="w-full h-full bg-green-400 rounded-full opacity-80 flex items-center justify-center">
                <div className="w-2 h-2 bg-white rounded-full"></div>
              </div>
            </motion.div>
          )}
        </div>

        {/* Shadow */}
        <motion.div
          className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-20 h-4 bg-black opacity-10 rounded-full blur-sm"
          animate={{ scale: isSpeaking ? 1.1 : 1 }}
          transition={{ duration: 0.3 }}
        />
      </motion.div>

      {/* Emotion Indicator */}
      <motion.div
        className="text-center"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <p className="text-sm font-medium text-gray-700 capitalize">
          {isLoading ? 'Thinking...' : 
           isSpeaking ? 'Speaking...' : 
           emotion}
        </p>
        
        {/* Emotion description */}
        <p className="text-xs text-gray-500 mt-1">
          {isLoading ? 'Processing your question' :
           isSpeaking ? 'Playing response' :
           getEmotionDescription(emotion)}
        </p>
      </motion.div>

      {/* Sound waves when speaking */}
      <AnimatePresence>
        {isSpeaking && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="flex space-x-1"
          >
            {[0, 1, 2].map((i) => (
              <motion.div
                key={i}
                className="w-1 bg-blue-400 rounded-full"
                animate={{
                  height: [4, 12, 4],
                }}
                transition={{
                  duration: 0.6,
                  repeat: Infinity,
                  delay: i * 0.1,
                  ease: 'easeInOut'
                }}
              />
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

const getEmotionDescription = (emotion: string): string => {
  switch (emotion) {
    case 'happy': return 'Excited to help!'
    case 'thinking': return 'Processing...'
    case 'explaining': return 'Teaching mode'
    case 'encouraging': return 'Supportive'
    case 'questioning': return 'Curious'
    default: return 'Ready to learn'
  }
}

export default AIMascot
