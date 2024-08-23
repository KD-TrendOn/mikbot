import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .database.connection import get_db
from .graphs.main_graph import create_main_graph
from .schemas.state import State, UserInput
import json
from langchain_core.messages import ToolMessage
from .database.crud import create_chat_message
from .services.router import update_router_parser
app = FastAPI()
main_graph = None

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    global main_graph
    db = next(get_db())
    await update_router_parser(db)
    main_graph = await create_main_graph(db)

@app.post("/chat")
async def chat(user_input: UserInput, db: AsyncSession = Depends(get_db)):
    try:
        # Сохраняем сообщение пользователя
        await create_chat_message(db, user_input.user_id, "user", {"message": user_input.user_input})

        initial_state = State(
            user_input=user_input.user_input,
            user_id=user_input.user_id,
            metadata={"db": db}
        )
        
        result = await main_graph.ainvoke(initial_state)
        
        # Обработка результата
        pre_answer = result['answer'][0]
        if isinstance(pre_answer, ToolMessage):
            answer = json.loads(pre_answer.content)
            # Сохраняем ответ бота
            await create_chat_message(db, user_input.user_id, "bot", {
                "service": result.get('service'),
                "type": answer.get('result')[0],
                "tool_call": answer.get('result')[1],
                "message": answer.get('description')
            })
            return {
                "tool_call": answer.get('result'),
                "type": answer.get('result')[0],
                "message": answer.get('description')
            }
        else:
            answer = pre_answer.content
            await create_chat_message(db, user_input.user_id, "bot", {
                "service": result.get('service'),
                "message": answer
            })
            return {
                "tool_call": {},
                "type":'text',
                "message": answer
            }
    except Exception as e:
        logger.exception("An error occurred during chat processing")
        raise HTTPException(status_code=500, detail=str(e))
