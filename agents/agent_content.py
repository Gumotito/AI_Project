"""
Content Agent
Manages content creation, optimization, and quality control.
Generates and improves website content using AI.
"""

import asyncio
import logging
from typing import Dict, List, Any
from services.llm_service import get_llm_service
from services.agent_tools import web_search, image_search

logger = logging.getLogger(__name__)


class ContentAgent:
    """Agent responsible for content creation and management."""
    
    def __init__(self):
        self.name = "Content Agent"
        self.llm = get_llm_service()
        logger.info(f"{self.name} initialized")
    
    async def generate_content(self, topic: str, style: str = "professional") -> Dict[str, Any]:
        """
        Generate structured content for a given topic.
        Returns a dict with title, sections, and links.
        """
        logger.info(f"Generating content for topic: {topic}")
        # Fetch a few relevant links
        links_text = web_search(topic, max_results=3)

        prompt = (
            f"You are a content expert. Create a concise landing page outline for: '{topic}'.\n"
            f"Style: {style}.\n"
            "Return JSON with keys: title (string), sections (array of {heading, body}), and bullets (array of strings)."
        )
        try:
            resp = await self.llm.generate(prompt)
        except Exception:
            resp = "{\"title\": \"Landing Page\", \"sections\": [{\"heading\": \"Overview\", \"body\": \"Generated content\"}], \"bullets\": []}"

        # Best effort: if not JSON, wrap as a single section
        content: Dict[str, Any]
        if resp.strip().startswith("{"):
            try:
                import json
                content = json.loads(resp)
            except Exception:
                content = {"title": topic.title(), "sections": [{"heading": "Overview", "body": resp}], "bullets": []}
        else:
            content = {"title": topic.title(), "sections": [{"heading": "Overview", "body": resp}], "bullets": []}

        # Attach parsed links (simple parse from search output)
        link_lines = [l for l in links_text.splitlines() if l.strip().startswith("URL:") or l.strip().startswith("   URL:")]
        links = [l.split("URL:")[-1].strip() for l in link_lines][:3]
        content["links"] = links
        return content

    async def answer_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        General Q&A: perform a quick web search and produce a concise answer with references.
        Returns: { answer: str, bullets: list[str], links: list[str] }
        """
        logger.info("Answering prompt with content agent")
        
        # Get a few links with timeout to prevent hanging
        try:
            links_text = await asyncio.wait_for(
                asyncio.to_thread(web_search, prompt, 5),
                timeout=5.0
            )
        except asyncio.TimeoutError:
            logger.warning("Web search timed out")
            links_text = ""
        except Exception as e:
            logger.error(f"Web search error: {e}")
            links_text = ""
        
        link_lines = [l for l in links_text.splitlines() if l.strip().startswith("URL:") or l.strip().startswith("   URL:")]
        links = [l.split("URL:")[-1].strip() for l in link_lines][:5]

        qa_system = (
            "You are a helpful research assistant. Given a user prompt, write a concise answer (5-8 sentences),"
            " followed by 3-6 bullet key points. Avoid hallucinations; if unsure, say what would be needed to verify."
        )
        llm_prompt = (
            f"System: {qa_system}\n"
            f"User prompt: {prompt}\n"
            f"Useful references (URLs may be relevant):\n" + "\n".join(links)
        )
        try:
            answer_text = await self.llm.generate(llm_prompt, timeout=20.0)
        except Exception as e:
            logger.error(f"LLM error: {e}")
            answer_text = "I could not generate an answer right now. Please try again."

        # Extract bullets heuristically from answer_text
        lines = [l.rstrip() for l in answer_text.splitlines()]
        bullets = []
        body_lines = []
        for l in lines:
            ls = l.lstrip()
            if ls.startswith("- ") or ls.startswith("• ") or ls.startswith("* "):
                # remove bullet marker
                item = ls[2:] if ls[:2] in ("- ", "* ") else ls[2:]
                bullets.append(item.strip())
            else:
                body_lines.append(l)
        answer_clean = "\n".join([bl for bl in body_lines if bl.strip()])

        # Search for relevant images with timeout
        images = []
        try:
            images = await asyncio.wait_for(
                asyncio.to_thread(image_search, prompt, 6),
                timeout=5.0
            )
        except asyncio.TimeoutError:
            logger.warning("Image search timed out")
        except Exception as e:
            logger.error(f"Image search error: {e}")

        return {
            "answer": answer_clean if answer_clean else answer_text,
            "bullets": bullets,
            "links": links,
            "images": images
        }
    
    async def improve_content(self, content: str, criteria: List[str]) -> str:
        """
        Improve existing content based on criteria.
        
        Args:
            content: The content to improve
            criteria: List of improvement criteria
            
        Returns:
            Improved content
        """
        logger.info("Improving content")
        # TODO: Implement content improvement logic
        return content
    
    async def analyze_readability(self, content: str) -> Dict[str, Any]:
        """
        Analyze content readability metrics.
        
        Args:
            content: The content to analyze
            
        Returns:
            Dictionary with readability scores and suggestions
        """
        logger.info("Analyzing content readability")
        from services.agent_tools import calculate_readability_score
        analysis_text = calculate_readability_score(content)
        return {"analysis": analysis_text}
    
    async def suggest_topics(self, category: str) -> List[str]:
        """
        Suggest content topics based on category.
        
        Args:
            category: Content category
            
        Returns:
            List of suggested topics
        """
        logger.info(f"Suggesting topics for category: {category}")
        # TODO: Implement topic suggestion logic
        return []
    
    async def check_plagiarism(self, content: str) -> Dict[str, Any]:
        """
        Check content for potential plagiarism.
        
        Args:
            content: The content to check
            
        Returns:
            Plagiarism check results
        """
        logger.info("Checking content for plagiarism")
        # TODO: Implement plagiarism checking
        return {
            "is_original": True,
            "similarity_score": 0,
            "matches": []
        }
