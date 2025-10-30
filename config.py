"""
Configuration settings for AI Project.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    APP_NAME: str = "AI Project"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # API Keys (set via environment variables)
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # LangSmith Configuration
    # Set LANGCHAIN_TRACING_V2=true in .env to enable tracing
    LANGCHAIN_TRACING_V2: str = os.getenv("LANGCHAIN_TRACING_V2", "false")
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")
    LANGCHAIN_PROJECT: str = os.getenv("LANGCHAIN_PROJECT", "default")
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:14b"  # Options: qwen2.5:32b, qwen2.5:14b, llama3.3:70b, llama3.1:8b
    OLLAMA_TEMPERATURE: float = 0.7
    OLLAMA_NUM_CTX: int = 8192  # Context window size
    
    # Agent LLM Settings
    USE_LOCAL_LLM: bool = True  # Use Ollama (True) or OpenAI (False)
    ENABLE_TOOLS: bool = True   # Enable web search and other tools
    
    # Database
    DATABASE_URL: str = "sqlite:///./ai_project.db"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # Agent Configuration
    AGENT_TIMEOUT: int = 30  # seconds
    MAX_CONCURRENT_AGENTS: int = 5
    
    # Guardrails Configuration
    GUARDRAILS_ENABLED: bool = True
    GUARDRAILS_MAX_LENGTH: int = 5000
    GUARDRAILS_MIN_LENGTH: int = 1
    GUARDRAILS_CONTENT_FILTER: bool = True
    GUARDRAILS_PII_DETECTION: bool = True
    GUARDRAILS_RATE_LIMITING: bool = True
    GUARDRAILS_RATE_LIMIT_REQUESTS: int = 100  # requests per window
    GUARDRAILS_RATE_LIMIT_WINDOW: int = 60  # seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Initialize settings and set environment variables for LangSmith
settings = Settings()

# Set LangSmith environment variables
os.environ["LANGCHAIN_TRACING_V2"] = settings.LANGCHAIN_TRACING_V2
os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT
os.environ["LANGCHAIN_ENDPOINT"] = settings.LANGCHAIN_ENDPOINT

