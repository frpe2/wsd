import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import common, admin
from database.models import Base
from database.db import engine

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    print("STARTING BOT...")  # 👈 добавь

    await init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(common.router)
    dp.include_router(admin.router)

    print("BOT STARTED")  # 👈 добавь

    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())