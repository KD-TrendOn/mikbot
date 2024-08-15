__all__ = (
    "accounts_subgraph",
    "cards_subgraph",
    "parking_subgraph"
)

from .subgraph_construct import create_worker_subgraph
from .accounts import name as accounts_name, tools as accounts_tools
from .cards import name as cards_name, tools as cards_tools
from .parking import name as parking_name, tools as parking_tools
accounts_subgraph = create_worker_subgraph(accounts_name, accounts_tools)
cards_subgraph = create_worker_subgraph(cards_name, cards_tools)
parking_subgraph = create_worker_subgraph(parking_name, parking_tools)