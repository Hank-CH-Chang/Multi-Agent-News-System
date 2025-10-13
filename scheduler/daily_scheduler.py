# scheduler/daily_scheduler.py
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from core.a2a_bus import bus

async def run_daily_job():
    print(f"[Scheduler] Triggered at {datetime.now()}")
    await bus.call("commander", {})

def start_scheduler():
    tz = pytz.timezone("Asia/Taipei")
    scheduler = AsyncIOScheduler(timezone=tz)
    scheduler.add_job(run_daily_job, "cron", hour=9, minute=0)
    scheduler.start()
    print("[Scheduler] Running daily at 9:00 AM Taipei time")
