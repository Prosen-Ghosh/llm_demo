from app.graph import build_graph

async def run_agent(payload: dict):
    graph = build_graph(lambda state: {
        "output": f"Processed: {payload.get('input')}"
    })
    return graph.invoke({})
