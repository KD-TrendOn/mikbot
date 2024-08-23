from langgraph.graph import StateGraph, END
from ..schemas.state import State
from ..services.router import service_router
from .worker_subgraph import create_worker_subgraph
from ..database.crud import get_chat_history, get_all_services

async def load_chat_history(state: State):
    db = state.metadata.get("db")
    if db is None:
        raise ValueError("Database session is not available")
    
    history = await get_chat_history(db, state.user_id)
    return {"chat_history": history}

async def create_main_graph(db):
    main_graph = StateGraph(State)
    
    main_graph.add_node("load_chat_history", load_chat_history)
    main_graph.add_node("service_router", service_router)
    
    # Получаем все сервисы из базы данных
    services = await get_all_services(db)
    service_names = [service.name for service in services]
    
    for service_name in service_names:
        main_graph.add_node(service_name, create_worker_subgraph(service_name))

    main_graph.set_entry_point("load_chat_history")
    main_graph.add_edge("load_chat_history", "service_router")

    def route_to_service(state: State):
        return state.service if state.service in service_names else END

    main_graph.add_conditional_edges(
        "service_router",
        route_to_service,
        {service_name: service_name for service_name in service_names}
    )

    for service_name in service_names:
        main_graph.add_edge(service_name, END)

    return main_graph.compile()