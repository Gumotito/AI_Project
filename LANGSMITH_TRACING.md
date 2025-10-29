# LangSmith Tracing Integration

## Overview

Your AI Project is now fully integrated with **LangSmith** for comprehensive agent tracing and monitoring. Every agent operation is automatically traced and logged to your LangSmith dashboard.

## What's Traced

All agent operations are automatically traced, including:

### SEO Agent
- `analyze_seo()` - SEO analysis operations
- `generate_keywords()` - Keyword generation
- `optimize_meta_tags()` - Meta tag optimization
- `get_recommendations()` - SEO recommendations

### Content Agent
- Content generation
- Readability analysis
- Topic suggestions
- Plagiarism checking

### Monetization Agent
- Revenue analysis
- Ad placement optimization
- Pricing recommendations
- Conversion tracking

### UI/UX Agent
- User flow analysis
- Accessibility audits
- Performance monitoring
- Design recommendations

### Oversight Agent
- Overall health analysis
- Agent coordination
- Report generation
- Strategy suggestions

## Viewing Traces

1. **Visit your LangSmith Dashboard**: https://smith.langchain.com/
2. **Select Project**: `AI_Project`
3. **View Traces**: All agent operations will appear in real-time

## Trace Information Includes

- **Operation Name**: What the agent was doing
- **Inputs/Outputs**: All parameters and return values
- **Timing**: Duration of each operation
- **Metadata**: Agent type, action, and custom tags
- **Errors**: Full stack traces if operations fail
- **Chain Structure**: How agents coordinate with each other

## Configuration

LangSmith is configured in `config.py`:
```python
LANGCHAIN_TRACING_V2 = "true"
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")  # Set via environment variable
LANGCHAIN_PROJECT = "AI_Project"
LANGCHAIN_ENDPOINT = "https://api.smith.langchain.com"
```

## Testing Tracing

Run the test script to verify tracing is working:
```powershell
python test_tracing.py
```

This will:
1. Initialize agents
2. Run sample operations
3. Send traces to LangSmith
4. Display results

## Adding Tracing to New Agent Methods

Use the `@trace_agent` decorator:

```python
from services.langsmith_service import trace_agent

@trace_agent(
    name="My Custom Operation",
    metadata={"agent": "my_agent", "action": "custom"}
)
async def my_operation(self, param: str):
    # Your code here
    return result
```

## Benefits

✅ **Debug Issues**: See exactly what went wrong and where
✅ **Optimize Performance**: Identify slow operations
✅ **Monitor Costs**: Track LLM token usage
✅ **Improve Agents**: A/B test different prompts
✅ **Production Monitoring**: Real-time alerts and dashboards
✅ **Audit Trail**: Complete history of all operations

## Dashboard Features

Your LangSmith dashboard shows:
- Real-time operation feed
- Performance metrics
- Cost analysis
- Error rates
- Custom filters and searches
- Shareable trace links
- Comparison tools

## Next Steps

1. **Add LLM Calls**: When you integrate OpenAI/Anthropic, their calls will be automatically traced
2. **Set Up Alerts**: Configure notifications for errors or slow operations
3. **Create Datasets**: Build test datasets for agent evaluation
4. **Run Experiments**: Compare different agent implementations

## Troubleshooting

If traces aren't appearing:
1. Check your API key is correct
2. Verify network connectivity to api.smith.langchain.com
3. Look for errors in `logs/app.log`
4. Run `python test_tracing.py` to diagnose

## Learn More

- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Tracing Best Practices](https://docs.smith.langchain.com/tracing)
- [Agent Monitoring Guide](https://docs.smith.langchain.com/monitoring)
