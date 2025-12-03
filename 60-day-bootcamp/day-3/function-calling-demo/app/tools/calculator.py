from pydantic import BaseModel, Field
from app.tools.base import BaseTool
from typing import Literal


class CalculatorParams(BaseModel):
    operation: Literal["add", "subtract", "multiply", "divide", "mod", "power", "floor_divide", "average", "max", "min"] = Field(
        ..., description="Mathematical operation to perform"
    )
    a: float = Field(..., description="First number")
    b: float = Field(..., description="Second number")


class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Performs basic mathematical operations (add, subtract, multiply, divide, mod, power, floor_divide, average, max, min)"
    parameters_schema = CalculatorParams
    
    async def execute(self, operation: str, a: float, b: float) -> dict:
        operations = {
            "add": lambda x, y: x + y,
            "subtract": lambda x, y: x - y,
            "multiply": lambda x, y: x * y,
            "divide": lambda x, y: x / y if y != 0 else "Error: Division by zero",
            "mod": lambda x, y: x % y if y != 0 else "Error: Modulus by zero",
            "power": lambda x, y: x ** y,
            "floor_divide": lambda x, y: x // y if y != 0 else "Error: Division by zero",
            "average": lambda x, y: (x + y) / 2,
            "max": lambda x, y: max(x, y),
            "min": lambda x, y: min(x, y),
        }
        
        result = operations[operation](a, b)
        return {
            "operation": operation,
            "operands": {"a": a, "b": b},
            "result": result
        }