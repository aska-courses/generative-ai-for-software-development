import asyncio
from typing import Dict, Any, Optional
import aiohttp
import json

class MCPClient:
    """
    Client for interacting with MCP servers
    Handles weather and news data retrieval
    """
    
    def __init__(self):
        self.weather_available = False
        self.news_available = False
        self.news_api_key = None
        
    async def initialize_all_servers(self) -> Dict[str, bool]:
        """Initialize all MCP server connections"""
        import os
        
        # Weather is always available (Open-Meteo is free)
        self.weather_available = True
        
        # Check for news API key
        self.news_api_key = os.getenv('THENEWSAPI_KEY')
        self.news_available = bool(self.news_api_key)
        
        return {
            "weather": self.weather_available,
            "news": self.news_available
        }
    
    async def get_weather(self, location: str) -> Dict[str, Any]:
        """Get weather data via Open-Meteo API"""
        if not self.weather_available:
            return {"error": "Weather service unavailable"}
        
        try:
            async with aiohttp.ClientSession() as session:
                # Geocode location
                geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"
                async with session.get(geo_url) as response:
                    geo_data = await response.json()
                
                if not geo_data.get("results"):
                    return {"error": f"Location '{location}' not found"}
                
                lat = geo_data["results"][0]["latitude"]
                lon = geo_data["results"][0]["longitude"]
                city_name = geo_data["results"][0]["name"]
                country = geo_data["results"][0].get("country", "")
                
                # Get weather
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m&timezone=auto"
                async with session.get(weather_url) as response:
                    weather_data = await response.json()
                
                current = weather_data.get("current", {})
                
                weather_codes = {
                    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
                    45: "Foggy", 51: "Light drizzle", 61: "Slight rain", 63: "Moderate rain",
                    65: "Heavy rain", 71: "Slight snow", 95: "Thunderstorm"
                }
                
                weather_code = current.get("weather_code", 0)
                condition = weather_codes.get(weather_code, "Unknown")
                
                return {import asyncio
from typing import Dict, Any, Optional
import aiohttp
import json

class MCPClient:
    """
    Client for interacting with MCP servers
    Handles weather and news data retrieval
    """
    
    def __init__(self):
        self.weather_available = False
        self.news_available = False
        self.news_api_key = None
        
    async def initialize_all_servers(self) -> Dict[str, bool]:
        """Initialize all MCP server connections"""
        import os
        
        # Weather is always available (Open-Meteo is free)
        self.weather_available = True
        
        # Check for news API key
        self.news_api_key = os.getenv('THENEWSAPI_KEY')
        self.news_available = bool(self.news_api_key)
        
        return {
            "weather": self.weather_available,
            "news": self.news_available
        }
    
    async def get_weather(self, location: str) -> Dict[str, Any]:
        """Get weather data via Open-Meteo API"""
        if not self.weather_available:
            return {"error": "Weather service unavailable"}
        
        try:
            async with aiohttp.ClientSession() as session:
                # Geocode location
                geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"
                async with session.get(geo_url) as response:
                    geo_data = await response.json()
                
                if not geo_data.get("results"):
                    return {"error": f"Location '{location}' not found"}
                
                lat = geo_data["results"][0]["latitude"]
                lon = geo_data["results"][0]["longitude"]
                city_name = geo_data["results"][0]["name"]
                country = geo_data["results"][0].get("country", "")
                
                # Get weather
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m&timezone=auto"
                async with session.get(weather_url) as response:
                    weather_data = await response.json()
                
                current = weather_data.get("current", {})
                
                weather_codes = {
                    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
                    45: "Foggy", 51: "Light drizzle", 61: "Slight rain", 63: "Moderate rain",
                    65: "Heavy rain", 71: "Slight snow", 95: "Thunderstorm"
                }
                
                weather_code = current.get("weather_code", 0)
                condition = weather_codes.get(weather_code, "Unknown")
                
                return {
                    "location": f"{city_name}, {country}",
                    "temperature": round(current.get("temperature_2m", 0), 1),
                    "feels_like": round(current.get("apparent_temperature", 0), 1),
                    "humidity": current.get("relative_humidity_2m", 0),
                    "wind_speed": round(current.get("wind_speed_10m", 0), 1),
                    "condition": condition,
                    "precipitation": current.get("precipitation", 0)
                }
                
        except Exception as e:
            return {"error": f"Weather fetch failed: {str(e)}"}
    
    async def get_news(self, topic: Optional[str] = None) -> Dict[str, Any]:
        """Get news data via TheNews API"""
        if not self.news_available:
            return {
                "error": "News service unavailable",
                "note": "Please set THENEWSAPI_KEY environment variable"
            }
        
        try:
            async with aiohttp.ClientSession() as session:
                if topic and topic != "general":
                    url = f"https://api.thenewsapi.com/v1/news/all?api_token={self.news_api_key}&search={topic}&limit=5&language=en"
                else:
                    url = f"https://api.thenewsapi.com/v1/news/top?api_token={self.news_api_key}&limit=5&language=en"
                
                async with session.get(url) as response:
                    if response.status != 200:
                        return {"error": f"News API returned status {response.status}"}
                    
                    data = await response.json()
                    articles = []
                    
                    for item in data.get("data", [])[:5]:
                        articles.append({
                            "title": item.get("title", "No title"),
                            "description": item.get("description", "No description"),
                            "url": item.get("url", ""),
                            "published_at": item.get("published_at", ""),
                            "source": item.get("source", "Unknown")
                        })
                    
                    return {"articles": articles, "total": len(articles)}
                    
        except Exception as e:
            return {"error": f"News fetch failed: {str(e)}"}

                    "location": f"{city_name}, {country}",
                    "temperature": round(current.get("temperature_2m", 0), 1),
                    "feels_like": round(current.get("apparent_temperature", 0), 1),
                    "humidity": current.get("relative_humidity_2m", 0),
                    "wind_speed": round(current.get("wind_speed_10m", 0), 1),
                    "condition": condition,
                    "precipitation": current.get("precipitation", 0)
                }
                
        except Exception as e:
            return {"error": f"Weather fetch failed: {str(e)}"}
    
    async def get_news(self, topic: Optional[str] = None) -> Dict[str, Any]:
        """Get news data via TheNews API"""
        if not self.news_available:
            return {
                "error": "News service unavailable",
                "note": "Please set THENEWSAPI_KEY environment variable"
            }
        
        try:
            async with aiohttp.ClientSession() as session:
                if topic and topic != "general":
                    url = f"https://api.thenewsapi.com/v1/news/all?api_token={self.news_api_key}&search={topic}&limit=5&language=en"
                else:
                    url = f"https://api.thenewsapi.com/v1/news/top?api_token={self.news_api_key}&limit=5&language=en"
                
                async with session.get(url) as response:
                    if response.status != 200:
                        return {"error": f"News API returned status {response.status}"}
                    
                    data = await response.json()
                    articles = []
                    
                    for item in data.get("data", [])[:5]:
                        articles.append({
                            "title": item.get("title", "No title"),
                            "description": item.get("description", "No description"),
                            "url": item.get("url", ""),
                            "published_at": item.get("published_at", ""),
                            "source": item.get("source", "Unknown")
                        })
                    
                    return {"articles": articles, "total": len(articles)}
                    
        except Exception as e:
            return {"error": f"News fetch failed: {str(e)}"}
