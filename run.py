import asyncio
from app.main import app
from app.database.connection import AsyncSessionLocal
from app.services.service_creator import init_real_services
import uvicorn


async def init_data():
    async with AsyncSessionLocal() as db:
        await init_real_services(db)


async def main():
    # await init_data()
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    import sys

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
