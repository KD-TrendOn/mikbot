import asyncio
from app.main import app, startup_event
from app.database.connection import AsyncSessionLocal
from app.services.service_creator import init_real_services
import uvicorn

async def init_data():
    async with AsyncSessionLocal() as db:
        await init_real_services(db)
    await startup_event()

async def main():
    await init_data()
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
