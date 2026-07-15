from typing import Dict, Any, List, Optional
from enum import Enum
from dataclasses import dataclass
import logging
from .vector_store import VectorStore
from .config import CONFIG
from .response_generator import ResponseGenerator

logger = logging.getLogger(__name__)

class DecisionType(Enum):
    ANSWER = "answer"
    CLARIFY = "clarify"
    DECLINE = "decline"

@dataclass
class Decision:
    type: DecisionType
    response: str
    confidence: Optional[float] = None
    source: Optional[str] = None
    category: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class DecisionEngine:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.response_generator = ResponseGenerator()
        self.config = CONFIG.agent
        
    def process(self, query: str) -> Decision:
        """Process a query and return a decision."""
        results = self.vector_store.search(query, n_results=self.config.max_results)
        
        if not results:
            return self._make_decline_decision("I couldn't find any relevant information. Please contact support@test.com.")
        
        top_result = results[0]
        
        if self._is_out_of_scope(top_result):
             return self._make_decline_decision(top_result["answer"])
        
        top_score = top_result["score"]
        
        # Decision Branch 1: High Confidence Answer
        if top_score >= self.config.similarity_threshold:
            return self._make_answer_decision(results[0], results)
        
        # Decision Branch 2: Ambiguous Query
        if self._is_ambiguous(results):
            return self._make_clarify_decision(query, results)
        
        # Decision Branch 3: Decline
        return self._make_decline_decision("I'm not confident about answering this question. Please rephrase or contact support@test.com.")
    
    def _is_ambiguous(self, results: List[Dict]) -> bool:
        if len(results) < 2:
            return False
        
        scores = [r['score'] for r in results]
        top_score = scores[0]
        
        if self.config.ambiguity_threshold <= top_score < self.config.similarity_threshold:
            return True
        
        if max(scores) - min(scores) < 0.1:
            return True
            
        return False
    
    def _make_answer_decision(self, top_result: Dict, all_results: List[Dict]) -> Decision: 
        response = self.response_generator.generate_answer(top_result, all_results[:2])
        
        return Decision(
            type=DecisionType.ANSWER,
            response=response,
            confidence=top_result['score'],
            source=top_result.get('id'),
            category=top_result.get('category'),
            metadata={'all_results': all_results[:2]}
        )
    
    def _make_clarify_decision(self, query: str, results: List[Dict]) -> Decision:
        response = self.response_generator.generate_clarification(query, results[:2])
        
        return Decision(
            type=DecisionType.CLARIFY,
            response=response,
            metadata={'suggested_topics': [r.get('category', 'General') for r in results[:2]]}
        )
    
    def _make_decline_decision(self, message: str) -> Decision:
        return Decision(
            type=DecisionType.DECLINE,
            response=message
        )
    
    def _is_out_of_scope(self, result):
        return result.get("category") == "Out of Scope"