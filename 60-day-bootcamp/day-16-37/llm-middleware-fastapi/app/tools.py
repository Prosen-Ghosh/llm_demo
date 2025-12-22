from langchain.tools import tool
from fastapi import Request

@tool
def echo_tool(text: str, request: Request) -> str:
    req_id = request.state.req_id
    return f"[req_id={req_id}] Echo: {text}"
