from langgraph.graph import StateGraph

def build_graph(agent_node):
    graph = StateGraph(dict)
    graph.add_node("agent", agent_node)
    graph.set_entry_point("agent")
    return graph.compile()
