from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from ..core.state import ResearchState, SubQuery
from ..core.config import get_settings
from .nodes import (node_compose, 
                    node_web_search, 
                    node_doc_retrieval, 
                    node_merge_results, 
                    node_extract_citations, 
                    node_synthesize, 
                    edge_fan_out_web, 
                    edge_fan_out_doc)
import sqlite3


#Building the graph 

def build_research_graph():
    s = get_settings()
    builder = StateGraph(ResearchState)
    
    # Add nodes
    builder.add_node("decompose", node_compose)
    builder.add_node("web_search", node_web_search)
    builder.add_node("doc_retrieval", node_doc_retrieval)
    builder.add_node("merge_results", node_merge_results)
    builder.add_node("extract_citations", node_extract_citations)
    builder.add_node("synthesise", node_synthesize)

    #wiring edges
    builder.set_entry_point('decompose')
    #conditional edges
    builder.add_conditional_edges(
        'decompose', edge_fan_out_web,['web_search'])
    
    builder.add_conditional_edges('decompose',edge_fan_out_doc,['doc_retrieval'])

    #Fan in 
    builder.add_edge('web_search', 'merge_results')
    builder.add_edge('doc_retrieval', 'merge_results')
    builder.add_edge('merge_results', 'extract_citations')
    builder.add_edge('extract_citations', 'synthesise')
    builder.add_edge('synthesise', END)

    #SQLite Checkpoint
    conn = sqlite3.connect(s.sqlite_db_path,check_same_thread=False)
    saver = SqliteSaver(conn)
    return builder.compile(checkpointer=saver)

# Module level singleton
_GRAPH = None
def get_graph():
    global _GRAPH
    if _GRAPH is None:
        _GRAPH = build_research_graph()
    return _GRAPH
    


