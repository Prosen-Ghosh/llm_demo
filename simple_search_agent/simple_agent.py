import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

class SimpleAgent:
    def __init__(self, api_key: str, messages: list[tuple]):
        OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'deepseek/deepseek-r1-0528')
        
        self.llm = ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=0.7,
            max_tokens=2000,  # Limit token usage
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "http://localhost:8501",
                "X-Title": "Simple Search Agent"
            }
        )
        
        self.prompt = ChatPromptTemplate.from_messages(messages)

        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def invoke(self, inputs: dict, tools: dict) -> dict:
        query = inputs.get("input", "")
        num_results = inputs.get('num_results', 1)
        search_results = tools["web_search"].invoke({"query": query, "num_results": num_results })
        
        answer = self.chain.invoke({
            "question": query,
            "search_results": search_results
        })
        
        return {
            "output": answer,
            "search_results": search_results
        }