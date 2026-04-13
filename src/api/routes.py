from fastapi import APIRouter, BackgroundTasks, HTTPException
from .schemas import ResearchRequest, ResearchResponse
from ..graph.builder import get_graph
from ..core.state import ResearchState
import uuid, asyncio

router = APIRouter()

_sessions:dict[str, dict] = {}

@router.post("/research", response_model=ResearchResponse,status_code=202)
async def start_research(req:ResearchRequest, bg:BackgroundTasks):
    session_id = str(uuid.uuid4())
    _sessions[session_id] = {"status":"pending"}
    bg.add_task(_run_research,session_id,req.query)
    return ResearchResponse(session_id=session_id,status="pending")

@router.get("/status/{session_id}",response_model=ResearchResponse)
async def get_research(session_id:str):
    if session_id not in _sessions:
        raise HTTPException(status_code=404,detail="Session not found")
    state = _sessions[session_id]
    return ResearchResponse(session_id=session_id,status=state.get("status","unknown"),
                            final_report=state.get("final_report"),
                            citations=state.get("citations"),
                            error=state.get("error"))

async def _run_research(session_id:str,query:str):
    _sessions[session_id]["status"] = "searching"
    try:
        graph = get_graph()
        config = {'configurable':{'thread_id':session_id}}
        init_state = ResearchState(
            original_query=query,
            session_id=session_id,
            sub_queries=[],
            web_results=[],
            doc_results=[],
            combined_results=[],
            citations=[],
            synthesized_findings='',
            final_report='',
            status='pending',
            error_message=None,
        )
        final = await asyncio.to_thread(
            graph.invoke, init_state, config
        )
        _sessions[session_id].update({
            'status': 'complete',
            'final_report': final['final_report'],
            'citations': final['citations'],
        })
    except Exception as e:
        _sessions[session_id].update({'status': 'error', 'error': str(e)})
    
    

    
    


