import asyncio

from aiogram import Bot, Dispatcher

from config import TOKEN
from app.handlers import router

async def main() -> None:
    bot = Bot(TOKEN)
    dp = Dispatcher()

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
