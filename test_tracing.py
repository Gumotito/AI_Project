"""
Test LangSmith Tracing
Quick test to verify LangSmith integration is working.
"""

import asyncio
import sys
sys.path.insert(0, '.')

from agents.agent_seo import SEOAgent
from agents.agent_oversight import OversightAgent


async def test_tracing():
    """Test LangSmith tracing with agent operations."""
    print("🔍 Testing LangSmith Tracing Integration...\n")
    
    # Initialize agents
    seo_agent = SEOAgent()
    oversight_agent = OversightAgent()
    oversight_agent.register_agent("seo", seo_agent)
    
    print("✅ Agents initialized\n")
    
    # Test SEO Agent
    print("📊 Testing SEO Agent...")
    result = await seo_agent.analyze_seo("https://example.com")
    print(f"Result: {result}\n")
    
    # Test getting recommendations
    print("💡 Testing SEO Recommendations...")
    recommendations = await seo_agent.get_recommendations()
    print(f"Recommendations: {recommendations}\n")
    
    # Test Oversight Agent
    print("🎯 Testing Oversight Agent...")
    health = await oversight_agent.analyze_overall_health()
    print(f"Health Check: {health}\n")
    
    print("✨ All tests completed!")
    print("\n🔗 Check your LangSmith dashboard at: https://smith.langchain.com/")
    print("   Project: AI_Project")


if __name__ == "__main__":
    asyncio.run(test_tracing())
