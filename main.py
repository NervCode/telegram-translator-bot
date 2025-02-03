import asyncio
from aiogram import Bot, Dispatcher
from config_example import TOKEN
from app.handlers import router

bot = Bot(TOKEN)
dp = Dispatcher()


async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
