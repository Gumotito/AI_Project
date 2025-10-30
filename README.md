# AI Project

An intelligent, agent-managed website platform powered by specialized AI agents with **full LangSmith tracing integration**.

## Overview

AI Project is a Python-based web application that uses multiple AI agents to manage, optimize, and improve different aspects of a website:

- **SEO Agent**: Handles search engine optimization, keyword research, and meta tag optimization
- **Content Agent**: Manages content creation, improvement, and quality control
- **Monetization Agent**: Optimizes revenue streams, ad placement, and pricing strategies
- **UI/UX Agent**: Analyzes and improves user interface, accessibility, and user experience
- **Oversight Agent**: Coordinates all agents and provides strategic recommendations

## 🔍 LangSmith Tracing

**All agent operations are automatically traced** to your LangSmith dashboard for:
- Real-time monitoring and debugging
- Performance analysis and optimization
- Cost tracking and management
- Quality assurance and testing

📊 **View your traces**: https://smith.langchain.com/ (Project: `AI_Project`)

See [LANGSMITH_TRACING.md](LANGSMITH_TRACING.md) for detailed documentation.

## Project Structure

```
AI_Project/
├── agents/              # AI agent modules
│   ├── agent_seo.py
│   ├── agent_content.py
│   ├── agent_monetization.py
│   ├── agent_uiux.py
│   └── agent_oversight.py
├── routes/              # API and web routes
├── services/            # Business logic services
├── templates/           # HTML templates
├── static/              # CSS, JS, images
├── logs/                # Application logs
├── app.py              # Main application
├── config.py           # Configuration
└── requirements.txt    # Python dependencies
```

## Setup

1. **Create a virtual environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_api_key_here
   DEBUG=True
   PORT=8000
   ```

4. **Run the application**:
   ```powershell
   python app.py
   ```

   Or use uvicorn directly:
   ```powershell
   uvicorn app:app --reload
   ```

5. **Access the application**:
   Open your browser to `http://localhost:8000`

## Development

### Adding New Features

Each agent is modular and can be extended independently. To add functionality:

1. Locate the appropriate agent in `agents/`
2. Add new methods following the async pattern
3. Update the agent's API routes in `routes/api_routes.py`
4. Document changes in this README

### Testing

Run tests with pytest:
```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_agents.py -v
```

**Test Coverage**: Unit tests for agents, API integration tests, and guardrails validation.

## API Endpoints

### Q&A Interface
- `POST /api/ask` - Ask a question, get AI answer with sources
- `POST /api/ask/suggest` - Get follow-up question suggestions

### Agent Management
- `GET /api/agents` - List all agents and their status
- `GET /health` - System health check
- `GET /ready` - Readiness probe

### SEO Operations
- `POST /api/seo/analyze` - Analyze page SEO
- `POST /api/seo/keywords` - Generate keywords
- `GET /api/seo/recommendations` - Get SEO recommendations

### Content Operations
- `POST /api/content/generate` - Generate content
- `POST /api/content/analyze` - Analyze content quality
- `GET /api/content/topics/{category}` - Get topic suggestions

### Monetization
- `GET /api/monetization/revenue/{timeframe}` - Revenue analysis
- `GET /api/monetization/strategies` - Get monetization strategies
- `POST /api/monetization/ad-placement` - Optimize ad placement

### UI/UX Operations
- `POST /api/uiux/analyze-flow` - Analyze user flow
- `POST /api/uiux/accessibility` - Check accessibility
- `GET /api/uiux/design-suggestions` - Get design recommendations
- `POST /api/uiux/performance` - Performance audit

### Oversight
- `GET /api/oversight/health` - Overall system health
- `GET /api/oversight/report/{type}` - Generate reports
- `GET /api/oversight/priorities` - Get priority tasks
- `POST /api/oversight/strategy` - Strategy suggestions

**Full API Documentation**: Available at `/docs` (Swagger UI) or `/redoc` (ReDoc)

## Configuration

Key settings in `config.py` (override with `.env`):

### Application
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `DEBUG`: Debug mode (default: True)
- `ENVIRONMENT`: Environment (development/production)

### LLM
- `OLLAMA_BASE_URL`: Ollama endpoint (default: http://127.0.0.1:11434)
- `OLLAMA_MODEL`: Model name (default: qwen2.5:14b)
- `OLLAMA_TEMPERATURE`: Generation temperature (default: 0.7)
- `OLLAMA_NUM_CTX`: Context window size (default: 8192)

### Guardrails (Safety & Security)
- `GUARDRAILS_ENABLED`: Enable content filtering (default: true)
- `GUARDRAILS_MAX_LENGTH`: Max input length (default: 5000)
- `GUARDRAILS_CONTENT_FILTER`: Filter harmful content (default: true)
- `GUARDRAILS_PII_DETECTION`: Detect PII in outputs (default: true)
- `GUARDRAILS_RATE_LIMITING`: Enable rate limiting (default: true)
- `GUARDRAILS_RATE_LIMIT_REQUESTS`: Requests per window (default: 100)
- `GUARDRAILS_RATE_LIMIT_WINDOW`: Time window in seconds (default: 60)

See [`.env.example`](.env.example) for full configuration options.

## Documentation

- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment instructions
- **[Guardrails](docs/GUARDRAILS.md)** - Content filtering and safety features
- **[LangSmith Tracing](LANGSMITH_TRACING.md)** - Observability and monitoring
- **[Ollama Setup](OLLAMA_SETUP.md)** - Local LLM configuration
- **[Project Review](PROJECT_REVIEW.md)** - Comprehensive improvement recommendations

## Docker Deployment

### Quick Start
```powershell
# Start all services (web + ollama + redis)
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

### Production Deployment
See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for complete production setup including:
- SSL configuration
- Nginx reverse proxy
- Health checks and monitoring
- Security hardening
- Performance tuning

## CI/CD

Automated CI/CD pipeline runs on push:
- ✅ Unit tests with coverage
- ✅ Code quality checks (black, flake8, mypy)
- ✅ Security scanning (bandit, safety)
- ✅ Docker image build

See [`.github/workflows/ci.yml`](.github/workflows/ci.yml)

## Features

### ✅ Implemented
- Multi-agent architecture (6 specialized agents)
- Q&A interface with web search integration
- LangSmith tracing for all operations
- Comprehensive guardrails (content filtering, PII detection, rate limiting)
- Follow-up question suggestions
- Async/await design for performance
- Docker containerization
- Health check endpoints
- Structured logging

### 🚧 In Progress
- Agent method implementations (26+ TODOs)
- Authentication (JWT)
- Redis caching layer
- Background task queue (Celery)

### 📋 Planned
- Database persistence
- Real-time monitoring dashboard
- Advanced analytics
- A/B testing framework
- Multi-region deployment

See [PROJECT_REVIEW.md](PROJECT_REVIEW.md) for detailed roadmap.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests (`pytest`)
4. Run linters (`black . && flake8 .`)
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

MIT License

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/AI_Project/issues)
- **Documentation**: See `docs/` directory
- **LangSmith**: https://docs.smith.langchain.com/
