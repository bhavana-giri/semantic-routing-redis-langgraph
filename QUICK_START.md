# Quick Start Guide - Banking AI Assistant

## 🚀 Get Running in 5 Minutes

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (for Redis Stack)

### Step 1: Clone & Setup Python (2 min)
```bash
cd /path/to/bank_langcache

# Create virtual environment with Python 3.11
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Start Redis Stack (1 min)
```bash
docker run -d --name redis-stack -p 6380:6379 -p 8001:8001 redis/redis-stack:latest
```

### Step 3: Configure Environment (30 sec)
Create `.env` file:
```env
OPENAI_API_KEY=sk-your-key-here
REDIS_URL=redis://localhost:6380
USE_LANGCACHE=false
```

### Step 4: Start Backend (30 sec)
```bash
source .venv/bin/activate
python3 -m uvicorn main:app --reload --port 8000
```

Backend running at: `http://localhost:8000`

### Step 5: Start Frontend (1 min)
```bash
# New terminal
cd nextjs-app
npm install
npm run dev
```

Frontend running at: `http://localhost:3000`

## ✅ You're Done!

Open `http://localhost:3000` and start chatting!

## 💬 Try These Queries

1. **Loan**: "I need a personal loan"
2. **Credit Card**: "I want a credit card"
3. **FD**: "Tell me about fixed deposit rates"
4. **Forex**: "I need USD for my trip"
5. **Fraud**: "Someone used my card without permission"
6. **Policy**: "What are your branch timings?"

## 🔍 Check If Everything Works

### Test Router
```bash
python3 router_bank.py
```

### Test Orchestrator
```bash
python3 orchestrator.py
```

### Test API
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "I need a loan"}'
```

## 🛠️ Troubleshooting

### Redis Not Running?
```bash
docker ps | grep redis-stack
# If not running:
docker start redis-stack
```

### Python Version Wrong?
```bash
python3 --version  # Should be 3.11+
# If not, use: python3.11 or install from python.org
```

### Port Already in Use?
```bash
# Backend on different port:
uvicorn main:app --reload --port 8001

# Frontend on different port:
PORT=3001 npm run dev
```

### Import Errors?
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## 📊 What You Get

- **Smart Routing**: Automatically understands user intent
- **Slot Filling**: Asks follow-up questions to collect info
- **6 Banking Tools**: Loans, Cards, FD, Forex, Fraud, Policy
- **Beautiful UI**: Modern glassmorphism design
- **Session Management**: Maintains conversation context
- **Optional Caching**: Enable with `USE_LANGCACHE=true`

## 📚 Next Steps

- Read [README.md](README.md) for detailed documentation
- See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for architecture
- Check [SETUP.md](SETUP.md) for advanced configuration

## 🎯 Key Features Enabled

✅ Semantic query routing  
✅ Conversational slot filling  
✅ Banking tool execution  
✅ EMI calculation  
✅ Card recommendations  
✅ FD ladder planning  
✅ Forex rates  
✅ Fraud handling  
✅ Policy search  
✅ Beautiful modern UI  
✅ Session persistence  
✅ LangCache ready (disabled by default)

Enjoy your intelligent banking assistant! 🏦🤖

