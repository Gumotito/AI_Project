"""
Agent Tools
Provides tools for agents to interact with external services and data.
"""

import logging
from typing import List, Optional, Dict
from langchain_core.tools import Tool
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def web_search(query: str, max_results: int = 5) -> str:
    """
    Search the web using DuckDuckGo.
    
    Args:
        query: Search query
        max_results: Maximum number of results to return
        
    Returns:
        Formatted search results
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            
        if not results:
            return "No results found."
        
        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"{i}. {result['title']}\n"
                f"   URL: {result['href']}\n"
                f"   {result['body']}\n"
            )
        
        return "\n".join(formatted_results)
    except Exception as e:
        logger.error(f"Error in web search: {e}")
        return f"Error performing search: {str(e)}"


def image_search(query: str, max_results: int = 6) -> List[Dict[str, str]]:
    """
    Search for images using DuckDuckGo.
    
    Args:
        query: Search query
        max_results: Maximum number of images to return
        
    Returns:
        List of image dictionaries with 'url', 'title', and 'thumbnail' keys
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(query, max_results=max_results))
            
        if not results:
            return []
        
        images = []
        for result in results:
            images.append({
                'url': result.get('image', ''),
                'title': result.get('title', 'Image'),
                'thumbnail': result.get('thumbnail', result.get('image', ''))
            })
        
        return images
    except Exception as e:
        logger.error(f"Error in image search: {e}")
        return []


def fetch_webpage_content(url: str, max_length: int = 5000) -> str:
    """
    Fetch and extract main content from a webpage.
    
    Args:
        url: URL to fetch
        max_length: Maximum content length to return
        
    Returns:
        Extracted webpage content
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Truncate if too long
        if len(text) > max_length:
            text = text[:max_length] + "... (truncated)"
        
        return text
    except Exception as e:
        logger.error(f"Error fetching webpage: {e}")
        return f"Error fetching webpage: {str(e)}"


def analyze_seo_metrics(url: str) -> str:
    """
    Analyze basic SEO metrics of a webpage.
    
    Args:
        url: URL to analyze
        
    Returns:
        SEO analysis summary
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract SEO elements
        title = soup.find('title')
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        h1_tags = soup.find_all('h1')
        h2_tags = soup.find_all('h2')
        images = soup.find_all('img')
        links = soup.find_all('a')
        
        analysis = f"SEO Analysis for {url}:\n\n"
        analysis += f"Title: {title.string if title else 'Missing'}\n"
        analysis += f"Meta Description: {meta_desc.get('content') if meta_desc else 'Missing'}\n"
        analysis += f"H1 Tags: {len(h1_tags)}\n"
        analysis += f"H2 Tags: {len(h2_tags)}\n"
        analysis += f"Images: {len(images)} (with alt text: {sum(1 for img in images if img.get('alt'))})\n"
        analysis += f"Internal Links: {len([l for l in links if l.get('href', '').startswith('/')])}\n"
        analysis += f"External Links: {len([l for l in links if l.get('href', '').startswith('http')])}\n"
        
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing SEO: {e}")
        return f"Error analyzing SEO: {str(e)}"


def get_competitor_keywords(domain: str) -> str:
    """
    Simulate getting competitor keywords (placeholder for actual API).
    
    Args:
        domain: Competitor domain
        
    Returns:
        Keyword suggestions
    """
    # This is a placeholder - in production, you'd use an API like SEMrush or Ahrefs
    return f"Simulated competitor keywords for {domain}:\n- keyword research\n- seo optimization\n- content marketing\n- digital strategy"


def calculate_readability_score(text: str) -> str:
    """
    Calculate readability metrics for text.
    
    Args:
        text: Text to analyze
        
    Returns:
        Readability analysis
    """
    try:
        # Simple readability metrics
        words = text.split()
        sentences = text.count('.') + text.count('!') + text.count('?')
        
        if sentences == 0:
            sentences = 1
        
        avg_words_per_sentence = len(words) / sentences
        
        # Count syllables (simplified)
        syllables = sum(max(1, len([c for c in word if c.lower() in 'aeiou'])) for word in words)
        avg_syllables_per_word = syllables / len(words) if words else 0
        
        analysis = f"Readability Analysis:\n"
        analysis += f"Total Words: {len(words)}\n"
        analysis += f"Total Sentences: {sentences}\n"
        analysis += f"Avg Words per Sentence: {avg_words_per_sentence:.1f}\n"
        analysis += f"Avg Syllables per Word: {avg_syllables_per_word:.1f}\n"
        
        if avg_words_per_sentence > 20:
            analysis += "⚠️ Sentences may be too long. Consider breaking them up.\n"
        
        return analysis
    except Exception as e:
        logger.error(f"Error calculating readability: {e}")
        return f"Error analyzing readability: {str(e)}"


# Create tool instances
def get_agent_tools() -> List[Tool]:
    """
    Get all available tools for agents.
    
    Returns:
        List of Tool objects
    """
    return [
        Tool(
            name="web_search",
            func=web_search,
            description="Search the web for information. Input should be a search query string. Returns top search results with titles, URLs, and descriptions."
        ),
        Tool(
            name="fetch_webpage",
            func=fetch_webpage_content,
            description="Fetch and extract the main content from a webpage. Input should be a URL. Returns the text content of the page."
        ),
        Tool(
            name="analyze_seo",
            func=analyze_seo_metrics,
            description="Analyze SEO metrics of a webpage including title, meta description, headers, images, and links. Input should be a URL."
        ),
        Tool(
            name="readability_check",
            func=calculate_readability_score,
            description="Analyze the readability of text content. Input should be the text to analyze. Returns readability metrics and suggestions."
        ),
        Tool(
            name="competitor_keywords",
            func=get_competitor_keywords,
            description="Get keyword suggestions based on competitor analysis. Input should be a competitor domain."
        ),
    ]


def get_seo_tools() -> List[Tool]:
    """Get tools specific to SEO agent."""
    all_tools = get_agent_tools()
    return [t for t in all_tools if t.name in ["web_search", "fetch_webpage", "analyze_seo", "competitor_keywords"]]


def get_content_tools() -> List[Tool]:
    """Get tools specific to Content agent."""
    all_tools = get_agent_tools()
    return [t for t in all_tools if t.name in ["web_search", "fetch_webpage", "readability_check"]]
