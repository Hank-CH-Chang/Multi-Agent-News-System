# agents/crawler_agent.py
import json
import re
from typing import List, Dict
from core.llm_client import LLMClient
from core.tools import google_web_search

class CrawlerAgent:
    def __init__(self, a2a_bus, llm_client: LLMClient):
        self.a2a_bus = a2a_bus
        self.llm = llm_client

    def crawl(self, topic: str, max_articles: int = 30) -> List[Dict[str, str]]:
        """
        Uses an LLM with a search tool to find and summarize news articles on a given topic.
        """
        print(f"[CrawlerAgent] Using LLM with search tool to find articles for topic: '{topic}'")

        prompt = f"""You are a news analyst. Your task is to find {max_articles} recent, significant news articles about '{topic}'.

You MUST use the provided search tool to find the news. Do not make up news.

For each article, you must provide:
1. The exact title of the article.
2. The full URL.
3. The source publication name.
4. A 3-sentence summary in Traditional Chinese.

**ACCURACY IS PARAMOUNT.** The URL, title, and source *must* come from the search tool. The summary must be based on the real article content. I will be checking your work.

After finding the articles, format the information into a single JSON response under the key "articles".
If you cannot find any relevant articles after searching, you MUST return a JSON object with an empty list for the "articles" key, like this: {{"articles": []}}

Example format for when articles are found:
{{
  "articles": [
    {{
      "title": "Verified News Title from Search",
      "url": "https://example.com/the-correct-url",
      "source": "Example News Outlet",
      "summary": "A three-sentence summary based on the content at the provided URL."
    }}
  ]
}}
"""

        try:
            response_text = self.llm.chat(prompt, tools=[google_web_search])
            
            # Use regex to find the JSON block more reliably
            json_match = re.search(r'```json\s*\n(.*?)\n\s*```', response_text, re.DOTALL)
            if not json_match:
                # Fallback for plain JSON without markdown
                json_match = re.search(r'({.*})', response_text, re.DOTALL)

            if not json_match:
                print(f"[CrawlerAgent] Error: No JSON object found in LLM response. Response: {response_text}")
                return []

            json_part = json_match.group(1).strip()
            
            data = json.loads(json_part)
            articles = data.get("articles", [])
            print(f"[CrawlerAgent] LLM with search found {len(articles)} articles.")
            return articles
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[CrawlerAgent] Error parsing LLM response for crawling: {e}. Response was: {response_text}")
            return []
        except Exception as e:
            print(f"[CrawlerAgent] An unexpected error occurred during LLM crawl: {e}")
            return []

    def receive(self, message: str) -> List[Dict[str, str]]:
        """
        Receives a topic and initiates the crawling process.
        """
        print(f"[CrawlerAgent] Received task: {message}")
        return self.crawl(message)
    