# Guardrails

The AI Project includes comprehensive guardrails to ensure safe, appropriate, and high-quality agent outputs.

## Features

### Content Filtering
- **Harmful Content Detection**: Blocks requests and responses containing patterns related to:
  - Violence and self-harm
  - Weapons and explosives
  - Hacking and security exploits
  - Fraud and theft
- **Custom Patterns**: Easily extensible with regex patterns

### Input Validation
- **Length Constraints**: Enforces minimum (1 char) and maximum (5000 char) content length
- **Format Sanitization**: Removes excessive whitespace, control characters, and repeated punctuation
- **Empty Input Protection**: Rejects empty or whitespace-only inputs

### Output Validation
- **Quality Checks**: Ensures agents don't produce empty responses
- **Harmful Content Screening**: Validates all agent outputs before returning to users
- **Length Management**: Automatically truncates overly long responses with ellipsis

### PII Detection
- **Pattern Recognition**: Detects potential personally identifiable information:
  - Email addresses
  - Phone numbers
  - Social Security Numbers
  - Credit card numbers
- **Warning System**: Logs PII detections without blocking (may be intentional context)

### Rate Limiting
- **Request Throttling**: Limits requests per IP to prevent abuse
  - Default: 100 requests per 60-second window
  - Configurable via environment variables
- **User-based Tracking**: Per-IP rate limit enforcement

### URL Validation
- **Protocol Checking**: Only allows http:// and https:// URLs
- **Suspicious Pattern Detection**: Blocks javascript:, data:, file:, and vbscript: protocols
- **Length Limits**: Rejects URLs over 2000 characters

### Follow-up Validation
- **Question Quality**: Ensures follow-up suggestions are:
  - Between 10-200 characters
  - Properly formatted as questions
  - Free from harmful content

## Configuration

Guardrails can be configured in `config.py` or via environment variables:

```python
# .env or environment variables
GUARDRAILS_ENABLED=true
GUARDRAILS_MAX_LENGTH=5000
GUARDRAILS_MIN_LENGTH=1
GUARDRAILS_CONTENT_FILTER=true
GUARDRAILS_PII_DETECTION=true
GUARDRAILS_RATE_LIMITING=true
GUARDRAILS_RATE_LIMIT_REQUESTS=100
GUARDRAILS_RATE_LIMIT_WINDOW=60
```

## Integration Points

### Agent Level
- **ContentAgent**: Validates inputs and outputs, sanitizes prompts
- **EngagementAgent**: Validates follow-up suggestions for quality and safety

### API Level
- **Request Validation**: All API endpoints validate inputs before processing
- **Rate Limiting**: Per-IP throttling on /api/ask and other endpoints
- **URL Validation**: SEO and content endpoints validate URLs

## Testing

Run the guardrails test suite:

```powershell
python -m pytest tests/test_guardrails.py -v
```

Tests cover:
- Valid and invalid inputs
- Harmful content detection
- Length constraints
- Output validation
- PII detection
- Rate limiting
- URL validation
- Follow-up validation

## Error Handling

### Input Violations
Return HTTP 400 with clear error messages:
```json
{
  "detail": "Input too long (maximum 5000 characters)"
}
```

### Output Violations
Agents catch `GuardrailViolation` exceptions and return safe fallback responses:
```python
"I apologize, but I cannot provide that response. Please try rephrasing your question."
```

### Rate Limit Violations
Return HTTP 400:
```json
{
  "detail": "Rate limit exceeded. Please try again later."
}
```

## Extending Guardrails

### Add Custom Harmful Patterns

Edit `services/guardrails.py`:

```python
HARMFUL_PATTERNS = [
    # Existing patterns...
    r'\byour_custom_pattern\b',
]
```

### Add Custom PII Patterns

```python
PII_PATTERNS = {
    'email': r'...',
    'your_pattern': r'\byour_regex\b',
}
```

### Adjust Rate Limits

For specific endpoints, override in the route:

```python
@router.post("/special")
async def special_endpoint(request: Request):
    custom_guardrails = Guardrails(rate_limit_requests=10)
    is_valid, error = custom_guardrails.validate_input(...)
```

## Monitoring

Guardrails log all violations:

```
WARNING - Harmful content detected: make a bomb
WARNING - Invalid follow-up generated: too short
ERROR - Agent produced harmful content: ...
```

Check `logs/app.log` for guardrail activity.

## Best Practices

1. **Always validate at API level first**: Fail fast before expensive agent operations
2. **Use specific error messages**: Help users understand what went wrong
3. **Log violations**: Track patterns for improving guardrails
4. **Test edge cases**: Ensure legitimate content isn't blocked
5. **Review PII warnings**: Assess if intentional or accidental exposure
6. **Tune rate limits**: Balance abuse prevention with user experience
7. **Extend patterns carefully**: Test new patterns to avoid false positives

## Performance Impact

- **Input Validation**: ~1-2ms per request
- **Output Validation**: ~2-3ms per response
- **Rate Limiting**: ~0.1ms (in-memory lookup)
- **Content Filtering**: ~1-3ms (regex matching)

Total overhead: typically <10ms per request/response cycle.
