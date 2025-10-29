"""
Test Ollama Integration
Tests the SEO agent with Ollama LLM and tools.
"""

import asyncio
import sys
sys.path.insert(0, '.')

from agents.agent_seo import SEOAgent


async def test_ollama_integration():
    """Test Ollama-powered agent with tools."""
    print("🤖 Testing Ollama Integration with AI_Project\n")
    print("=" * 60)
    
    # Check if Ollama is running
    print("\n1️⃣ Checking Ollama connection...")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Ollama is running")
            print(f"📦 Available models: {[m['name'] for m in models.get('models', [])]}")
        else:
            print("⚠️ Ollama responded but with error")
    except Exception as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        print("\n💡 Make sure Ollama is running:")
        print("   - Download from: https://ollama.com/download")
        print("   - Run: ollama serve")
        print("   - Pull model: ollama pull qwen2.5:32b")
        return
    
    print("\n" + "=" * 60)
    print("\n2️⃣ Initializing SEO Agent...")
    try:
        seo_agent = SEOAgent()
        print("✅ SEO Agent initialized with LLM and tools")
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        return
    
    print("\n" + "=" * 60)
    print("\n3️⃣ Testing SEO Analysis with real LLM...")
    print("   This will:")
    print("   - Use Ollama to reason about the task")
    print("   - Call web search tools to gather information")
    print("   - Analyze SEO metrics")
    print("   - Generate intelligent recommendations")
    print("\n   Target: https://example.com")
    print("   (This may take 30-60 seconds...)\n")
    
    try:
        result = await seo_agent.analyze_seo("https://example.com")
        
        print("=" * 60)
        print("\n✅ Analysis Complete!\n")
        print(f"Status: {result['status']}")
        print(f"\nAnalysis:\n{result.get('analysis', 'No analysis')}")
        
        if result.get('steps'):
            print(f"\n📊 Agent used {len(result['steps'])} tool calls")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("\n🔗 Check LangSmith Dashboard:")
    print("   https://smith.langchain.com/")
    print("   Project: AI_Project")
    print("\n✨ Test Complete!")


if __name__ == "__main__":
    asyncio.run(test_ollama_integration())
