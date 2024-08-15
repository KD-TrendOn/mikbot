from langchain_core.tools import tool
@tool
def reissue_card() -> str:
    """_summary_

    Returns:
        str: _description_
    """
    return "Button: Reissue card"

tools = [reissue_card]