import logging
from typing import List, Dict, Any
import ollama

from .config import CONFIG

logger = logging.getLogger(__name__)

class ResponseGenerator:
    
    def __init__(self):
        self.use_llm = True
        self.model = CONFIG.model.llm_model
        
    def generate_answer(self, top_result: Dict, context_results: List[Dict]) -> str:
        
        if self.use_llm:
            try:
                return self._generate_with_llm(top_result, context_results)
            except Exception as e:
                logger.warning(f"LLM generation failed, using stored answer: {e}")
        
        return top_result['answer']
    
    def _generate_with_llm(self, top_result: Dict, context_results: List[Dict]) -> str:
        context = self._build_context(context_results)
        
        prompt = f"""
        You are a customer support assistant. Provide a helpful, concise, and professional answer.
        
        Context from knowledge base:
        {context}
        
        User question: {top_result['question']}
        
        Your answer:
        """
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': 'You are a helpful customer support assistant. Provide clear, accurate answers based on the context provided.'},
                    {'role': 'user', 'content': prompt}
                ],
                options={
                    'temperature': 0.3,
                    'top_p': 0.9,
                    'num_tokens': 200
                }
            )
            return response['message']['content'].strip()
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            raise
    
    def generate_clarification(self, query: str, results: List[Dict]) -> str:
        
        if self.use_llm:
            try:
                return self._generate_clarification_with_llm(query, results)
            except Exception as e:
                logger.warning(f"LLM clarification failed: {e}")
        
        categories = ', '.join([r.get('category', '') for r in results if r.get('category')])
        if categories:
            return f"Could you clarify which aspect you're asking about? (e.g., {categories})"
        return "Could you please provide more details about your question?"
    
    def _generate_clarification_with_llm(self, query: str, results: List[Dict]) -> str:
        categories = ', '.join([r.get('category', '') for r in results if r.get('category')])
        
        prompt = f"""
        The user asked: "{query}"
        
        Potential topics: {categories if categories else 'various topics'}
        
        Ask a short, specific clarifying question to understand what they need.
        Question:
        """
        
        response = ollama.chat(
            model=self.model,
            messages=[
                {'role': 'system', 'content': 'You ask clarifying questions to better understand user needs.'},
                {'role': 'user', 'content': prompt}
            ],
            options={
                'temperature': 0.5,
                'num_tokens': 50
            }
        )
        return response['message']['content'].strip()
    
    def _build_context(self, results: List[Dict]) -> str:
        """Build context string from results."""
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(f"{i}. Q: {result.get('question', '')}")
            context_parts.append(f"   A: {result.get('answer', '')}")
        return '\n'.join(context_parts)