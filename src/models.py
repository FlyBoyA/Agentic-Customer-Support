from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime

class QueryRequest(BaseModel):
    question: str = Field(..., description="The user's question", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "How do I reset my password?"
            }
        }

class QueryResponse(BaseModel):
    response: str = Field(..., description="The agent's response")
    action: Literal["answer", "clarify", "decline"] = Field(
        ..., 
        description="The decision made by the agent"
    )
    confidence: Optional[float] = Field(
        None, 
        description="Confidence score (0-1) for answer actions",
        ge=0,
        le=1
    )
    source: Optional[str] = Field(
        None, 
        description="Source document ID for answer actions"
    )
    category: Optional[str] = Field(
        None, 
        description="Category of the answer"
    )
    suggested_topics: Optional[List[str]] = Field(
        None,
        description="Suggested topics for clarification actions"
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Response timestamp"
    )

class HealthResponse(BaseModel):
    status: Literal["healthy", "unhealthy"]
    vector_store_count: int
    version: str = "1.0.0"

class StatsResponse(BaseModel):
    total_documents: int
    categories: List[str]
    embedding_model: str
    vector_store_type: str = "ChromaDB"

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())