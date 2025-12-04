import json

def format_sse_data(data_type: str, content: dict) -> str:
    return f"data: {json.dumps(content)}\n\n"