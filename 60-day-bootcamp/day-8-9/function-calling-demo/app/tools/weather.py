from pydantic import BaseModel, Field, validator
from app.tools.base import BaseTool
import random


class WeatherParams(BaseModel):
    location: str = Field(..., description="City name or location", min_length=2)
    unit: str = Field(default="celsius", pattern="^(celsius|fahrenheit)$")

    @validator('unit', pre=True)
    def validate_unit(cls, v):
        allowed_units = ["celsius", "fahrenheit"]
        if v is None:
            return "celsius"
        
        v_lower = str(v).lower().strip()
        if v_lower in allowed_units:
            return v_lower
        
        # If pattern doesn't match, fallback to default
        print(f"Warning: Unit '{v}' is not valid. Defaulting to 'celsius'")
        return "celsius"

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