from pydantic import BaseModel, Field
from typing import Optional

class ResearchRequest(BaseModel):
    query: str = Field(..., description="The research question to investigate",
                        min_length=10,
                        max_length=500)

class ResearchResponse(BaseModel):
    session_id:str
    status:str # pending, searching, synthesising, complete, error
    final_report: Optional[str] = None
    citations: Optional[list[dict]] = None
    error: Optional[str] = None
    