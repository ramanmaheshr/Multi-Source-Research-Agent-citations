from .document_loader import load_vector_store
from ..core.state import SearchResult
import logging

logger = logging.getLogger(__name__)
_store = None

def _get_store():
    global _store
    if _store is None:
        _store = load_vector_store()
    return _store

def faiss_retrieve(sub_query_id:str,query_text:str,top_k:int = 3) -> list[SearchResult]:
    try: 
        store = _get_store()
        docs = store.similarity_search_with_score(query_text,k=top_k)
        return [
            SearchResult(
                source=doc.metadata.get("source","internal_doc"),
                title=doc.metadata.get("title","Internal Document"),
                excerpt=doc.page_content[:500],
                relevance_score=max(0.0,1.0-score),
                sub_query_id=sub_query_id
            )
            for doc,score in docs
        ]
    except Exception as e:
        logger.error(f"Faiss retrieval failed: {e}")
        return []
        

    
