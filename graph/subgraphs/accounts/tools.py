from langchain_core.tools import tool

@tool
def transfer_money(amount: float, to_account: str) -> str:
    """_summary_

    Args:
        amount (float): _description_
        to_account (str): _description_

    Returns:
        str: _description_
    """
    return f"Button: Transfer {amount} to {to_account}"

tools=[transfer_money]