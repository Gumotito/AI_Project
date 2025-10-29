"""
LangSmith Service
Provides utilities for LangSmith tracing and monitoring.
"""

import logging
from typing import Any, Dict, Optional
from functools import wraps
from langsmith import traceable, Client
from langsmith.run_helpers import get_current_run_tree

logger = logging.getLogger(__name__)


class LangSmithService:
    """Service for LangSmith tracing and monitoring."""
    
    def __init__(self):
        """Initialize LangSmith client."""
        try:
            self.client = Client()
            logger.info("LangSmith client initialized")
        except Exception as e:
            logger.warning(f"Could not initialize LangSmith client: {e}")
            self.client = None
    
    def get_run_url(self) -> Optional[str]:
        """Get the URL for the current run in LangSmith."""
        try:
            run_tree = get_current_run_tree()
            if run_tree:
                return run_tree.get_url()
        except Exception as e:
            logger.debug(f"Could not get run URL: {e}")
        return None
    
    def log_feedback(self, run_id: str, key: str, score: float, comment: Optional[str] = None):
        """Log feedback for a specific run."""
        if not self.client:
            return
        
        try:
            self.client.create_feedback(
                run_id=run_id,
                key=key,
                score=score,
                comment=comment
            )
            logger.info(f"Logged feedback for run {run_id}: {key}={score}")
        except Exception as e:
            logger.error(f"Error logging feedback: {e}")


# Create a singleton instance
langsmith_service = LangSmithService()


def trace_agent(name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
    """
    Decorator to trace agent methods with LangSmith.
    
    Args:
        name: Optional name for the trace (defaults to function name)
        metadata: Optional metadata to include in the trace
    
    Usage:
        @trace_agent(name="SEO Analysis", metadata={"agent": "seo"})
        async def analyze_seo(self, url: str):
            ...
    """
    def decorator(func):
        # Use traceable decorator from langsmith
        traced_func = traceable(
            name=name or func.__name__,
            metadata=metadata or {},
            run_type="chain"  # Use "chain" for agent operations
        )(func)
        
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                result = await traced_func(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Error in traced agent function {func.__name__}: {e}")
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                result = traced_func(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Error in traced agent function {func.__name__}: {e}")
                raise
        
        # Return appropriate wrapper based on whether function is async
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator
