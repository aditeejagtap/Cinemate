import streamlit as st
from src.services.agent_orchestrator import AgentOrchestrator
from src.models.schemas import MovieRequest
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Cinemate 🎬",
    page_icon="🍿",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .movie-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #ff4b4b;
    }
    .movie-title {
        font-size: 20px;
        font-weight: bold;
        color: #262730;
    }
    .movie-meta {
        color: #666;
        font-size: 14px;
    }
    .movie-reason {
        margin-top: 10px;
        font-style: italic;
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize orchestrator
@st.cache_resource
def get_orchestrator():
    return AgentOrchestrator()

# Header
st.title("🎬 Cinemate")
st.subheader("AI-powered movie recommendations based on your mood")

# Check API keys
if not os.getenv("GROQ_API_KEY"):
    st.error("⚠️ Groq API key not found. Please set GROQ_API_KEY in your .env file")
    st.stop()

if not os.getenv("TMDB_API_KEY"):
    st.warning("⚠️ TMDB API key not found. Movie posters will not be displayed. Get one free at https://www.themoviedb.org/settings/api")

# Input section
with st.form("mood_form"):
    mood = st.text_area(
        "How are you feeling?",
        placeholder="e.g., feeling nostalgic and want something heartwarming...",
        height=100
    )
    
    preferences = st.text_input(
        "Any preferences? (optional)",
        placeholder="e.g., prefer 90s movies, love sci-fi, no horror..."
    )
    
    submitted = st.form_submit_button("Get Recommendations 🎯", use_container_width=True)

# Process request
if submitted:
    if not mood.strip():
        st.warning("Please describe your mood first!")
    else:
        with st.spinner("🤖 Our agents are analyzing your mood and finding perfect movies..."):
            try:
                orchestrator = get_orchestrator()
                request = MovieRequest(
                    mood=mood,
                    preferences=preferences if preferences.strip() else None
                )
                
                # Get recommendations
                import asyncio
                response = asyncio.run(orchestrator.process_request(request))
                
                # Display results
                st.success("✨ Here are your personalized recommendations!")
                
                # Mood analysis
                with st.expander("🧠 Mood Analysis", expanded=False):
                    st.write(response.mood_analysis)
                
                # Personalized message
                st.info(response.message)
                
                # Movie recommendations
                st.markdown("### 🎥 Recommended Movies")
                
                for i, movie in enumerate(response.recommendations, 1):
                    genres = " • ".join(movie.genre)
                    
                    if movie.poster_url:
                        # Show with poster in 2 columns
                        col1, col2 = st.columns([1, 3])
                        
                        with col1:
                            st.image(movie.poster_url, width=150)
                        
                        with col2:
                            st.markdown(f"""
                                <div class="movie-card">
                                    <div class="movie-title">{i}. {movie.title}</div>
                                    <div class="movie-meta">📅 {movie.year} | 🎭 {genres}</div>
                                    <div class="movie-reason">💡 {movie.reason}</div>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        # Show full width without poster
                        st.markdown(f"""
                            <div class="movie-card">
                                <div class="movie-title">{i}. {movie.title}</div>
                                <div class="movie-meta">📅 {movie.year} | 🎭 {genres}</div>
                                <div class="movie-reason">💡 {movie.reason}</div>
                            </div>
                        """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Make sure your Groq API key is valid and you have internet connection.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Powered by Groq AI • Built with Streamlit</div>",
    unsafe_allow_html=True
)
