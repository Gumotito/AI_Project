"""
AI Project - Agent-Managed Website
Main application entry point using FastAPI.
"""

import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routes import main_routes, api_routes
from agents import (
    SEOAgent,
    ContentAgent,
    MonetizationAgent,
    UIUXAgent,
    OversightAgent
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Project",
    description="Agent-managed website platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize agents
seo_agent = SEOAgent()
content_agent = ContentAgent()
monetization_agent = MonetizationAgent()
uiux_agent = UIUXAgent()
oversight_agent = OversightAgent()

# Register agents with oversight
oversight_agent.register_agent("seo", seo_agent)
oversight_agent.register_agent("content", content_agent)
oversight_agent.register_agent("monetization", monetization_agent)
oversight_agent.register_agent("uiux", uiux_agent)

# Store agents in app state
app.state.agents = {
    "seo": seo_agent,
    "content": content_agent,
    "monetization": monetization_agent,
    "uiux": uiux_agent,
    "oversight": oversight_agent
}

# Include routers
app.include_router(main_routes.router)
app.include_router(api_routes.router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("AI Project application starting up...")
    logger.info("All agents initialized successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("AI Project application shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
