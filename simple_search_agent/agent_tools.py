import os
import requests
from dotenv import load_dotenv
from langchain.tools import tool
from simple_agent import SimpleAgent
load_dotenv()

SERPAPI_KEY = os.environ.get("SERPAPI_API_KEY")
SERPAPI_ENDPOINT = os.environ.get('SERPAPI_ENDPOINT', "https://serpapi.com/search")

if not SERPAPI_KEY:
    raise EnvironmentError("Set SERPAPI_API_KEY in your environment (.env)")

@tool("web_search", description="Perform a web search for the given query and return formatted results")
def web_search(query: str, num_results: int = 1) -> str:
    """"""
    params = {
        "q": query,
        "num": num_results,
        "api_key": SERPAPI_KEY,
    }

    try:
        res = requests.get(SERPAPI_ENDPOINT, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()

        results = []
        organic = data.get("organic") or []
        for r in organic:
            title = r.get("title", "")
            snippet = r.get("snippet", "")
            link = r.get("link") or ""
            results.append(f"Title: {title}\nSnippet: {snippet}\nURL: {link}")
        
        if not results:
            return "No search results found."
        return "\n\n---\n\n".join(results)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            return f"❌ SerpAPI Authentication Error: Invalid or expired API key. Please check your SERPAPI_API_KEY at https://serpapi.com/manage-api-key"
        elif e.response.status_code == 403:
            return f"❌ SerpAPI Access Denied: Your plan may not have sufficient credits. Check at https://serpapi.com/dashboard"
        else:
            return f"Search error: {str(e)}"
    except Exception as e:
        return f"Search error: {str(e)}"

def create_agent(api_key: str):
    messages = [
            ("system", """You are a helpful AI assistant. You will be provided with web search results.
            Use these search results to answer the user's question accurately and comprehensively.
            Cite the sources when relevant."""),
                        ("user", """Question: {question}

            Search Results:
            {search_results}

            Please provide a detailed answer based on the search results above.""")
        ]
    return SimpleAgent(api_key, messages)