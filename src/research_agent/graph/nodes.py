from langgraph.types import Send
from ..core.state import ResearchState, SubQuery,SearchResult
from ..agents.decomposition_agent import DecomposeQuery
from ..agents.citation_agent import extract_citations
from ..agents.synthesis_agent import synthesize_report
from ..tools.tavily_search import tavily_search
from ..tools.faiss_retriever import faiss_retrieve
from ..core.config import get_settings
import logging

logger = logging.getLogger(__name__)

# Node 1 : Decompose the original query 

def node_compose(state:ResearchState) -> dict:
    logger.info("Decomposing the query")
    s = get_settings()
    sub_queries = DecomposeQuery(state['original_query'],
                                    max_queries=s.max_sub_queries)
    return {"sub_queries": sub_queries, 'status': 'searching'}

# Node 2 : WebSearch for one sub query

def node_web_search(sub_query:SubQuery) -> dict:
    results = tavily_search(sub_query_id=  sub_query['id'],
                            query_text=sub_query['text'],
    )

    return {"web_results": results}
# Node 3: Document retrieval for one sub query 

def node_doc_retrieval(sub_query:SubQuery) -> dict:
    results = faiss_retrieve(sub_query_id=sub_query['id'],
                            query_text=sub_query['text'],
    )
    return {"doc_results": results}

# Node 4: Merge and deduplicate results

def node_merge_results(state:ResearchState) -> dict:
    all_results = state.get('web_results',[]) + state.get('doc_results',[])
    # Deduplicate by source URL
    seen = set()
    unique = []
    for r in sorted(all_results, key=lambda x: -x['relevance_score']):
        if r['source'] not in seen:
            seen.add(r['source'])
            unique.append(r)
    return {"combined_results": unique[:20]}

# Node 5 : Extract and validate citations

def node_extract_citations(state:ResearchState) -> dict:
    citations = extract_citations(state['combined_results'])
    return {"citations": citations}

# Node 6 :  Synthesize final report

def node_synthesize(state:ResearchState) -> dict:
    report = synthesize_report(state['original_query'],
                            combined_results=state['combined_results'],
                            citations=state['citations'])
    return {"final_report": report, "status": "complete"}

# Fan Out Edge: Return send objects for each sub query

def edge_fan_out_web(state:ResearchState) -> list[Send]:
    return [Send('web_search', sub_query) for sub_query in state['sub_queries']]

def edge_fan_out_doc(state:ResearchState) -> list[Send]:
    return [Send('doc_retrieval', sub_query) for sub_query in state['sub_queries']]
                
    
        

    

