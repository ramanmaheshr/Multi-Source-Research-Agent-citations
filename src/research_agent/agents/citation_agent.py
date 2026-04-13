from ..core.state import SearchResult,Citation
from urllib.parse import urlparse, urlunparse
import uuid, hashlib


def _normalize_url(url:str) -> str:
    p = urlparse(url)
    # remove query params and fragments for dedup purpose
    return urlunparse((p.scheme,p.netloc,p.path,'','',''))

def extract_citations(results:list[SearchResult],
                        min_relevance:float = 0.3,
                        ) -> list[Citation]:
    '''
Deduplicate by normalised URL, filter by relevance threshold,
and return clean citations.
'''
    seen_urls = {}
    citations = []
    for r in sorted(results,key = lambda x: -x['relevance_score']):
        if r['relevance_score'] < min_relevance:
            continue
        norm = _normalize_url(r['source'])
        if norm in seen_urls:
            continue
        seen_urls[norm] = True
        cid = 'cit_' + hashlib.md5(norm.encode()).hexdigest()[:8]
        citations.append(
            Citation(
                id=cid,
                url=r['source'],
                title=r['title'],
                excerpt=r['excerpt'][:400],
                relevance_score= round(r['relevance_score'],2)
            )
        )
    return citations