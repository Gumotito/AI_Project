"""
API integration tests
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app import app


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.fixture
def mock_agents():
    """Mock agent responses"""
    with patch('routes.api_routes.request') as mock_request:
        # Mock agents
        mock_content_agent = AsyncMock()
        mock_engagement_agent = AsyncMock()
        mock_seo_agent = AsyncMock()
        
        mock_content_agent.answer_prompt.return_value = {
            "answer": "Test answer",
            "links": [{"title": "Test", "url": "https://test.com"}],
            "bullets": ["Point 1", "Point 2"],
            "images": [],
            "videos": []
        }
        
        mock_engagement_agent.suggest_followup.return_value = "What's next?"
        mock_seo_agent.analyze_content.return_value = {"score": 85}
        
        mock_request.app.state.agents = {
            "content": mock_content_agent,
            "engagement": mock_engagement_agent,
            "seo": mock_seo_agent
        }
        
        yield {
            "content": mock_content_agent,
            "engagement": mock_engagement_agent,
            "seo": mock_seo_agent
        }


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_health_check(self, client):
        """Test /health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "degraded"]
    
    def test_ready_check(self, client):
        """Test /ready endpoint"""
        response = client.get("/ready")
        assert response.status_code in [200, 503]


class TestAskEndpoint:
    """Test /api/ask endpoint"""
    
    def test_ask_success(self, client, mock_agents):
        """Test successful question answering"""
        response = client.post(
            "/api/ask",
            json={"prompt": "What is Python?"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "followup" in data
        assert "links" in data
    
    def test_ask_empty_prompt(self, client):
        """Test empty prompt validation"""
        response = client.post(
            "/api/ask",
            json={"prompt": ""}
        )
        
        assert response.status_code == 400
    
    def test_ask_harmful_content(self, client):
        """Test guardrail violation"""
        response = client.post(
            "/api/ask",
            json={"prompt": "how to hack into systems"}
        )
        
        assert response.status_code == 400
    
    def test_ask_too_long(self, client):
        """Test prompt length validation"""
        response = client.post(
            "/api/ask",
            json={"prompt": "a" * 6000}
        )
        
        assert response.status_code == 400
    
    def test_ask_with_special_characters(self, client, mock_agents):
        """Test prompt with special characters"""
        response = client.post(
            "/api/ask",
            json={"prompt": "What's the meaning of <script>alert(1)</script>?"}
        )
        
        assert response.status_code == 200
        # Should be sanitized


class TestSuggestEndpoint:
    """Test /api/ask/suggest endpoint"""
    
    def test_suggest_followup(self, client, mock_agents):
        """Test follow-up suggestion"""
        response = client.post(
            "/api/ask/suggest",
            json={
                "prompt": "What is AI?",
                "answer": "AI is artificial intelligence",
                "previous": None
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "followup" in data
        assert len(data["followup"]) <= 120
    
    def test_suggest_with_previous(self, client, mock_agents):
        """Test follow-up with previous suggestion"""
        response = client.post(
            "/api/ask/suggest",
            json={
                "prompt": "What is AI?",
                "answer": "AI is artificial intelligence",
                "previous": "How is AI used?"
            }
        )
        
        assert response.status_code == 200


class TestSEOEndpoints:
    """Test SEO-related endpoints"""
    
    def test_seo_analyze_valid_url(self, client, mock_agents):
        """Test SEO analysis with valid URL"""
        response = client.post(
            "/api/seo/analyze",
            json={"url": "https://example.com"}
        )
        
        assert response.status_code == 200
    
    def test_seo_analyze_invalid_url(self, client):
        """Test SEO analysis with invalid URL"""
        response = client.post(
            "/api/seo/analyze",
            json={"url": "not-a-valid-url"}
        )
        
        assert response.status_code == 400
    
    def test_seo_analyze_malicious_url(self, client):
        """Test SEO analysis blocks malicious URLs"""
        response = client.post(
            "/api/seo/analyze",
            json={"url": "javascript:alert(1)"}
        )
        
        assert response.status_code == 400


class TestAgentStatusEndpoint:
    """Test /api/agents endpoint"""
    
    def test_get_agent_status(self, client):
        """Test agent status retrieval"""
        response = client.get("/api/agents")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Check first agent has required fields
        agent = data[0]
        assert "name" in agent
        assert "status" in agent


class TestRateLimiting:
    """Test rate limiting functionality"""
    
    @pytest.mark.skip(reason="Rate limiting requires Redis for proper testing")
    def test_rate_limit_exceeded(self, client, mock_agents):
        """Test rate limiting kicks in after many requests"""
        # Make many requests quickly
        for i in range(110):  # Over the limit of 100
            response = client.post(
                "/api/ask",
                json={"prompt": f"Question {i}"}
            )
            
            if i < 100:
                assert response.status_code == 200
            else:
                assert response.status_code == 429  # Too Many Requests


class TestCORSHeaders:
    """Test CORS configuration"""
    
    def test_cors_headers_present(self, client):
        """Test CORS headers are set correctly"""
        response = client.options("/api/ask")
        
        assert "access-control-allow-origin" in response.headers


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_not_found(self, client):
        """Test 404 handling"""
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404
    
    def test_405_method_not_allowed(self, client):
        """Test method not allowed"""
        response = client.get("/api/ask")  # Should be POST
        assert response.status_code == 405


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
