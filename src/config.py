from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import os

@dataclass(frozen=True)
class ModelConfig:
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    llm_model: str = "qwen2.5:0.5b"
    embedding_dim: int = 384
    
@dataclass(frozen=True)
class VectorStoreConfig:
    collection_name: str = "support_qa"
    persistence_dir: Path = Path("./chroma_db")
    similarity_metric: str = "cosine"
    
@dataclass(frozen=True)
class AgentConfig:
    similarity_threshold: float = 0.55
    ambiguity_threshold: float = 0.40
    max_results: int = 3
    min_results: int = 1
    
@dataclass(frozen=True)
class APIConfig:
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    workers: int = 1
    cors_origins: tuple = ("*",)
    
@dataclass(frozen=True)
class LoggingConfig:
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[Path] = None

@dataclass(frozen=True)
class Config:
    model: ModelConfig = ModelConfig()
    vector_store: VectorStoreConfig = VectorStoreConfig()
    agent: AgentConfig = AgentConfig()
    api: APIConfig = APIConfig()
    logging: LoggingConfig = LoggingConfig()
    knowledge_base_path: Path = Path("./data/knowledge_base.json")
    
    @classmethod
    def from_env(cls):
        return cls(model=ModelConfig( embedding_model=os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5"), llm_model= os.getenv("LLM_MODEL", "qwen2.5:0.5b" )) )
    
    def ensure_directories(self) -> None:
        self.vector_store.persistence_dir.mkdir(parents=True, exist_ok=True)
        self.knowledge_base_path.parent.mkdir(parents=True, exist_ok=True)
        if self.logging.file:
            self.logging.file.parent.mkdir(parents=True, exist_ok=True)


CONFIG = Config.from_env()