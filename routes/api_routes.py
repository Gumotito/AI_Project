"""
API Routes
Handles all API endpoints for agent interactions.
"""

from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

router = APIRouter()


# Request/Response Models
class SEOAnalysisRequest(BaseModel):
    url: str


class ContentGenerationRequest(BaseModel):
    topic: str
    style: str = "professional"


class AgentStatusResponse(BaseModel):
    name: str
    status: str
    active: bool


class PageGenerateRequest(BaseModel):
    prompt: str
    style: str = "clean"
    target_audience: str | None = None
    tone: str = "professional"


class AskRequest(BaseModel):
    prompt: str


class InteractionEvent(BaseModel):
    event_type: str  # 'click', 'scroll', 'time', 'input'
    element_id: str | None = None
    metadata: Dict[str, Any] | None = None


# Agent Status Endpoints
@router.get("/agents", response_model=List[AgentStatusResponse])
async def list_agents(request: Request):
    """Get status of all agents."""
    agents = request.app.state.agents
    return [
        {
            "name": name.capitalize() + " Agent",
            "status": "active",
            "active": True
        }
        for name in agents.keys()
    ]


# SEO Agent Endpoints
@router.post("/seo/analyze")
async def analyze_seo(request: Request, data: SEOAnalysisRequest):
    """Analyze SEO for a given URL."""
    seo_agent = request.app.state.agents["seo"]
    result = await seo_agent.analyze_seo(data.url)
    return {"status": "success", "data": result}


@router.post("/seo/keywords")
async def generate_keywords(request: Request, data: Dict[str, str]):
    """Generate keywords from content."""
    seo_agent = request.app.state.agents["seo"]
    content = data.get("content", "")
    keywords = await seo_agent.generate_keywords(content)
    return {"status": "success", "keywords": keywords}


@router.get("/seo/recommendations")
async def get_seo_recommendations(request: Request):
    """Get SEO improvement recommendations."""
    seo_agent = request.app.state.agents["seo"]
    recommendations = await seo_agent.get_recommendations()
    return {"status": "success", "recommendations": recommendations}


# Content Agent Endpoints
@router.post("/content/generate")
async def generate_content(request: Request, data: ContentGenerationRequest):
    """Generate content for a topic."""
    content_agent = request.app.state.agents["content"]
    content = await content_agent.generate_content(data.topic, data.style)
    return {"status": "success", "content": content}


@router.post("/content/analyze")
async def analyze_content(request: Request, data: Dict[str, str]):
    """Analyze content readability."""
    content_agent = request.app.state.agents["content"]
    content = data.get("content", "")
    analysis = await content_agent.analyze_readability(content)
    return {"status": "success", "analysis": analysis}


@router.get("/content/topics/{category}")
async def suggest_topics(request: Request, category: str):
    """Suggest content topics for a category."""
    content_agent = request.app.state.agents["content"]
    topics = await content_agent.suggest_topics(category)
    return {"status": "success", "topics": topics}


# Monetization Agent Endpoints
@router.get("/monetization/revenue/{timeframe}")
async def analyze_revenue(request: Request, timeframe: str = "month"):
    """Analyze revenue for a timeframe."""
    monetization_agent = request.app.state.agents["monetization"]
    analysis = await monetization_agent.analyze_revenue(timeframe)
    return {"status": "success", "data": analysis}


@router.get("/monetization/strategies")
async def get_monetization_strategies(request: Request):
    """Get monetization strategy suggestions."""
    monetization_agent = request.app.state.agents["monetization"]
    strategies = await monetization_agent.suggest_monetization_strategies()
    return {"status": "success", "strategies": strategies}


@router.post("/monetization/ad-placement")
async def optimize_ad_placement(request: Request, data: Dict[str, Any]):
    """Optimize ad placement for a page."""
    monetization_agent = request.app.state.agents["monetization"]
    placements = await monetization_agent.optimize_ad_placement(data)
    return {"status": "success", "placements": placements}


# UI/UX Agent Endpoints
@router.post("/uiux/analyze-flow")
async def analyze_user_flow(request: Request, data: Dict[str, Any]):
    """Analyze user flow patterns."""
    uiux_agent = request.app.state.agents["uiux"]
    analysis = await uiux_agent.analyze_user_flow(data)
    return {"status": "success", "analysis": analysis}


@router.post("/uiux/accessibility")
async def check_accessibility(request: Request, data: Dict[str, str]):
    """Check accessibility compliance."""
    uiux_agent = request.app.state.agents["uiux"]
    html = data.get("html", "")
    result = await uiux_agent.check_accessibility(html)
    return {"status": "success", "result": result}


@router.get("/uiux/design-suggestions")
async def get_design_suggestions(request: Request):
    """Get design improvement suggestions."""
    uiux_agent = request.app.state.agents["uiux"]
    suggestions = await uiux_agent.suggest_design_improvements({})
    return {"status": "success", "suggestions": suggestions}


@router.post("/uiux/performance")
async def analyze_performance(request: Request, data: Dict[str, str]):
    """Analyze page performance."""
    uiux_agent = request.app.state.agents["uiux"]
    url = data.get("url", "")
    analysis = await uiux_agent.analyze_performance(url)
    return {"status": "success", "analysis": analysis}


# Oversight Agent Endpoints
@router.get("/oversight/health")
async def get_site_health(request: Request):
    """Get overall site health report."""
    oversight_agent = request.app.state.agents["oversight"]
    health = await oversight_agent.analyze_overall_health()
    return {"status": "success", "health": health}


@router.get("/oversight/report/{report_type}")
async def generate_report(request: Request, report_type: str = "daily"):
    """Generate a performance report."""
    oversight_agent = request.app.state.agents["oversight"]
    report = await oversight_agent.generate_report(report_type)
    return {"status": "success", "report": report}


@router.get("/oversight/priorities")
async def get_priorities(request: Request):
    """Get prioritized improvement recommendations."""
    oversight_agent = request.app.state.agents["oversight"]
    priorities = await oversight_agent.prioritize_improvements()
    return {"status": "success", "priorities": priorities}


@router.post("/oversight/strategy")
async def suggest_strategy(request: Request, data: Dict[str, str]):
    """Get strategic plan for a goal."""
    oversight_agent = request.app.state.agents["oversight"]
    goal = data.get("goal", "")
    strategy = await oversight_agent.suggest_strategy(goal)
    return {"status": "success", "strategy": strategy}


# Page generation pipeline
@router.post("/page/generate")
async def generate_page(request: Request, data: PageGenerateRequest):
    """Generate a landing page from a user prompt by coordinating agents."""
    agents = request.app.state.agents
    content_agent = agents["content"]
    uiux_agent = agents["uiux"]
    seo_agent = agents["seo"]
    oversight_agent = agents["oversight"]

    # 1) Content generation (links, text blocks, outline)
    content = await content_agent.generate_content(data.prompt, data.tone)

    # 2) UX render to styled HTML
    page_html = await uiux_agent.render_page({
        "title": content.get("title", "Generated Page"),
        "sections": content.get("sections", []),
        "links": content.get("links", [])
    }, style=data.style)

    # 3) SEO review (best-effort on HTML content)
    seo_review = await seo_agent.review_html(page_html)

    # 4) Oversight finalization + metrics logging
    final = await oversight_agent.finalize_and_log(
        prompt=data.prompt,
        html=page_html,
        content=content,
        seo=seo_review
    )

    return {
        "status": "success",
        "prompt": data.prompt,
        "content": content,
        "html": page_html,
        "seo": seo_review,
        "final": final,
    }


# General Q&A endpoint
@router.post("/ask")
async def ask(request: Request, data: AskRequest):
    """Answer a general question and return summary with references."""
    agents = request.app.state.agents
    content_agent = agents["content"]
    oversight_agent = agents["oversight"]
    result = await content_agent.answer_prompt(data.prompt)
    # Log interaction for local learning
    await oversight_agent.log_qa_interaction(
        prompt=data.prompt,
        answer=result.get("answer", ""),
        links=result.get("links", []),
        images=result.get("images", []),
        videos=result.get("videos", [])
    )
    return {"status": "success", **result}

@router.post("/uiux/track")
async def track_ui_interaction(request: Request, event: InteractionEvent):
    """Track user interface interaction for analytics and optimization."""
    agents = request.app.state.agents
    uiux_agent = agents["uiux"]
    result = await uiux_agent.track_interaction(event.dict())
    return result


@router.get("/uiux/recommendations")
async def get_ui_recommendations(request: Request):
    """Get UI/UX optimization recommendations based on collected data."""
    agents = request.app.state.agents
    uiux_agent = agents["uiux"]
    recommendations = await uiux_agent.get_optimization_recommendations()
    return {"recommendations": recommendations, "count": len(recommendations)}

