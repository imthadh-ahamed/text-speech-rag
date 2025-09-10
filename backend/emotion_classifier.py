from typing import Dict, List
import re
import logging

logger = logging.getLogger(__name__)

class EmotionClassifier:
    """
    Simple rule-based emotion classifier for AI tutor responses
    """
    
    def __init__(self):
        # Define emotion patterns and keywords
        self.emotion_patterns = {
            "happy": {
                "keywords": ["great", "excellent", "wonderful", "fantastic", "amazing", "perfect", 
                           "congratulations", "well done", "brilliant", "awesome", "good job"],
                "patterns": [
                    r"that's\s+(great|excellent|wonderful|fantastic|amazing|perfect)",
                    r"(well\s+done|good\s+job|great\s+work)",
                    r"you\s+(got\s+it|did\s+it|understand|figured\s+it\s+out)",
                ]
            },
            "thinking": {
                "keywords": ["let me", "consider", "think", "analyze", "examine", "look at",
                           "hmm", "interesting", "complex", "challenging", "difficult"],
                "patterns": [
                    r"let\s+me\s+(think|consider|analyze|examine)",
                    r"this\s+is\s+(interesting|complex|challenging|difficult)",
                    r"(hmm|well|now)",
                    r"i\s+need\s+to\s+(think|consider|analyze)",
                ]
            },
            "explaining": {
                "keywords": ["because", "since", "therefore", "thus", "so", "explanation",
                           "reason", "cause", "due to", "as a result", "consequently"],
                "patterns": [
                    r"(because|since|therefore|thus|so)\s+",
                    r"the\s+reason\s+(is|for|that)",
                    r"this\s+happens\s+because",
                    r"(step\s+by\s+step|first|second|third|next|then|finally)",
                    r"(for\s+example|such\s+as|like)",
                ]
            },
            "encouraging": {
                "keywords": ["keep", "try", "practice", "don't worry", "you can", "believe",
                           "confident", "progress", "improve", "learning"],
                "patterns": [
                    r"(keep\s+trying|keep\s+practicing|don't\s+worry)",
                    r"you\s+can\s+(do\s+it|learn|improve|get\s+better)",
                    r"(practice\s+makes\s+perfect|with\s+practice)",
                    r"you're\s+(learning|improving|making\s+progress)",
                ]
            },
            "questioning": {
                "keywords": ["what", "how", "why", "when", "where", "which", "can you",
                           "do you", "have you", "would you", "could you"],
                "patterns": [
                    r"(what|how|why|when|where|which)\s+",
                    r"(can\s+you|do\s+you|have\s+you|would\s+you|could\s+you)\s+",
                    r"\?",
                ]
            }
        }
        
        # Default emotion weights
        self.default_emotion = "explaining"
        
    def classify_emotion(self, ai_response: str, user_query: str = "") -> str:
        """
        Classify the emotion of the AI response
        
        Args:
            ai_response: The AI's response text
            user_query: The user's original query (optional, for context)
            
        Returns:
            Emotion string: "happy", "thinking", "explaining", "encouraging", or "questioning"
        """
        try:
            # Convert to lowercase for analysis
            response_lower = ai_response.lower()
            query_lower = user_query.lower()
            
            # Calculate emotion scores
            emotion_scores = {}
            
            for emotion, patterns in self.emotion_patterns.items():
                score = 0
                
                # Check keywords
                for keyword in patterns["keywords"]:
                    score += response_lower.count(keyword.lower())
                
                # Check regex patterns
                for pattern in patterns["patterns"]:
                    matches = re.findall(pattern, response_lower, re.IGNORECASE)
                    score += len(matches) * 2  # Give patterns higher weight
                
                emotion_scores[emotion] = score
            
            # Apply contextual rules
            emotion_scores = self._apply_contextual_rules(emotion_scores, ai_response, user_query)
            
            # Get the emotion with the highest score
            if max(emotion_scores.values()) > 0:
                best_emotion = max(emotion_scores, key=emotion_scores.get)
                logger.info(f"Classified emotion: {best_emotion} (scores: {emotion_scores})")
                return best_emotion
            else:
                logger.info(f"No strong emotion detected, using default: {self.default_emotion}")
                return self.default_emotion
                
        except Exception as e:
            logger.error(f"Error in emotion classification: {str(e)}")
            return self.default_emotion
    
    def _apply_contextual_rules(self, emotion_scores: Dict[str, int], 
                              ai_response: str, user_query: str) -> Dict[str, int]:
        """
        Apply contextual rules to adjust emotion scores
        """
        response_lower = ai_response.lower()
        query_lower = user_query.lower()
        
        # Rule 1: If response is very short, likely thinking
        if len(ai_response.strip()) < 20:
            emotion_scores["thinking"] += 2
        
        # Rule 2: If response contains formulas or code, likely explaining
        if any(char in ai_response for char in ["=", "+", "-", "*", "/", "{", "}", "[", "]"]):
            emotion_scores["explaining"] += 3
        
        # Rule 3: If user made an error (common error phrases), be encouraging
        error_indicators = ["wrong", "incorrect", "mistake", "error", "not right"]
        if any(indicator in query_lower for indicator in error_indicators):
            emotion_scores["encouraging"] += 2
        
        # Rule 4: If user is struggling (help-seeking phrases), be encouraging
        struggle_indicators = ["help", "don't understand", "confused", "stuck", "difficult"]
        if any(indicator in query_lower for indicator in struggle_indicators):
            emotion_scores["encouraging"] += 2
        
        # Rule 5: If response contains praise words, definitely happy
        praise_words = ["correct", "right", "good", "excellent", "perfect", "exactly"]
        praise_count = sum(1 for word in praise_words if word in response_lower)
        if praise_count >= 2:
            emotion_scores["happy"] += 4
        
        # Rule 6: If response asks questions, likely questioning
        question_count = ai_response.count("?")
        emotion_scores["questioning"] += question_count * 2
        
        # Rule 7: If response is very long and detailed, likely explaining
        if len(ai_response.strip()) > 200:
            emotion_scores["explaining"] += 2
        
        # Rule 8: If response contains encouraging phrases, boost encouraging
        encouraging_phrases = ["keep going", "you're on the right track", "good effort", 
                             "try again", "practice more"]
        for phrase in encouraging_phrases:
            if phrase in response_lower:
                emotion_scores["encouraging"] += 3
        
        return emotion_scores
    
    def get_emotion_description(self, emotion: str) -> str:
        """
        Get a description of what the emotion means for the mascot
        
        Args:
            emotion: The emotion string
            
        Returns:
            Description of the emotion for UI purposes
        """
        descriptions = {
            "happy": "Cheerful and positive, celebrating success",
            "thinking": "Contemplative and thoughtful, processing information",
            "explaining": "Educational and informative, sharing knowledge",
            "encouraging": "Supportive and motivating, building confidence",
            "questioning": "Curious and inquisitive, seeking understanding"
        }
        
        return descriptions.get(emotion, "Neutral and calm")
    
    def get_available_emotions(self) -> List[str]:
        """
        Get list of all available emotions
        
        Returns:
            List of emotion strings
        """
        return list(self.emotion_patterns.keys())
