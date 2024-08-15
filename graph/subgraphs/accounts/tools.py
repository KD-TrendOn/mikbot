from langchain_core.tools import tool

@tool
def transfer_money(amount: float, to_account: str) -> str:
    return f"Button: Transfer {amount} to {to_account}"

tools=[transfer_money]