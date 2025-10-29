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
