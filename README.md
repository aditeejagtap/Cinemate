# Cinemate 🎬

An agentic service that suggests movies based on your mood using multiple AI agents powered by Groq.

## Try Cinemate here : 

`https://cinemate12.streamlit.app` 

## Architecture

Cinemate uses three specialized agents:

1. **Mood Analyzer Agent** - Analyzes user mood and extracts emotional preferences
2. **Movie Recommender Agent** - Suggests movies matching the mood analysis
3. **Response Formatter Agent** - Creates personalized, engaging responses

All agents use Groq's fast LLM inference with Llama 3.3 70B model.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
copy .env.example .env
```
Edit `.env` and add your API keys:
- **GROQ_API_KEY**: Get free at https://console.groq.com
- **TMDB_API_KEY**: Get free at https://www.themoviedb.org/settings/api (for movie posters)

## Usage

### Streamlit UI (Recommended)

Run the interactive web interface:
```bash
streamlit run app.py
```

The UI will open in your browser at `http://localhost:8501`

### FastAPI Backend

Run the REST API:
```bash
python -m src.main
```

The API will be available at `http://localhost:8000`

**POST /recommend**

Request:
```json
{
  "mood": "feeling nostalgic and want something heartwarming",
  "preferences": "prefer 90s movies"
}
```

Response:
```json
{
  "mood_analysis": "...",
  "recommendations": [
    {
      "title": "The Shawshank Redemption",
      "year": 1994,
      "genre": ["Drama"],
      "reason": "Perfect for nostalgic, heartwarming feelings..."
    }
  ],
  "message": "Based on your nostalgic mood..."
}
```

### Example with curl

```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d "{\"mood\": \"stressed and need to relax\"}"
```

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.
