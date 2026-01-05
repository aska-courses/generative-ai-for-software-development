import asyncio
from typing import Dict, Any, List, Optional
from openai import OpenAI
import json
from .intent_classifier import IntentClassifier
from .mcp_client import MCPClient

class AgentOrchestrator:
    """
    Main orchestrator that coordinates between intent classification,
    MCP servers, and response generation
    """
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
        self.intent_classifier = IntentClassifier(api_key)
        self.mcp_client = MCPClient()
        self.conversation_context = []
        
    def initialize_mcp_servers(self) -> Dict[str, bool]:
        """Initialize all MCP servers and return their status"""
        try:
            status = asyncio.run(self.mcp_client.initialize_all_servers())
            return status
        except Exception as e:
            print(f"Error initializing MCP servers: {e}")
            return {"weather": False, "news": False}
    
    def process_query(self, messages: List[Dict], current_query: str) -> Dict[str, Any]:
        """
        Main processing pipeline:
        1. Classify intent
        2. Route to appropriate MCP servers
        3. Aggregate results
        4. Generate natural response
        """
        try:
            # Step 1: Classify intent
            intent = self.intent_classifier.classify(current_query)
            
            # Step 2: Route to MCP servers based on intent
            results = {"intent": intent}
            
            # Handle weather requests
            if intent["weather"]["needed"]:
                location = intent["weather"]["location"]
                if location:
                    weather_data = asyncio.run(
                        self.mcp_client.get_weather(location)
                    )
                    results["weather"] = weather_data
            
            # Handle news requests
            if intent["news"]["needed"]:
                topic = intent["news"]["topic"]
                news_data = asyncio.run(
                    self.mcp_client.get_news(topic)
                )
                results["news"] = news_data
            
            # Step 3: Generate natural language response
            if not intent["weather"]["needed"] and not intent["news"]["needed"]:
                # General conversation
                results["text"] = self._generate_general_response(messages, current_query)
            else:
                # Generate contextual response with data
                results["text"] = self._generate_contextual_response(results, current_query)
            
            return results
            
        except Exception as e:
            return {"error": str(e), "text": f"I encountered an error: {str(e)}"}
    
    def _generate_general_response(self, messages: List[Dict], query: str) -> str:
        """Generate response for general queries not needing MCP"""
        try:
            # Filter messages for API
            api_messages = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in messages
                if msg["role"] in ["user", "assistant"] and isinstance(msg.get("content"), str)
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=api_messages,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I'm having trouble processing that. Could you rephrase your question?"
    
    def _generate_contextual_response(self, results: Dict, query: str) -> str:
        """Generate natural response incorporating MCP results"""
        context_parts = []
        
        if results.get("weather"):
            weather = results["weather"]
            if "error" not in weather:
                context_parts.append(
                    f"The weather in {weather.get('location')} is {weather.get('temperature')}°C "
                    f"with {weather.get('condition').lower()} conditions."
                )
        
        if results.get("news"):
            news = results["news"]
            if "error" not in news:
                articles = news.get('articles', [])
                if articles:
                    context_parts.append(
                        f"I found {len(articles)} recent news articles for you."
                    )
        
        if not context_parts:
            return "I'm having trouble retrieving that information right now. Please try again."
        
        # Generate brief natural response
        return " ".join(context_parts)


