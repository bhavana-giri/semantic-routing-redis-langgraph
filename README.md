# Chat API - FastAPI with OpenAI Integration & LangCache

A minimal FastAPI application that provides a chat endpoint using OpenAI's GPT models with intelligent caching via LangCache.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI API Configuration
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Server

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /chat

Send a chat message and receive an AI-generated response.

**Request Body:**
```json
{
  "userId": "optional_user_id",
  "text": "Your message here"
}
```

**Response:**
```json
{
  "reply": "AI generated response",
  "userId": "optional_user_id"
}
```

### GET /

Health check endpoint.

## Example Usage

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"text": "What services does your bank offer?"}'
```

## 🚀 Caching Features

This API includes intelligent caching using LangCache:

- **Cache Check**: Each query is first checked against the cache using semantic similarity (threshold: 0.8)
- **Cache Hit**: If a similar query exists, returns cached response instantly (no LLM call)
- **Cache Miss**: If no similar query found, calls OpenAI LLM and stores the response
- **Automatic Storage**: All new responses are automatically cached for future queries

### Cache Benefits:
- ⚡ **Faster responses** for repeated/similar queries
- 💰 **Cost savings** by reducing LLM API calls
- 🔄 **Semantic matching** finds similar queries even with different wording

## CORS Configuration

The API is configured to accept requests from `http://localhost:3000` for frontend integration.

## Dependencies

- FastAPI: Web framework
- Uvicorn: ASGI server
- OpenAI: AI model integration
- LangCache: Intelligent semantic caching
- Python-dotenv: Environment variable management
- Pydantic: Data validation
