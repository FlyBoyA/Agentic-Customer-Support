from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from pathlib import Path
from .config import CONFIG
from .vector_store import VectorStore
from .knowledge_base import load_knowledge_base
from .decision_engine import DecisionEngine
from .routes import router, initialize

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Customer Support Agent",
    description="Agentic RAG-based customer support assistant with decision-making",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def initialize_components():
    try:
        CONFIG.ensure_directories()
        
        logger.info("Loading knowledge base...")
        knowledge_base = load_knowledge_base(CONFIG.knowledge_base_path)
        logger.info(f"Loaded {len(knowledge_base)} documents")
        
        logger.info("Initializing vector store...")
        vector_store = VectorStore()
        
        if vector_store.count() == 0:
            logger.info("Adding documents to vector store...")
            vector_store.add_documents(knowledge_base)
            logger.info(f"Added {len(knowledge_base)} documents")
        else:
            logger.info(f"Using existing collection with {vector_store.count()} documents")
        
        logger.info("Initializing decision engine...")
        decision_engine = DecisionEngine(vector_store)
        
        initialize(decision_engine, vector_store)
        
        logger.info("All components initialized successfully")
        return vector_store, decision_engine
        
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        raise

@app.on_event("startup")
async def startup_event():
    initialize_components()

app.include_router(router, prefix="/api/v1", tags=["agent"])

@app.get("/api")
async def root():
    return {
        "service": "Customer Support Agent",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/v1/health",
            "stats": "/api/v1/stats",
            "ask": "/api/v1/ask (POST)",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=CONFIG.api.host,
        port=CONFIG.api.port,
        reload=CONFIG.api.reload,
        workers=CONFIG.api.workers
    )