"""
LLM Service
Provides LLM capabilities using Ollama (local) or OpenAI (cloud).
Supports tool calling and function execution.
"""

import logging
from typing import List, Dict, Any, Optional, Callable, Union
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.tools import Tool
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import AIMessage
from config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """Service for managing LLM interactions with tool support."""
    
    def __init__(self, use_local: bool = None):
        """
        Initialize LLM service.
        
        Args:
            use_local: Use Ollama if True, OpenAI if False. Defaults to settings.USE_LOCAL_LLM
        """
        self.use_local = use_local if use_local is not None else settings.USE_LOCAL_LLM
        self.llm = self._initialize_llm()
        logger.info(f"LLM Service initialized with {'Ollama' if self.use_local else 'OpenAI'}")
    
    def _initialize_llm(self):
        """Initialize the appropriate LLM based on configuration."""
        if self.use_local:
            return ChatOllama(
                base_url=settings.OLLAMA_BASE_URL,
                model=settings.OLLAMA_MODEL,
                temperature=settings.OLLAMA_TEMPERATURE,
                num_ctx=settings.OLLAMA_NUM_CTX,
            )
        else:
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not set in environment")
            return ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.7,
                api_key=settings.OPENAI_API_KEY
            )
    
    def get_llm(self):
        """Get the initialized LLM instance."""
        return self.llm
    
    async def generate(self, prompt: str, system_message: str = None, timeout: float = 25.0) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The user prompt
            system_message: Optional system message to set context
            timeout: Max seconds to wait for LLM response (default 25s)
            
        Returns:
            Generated response as string
        """
        import asyncio
        try:
            messages = []
            if system_message:
                messages.append(("system", system_message))
            messages.append(("human", prompt))
            
            # Wrap LLM call with timeout to prevent hanging
            async def _call_llm():
                return await self.llm.ainvoke(messages)
            
            response = await asyncio.wait_for(_call_llm(), timeout=timeout)
            return response.content
        except asyncio.TimeoutError:
            logger.warning(f"LLM generate timed out after {timeout}s")
            return "Sorry, this is taking longer than expected. Please try a shorter or clearer prompt."
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            raise
    
    def create_agent(
        self,
        tools: List[Tool],
        system_prompt: str,
        agent_name: str = "Agent"
    ):
        """
        Create a tool-calling LLM configured with the given tools and prompt.
        
        Args:
            tools: List of tools the agent can use
            system_prompt: System prompt defining agent behavior
            agent_name: Name of the agent for logging
            
        Returns:
            A configured LLM with tools bound
        """
        try:
            # Bind tools to LLM
            llm_with_tools = self.llm.bind_tools(tools)
            
            logger.info(f"Created agent '{agent_name}' with {len(tools)} tools")
            return llm_with_tools, system_prompt
            
        except Exception as e:
            logger.error(f"Error creating agent: {e}")
            raise
    
    async def invoke_with_tools(
        self,
        prompt: str,
        tools: List[Tool],
        system_prompt: str = None
    ) -> Dict[str, Any]:
        """
        Invoke LLM with simplified execution (tools available but not auto-executed).
        """
        try:
            messages = [
                ("system", system_prompt or "You are a helpful AI assistant."),
                ("human", prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            
            return {
                "output": response.content if hasattr(response, 'content') else str(response),
                "intermediate_steps": []
            }
        except Exception as e:
            logger.error(f"Error invoking LLM: {e}")
            raise


# Create singleton instance
llm_service = LLMService()


def get_llm_service() -> LLMService:
    """Get the LLM service singleton."""
    return llm_service
