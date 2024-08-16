from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database.connection import get_db
from .graphs.main_graph import create_main_graph
from .schemas.state import State

app = FastAPI()

main_graph = create_main_graph()

@app.post("/chat")
async def chat(state: State, db: Session = Depends(get_db)):
    try:
        result = await main_graph.ainvoke({}, {"db": db})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))