# agents/ranker_agent.py
from core.llm_client import LLMClient
from typing import List, Dict
import json

class RankerAgent:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def rank(self, titles: List[str]) -> Dict[int, int]:
        """Ranks a list of article titles and returns a mapping of index to score."""
        print(f"[RankerAgent] Ranking {len(titles)} titles...")
        if not titles:
            return {}

        titles_for_prompt = "\n".join([f"{i+1}. {title}" for i, title in enumerate(titles)])

        prompt = f"""Based on the following list of news titles, please evaluate the potential popularity of each on a scale from 0 to 100. Consider factors like public interest, impact, and keyword relevance. Your response MUST be a JSON array of objects, where each object has 'id' (the original number) and 'score' (0-100).

Titles:
{titles_for_prompt}

Example JSON response: [{{"id": 1, "score": 85}}, {{"id": 2, "score": 60}}]"""

        try:
            response_text = self.llm.chat(prompt)
            json_part = response_text[response_text.find('['):response_text.rfind(']')+1]
            scores = json.loads(json_part)
            
            score_map = {item['id']: item['score'] for item in scores}
            print("[RankerAgent] Successfully ranked titles.")
            return score_map
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[RankerAgent] Error parsing LLM response for ranking: {e}. Returning empty scores.")
            return {{}}

    def receive(self, titles: List[str]) -> Dict[int, int]:
        """Receives a list of titles to start the ranking process."""
        print(f"[RankerAgent] Received ranking task...")
        return self.rank(titles)
