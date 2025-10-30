"""
Main Routes
Handles main web page routes and rendering.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main dashboard page."""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "AI Project Dashboard",
            "agents": [
                {"name": "SEO Agent", "status": "active"},
                {"name": "Content Agent", "status": "active"},
                {"name": "Monetization Agent", "status": "active"},
                {"name": "UI/UX Agent", "status": "active"},
                {"name": "Oversight Agent", "status": "active"}
            ]
        }
    )


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Render the detailed dashboard."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Dashboard"}
    )


@router.get("/health")
async def health_check(request: Request):
    """
    Health check endpoint for load balancers and orchestrators.
    Returns overall system health status.
    """
    try:
        # Check Ollama connectivity
        import httpx
        from config import settings
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.OLLAMA_BASE_URL}/api/tags", 
                timeout=5.0
            )
            ollama_status = "healthy" if response.status_code == 200 else "degraded"
    except Exception as e:
        ollama_status = "unhealthy"
    
    overall_status = "healthy" if ollama_status != "unhealthy" else "degraded"
    
    return {
        "status": overall_status,
        "version": "1.0.0",
        "services": {
            "ollama": ollama_status,
            "api": "healthy"
        }
    }


@router.get("/ready")
async def readiness_check(request: Request):
    """
    Readiness check endpoint.
    Returns 200 when application is ready to handle requests.
    Returns 503 when application is still warming up.
    """
    from fastapi.responses import JSONResponse
    
    # Check if LLM warmup is complete
    if not hasattr(request.app.state, 'agents'):
        return JSONResponse(
            status_code=503,
            content={"status": "not ready", "reason": "agents not initialized"}
        )
    
    return {"status": "ready"}

