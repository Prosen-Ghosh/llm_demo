from pydantic import BaseModel, Field
from app.tools.base import BaseTool
import random


class WeatherParams(BaseModel):
    location: str = Field(..., description="City name or location", min_length=2)
    unit: str = Field(default="celsius", pattern="^(celsius|fahrenheit)$")


class WeatherTool(BaseTool):
    name = "get_weather"
    description = "Get current weather information for a specific location"
    parameters_schema = WeatherParams
    
    async def execute(self, location: str, unit: str = "celsius") -> dict:
        # Simulated weather data
        temp_c = random.randint(-10, 35)
        temp_f = int(temp_c * 9/5 + 32)
        
        conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Stormy"]
        
        return {
            "location": location,
            "temperature": temp_c if unit == "celsius" else temp_f,
            "unit": "°C" if unit == "celsius" else "°F",
            "condition": random.choice(conditions),
            "humidity": f"{random.randint(30, 90)}%",
            "note": "This is simulated data for demonstration purposes"
        }