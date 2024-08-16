import asyncio
from app.main import app
from app.database.connection import AsyncSessionLocal
from app.test_data import init_test_data
import uvicorn

async def init_data():
    async with AsyncSessionLocal() as db:
        await init_test_data(db)

async def main():
    await init_data()
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
