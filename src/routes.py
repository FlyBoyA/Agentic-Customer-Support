from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging
from .models import QueryRequest, QueryResponse, HealthResponse, StatsResponse
from .decision_engine import DecisionEngine, DecisionType
from .vector_store import VectorStore
from .config import CONFIG

logger = logging.getLogger(__name__)

_decision_engine: DecisionEngine = None
_vector_store: VectorStore = None

def get_decision_engine() -> DecisionEngine:
    if _decision_engine is None:
        raise RuntimeError("Decision engine not initialized")
    return _decision_engine

def get_vector_store() -> VectorStore:
    if _vector_store is None:
        raise RuntimeError("Vector store not initialized")
    return _vector_store

def initialize(decision_engine: DecisionEngine, vector_store: VectorStore):
    global _decision_engine, _vector_store
    _decision_engine = decision_engine
    _vector_store = vector_store

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    try:
        count = _vector_store.count() if _vector_store else 0
        return HealthResponse(status="healthy", vector_store_count=count, version="1.0.0")
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(status="unhealthy", vector_store_count=0, version="1.0.0")

@router.get("/stats", response_model=StatsResponse)
async def get_stats() -> StatsResponse:
    try:
        return StatsResponse(
            total_documents=_vector_store.count(),
            categories=["Account", "Billing", "Integrations", "Data & Security"],
            embedding_model=CONFIG.model.embedding_model,
            vector_store_type="ChromaDB"
        )
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask", response_model=QueryResponse)
async def ask_question(
    request: QueryRequest,
    engine: DecisionEngine = Depends(get_decision_engine)
) -> QueryResponse:
    try:
        decision = engine.process(request.question)
        
        response = QueryResponse(
            response=decision.response,
            action=decision.type.value
        )
        
        if decision.type == DecisionType.ANSWER:
            response.confidence = decision.confidence
            response.source = decision.source
            response.category = decision.category
        elif decision.type == DecisionType.CLARIFY:
            response.suggested_topics = decision.metadata.get('suggested_topics') if decision.metadata else None
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process question: {str(e)}")

@router.post("/reset")
async def reset_agent():
    return {"message": "Agent reset successfully"}

@router.get("/status")
async def get_status():
    try:
        return {
            "status": "operational",
            "vector_store_count": _vector_store.count() if _vector_store else 0,
            "config": {
                "embedding_model": CONFIG.model.embedding_model,
                "llm_model": CONFIG.model.llm_model,
                "similarity_threshold": CONFIG.agent.similarity_threshold
            }
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}