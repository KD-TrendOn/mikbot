import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .database.connection import get_db
from .graphs.main_graph import create_main_graph
from .schemas.state import State, UserInput

app = FastAPI()

main_graph = create_main_graph()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.post("/chat")
async def chat(user_input: UserInput, db: AsyncSession = Depends(get_db)):
    try:
        initial_state = State(
            user_input=user_input.user_input,
            user_id=user_input.user_id,
            metadata={"db": db}
        )
        logger.debug(f"Initial state: {initial_state}")
        
        result = await main_graph.ainvoke(initial_state)
        return result
    except Exception as e:
        logger.exception("An error occurred during chat processing")
        raise HTTPException(status_code=500, detail=str(e))

# Удалите эту функцию, так как она больше не нужна
# @app.on_event("startup")
# async def startup_event():
#     loop = asyncio.get_event_loop()
#     asyncio.set_event_loop(loop)
