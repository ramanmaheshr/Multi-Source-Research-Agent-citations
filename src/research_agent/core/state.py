from ast import operator
from ast import Str
from typing import TypedDict, Annotated, Optional
from langgraph.graph.message import add_messages
import operator

class SubQuery(TypedDict):
    id:str
    text:str
    topic_area:str

class SearchResult(TypedDict):
    source:str #url
    title:str
    excerpt:str
    relevance_score:float
    sub_query_id:str

class Citation(TypedDict):
    id:str 
    url:str
    title:str
    excerpt:str
    relevance_score:float

class ResearchState(TypedDict):
    #input
    original_query:str
    session_id:str
    
    #Decomposition
    sub_queries:list[SubQuery]
    #parallel results
    web_results: Annotated[list[SearchResult],operator.add]
    doc_results: Annotated[list[SearchResult],operator.add]
    #post processing
    combined_results: list[SearchResult]
    citations:list[Citation]

    #output
    synthesized_findings:str
    final_report:str
    status:str # pending | searching | synthesizing | complete | error
    error_message:Optional[str]
    
    