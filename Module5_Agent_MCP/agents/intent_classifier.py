from openai import OpenAI
from typing import Dict, Any
import json
import re

class IntentClassifier:
    """
    Classifies user intent to determine which MCP servers to query
    """
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
    
    def classify(self, query: str) -> Dict[str, Any]:
        """
        Classify user query into intents: weather, news, or both
        Returns structured intent data
        """
        
        system_prompt = """You are an intent classifier. Analyze the user's query and determine:
1. If they want weather information (and which location)
2. If they want news (and which topic, if specified)

IMPORTANT RULES:
- If query mentions "today", "happening", "what's going on" with a location → BOTH weather AND news
- If just a location name with no clear intent → BOTH weather AND news
- "Hello", "Hi", greetings → NEITHER weather NOR news
- Pure weather queries: "weather in X", "temperature in X" → ONLY weather
- Pure news queries: "tech news", "latest headlines" → ONLY news

Respond ONLY with valid JSON:
{
    "weather": {
        "needed": true/false,
        "location": "city name or null"
    },
    "news": {
        "needed": true/false,
        "topic": "topic or null (use 'general' for general news)"
    }
}

Examples:
- "What's happening in London today?" → {"weather": {"needed": true, "location": "London"}, "news": {"needed": true, "topic": "general"}}
- "weather in Paris" → {"weather": {"needed": true, "location": "Paris"}, "news": {"needed": false, "topic": null}}
- "tech news" → {"weather": {"needed": false, "location": null}, "news": {"needed": true, "topic": "technology"}}
- "Hello" → {"weather": {"needed": false, "location": null}, "news": {"needed": false, "topic": null}}
- "Tell me about Tokyo" → {"weather": {"needed": true, "location": "Tokyo"}, "news": {"needed": true, "topic": "general"}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            content = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            content = re.sub(r'```json\s*|\s*```', '', content)
            
            intent = json.loads(content)
            return intent
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response was: {content}")
            return self._default_intent()
        except Exception as e:
            print(f"Intent classification error: {e}")
            return self._default_intent()
    
    def _default_intent(self) -> Dict[str, Any]:
        """Return default intent when classification fails"""
        return {
            "weather": {"needed": False, "location": None},
            "news": {"needed": False, "topic": None}
        }

