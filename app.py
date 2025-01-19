from bot import (
    bot,
    dp,
    main_router,
    product_router,
    redis,
    purchases_router
)
from db.models import Base, engine

import asyncio


async def start_redis():
    await redis.ping()


async def start_bot():
    Base.metadata.create_all(engine)

    dp.include_routers(main_router, product_router, purchases_router)
    asyncio.create_task(start_redis())
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start_bot())
