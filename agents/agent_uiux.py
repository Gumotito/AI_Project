"""
UI/UX Agent
Analyzes and improves user interface and user experience.
Provides recommendations for design, accessibility, and usability.
Collects data from user interactions and adapts the interface accordingly.
"""

import logging
import json
import os
from typing import Dict, List, Any
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)


class UIUXAgent:
    """
    Agent responsible for UI/UX optimization and analysis.
    
    System Prompt: You are a UI/UX expert. You collect data from user inputs, 
    and adjust the interface based on interaction patterns to improve usability,
    engagement, and conversion. You analyze clicks, time on page, scroll behavior,
    and user flow to make data-driven design decisions.
    """
    
    def __init__(self):
        self.name = "UI/UX Agent"
        self.interaction_log_path = "logs/ui_interactions.jsonl"
        self.analytics_path = "logs/ui_analytics.json"
        self._ensure_logs()
        logger.info(f"{self.name} initialized")
    
    def _ensure_logs(self):
        """Ensure log directories and files exist."""
        os.makedirs("logs", exist_ok=True)
        if not os.path.exists(self.analytics_path):
            with open(self.analytics_path, "w") as f:
                json.dump({
                    "total_interactions": 0,
                    "button_clicks": {},
                    "avg_time_on_page": 0,
                    "scroll_depth": [],
                    "search_patterns": [],
                    "optimizations_applied": []
                }, f)
    
    async def track_interaction(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Track user interaction event.
        
        Args:
            event_data: {
                'event_type': 'click' | 'scroll' | 'time' | 'input',
                'element_id': str,
                'timestamp': str,
                'metadata': dict
            }
        """
        try:
            event_data['timestamp'] = datetime.now().isoformat()
            
            # Log raw interaction
            with open(self.interaction_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(event_data, ensure_ascii=False) + "\n")
            
            # Update analytics
            await self._update_analytics(event_data)
            
            logger.info(f"Tracked {event_data['event_type']} on {event_data.get('element_id', 'unknown')}")
            return {"status": "tracked", "timestamp": event_data['timestamp']}
        except Exception as e:
            logger.error(f"Error tracking interaction: {e}")
            return {"status": "error", "message": str(e)}
    
    async def _update_analytics(self, event_data: Dict[str, Any]):
        """Update aggregated analytics with new event."""
        try:
            with open(self.analytics_path, "r") as f:
                analytics = json.load(f)
            
            analytics['total_interactions'] += 1
            
            if event_data['event_type'] == 'click':
                element_id = event_data.get('element_id', 'unknown')
                analytics['button_clicks'][element_id] = analytics['button_clicks'].get(element_id, 0) + 1
            
            elif event_data['event_type'] == 'scroll':
                depth = event_data.get('metadata', {}).get('scroll_depth', 0)
                analytics['scroll_depth'].append(depth)
            
            elif event_data['event_type'] == 'input':
                query = event_data.get('metadata', {}).get('query', '')
                if query:
                    analytics['search_patterns'].append({
                        'query': query,
                        'timestamp': event_data['timestamp']
                    })
            
            with open(self.analytics_path, "w") as f:
                json.dump(analytics, f, indent=2)
        except Exception as e:
            logger.error(f"Error updating analytics: {e}")
    
    async def get_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """
        Analyze collected data and provide UI/UX optimization recommendations.
        
        Returns:
            List of actionable optimization recommendations
        """
        try:
            with open(self.analytics_path, "r") as f:
                analytics = json.load(f)
            
            recommendations = []
            
            # Analyze button click patterns
            if analytics['button_clicks']:
                sorted_clicks = sorted(analytics['button_clicks'].items(), key=lambda x: x[1], reverse=True)
                most_used = sorted_clicks[0]
                least_used = sorted_clicks[-1] if len(sorted_clicks) > 1 else None
                
                recommendations.append({
                    'type': 'button_prominence',
                    'priority': 'high',
                    'recommendation': f"Button '{most_used[0]}' is most used ({most_used[1]} clicks). Consider making it more prominent.",
                    'element': most_used[0]
                })
                
                if least_used and least_used[1] < most_used[1] * 0.2:
                    recommendations.append({
                        'type': 'button_visibility',
                        'priority': 'medium',
                        'recommendation': f"Button '{least_used[0]}' rarely used ({least_used[1]} clicks). Consider repositioning or removing.",
                        'element': least_used[0]
                    })
            
            # Analyze scroll behavior
            if analytics['scroll_depth']:
                avg_scroll = sum(analytics['scroll_depth']) / len(analytics['scroll_depth'])
                if avg_scroll < 50:
                    recommendations.append({
                        'type': 'content_visibility',
                        'priority': 'high',
                        'recommendation': f"Users only scroll {avg_scroll:.0f}% on average. Consider placing key content higher or improving above-the-fold content.",
                        'data': {'avg_scroll_depth': avg_scroll}
                    })
            
            # Analyze search patterns
            if len(analytics['search_patterns']) > 5:
                recent_queries = [p['query'] for p in analytics['search_patterns'][-10:]]
                recommendations.append({
                    'type': 'search_optimization',
                    'priority': 'medium',
                    'recommendation': f"Common recent searches: {', '.join(recent_queries[:3])}. Consider adding quick links or suggestions.",
                    'data': {'recent_queries': recent_queries}
                })
            
            logger.info(f"Generated {len(recommendations)} optimization recommendations")
            return recommendations
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return []

    async def render_page(self, content: Dict[str, Any], style: str = "clean") -> str:
        """
        Render a simple, styled HTML page from structured content.
        Expects keys: title, sections (list of {heading, body}), links (list[str]).
        """
        title = content.get("title", "Generated Page")
        sections = content.get("sections", [])
        links = content.get("links", [])

        # Minimal inline CSS for portability (kept simple)
        css = """
        body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 0; color: #222; }
        header { background: #0f172a; color: #fff; padding: 28px 20px; }
        main { max-width: 880px; margin: 24px auto; padding: 0 16px; }
        h1 { margin: 0; font-size: 2rem; }
        section { background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 20px; margin: 16px 0; box-shadow: 0 1px 2px rgba(0,0,0,.04); }
        h2 { margin-top: 0; font-size: 1.25rem; }
        ul.links { list-style: none; padding-left: 0; }
        ul.links li { margin: 6px 0; }
        a { color: #2563eb; text-decoration: none; }
        a:hover { text-decoration: underline; }
        footer { text-align: center; color: #64748b; padding: 24px 0 36px; }
        """

        html_parts = [
            "<!DOCTYPE html>",
            "<html lang=\"en\">",
            "<head>",
            "  <meta charset=\"utf-8\">",
            "  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">",
            f"  <title>{title}</title>",
            f"  <style>{css}</style>",
            "</head>",
            "<body>",
            "  <header>",
            f"    <h1>{title}</h1>",
            "  </header>",
            "  <main>",
        ]

        for sec in sections:
            heading = sec.get("heading", "Section")
            body = sec.get("body", "")
            html_parts += [
                "    <section>",
                f"      <h2>{heading}</h2>",
                f"      <p>{body}</p>",
                "    </section>",
            ]

        if links:
            html_parts += [
                "    <section>",
                "      <h2>References</h2>",
                "      <ul class=\"links\">",
            ]
            for link in links:
                html_parts.append(f"        <li><a href=\"{link}\" target=\"_blank\" rel=\"noopener\">{link}</a></li>")
            html_parts += [
                "      </ul>",
                "    </section>",
            ]

        html_parts += [
            "  </main>",
            "  <footer>Generated by AI_Project UI/UX Agent</footer>",
            "</body>",
            "</html>",
        ]

        return "\n".join(html_parts)
    
    async def analyze_user_flow(self, page_analytics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze user navigation patterns and flow.
        
        Args:
            page_analytics: Analytics data for pages
            
        Returns:
            User flow analysis results
        """
        logger.info("Analyzing user flow")
        # TODO: Implement user flow analysis
        return {
            "bounce_rate": 0,
            "avg_time_on_page": 0,
            "navigation_patterns": [],
            "drop_off_points": []
        }
    
    async def check_accessibility(self, page_html: str) -> Dict[str, Any]:
        """
        Check page for accessibility compliance (WCAG).
        
        Args:
            page_html: HTML content to check
            
        Returns:
            Accessibility audit results
        """
        logger.info("Checking accessibility")
        # TODO: Implement accessibility checking
        return {
            "score": 0,
            "issues": [],
            "recommendations": [],
            "wcag_level": "unknown"
        }
    
    async def analyze_mobile_responsiveness(self, url: str) -> Dict[str, Any]:
        """
        Analyze mobile responsiveness and mobile UX.
        
        Args:
            url: URL to analyze
            
        Returns:
            Mobile responsiveness analysis
        """
        logger.info(f"Analyzing mobile responsiveness for {url}")
        # TODO: Implement mobile analysis
        return {
            "is_mobile_friendly": False,
            "issues": [],
            "viewport_configuration": {},
            "touch_targets": []
        }
    
    async def suggest_design_improvements(self, page_data: Dict[str, Any]) -> List[str]:
        """
        Suggest design improvements based on best practices.
        
        Args:
            page_data: Page structure and design data
            
        Returns:
            List of design improvement suggestions
        """
        logger.info("Generating design improvement suggestions")
        # TODO: Implement design analysis
        return [
            "Increase contrast ratio for better readability",
            "Add more whitespace between sections",
            "Improve call-to-action button visibility"
        ]
    
    async def analyze_performance(self, url: str) -> Dict[str, Any]:
        """
        Analyze page performance metrics (load time, etc).
        
        Args:
            url: URL to analyze
            
        Returns:
            Performance analysis results
        """
        logger.info(f"Analyzing performance for {url}")
        # TODO: Implement performance analysis
        return {
            "load_time": 0,
            "first_contentful_paint": 0,
            "time_to_interactive": 0,
            "recommendations": []
        }
    
    async def generate_color_scheme(self, brand_colors: List[str]) -> Dict[str, Any]:
        """
        Generate complementary color scheme based on brand colors.
        
        Args:
            brand_colors: List of hex color codes
            
        Returns:
            Complete color scheme recommendations
        """
        logger.info("Generating color scheme")
        # TODO: Implement color scheme generation
        return {
            "primary": "",
            "secondary": "",
            "accent": "",
            "background": "",
            "text": ""
        }
