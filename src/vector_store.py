import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any
import logging
from .config import CONFIG

logger = logging.getLogger(__name__)

class VectorStore:
    
    def __init__(self):
        self.config = CONFIG.vector_store
        
        self.config.persistence_dir.mkdir(parents=True, exist_ok=True)
        
        self.client = chromadb.PersistentClient( path=str(self.config.persistence_dir))
        
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction( model_name=CONFIG.model.embedding_model)
        
        self._collection = None
        self._initialize_collection()
        
    def _initialize_collection(self) -> None:
        try:
            self._collection = self.client.get_or_create_collection(
                name=self.config.collection_name,
                embedding_function=self.embedding_function,
                metadata={"hnsw:space": self.config.similarity_metric}
            )
            logger.info(f"Collection '{self.config.collection_name}' initialized")
        except Exception as e:
            logger.error(f"Failed to initialize collection: {e}")
            raise
    
    @property
    def collection(self):
        """Get the collection."""
        if self._collection is None:
            self._initialize_collection()
        return self._collection
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> int:
        if not documents:
            return 0
            
        try:
            ids = [str(doc['id']) for doc in documents]
            texts = [
                f""" 
                Question: {doc['question']} 
                Answer: {doc['answer']} """ 
                for doc in documents]
            
            metadatas = [
                {
                    'answer': doc['answer'],
                    'category': doc.get('category', ''),
                    'question': doc['question'],
                    'source': "knowledge_base"
                }
                for doc in documents
            ]
            
            self.collection.upsert(
                ids=ids,
                documents=texts,
                metadatas=metadatas
            )
            
            logger.info(f"Added {len(documents)} documents to vector store")
            return len(documents)
            
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise
    
    def search(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include=["metadatas", "distances", "documents"]
            )
            
            formatted_results = []
            if results['ids'] and results['ids'][0]:
                for idx, doc_id in enumerate(results['ids'][0]):
                    distance = results['distances'][0][idx]
                    similarity = max(0, 1 - distance)
                    
                    formatted_results.append({
                        'id': doc_id,
                        'question': results['metadatas'][0][idx].get('question', ''),
                        'answer': results['metadatas'][0][idx].get('answer', ''),
                        'category': results['metadatas'][0][idx].get('category', ''),
                        'score': similarity
                    })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def count(self) -> int:
        try:
            return self.collection.count()
        except Exception as e:
            logger.error(f"Failed to get count: {e}")
            return 0
    
    def delete_collection(self) -> None:
        try:
            self.client.delete_collection(self.config.collection_name)
            self._collection = None
            logger.info(f"Collection '{self.config.collection_name}' deleted")
        except Exception as e:
            logger.warning(f"Failed to delete collection: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "document_count": self.count(),
            "collection_name": self.config.collection_name,
            "similarity_metric": self.config.similarity_metric,
            "embedding_model": CONFIG.model.embedding_model,
            "embedding_dim": CONFIG.model.embedding_dim,
            "vector_store": "ChromaDB"
            # "cache_stats": self.embedding_model.get_cache_stats()
        }