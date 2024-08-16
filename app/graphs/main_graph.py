from langgraph.graph import StateGraph, END
from ..schemas.state import State, RouterOutput
from ..services.router import service_router
from .worker_subgraph import create_worker_subgraph

def create_main_graph():
    main_graph = StateGraph(State)
    
    main_graph.add_node("service_router", service_router)
    
    services = ["accounts", "cards", "parking", "legal_assistant"]
    for service in services:
        main_graph.add_node(service, create_worker_subgraph(service))

    main_graph.set_entry_point("service_router")

    def route_to_service(state: State) -> RouterOutput:
        return RouterOutput(service=state.service)

    main_graph.add_conditional_edges(
        "service_router",
        route_to_service,
        {service: service for service in services}
    )

    for service in services:
        main_graph.add_edge(service, END)

    return main_graph.compile()