# core/config.py
import os
from datetime import timedelta

# === LLM 設定 ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDGA-n3UxeFf_gBiu0FB3xLYF97s04hQ8c")
LLM_MODEL = "gemini-2.5-flash"  # 預設模型，可改成 gemini-1.5-pro / flash

# === Database ===
DB_PATH = os.path.join("database", "news.db")

# === Logging ===
LOG_LEVEL = "INFO"

# === 排程設定 ===
# 例如每日早上 9:00（台北時間）
SCHEDULER_TIMEZONE = "Asia/Taipei"
SCHEDULER_HOUR = 9
SCHEDULER_MINUTE = 0

# === MCP & Agent 名稱設定 ===
AGENT_NAMES = {
    "crawler": "CrawlerAgent",
    "summarizer": "SummarizerAgent",
    "classifier": "ClassifierAgent",
    "ranker": "RankerAgent",
    "commander": "CommanderAgent",
    "storage": "StorageAgent"
}

# === 網頁設定 ===
APP_HOST = "0.0.0.0"
APP_PORT = 8000

# === 其他設定 ===
MAX_NEWS_DISPLAY = 30
CACHE_EXPIRE_TIME = timedelta(hours=1)
