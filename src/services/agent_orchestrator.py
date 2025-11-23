from src.agents.mood_analyzer import MoodAnalyzerAgent
from src.agents.movie_recommender import MovieRecommenderAgent
from src.agents.response_formatter import ResponseFormatterAgent
from src.services.poster_service import PosterService
from src.models.schemas import MovieRequest, MovieResponse, Movie
import asyncio
from concurrent.futures import ThreadPoolExecutor


class AgentOrchestrator:
    """Orchestrates multiple agents to provide movie recommendations."""
    
    def __init__(self):
        self.mood_analyzer = MoodAnalyzerAgent()
        self.movie_recommender = MovieRecommenderAgent()
        self.response_formatter = ResponseFormatterAgent()
        self.poster_service = PosterService()
        self.executor = ThreadPoolExecutor(max_workers=5)
    
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
        
        # Step 4: Fetch posters concurrently
        loop = asyncio.get_event_loop()
        poster_tasks = [
            loop.run_in_executor(
                self.executor,
                self.poster_service.get_poster,
                movie['title'],
                movie['year']
            )
            for movie in raw_recommendations
        ]
        posters = await asyncio.gather(*poster_tasks)
        
        # Step 5: Add posters to recommendations
        for movie, poster_url in zip(raw_recommendations, posters):
            movie['poster_url'] = poster_url
        
        # Step 6: Structure response
        movies = [Movie(**movie) for movie in raw_recommendations]
        
        return MovieResponse(
            mood_analysis=mood_analysis['mood_analysis'],
            recommendations=movies,
            message=message
        )
