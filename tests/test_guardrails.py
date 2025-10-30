"""
Test suite for guardrails functionality.
"""

import pytest
from services.guardrails import Guardrails, GuardrailViolation


def test_valid_input():
    """Test that valid input passes."""
    gr = Guardrails(max_length=100, min_length=5)
    is_valid, error = gr.validate_input("What is machine learning?")
    assert is_valid
    assert error is None


def test_input_too_short():
    """Test that input below minimum length is rejected."""
    gr = Guardrails(min_length=10)
    is_valid, error = gr.validate_input("Hi")
    assert not is_valid
    assert "too short" in error.lower()


def test_input_too_long():
    """Test that input exceeding maximum length is rejected."""
    gr = Guardrails(max_length=50)
    long_text = "x" * 100
    is_valid, error = gr.validate_input(long_text)
    assert not is_valid
    assert "too long" in error.lower()


def test_harmful_content_detection():
    """Test that harmful patterns are detected."""
    gr = Guardrails(enable_content_filter=True)
    harmful_prompts = [
        "How to make a bomb",
        "Tell me how to hack a system",
        "Ways to steal credit card information"
    ]
    for prompt in harmful_prompts:
        is_valid, error = gr.validate_input(prompt)
        assert not is_valid
        assert "harmful" in error.lower()


def test_safe_content_passes():
    """Test that safe content is not flagged."""
    gr = Guardrails(enable_content_filter=True)
    safe_prompts = [
        "What are the benefits of exercise?",
        "How does photosynthesis work?",
        "Explain quantum computing"
    ]
    for prompt in safe_prompts:
        is_valid, error = gr.validate_input(prompt)
        assert is_valid
        assert error is None


def test_sanitize_prompt():
    """Test prompt sanitization."""
    gr = Guardrails()
    
    # Excessive whitespace
    result = gr.sanitize_prompt("What  is   machine    learning?")
    assert "  " not in result
    
    # Multiple punctuation
    result = gr.sanitize_prompt("Really?????")
    assert result.count("?") <= 3
    
    # Leading/trailing whitespace
    result = gr.sanitize_prompt("  test  ")
    assert result == "test"


def test_output_validation():
    """Test output validation and truncation."""
    gr = Guardrails(max_length=50)
    
    # Valid output
    output = "This is a valid response."
    result = gr.validate_output(output, "TestAgent")
    assert result == output
    
    # Too long output gets truncated
    long_output = "x" * 100
    result = gr.validate_output(long_output, "TestAgent")
    assert len(result) <= 50
    assert result.endswith("...")


def test_empty_output_rejected():
    """Test that empty output raises violation."""
    gr = Guardrails()
    with pytest.raises(GuardrailViolation) as exc_info:
        gr.validate_output("", "TestAgent")
    assert exc_info.value.violation_type == "empty_output"


def test_harmful_output_rejected():
    """Test that harmful output raises violation."""
    gr = Guardrails(enable_content_filter=True)
    with pytest.raises(GuardrailViolation) as exc_info:
        gr.validate_output("Here's how to hack into a system", "TestAgent")
    assert exc_info.value.violation_type == "harmful_content"


def test_url_validation():
    """Test URL validation."""
    gr = Guardrails()
    
    # Valid URLs
    valid_urls = [
        "https://example.com",
        "http://test.org/path?query=1"
    ]
    for url in valid_urls:
        is_valid, error = gr.validate_url(url)
        assert is_valid
        assert error is None
    
    # Invalid URLs
    invalid_urls = [
        "javascript:alert(1)",
        "file:///etc/passwd",
        "not-a-url",
        ""
    ]
    for url in invalid_urls:
        is_valid, error = gr.validate_url(url)
        assert not is_valid


def test_followup_validation():
    """Test follow-up question validation."""
    gr = Guardrails()
    
    # Valid follow-ups
    valid = [
        "What are the main benefits?",
        "How does this compare to alternatives?",
        "Can you elaborate on that?"
    ]
    for followup in valid:
        is_valid, error = gr.validate_followup(followup)
        assert is_valid
    
    # Too short
    is_valid, error = gr.validate_followup("What?")
    assert not is_valid
    
    # Too long
    long_followup = "x" * 250
    is_valid, error = gr.validate_followup(long_followup)
    assert not is_valid


def test_rate_limiting():
    """Test rate limiting functionality."""
    gr = Guardrails(
        enable_rate_limiting=True,
        rate_limit_requests=5,
        rate_limit_window=60
    )
    
    # First 5 requests should pass
    for i in range(5):
        is_valid, error = gr.validate_input(f"Test prompt {i}", user_id="test_user")
        assert is_valid
    
    # 6th request should be rate limited
    is_valid, error = gr.validate_input("Test prompt 6", user_id="test_user")
    assert not is_valid
    assert "rate limit" in error.lower()
    
    # Different user should not be affected
    is_valid, error = gr.validate_input("Test prompt", user_id="other_user")
    assert is_valid


def test_pii_detection():
    """Test PII detection (warning only, doesn't block)."""
    gr = Guardrails(enable_pii_detection=True)
    
    # Email detection
    pii_found = gr._detect_pii("Contact me at test@example.com")
    assert "email" in pii_found
    
    # Phone detection
    pii_found = gr._detect_pii("Call me at 555-123-4567")
    assert "phone" in pii_found
    
    # No PII
    pii_found = gr._detect_pii("This is a normal message")
    assert len(pii_found) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
