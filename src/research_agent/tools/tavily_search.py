from tavily import TavilyClient
from ..core.config import get_settings
from ..core.state import SearchResult
import logging, uuid

logger = logging.getLogger(__name__)

def tavily_search(sub_query_id:str, query_text:str) -> list[SearchResult]:
    s = get_settings()
    client = TavilyClient(api_key=s.tavily_api_key)
    try:
        resp = client.search(
            query = query_text,
            max_results = s.tavily_max_results,
            include_raw_content = False 
        )
        return [
        SearchResult(
            source=article.get("url","No URL"),
            title=article.get("title","No Title"),
            excerpt=article.get("content","No Content")[:500],
            relevance_score=float(article.get("score",0.0)),
            sub_query_id=sub_query_id
        )
        for article in resp.results
    ]
    except Exception as e:
        logger.error(f"Tavily search failed: {e}")
        return []