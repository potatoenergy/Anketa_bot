import asyncio

import handlers
from database import async_db_main
from loader import dp, bot
from middlewares import ThrottlingMiddleware
from utils import on_startup_notify


async def on_startup():
    dp.message.middleware(ThrottlingMiddleware())

    # message_routers = handlers.setup_message_routers()
    # dp.include_router(message_routers)
    await async_db_main()
    await on_startup_notify()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(on_startup())
