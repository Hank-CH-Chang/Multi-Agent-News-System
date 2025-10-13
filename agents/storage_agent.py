
# agents/storage_agent.py
from typing import List, Dict
import json
import asyncio
import aiofiles
from pathlib import Path
from typing import List, Dict
from core.news_article import NewsArticle

class StorageAgent:
    def __init__(self, storage_path: str = "data/news_storage.json"):
        self.storage_path = Path(storage_path)
        self._lock = asyncio.Lock()
        
        # Create directory if it doesn't exist
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Synchronously check and create the file if it's missing on startup
        if not self.storage_path.exists():
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    async def receive(self, articles: List[NewsArticle]):
        """
        Asynchronously receives a list of processed NewsArticle objects and saves them.
        This will overwrite the existing file with the new list.
        """
        print(f"[StorageAgent] Received {len(articles)} articles to store.")
        await self._write(articles)
        print(f"[StorageAgent] Successfully saved articles.")
        return {"status": "saved", "count": len(articles)}

    async def load_all(self) -> List[Dict]:
        """Asynchronously loads all articles from the JSON file."""
        async with self._lock:
            try:
                async with aiofiles.open(self.storage_path, 'r', encoding='utf-8') as f:
                    content = await f.read()
                    return json.loads(content)
            except (FileNotFoundError, json.JSONDecodeError):
                return []

    async def get_sorted(self, sort_by: str = "latest") -> List[Dict]:
        """Asynchronously loads and sorts articles from storage."""
        articles = await self.load_all()
        
        # The sorting logic itself is CPU-bound and fast, so no need for async here.
        if sort_by == "popular":
            return sorted(articles, key=lambda x: x.get("popularity", 0), reverse=True)
        else:  # 'latest'
            return sorted(articles, key=lambda x: x.get("timestamp", 0), reverse=True)

    async def _write(self, articles: List[NewsArticle]):
        """Asynchronously writes the list of articles to the JSON file."""
        articles_as_dicts = [article.model_dump() for article in articles]
        async with self._lock:
            async with aiofiles.open(self.storage_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(articles_as_dicts, ensure_ascii=False, indent=2))

