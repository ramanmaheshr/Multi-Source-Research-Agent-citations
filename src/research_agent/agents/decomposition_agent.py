from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel,Field
from ..core.llm import get_llm
from ..core.state import SubQuery
import uuid

class DecomposeQuery(BaseModel):
    sub_queries:list[dict] = Field(description="List of focused sub queries")

Decompose_prompt = ChatPromptTemplate.from_messages([
    ('system', """You are a research strategist. 
                Break the user query into 3-7 focused sub-queries that together
                answer it comprehensively. 
                Return JSON only: 
                {"sub_queries": [{"id": "sq_1", "text": "...",
                 "focus_area": "market_data|technical|competitive|regulatory"}, ...]}"""),
    ('human', 'Research query: {query} Max sub-queries: {max_queries}')
])

def decompose_query(query:str, max_queries: int = 5) -> list[SubQuery]:
    llm = get_llm(temperature=0.0)
    parser = JsonOutputParser(pydantic_object=DecomposeQuery)
    chain = Decompose_prompt | llm | parser
    response = chain.invoke({"query":query, "max_queries":max_queries})
    return [SubQuery(
        id=str(uuid.uuid4()),
        text=sq["text"],
        topic_area=sq.get("focus_area", "general")
    ) for sq in response.get("sub_queries", [])]
    

