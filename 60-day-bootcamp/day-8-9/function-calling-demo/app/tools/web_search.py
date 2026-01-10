from pydantic import BaseModel, Field
from app.tools.base import BaseTool


class WebSearchParams(BaseModel):
    query: str = Field(..., description="Search query", min_length=1, max_length=200)
    num_results: int = Field(default=3, ge=1, le=10, description="Number of results to return")


class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Search the web for information on a given query"
    parameters_schema = WebSearchParams
    
    async def execute(self, query: str, num_results: int = 3) -> dict:
        # Simulated search results
        results = [
            {
                "title": f"Result {i+1} for: {query}",
                "url": f"https://example.com/result{i+1}",
                "snippet": f"This is a simulated search result snippet for query: {query}"
            }
            for i in range(num_results)
        ]
        
        return {
            "query": query,
            "num_results": len(results),
            "results": results,
            "note": "This is simulated data for demonstration purposes"
        }