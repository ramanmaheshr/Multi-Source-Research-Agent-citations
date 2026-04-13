from langchain_core.prompts import ChatPromptTemplate
from ..core.llm import get_llm
from ..core.config import get_settings
from ..core.state import SearchResult, Citation
import json 

SYNTHESIS_PROMPT = ChatPromptTemplate.from_messages([
('system', '''You are an expert research analyst.
Write a comprehensive research report based on the provided evidence.
FORMAT RULES:
- Use Markdown headings (##, ###)
- Cite sources inline as [Source Title](url) after each claim
- Include an Executive Summary (3-5 sentences) at the top
- Conclude with Key Takeaways bullet points
- Do NOT invent facts not found in the provided results'''),
('human', '''
ORIGINAL QUERY: {query}
RESEARCH RESULTS:
{results_json}
CITATIONS:
{citations_json}
Write the research report now:'''
),
])

def synthesise_report(original_query:str, 
                        combined_results:list[SearchResult], 
                        citations:list[Citation]) -> str:
    llm = get_llm(temperature=0.3)
    chain  = SYNTHESIS_PROMPT | llm
    result = chain.invoke(
        {
            'query': original_query,
            'results_json': json.dumps(combined_results[:12],indent = 2),
            'citations_json': json.dumps(citations[:10],indent = 2)
        }
    )
    return result.content
    
    