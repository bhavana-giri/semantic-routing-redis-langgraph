# Project Setup Guide

## Python Environment Setup

This project requires **Python 3.11+** (currently using Python 3.11.13).

### Activate Virtual Environment

```bash
source .venv/bin/activate
```

After activation, verify you're using Python 3.11:
```bash
python --version  # Should show: Python 3.11.13
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Applications

### 1. FastAPI Backend (Banking Chat API)

The backend requires Redis Stack for semantic caching with LangCache.

```bash
# Activate virtual environment first
source .venv/bin/activate

# Run the FastAPI server
python3 -m uvicorn main:app --reload --port 8000
```

API will be available at: `http://localhost:8000`

### 2. Next.js Frontend (Banking Dashboard)

```bash
cd nextjs-app
npm install
npm run dev
```

Frontend will be available at: `http://localhost:3000`

### 3. Semantic Router Demo

The semantic router demo requires **Redis Stack** (not regular Redis).

#### Install Redis Stack (one-time setup):

**Option A: Using Homebrew (Recommended)**
```bash
brew tap redis-stack/redis-stack
brew install redis-stack
```

**Option B: Using Docker**
```bash
docker run -d -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

#### Run Redis Stack:

```bash
# If installed via Homebrew
redis-stack-server

# If using Docker, it's already running from the docker run command above
```

#### Run the Semantic Router Demo:

```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Run the demo
python semantic_router_demo.py
```

## Environment Variables

Create a `.env` file in the project root with:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# LangCache Configuration (optional)
LANGCACHE_HOST=gcp-us-east4.langcache.redis.io
LANGCACHE_CACHE_ID=your_cache_id_here
LANGCACHE_API_KEY=your_langcache_api_key_here

# Redis Configuration (optional, defaults to localhost)
REDIS_URL=redis://localhost:6379
```

## Quick Start (All Services)

### Terminal 1 - Redis Stack:
```bash
redis-stack-server
```

### Terminal 2 - FastAPI Backend:
```bash
source .venv/bin/activate
python3 -m uvicorn main:app --reload --port 8000
```

### Terminal 3 - Next.js Frontend:
```bash
cd nextjs-app
npm run dev
```

### Terminal 4 - Semantic Router Demo (Optional):
```bash
source .venv/bin/activate
python semantic_router_demo.py
```

## Troubleshooting

### "command not found: uvicorn"
Make sure you're in the Python 3.11 virtual environment:
```bash
source .venv/bin/activate
python --version  # Should show 3.11.13
```

### "ModuleNotFoundError" errors
Reinstall dependencies:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### "unknown command 'FT._LIST'" in Redis
You need Redis Stack, not regular Redis. Regular Redis doesn't have the search module.

### Python version issues
This project requires Python 3.11+. Check your version:
```bash
python --version
```

If you're not on Python 3.11, recreate the virtual environment:
```bash
rm -rf .venv
/opt/homebrew/bin/python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Dependencies Summary

### Backend (Python 3.11+)
- FastAPI - Web framework
- Uvicorn - ASGI server
- OpenAI - AI integration
- LangCache - Semantic caching
- RedisVL - Vector search & routing
- Sentence Transformers - Text embeddings

### Frontend (Node.js)
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS

### Infrastructure
- Redis Stack - Vector database & search

