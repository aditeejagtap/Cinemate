from groq import Groq
import os


class ResponseFormatterAgent:
    """Agent responsible for creating engaging, personalized responses."""
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.system_prompt = """You are a friendly movie concierge. Create a warm, engaging message
        that introduces the movie recommendations. Keep it brief (2-3 sentences) and personalized to the mood."""
    
    def format(self, mood: str, movie_count: int) -> str:
        """Generate a personalized message for the recommendations."""
        user_message = f"User mood: {mood}. Recommending {movie_count} movies."
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.9,
            max_tokens=100
        )
        
        return response.choices[0].message.content
