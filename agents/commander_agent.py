
# agents/commander_agent.py
from typing import List
from core.a2a_bus import A2ABus
from core.news_article import NewsArticle

class CommanderAgent:
    def __init__(self, a2a_bus: A2ABus):
        self.a2a_bus = a2a_bus

    def start_pipeline(self, topic: str):
        print(f"[CommanderAgent] Pipeline started for topic: '{topic}'")

        # 1. Crawl for raw articles
        raw_articles = self.a2a_bus.send("commander_agent", "crawler_agent", topic)
        if not raw_articles:
            print("[CommanderAgent] Pipeline stopped: No articles found.")
            return {"status": "failed", "reason": "No articles found"}

        # 2. Process each article (the crawler now also provides a summary)
        processed_articles: List[NewsArticle] = []
        for i, raw_article in enumerate(raw_articles):
            print(f"--- Processing article {i+1}/{len(raw_articles)}: {raw_article['title']} ---")
            
            # The raw_article from the new crawler already contains the summary
            article = NewsArticle(
                title=raw_article['title'],
                url=raw_article['url'],
                source=raw_article.get('source'),
                summary=raw_article.get('summary', 'No summary available.') # Get summary from crawler
            )

            # The summarizer agent is no longer needed.
            # summary = self.a2a_bus.send(...)
            # article.summary = summary

            category = self.a2a_bus.send(
                sender="commander_agent", 
                receiver="classifier_agent", 
                message={"title": article.title, "summary": article.summary}
            )
            article.category = category
            
            article.image = f"https://picsum.photos/seed/{article.id}/400/300"

            processed_articles.append(article)
            print(f"--- Finished processing article {i+1} ---")

        # 3. Rank the collected articles
        titles_to_rank = [article.title for article in processed_articles]
        score_map = self.a2a_bus.send("commander_agent", "ranker_agent", titles_to_rank)

        if score_map:
            for i, article in enumerate(processed_articles):
                # The ID from the ranker prompt is 1-based
                article.popularity = score_map.get(str(i + 1), 0) # Ensure key is string if needed

        # 4. Store the final list
        result = self.a2a_bus.send("commander_agent", "storage_agent", processed_articles)

        print(f"[CommanderAgent] Pipeline finished successfully. {len(processed_articles)} articles processed and stored.")
        return result

