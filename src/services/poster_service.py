import requests
import os
from typing import Optional


class PosterService:
    """Service to fetch movie posters from TMDB API."""
    
    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY")
        self.base_url = "https://api.themoviedb.org/3"
        self.image_base_url = "https://image.tmdb.org/t/p/w500"
    
    def get_poster(self, title: str, year: int) -> Optional[str]:
        """Fetch movie poster URL from TMDB API."""
        if not self.api_key:
            return None
        
        try:
            # Step 1: Search for the movie
            search_url = f"{self.base_url}/search/movie"
            params = {
                "api_key": self.api_key,
                "query": title,
                "year": year,
                "language": "en-US"
            }
            
            response = requests.get(search_url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                
                if results:
                    # Get the first result (most relevant)
                    movie = results[0]
                    poster_path = movie.get("poster_path")
                    
                    if poster_path:
                        # Construct full poster URL
                        return f"{self.image_base_url}{poster_path}"
            
            return None
            
        except Exception:
            return None
