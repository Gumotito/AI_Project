"""
SEO Agent
Handles search engine optimization tasks including keyword research,
meta tags optimization, sitemap generation, and SEO analysis.
"""

import logging
from typing import Dict, List, Any
from services.langsmith_service import trace_agent
from services.llm_service import get_llm_service
from services.agent_tools import get_seo_tools, calculate_readability_score

logger = logging.getLogger(__name__)


class SEOAgent:
    """Agent responsible for SEO optimization and analysis."""
    
    def __init__(self):
        self.name = "SEO Agent"
        self.llm_service = get_llm_service()
        self.tools = get_seo_tools()
        
        # Create agent with tools (returns LLM with tools bound and system prompt)
        self.llm_with_tools, self.system_prompt = self.llm_service.create_agent(
            tools=self.tools,
            system_prompt="""You are an expert SEO analyst. Your role is to:
            - Analyze websites for SEO performance
            - Provide actionable SEO recommendations
            - Research keywords and competition
            - Optimize content for search engines
            
            Use the available tools to gather data and provide comprehensive analysis.
            Be specific and data-driven in your recommendations.""",
            agent_name="SEO Agent"
        )
        logger.info(f"{self.name} initialized")
    
    @trace_agent(name="SEO Analysis", metadata={"agent": "seo", "action": "analyze"})
    async def analyze_seo(self, url: str) -> Dict[str, Any]:
        """
        Analyze SEO metrics for a given URL.
        
        Args:
            url: The URL to analyze
            
        Returns:
            Dictionary containing SEO analysis results
        """
        logger.info(f"Analyzing SEO for {url}")
        
        prompt = f"""Analyze the SEO of this website: {url}
        
        Please:
        1. Use the analyze_seo tool to get technical SEO metrics
        2. Use web_search to find information about SEO best practices for this type of site
        3. Provide specific, actionable recommendations
        4. Rate the overall SEO on a scale of 1-10
        
        Format your response as a comprehensive SEO analysis."""
        
        try:
            result = await self.llm_service.invoke_with_tools(
                prompt=prompt,
                tools=self.tools,
                system_prompt=self.system_prompt
            )
            return {
                "status": "success",
                "url": url,
                "analysis": result["output"],
                "steps": result.get("intermediate_steps", [])
            }
        except Exception as e:
            logger.error(f"Error in SEO analysis: {e}")
            return {
                "status": "error",
                "url": url,
                "error": str(e)
            }

    @trace_agent(name="SEO Review HTML", metadata={"agent": "seo", "action": "review_html"})
    async def review_html(self, html: str) -> Dict[str, Any]:
        """
        Review SEO-relevant aspects of a raw HTML string (no URL required).
        Returns quick counts and readability notes.
        """
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('title')
            h1 = soup.find_all('h1')
            h2 = soup.find_all('h2')
            imgs = soup.find_all('img')
            links = soup.find_all('a')

            readability = calculate_readability_score(soup.get_text()[:8000])
            return {
                "title": title.get_text(strip=True) if title else None,
                "h1": len(h1),
                "h2": len(h2),
                "images": len(imgs),
                "images_with_alt": sum(1 for i in imgs if i.get('alt')),
                "links": len(links),
                "readability": readability,
                "notes": [
                    "Ensure a single, descriptive H1.",
                    "Include meta description and relevant keywords.",
                    "Use alt text for images.",
                ]
            }
        except Exception as e:
            logger.error(f"Error reviewing HTML: {e}")
            return {"error": str(e)}
    
    @trace_agent(name="Keyword Generation", metadata={"agent": "seo", "action": "keywords"})
    async def generate_keywords(self, content: str) -> List[str]:
        """
        Generate relevant keywords from content.
        
        Args:
            content: The content to analyze
            
        Returns:
            List of suggested keywords
        """
        logger.info("Generating keywords")
        # TODO: Implement keyword generation
        return []
    
    @trace_agent(name="Meta Tag Optimization", metadata={"agent": "seo", "action": "meta_tags"})
    async def optimize_meta_tags(self, page_content: str) -> Dict[str, str]:
        """
        Generate optimized meta tags for content.
        
        Args:
            page_content: The page content to optimize
            
        Returns:
            Dictionary of meta tag recommendations
        """
        logger.info("Optimizing meta tags")
        # TODO: Implement meta tag optimization
        return {
            "title": "",
            "description": "",
            "keywords": ""
        }
    
    @trace_agent(name="SEO Recommendations", metadata={"agent": "seo", "action": "recommendations"})
    async def get_recommendations(self) -> List[str]:
        """
        Get SEO improvement recommendations.
        
        Returns:
            List of actionable SEO recommendations
        """
        logger.info("Getting SEO recommendations")
        # TODO: Implement recommendation logic
        return [
            "Add meta descriptions to all pages",
            "Optimize page load speed",
            "Improve internal linking structure"
        ]
