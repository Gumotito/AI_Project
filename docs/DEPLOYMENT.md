# Deployment Guide

Complete guide for deploying the AI Project to production.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Health Checks](#health-checks)
7. [Monitoring](#monitoring)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- Python 3.13+
- Docker 24.0+ and Docker Compose 2.0+
- Git
- Ollama (for local LLM)

### Optional (Production)
- Redis (for caching and rate limiting)
- Nginx (reverse proxy)
- Certbot (SSL certificates)

---

## Local Development

### 1. Clone Repository
```powershell
git clone <repository-url>
cd AI_Project
```

### 2. Create Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

### 4. Configure Environment
Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```

Edit `.env` with your configuration:
```env
OPENAI_API_KEY=your_key_here
OLLAMA_BASE_URL=http://127.0.0.1:11434
DEBUG=True
```

### 5. Start Ollama
```powershell
ollama serve
ollama pull qwen2.5:14b
```

### 6. Run Application
```powershell
python app.py
# Or with uvicorn directly:
uvicorn app:app --reload
```

### 7. Access Application
- Web UI: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

---

## Docker Deployment

### Quick Start
```powershell
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

### Services Included
- **web**: FastAPI application (port 8000)
- **ollama**: Local LLM server (port 11434)
- **redis**: Caching and rate limiting (port 6379)

### Custom Configuration
Create `docker-compose.override.yml`:
```yaml
version: '3.8'

services:
  web:
    environment:
      - DEBUG=False
      - LANGCHAIN_API_KEY=your_key
    ports:
      - "80:8000"
```

---

## Production Deployment

### Architecture Overview
```
Internet
   │
   ├──> Nginx (SSL, Load Balancer)
   │       │
   │       └──> FastAPI (Docker)
   │               │
   │               ├──> Ollama (Docker)
   │               ├──> Redis (Docker)
   │               └──> LangSmith (Cloud)
```

### 1. Server Setup (Ubuntu/Debian)

#### Install Docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

#### Install Docker Compose
```bash
sudo apt-get update
sudo apt-get install docker-compose-plugin
```

### 2. Prepare Application

#### Clone Repository
```bash
git clone <repository-url>
cd AI_Project
```

#### Configure Production Environment
```bash
cp .env.example .env
nano .env  # Edit with production values
```

**Critical Production Settings**:
```env
# Security
DEBUG=False
SECRET_KEY=<generate-strong-secret>
ENVIRONMENT=production

# Database (if using)
DATABASE_URL=postgresql://user:pass@localhost/aiproject

# Redis
REDIS_URL=redis://redis:6379

# Monitoring
SENTRY_DSN=your_sentry_dsn
LANGCHAIN_API_KEY=your_langsmith_key

# LLM
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=qwen2.5:14b

# Guardrails
GUARDRAILS_ENABLED=true
GUARDRAILS_RATE_LIMITING=true
```

### 3. SSL Certificate (HTTPS)

#### Using Let's Encrypt
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### 4. Nginx Configuration

Create `/etc/nginx/sites-available/aiproject`:
```nginx
upstream aiproject {
    server localhost:8000;
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        proxy_pass http://aiproject;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # WebSocket support (if needed)
    location /ws {
        proxy_pass http://aiproject;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Static files (optional caching)
    location /static {
        proxy_pass http://aiproject;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/aiproject /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. Start Production Services
```bash
docker-compose -f docker-compose.yml up -d
```

### 6. Verify Deployment
```bash
# Check services
docker-compose ps

# Check logs
docker-compose logs -f web

# Test health endpoint
curl https://yourdomain.com/health

# Test API
curl -X POST https://yourdomain.com/api/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test question"}'
```

---

## Environment Configuration

### Required Variables
| Variable | Description | Example |
|----------|-------------|---------|
| `DEBUG` | Debug mode | `False` |
| `HOST` | Bind host | `0.0.0.0` |
| `PORT` | Bind port | `8000` |
| `OLLAMA_BASE_URL` | Ollama endpoint | `http://ollama:11434` |
| `OLLAMA_MODEL` | LLM model | `qwen2.5:14b` |

### Optional Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `REDIS_URL` | Redis connection | None (in-memory) |
| `SECRET_KEY` | JWT secret | Random |
| `LANGCHAIN_API_KEY` | LangSmith key | None |
| `SENTRY_DSN` | Error tracking | None |

### Guardrails Configuration
| Variable | Description | Default |
|----------|-------------|---------|
| `GUARDRAILS_ENABLED` | Enable filtering | `true` |
| `GUARDRAILS_MAX_LENGTH` | Max input length | `5000` |
| `GUARDRAILS_RATE_LIMITING` | Enable rate limits | `true` |
| `GUARDRAILS_RATE_LIMIT_REQUESTS` | Requests per window | `100` |
| `GUARDRAILS_RATE_LIMIT_WINDOW` | Window in seconds | `60` |

---

## Health Checks

### Endpoints

#### `/health` - System Health
Returns overall system status:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "ollama": "healthy",
    "api": "healthy"
  }
}
```

#### `/ready` - Readiness Probe
Returns 200 when ready to serve requests:
```json
{
  "status": "ready"
}
```

### Docker Health Checks
Configured in `docker-compose.yml`:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

---

## Monitoring

### Application Metrics
Access Prometheus metrics at `/metrics` (if enabled)

### Logging
- **Location**: `logs/` directory
- **Format**: JSON structured logs
- **Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL

### LangSmith Tracing
View all LLM interactions at https://smith.langchain.com/

---

## Troubleshooting

### Issue: "Connection refused" to Ollama
**Solution**: Ensure Ollama is running
```bash
docker-compose logs ollama
docker-compose restart ollama
```

### Issue: "Request timeout"
**Solution**: Increase timeout or check LLM performance
```env
# In .env
OLLAMA_REQUEST_TIMEOUT=60
```

### Issue: Out of memory
**Solution**: Limit Docker memory usage
```yaml
# In docker-compose.yml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 4G
```

### Issue: Port already in use
**Solution**: Change port mapping
```yaml
# In docker-compose.yml
services:
  web:
    ports:
      - "8080:8000"  # Use 8080 instead
```

### Issue: SSL certificate errors
**Solution**: Renew Let's Encrypt certificates
```bash
sudo certbot renew
sudo systemctl reload nginx
```

### Viewing Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web

# Last 100 lines
docker-compose logs --tail=100 web
```

### Restarting Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart web

# Full rebuild
docker-compose down
docker-compose up -d --build
```

---

## Backup and Recovery

### Backup Configuration
```bash
# Backup .env
cp .env .env.backup

# Backup logs
tar -czf logs-backup-$(date +%Y%m%d).tar.gz logs/
```

### Database Backup (if using)
```bash
docker-compose exec db pg_dump -U user dbname > backup.sql
```

### Restore
```bash
# Restore .env
cp .env.backup .env

# Restart services
docker-compose down
docker-compose up -d
```

---

## Performance Tuning

### Uvicorn Workers
For production, use multiple workers:
```yaml
# docker-compose.yml
services:
  web:
    command: uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Redis Caching
Enable Redis for better performance:
```env
REDIS_URL=redis://redis:6379
```

### Nginx Caching
Add caching to Nginx configuration:
```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g;

location /api {
    proxy_cache api_cache;
    proxy_cache_valid 200 5m;
    proxy_cache_key "$request_uri";
}
```

---

## Security Checklist

- [ ] Change default `SECRET_KEY`
- [ ] Set `DEBUG=False` in production
- [ ] Enable HTTPS with valid certificate
- [ ] Configure firewall (allow only 80, 443, 22)
- [ ] Enable guardrails and rate limiting
- [ ] Use strong passwords for services
- [ ] Keep Docker images updated
- [ ] Monitor logs for suspicious activity
- [ ] Implement authentication (JWT)
- [ ] Regular security audits with `bandit` and `safety`

---

## Support

For issues and questions:
- GitHub Issues: <repository-url>/issues
- Documentation: See `docs/` directory
- LangSmith Support: https://docs.smith.langchain.com/

