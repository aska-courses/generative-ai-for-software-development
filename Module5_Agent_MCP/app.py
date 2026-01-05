import streamlit as st
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.orchestrator import AgentOrchestrator
from agents.intent_classifier import IntentClassifier
import os
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(
    page_title="MCP Agent - Weather & News",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .weather-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        margin: 1rem 0;
    }
    .news-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-container {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
    }
    .metric-box {
        flex: 1;
        text-align: center;
        padding: 0.5rem;
        background: rgba(255,255,255,0.2);
        border-radius: 0.5rem;
    }
    .news-title {
        margin: 0 0 0.5rem 0;
        color: #333;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .news-desc {
        color: #666;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    .news-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 0.5rem;
    }
    .news-source {
        font-size: 0.8rem;
        color: #999;
    }
    .news-link {
        color: #667eea;
        text-decoration: none;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = None
if "mcp_status" not in st.session_state:
    st.session_state.mcp_status = {"weather": False, "news": False}
if "cache" not in st.session_state:
    st.session_state.cache = {}

def initialize_orchestrator(api_key: str):
    """Initialize the agent orchestrator with MCP servers"""
    if not api_key:
        return False, "API key is required"
    
    try:
        orchestrator = AgentOrchestrator(api_key)
        status = orchestrator.initialize_mcp_servers()
        
        st.session_state.orchestrator = orchestrator
        st.session_state.mcp_status = status
        
        return True, "Orchestrator initialized successfully"
    except Exception as e:
        return False, f"Failed to initialize: {str(e)}"

def render_weather_card(weather_data: dict):
    """Render weather data as a nice card"""
    if "error" in weather_data:
        st.error(f"❌ {weather_data['error']}")
        return
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"### 🌤️ {weather_data.get('location', 'Unknown')}")
        st.markdown(f"# {weather_data.get('temperature', 'N/A')}°C")
        st.markdown(f"**{weather_data.get('condition', 'Unknown')}**")
    
    with col2:
        st.metric("Feels Like", f"{weather_data.get('feels_like', 'N/A')}°C")
        st.metric("Humidity", f"{weather_data.get('humidity', 'N/A')}%")
    
    with col3:
        st.metric("Wind Speed", f"{weather_data.get('wind_speed', 'N/A')} km/h")
        st.metric("Precipitation", f"{weather_data.get('precipitation', 0)} mm")

def render_news_articles(news_data: dict):
    """Render news articles"""
    if "error" in news_data:
        st.error(f"❌ {news_data['error']}")
        if "note" in news_data:
            st.info(news_data['note'])
        return
    
    articles = news_data.get('articles', [])
    if not articles:
        st.warning("📰 No news articles found.")
        return
    
    st.markdown(f"### 📰 Latest News ({news_data.get('total', len(articles))} articles)")
    
    for idx, article in enumerate(articles[:5], 1):
        with st.container():
            st.markdown(f"**{idx}. {article.get('title', 'No title')}**")
            st.markdown(f"{article.get('description', 'No description available')[:250]}...")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.caption(f"📍 {article.get('source', 'Unknown')}")
            with col2:
                if article.get('url'):
                    st.markdown(f"[Read more →]({article['url']})")
            
            st.divider()

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=os.environ.get("OPENAI_API_KEY", ""),
        help="Enter your OpenAI API key"
    )
    
    model = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
        index=0,
        help="Select the GPT model to use"
    )
    
    st.markdown("---")
    
    # MCP Server Status
    st.subheader("🔌 MCP Server Status")
    
    if st.session_state.orchestrator is None:
        if st.button("🚀 Initialize MCP Servers", use_container_width=True):
            with st.spinner("Initializing MCP servers..."):
                success, message = initialize_orchestrator(api_key)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    else:
        col1, col2 = st.columns(2)
        with col1:
            weather_status = "✅" if st.session_state.mcp_status.get("weather") else "❌"
            st.metric("Weather", weather_status)
        with col2:
            news_status = "✅" if st.session_state.mcp_status.get("news") else "❌"
            st.metric("News", news_status)
        
        if st.button("🔄 Reconnect", use_container_width=True):
            st.session_state.orchestrator = None
            st.rerun()
    
    st.markdown("---")
    
    # Example queries
    st.subheader("💡 Example Queries")
    
    examples = [
        "What's happening in London today?",
        "Weather in Tokyo",
        "Latest tech news",
        "Paris weather and sports news",
        "Tell me about New York",
        "Hello!"
    ]
    
    for query in examples:
        if st.button(query, key=f"ex_{query}", use_container_width=True):
            st.session_state.example_query = query
            st.rerun()
    
    st.markdown("---")
    
    # Cache management
    st.subheader("💾 Cache")
    cache_size = len(st.session_state.cache)
    st.metric("Cached Responses", cache_size)
    
    if cache_size > 0 and st.button("Clear Cache", use_container_width=True):
        st.session_state.cache = {}
        st.success("Cache cleared!")
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.caption(f"**Model:** {model}")
    st.caption("**Powered by:** OpenAI + MCP")

# Main content
st.title("🤖 Intelligent Weather & News Agent")
st.markdown("Ask me about weather, news, or anything else!")

# Check if orchestrator is initialized
if st.session_state.orchestrator is None:
    st.info("👈 Please initialize the MCP servers from the sidebar to get started.")
    st.markdown("### Quick Start:")
    st.markdown("1. Enter your OpenAI API key in the sidebar")
    st.markdown("2. Click '🚀 Initialize MCP Servers'")
    st.markdown("3. Start asking questions!")
else:
    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                # Render structured response
                if isinstance(message.get("data"), dict):
                    data = message["data"]
                    
                    if data.get("weather"):
                        render_weather_card(data["weather"])
                    
                    if data.get("news"):
                        render_news_articles(data["news"])
                    
                    if data.get("text"):
                        st.markdown(data["text"])
                    
                    if data.get("error"):
                        st.error(data["error"])
                else:
                    st.markdown(message["content"])
            else:
                st.markdown(message["content"])
    
    # Handle example query
    if "example_query" in st.session_state:
        prompt = st.session_state.example_query
        del st.session_state.example_query
    else:
        prompt = st.chat_input("💬 Type your question here... (e.g., 'What's happening in London today?')")
    
    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process with orchestrator
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    orchestrator = st.session_state.orchestrator
                    orchestrator.model = model
                    
                    # Check cache first
                    cache_key = f"{prompt}_{model}"
                    if cache_key in st.session_state.cache:
                        response_data = st.session_state.cache[cache_key]
                        st.info("📦 Using cached response")
                    else:
                        # Process query
                        response_data = orchestrator.process_query(
                            st.session_state.messages,
                            prompt
                        )
                        st.session_state.cache[cache_key] = response_data
                    
                    # Render response
                    if response_data.get("weather"):
                        render_weather_card(response_data["weather"])
                    
                    if response_data.get("news"):
                        render_news_articles(response_data["news"])
                    
                    if response_data.get("text"):
                        st.markdown(response_data["text"])
                    
                    if response_data.get("error"):
                        st.error(response_data["error"])
                    
                    # Store structured data
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_data.get("text", ""),
                        "data": response_data
                    })
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🌐 Weather: Open-Meteo API")
with col2:
    st.caption("📰 News: TheNews API")
with col3:
    st.caption("🤖 AI: OpenAI GPT-4o-mini")


