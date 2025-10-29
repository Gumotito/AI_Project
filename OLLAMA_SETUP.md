# Ollama Setup Guide for AI_Project

## 🚀 Quick Start

### 1. Install Ollama

**Windows:**
Download from https://ollama.com/download

**Verify Installation:**
```powershell
ollama --version
```

### 2. Start Ollama Server

```powershell
ollama serve
```

Leave this running in a terminal window.

### 3. Pull Recommended Models

**For best quality (recommended for your 5 agents):**
```powershell
ollama pull qwen2.5:32b
```

**Alternative options:**

**Fast & Efficient:**
```powershell
ollama pull qwen2.5:14b
```

**Maximum Quality (requires powerful GPU):**
```powershell
ollama pull llama3.3:70b
```

**Lightweight (for testing):**
```powershell
ollama pull llama3.1:8b
```

### 4. Test Ollama

```powershell
ollama run qwen2.5:32b "Hello! Can you help me with SEO?"
```

### 5. Configure AI_Project

Edit `config.py` if you want to change models:
```python
OLLAMA_MODEL: str = "qwen2.5:32b"  # Change to your preferred model
```

### 6. Test Integration

```powershell
python test_ollama.py
```

## 📊 Model Comparison

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **qwen2.5:32b** | ~20GB | Medium | Excellent | **Recommended for all agents** |
| qwen2.5:14b | ~8GB | Fast | Very Good | Fast responses, good quality |
| llama3.3:70b | ~40GB | Slow | Best | Maximum quality analysis |
| llama3.1:8b | ~4GB | Very Fast | Good | Testing, simple tasks |

## 🛠️ Configuration Options

### Change Model in `config.py`:

```python
# Use different model
OLLAMA_MODEL: str = "qwen2.5:14b"

# Adjust temperature (0.0 = focused, 1.0 = creative)
OLLAMA_TEMPERATURE: float = 0.7

# Increase context window
OLLAMA_NUM_CTX: int = 16384  # Larger context for more history
```

### Switch Between Local and Cloud:

```python
# Use Ollama (local)
USE_LOCAL_LLM: bool = True

# Use OpenAI (cloud)
USE_LOCAL_LLM: bool = False
OPENAI_API_KEY: str = "sk-..."
```

## 🔧 Troubleshooting

### Ollama Not Found
```powershell
# Make sure Ollama is in PATH
ollama --version

# If not, reinstall from https://ollama.com/download
```

### Connection Refused
```powershell
# Start Ollama server
ollama serve

# Check if running
curl http://localhost:11434/api/tags
```

### Out of Memory
- Use smaller model (qwen2.5:14b or llama3.1:8b)
- Close other applications
- Reduce `OLLAMA_NUM_CTX` in config

### Slow Responses
- Use smaller model
- Ensure GPU drivers are updated
- Check CPU/GPU usage

## 🎯 Recommended Setup for Your Use Case

For **5 agents with web search tools**, I recommend:

```python
# config.py
OLLAMA_MODEL: str = "qwen2.5:32b"  # Best balance
OLLAMA_TEMPERATURE: float = 0.7    # Good creativity
OLLAMA_NUM_CTX: int = 8192         # Sufficient context
USE_LOCAL_LLM: bool = True         # Keep data local
ENABLE_TOOLS: bool = True          # Enable web search
```

**Why qwen2.5:32b:**
- Excellent at tool calling (critical for your agents)
- Strong reasoning for complex workflows
- Good balance of speed and quality
- Native function calling support
- Handles multiple tool calls well

## 📈 Performance Tips

1. **First Run is Slow**: Model loads into memory (30-60 seconds)
2. **Subsequent Calls Faster**: Model stays in memory
3. **GPU vs CPU**: GPU is 10-50x faster
4. **Context Size**: Larger context = slower but more aware
5. **Temperature**: Lower for factual tasks, higher for creative

## 🔄 Updating Models

```powershell
# Pull latest version
ollama pull qwen2.5:32b

# List installed models
ollama list

# Remove old model
ollama rm old-model-name
```

## 🌐 Using Multiple Models

You can switch models per agent:

```python
# In agent initialization
seo_llm = LLMService()  # Uses qwen2.5:32b
content_llm = LLMService()  # Could use different model
```

## 🔗 Resources

- **Ollama Docs**: https://github.com/ollama/ollama
- **Model Library**: https://ollama.com/library
- **Qwen2.5 Info**: https://ollama.com/library/qwen2.5
- **Community**: https://discord.gg/ollama

## ✅ Verification Checklist

Before running agents:
- [ ] Ollama installed and in PATH
- [ ] Ollama server running (`ollama serve`)
- [ ] Model downloaded (`ollama pull qwen2.5:32b`)
- [ ] Test successful (`ollama run qwen2.5:32b "test"`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Test script passes (`python test_ollama.py`)

## 🚨 Common Issues

**"Model not found"**
```powershell
ollama pull qwen2.5:32b
```

**"Connection refused"**
```powershell
ollama serve
```

**"Out of memory"**
```python
# Use smaller model
OLLAMA_MODEL: str = "qwen2.5:14b"
```

**"Too slow"**
```python
# Use faster model
OLLAMA_MODEL: str = "llama3.1:8b"
```

Now you're ready to run AI agents with local LLMs! 🎉
