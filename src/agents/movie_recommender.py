from groq import Groq
import os
import json


class MovieRecommenderAgent:
    """Agent responsible for recommending movies based on mood analysis."""
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.system_prompt = """You are a movie recommendation expert. Based on mood analysis,
        suggest 3-5 movies that perfectly match the emotional state and preferences.
        Return ONLY valid JSON with this exact structure:
        {"movies": [{"title": "Movie Name", "year": 2020, "genre": ["Drama", "Thriller"], "reason": "Why this matches the mood"}]}"""
    
    def recommend(self, mood_analysis: dict) -> list:        # -> list - indicates return type
        """Generate movie recommendations based on mood analysis."""
        user_message = f"""Mood Analysis: {mood_analysis['mood_analysis']}
        Original Mood: {mood_analysis['original_mood']}"""
        
        if mood_analysis.get('preferences'):
            user_message += f"\nPreferences: {mood_analysis['preferences']}"
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.8,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        # Handle both array and object responses
        try:
            result = json.loads(content)
            if isinstance(result, dict) and 'movies' in result:
                return result['movies']
            elif isinstance(result, dict) and 'recommendations' in result:
                return result['recommendations']
            return result if isinstance(result, list) else []
        except json.JSONDecodeError:
            return []
