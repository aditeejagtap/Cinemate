from pydantic import BaseModel
from typing import List, Optional


class MovieRequest(BaseModel):
    mood: str
    preferences: Optional[str] = None


class Movie(BaseModel):
    title: str
    year: int
    genre: List[str]
    reason: str
    poster_url: Optional[str] = None


class MovieResponse(BaseModel):
    mood_analysis: str
    recommendations: List[Movie]
    message: str
