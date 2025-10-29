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
pytest
```

## API Endpoints

- `GET /` - Main dashboard
- `GET /api/agents` - List all agents and their status
- `POST /api/seo/analyze` - Trigger SEO analysis
- `POST /api/content/generate` - Generate content
- `POST /api/monetization/analyze` - Analyze revenue
- `POST /api/uiux/audit` - Run UX audit
- `GET /api/oversight/health` - Get overall site health

## Configuration

Key settings in `config.py`:
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `DEBUG`: Debug mode (default: True)
- `AGENT_TIMEOUT`: Agent operation timeout in seconds
- `MAX_CONCURRENT_AGENTS`: Maximum concurrent agent operations

## Future Enhancements

- [ ] Integrate with LLM APIs (OpenAI, Anthropic)
- [ ] Add database persistence for agent insights
- [ ] Implement real-time monitoring dashboard
- [ ] Add authentication and user management
- [ ] Create scheduled agent tasks
- [ ] Build agent learning and improvement system
- [ ] Add comprehensive test coverage

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
