from groq import Groq
import os


class MoodAnalyzerAgent:
    """Agent responsible for analyzing user mood and extracting movie preferences."""
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.system_prompt = """You are a mood analysis expert. Analyze the user's mood description 
        and extract key emotional states, preferences, and movie characteristics that would match.
        Return a concise analysis focusing on: emotional tone, energy level, and suitable movie themes."""
    
    def analyze(self, mood: str, preferences: str = None) -> dict:
        """Analyze mood and return structured insights."""
        user_message = f"Mood: {mood}"
        if preferences:
            user_message += f"\nAdditional preferences: {preferences}"
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        
        analysis = response.choices[0].message.content
        return {
            "mood_analysis": analysis,
            "original_mood": mood,
            "preferences": preferences
        }
