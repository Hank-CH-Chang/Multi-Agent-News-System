# core/tools.py
import feedparser
import requests
from urllib.parse import quote

def google_web_search(query: str) -> dict:
    """Performs a web search using the Google News RSS feed and returns the results.
    This tool is useful for finding information on the internet based on a query.
    
    Args:
        query: The search query to find information on the web.
        
    Returns:
        A dictionary containing the search results.
    """
    encoded_query = quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    
    try:
        feed = feedparser.parse(url)
        if feed.bozo:
            print(f"[google_web_search] Warning: Feed from {url} is not well-formed. Bozo reason: {feed.bozo_exception}")

        results = []
        session = requests.Session()
        for entry in feed.entries[:30]:
            final_url = entry.get("link", "#")
            try:
                # Follow redirect to get the final URL
                response = session.head(final_url, allow_redirects=True, timeout=10)
                # Check for a successful status code
                if response.status_code == 200:
                    final_url = response.url
                else:
                    print(f"[google_web_search] Warning: Received status code {response.status_code} for {final_url}")
            except requests.RequestException as e:
                print(f"[google_web_search] Warning: Could not resolve final URL for {final_url}. Error: {e}")

            results.append({
                "title": entry.get("title", "No Title"),
                "link": final_url, # Use the resolved, final URL
                "summary": entry.get("summary", "No Summary"),
                "published": entry.get("published", "No Date"),
                "source": entry.source.get("title") if hasattr(entry, 'source') else "Unknown Source"
            })
        
        if not results:
            return {"results": "No articles found for the query."}
            
        return {"results": results}
    except Exception as e:
        print(f"[google_web_search] An unexpected error occurred: {e}")
        return {"results": f"An error occurred while trying to fetch news: {e}"}
