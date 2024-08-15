from langchain_core.tools import tool
@tool
def book_parking(hours: int) -> str:
    """_summary_

    Args:
        hours (int): _description_

    Returns:
        str: _description_
    """
    return f"Button: Book parking for {hours} hours"


@tool
def pay_parking(amount: float) -> str:
    """_summary_

    Args:
        amount (float): _description_

    Returns:
        str: _description_
    """
    return f"Button: Pay {amount} for parking"

tools = [book_parking, pay_parking]