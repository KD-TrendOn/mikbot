from langchain_core.tools import tool
@tool
def book_parking(hours: int) -> str:
    return f"Button: Book parking for {hours} hours"


@tool
def pay_parking(amount: float) -> str:
    return f"Button: Pay {amount} for parking"

tools = [book_parking, pay_parking]