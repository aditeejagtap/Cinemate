from fastapi import FastAPI, HTTPException
from src.models.schemas import MovieRequest, MovieResponse
from src.services.agent_orchestrator import AgentOrchestrator
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Cinemate",
    description="Agentic movie recommendation service based on mood",
    version="1.0.0"
)

orchestrator = AgentOrchestrator()


@app.get("/")
async def root():
    return {
        "service": "Cinemate",
        "description": "AI-powered movie recommendations based on your mood",
        "endpoints": {
            "POST /recommend": "Get movie recommendations based on mood"
        }
    }


@app.post("/recommend", response_model=MovieResponse)
async def recommend_movies(request: MovieRequest):
    """Get personalized movie recommendations based on mood."""
    try:
        if not os.getenv("GROQ_API_KEY"):
            raise HTTPException(
                status_code=500,
                detail="Groq API key not configured"
            )
        
        response = await orchestrator.process_request(request)
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
