from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler: AsyncIOScheduler | None = None


async def get_scheduler() -> AsyncIOScheduler | None:
    return scheduler
