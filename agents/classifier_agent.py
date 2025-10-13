# agents/classifier_agent.py
from core.llm_client import LLMClient

class ClassifierAgent:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def classify(self, title: str, summary: str) -> str:
        """Classifies an article based on its title and summary."""
        print(f"[ClassifierAgent] Classifying: {title}")
        prompt = f"Please classify the following news article into one of these categories: Politics, Technology, Sports, Finance, Entertainment, World, Health.\n\nTitle: {title}\nSummary: {summary}"
        
        # The LLM might return extra text, so we try to find the category from a list.
        raw_classification = self.llm.chat(prompt)
        categories = ["Politics", "Technology", "Sports", "Finance", "Entertainment", "World", "Health"]
        for cat in categories:
            if cat.lower() in raw_classification.lower():
                return cat
        return "General"

    def receive(self, article_info: dict) -> str:
        """Receives a dictionary with 'title' and 'summary' to start classification."""
        print(f"[ClassifierAgent] Received classification task...")
        title = article_info.get('title')
        summary = article_info.get('summary')
        if not title or not summary:
            return "Error: Title or summary missing."
        return self.classify(title, summary)