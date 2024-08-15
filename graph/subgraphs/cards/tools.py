from langchain_core.tools import tool
@tool
def reissue_card() -> str:
    return "Button: Reissue card"

tools = [reissue_card]