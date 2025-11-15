from src.agents.mood_analyzer import MoodAnalyzerAgent
from src.agents.movie_recommender import MovieRecommenderAgent
from src.agents.response_formatter import ResponseFormatterAgent
from src.models.schemas import MovieRequest, MovieResponse, Movie


class AgentOrchestrator:
    """Orchestrates multiple agents to provide movie recommendations."""
    
    def __init__(self):
        self.mood_analyzer = MoodAnalyzerAgent()
        self.movie_recommender = MovieRecommenderAgent()
        self.response_formatter = ResponseFormatterAgent()
    
    async def process_request(self, request: MovieRequest) -> MovieResponse:
        """Process movie recommendation request through agent pipeline."""
        
        # Step 1: Analyze mood
        mood_analysis = self.mood_analyzer.analyze(
            mood=request.mood,
            preferences=request.preferences
        )
        
        # Step 2: Get movie recommendations
        raw_recommendations = self.movie_recommender.recommend(mood_analysis)
        
        # Step 3: Format response message
        message = self.response_formatter.format(
            mood=request.mood,
            movie_count=len(raw_recommendations)
        )
        
        # Step 4: Structure response
        movies = [Movie(**movie) for movie in raw_recommendations]
        
        return MovieResponse(
            mood_analysis=mood_analysis['mood_analysis'],
            recommendations=movies,
            message=message
        )
