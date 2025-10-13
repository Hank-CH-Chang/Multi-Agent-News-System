import uvicorn
import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz

# 核心元件
from core.a2a_bus import A2ABus
from core.mcp_registry import MCPRegistry
from core.llm_client import LLMClient
from core import config

# Agents
from agents.commander_agent import CommanderAgent
from agents.crawler_agent import CrawlerAgent
# from agents.summarizer_agent import SummarizerAgent
from agents.classifier_agent import ClassifierAgent
from agents.ranker_agent import RankerAgent
from agents.storage_agent import StorageAgent

# --- 1. 初始化應用程式與核心服務 ---
app = FastAPI(title="Multi-Agent News System", version="1.0")
templates = Jinja2Templates(directory="templates")

# 初始化核心服務
llm_client = LLMClient(model=config.LLM_MODEL, api_key=config.GEMINI_API_KEY)
a2a_bus = A2ABus()
mcp_registry = MCPRegistry()

# --- 2. 實例化並註冊所有 Agents ---
print("[System] Initializing and registering agents...")

# 實例化所有 agent
commander_agent = CommanderAgent(a2a_bus)
crawler_agent = CrawlerAgent(a2a_bus, llm_client)
classifier_agent = ClassifierAgent(llm_client)
ranker_agent = RankerAgent(llm_client)
storage_agent = StorageAgent(storage_path="data/news_storage.json")

# 修正：使用 Agent 內部呼叫時的 'snake_case' 名稱進行註冊
# 這些名稱必須與 agent 程式碼中 a2a_bus.send() 裡的接收者名稱完全匹配
agents_to_register = {
    "commander_agent": commander_agent,
    "crawler_agent": crawler_agent,
    "classifier_agent": classifier_agent,
    "ranker_agent": ranker_agent,
    "storage_agent": storage_agent
}

# 註冊到 A2A Bus 和 MCP Registry
for name, agent_instance in agents_to_register.items():
    a2a_bus.register(name, agent_instance)
    mcp_registry.register(name, agent_instance)
    print(f"- Agent '{name}' registered.")

print("[System] All agents are ready.")

# --- 3. 定義 API 端點 ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    提供系統狀態儀表板或新聞前端頁面。
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/run-pipeline", status_code=202)
async def run_pipeline(topic: str = "科技"):
    """
    手動觸發一次完整的新聞處理流程。
    """
    print(f"[API] Manual pipeline run triggered for topic: '{topic}'")
    commander = mcp_registry.get("commander_agent")
    if not commander:
        raise HTTPException(status_code=500, detail="CommanderAgent not found.")
    
    # Since the pipeline can be long-running, run it in the background
    asyncio.create_task(asyncio.to_thread(commander.start_pipeline, topic))
    return {"status": "success", "message": f"Pipeline started for topic '{topic}'."}

@app.get("/api/news")
async def get_news(sort_by: str = "latest"):
    """
    從儲存中獲取新聞列表 (latest 或 popular)。
    """
    storage = mcp_registry.get("storage_agent")
    if not storage:
        raise HTTPException(status_code=500, detail="StorageAgent not found.")
    
    if sort_by not in ["latest", "popular"]:
        raise HTTPException(status_code=400, detail="Invalid sort_by parameter. Use 'latest' or 'popular'.")

    news_list = await storage.get_sorted(sort_by=sort_by)
    return {"status": "success", "count": len(news_list), "articles": news_list}

@app.get("/api/agents")
async def list_registered_agents():
    """
    列出所有已註冊的 agent。
    """
    return {"status": "success", "agents": mcp_registry.list_agents()}

# --- 4. 設定排程任務 ---
async def scheduled_news_pipeline_job():
    """
    排程執行的任務，會觸發 CommanderAgent。
    """
    print(f"[Scheduler] Triggering scheduled news pipeline job...")
    commander = mcp_registry.get("commander_agent")
    try:
        default_topic = "人工智慧"
        # Run the synchronous pipeline function in a separate thread
        await asyncio.to_thread(commander.start_pipeline, default_topic)
        print(f"[Scheduler] Successfully completed job for topic '{default_topic}'.")
    except Exception as e:
        print(f"[Scheduler] Error during scheduled job: {e}")

scheduler = AsyncIOScheduler(timezone=pytz.timezone(config.SCHEDULER_TIMEZONE))

# --- 5. FastAPI 生命週期事件 ---
@app.on_event("startup")
async def startup_event():
    """
    應用程式啟動時執行的任務。
    """
    print("[System] Application starting up...")
    scheduler.add_job(
        scheduled_news_pipeline_job, 
        "cron", 
        hour=config.SCHEDULER_HOUR, 
        minute=config.SCHEDULER_MINUTE
    )
    scheduler.start()
    print(f"[Scheduler] Job scheduled daily at {config.SCHEDULER_HOUR}:{config.SCHEDULER_MINUTE:02d} ({config.SCHEDULER_TIMEZONE}).")
    
    print("[System] Performing an initial run on startup...")
    asyncio.create_task(scheduled_news_pipeline_job())


@app.on_event("shutdown")
async def shutdown_event():
    """
    應用程式關閉時執行的任務。
    """
    print("[System] Application shutting down...")
    scheduler.shutdown()
    print("[Scheduler] Shutdown complete.")

# --- 6. 執行應用程式 ---
if __name__ == "__main__":
    print(f"[System] Starting Uvicorn server on {config.APP_HOST}:{config.APP_PORT}")
    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT)
