import os, logging, sys, traceback
from datetime import datetime
from fastapi import FastAPI, Request, Response, status
from typing import Optional
from pydantic import BaseModel
from store import ingest_doc as save_result
from dotenv import load_dotenv

load_dotenv()

from fetch import get_data_raw

class GetRelevantDocumentParams(BaseModel):
    query: str
    agent_id: str
    session_id: str
    top_k: Optional[int] = 5
    threshold: Optional[float] = 0.7
    created_at: Optional[str] = None

class SaveExecutionResultParams(BaseModel):
    agent_id: str
    session_id: str
    strategy: str
    strategy_data: str
    reference_id: str
    created_at: Optional[str] = None

app = FastAPI()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('📡 RAG API is starting up...')

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

def now():
    return datetime.utcnow().isoformat()

@app.post('/relevant_strategy_raw')
async def get_relevant_document_raw(params: GetRelevantDocumentParams):
    try:
        data = get_data_raw(
            query=params.query,
            agent_id=params.agent_id,
            session_id=params.session_id,
            top_k=params.top_k,
            threshold=params.threshold,
            created_at=params.created_at,
        )
        msg = 'Relevant strategy found' if data else 'No relevant strategy found'
        return {'status': 'success', 'data': data, "msg": msg}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@app.post('/save_result')
async def store_execution_result(params: SaveExecutionResultParams):
    try:
        created_at = params.created_at or now()
        output = save_result(
            strategy=params.strategy,
            reference_id=params.reference_id,
            strategy_data=params.strategy_data,
            agent_id=params.agent_id,
            session_id=params.session_id,
            created_at=created_at,
        )
        return {'status': 'success', 'message': output}
    except Exception as e:
        return {'status': 'error', 'message': f'Error: {str(e)}'}

@app.post('/save_result_batch')
async def store_execution_result_batch(request: Request):
    try:
        items = await request.json()
        for item in items:
            output = save_result(
                strategy=item["strategy"],
                reference_id=item["reference_id"],
                strategy_data=item["strategy_data"],
                agent_id=item["agent_id"],
                session_id=item["session_id"],
                created_at=item.get("created_at") or now()
            )
        return {'status': 'success', 'message': 'Batch saved successfully'}
    except Exception as e:
        print(f"Error: {traceback.format_exc()}")
        return {'status': 'error', 'message': f'Error: {str(e)}'}
