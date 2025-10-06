# RedisVL MessageHistory Integration 📚

## Overview

The system now uses **RedisVL's MessageHistory** class for conversation tracking, providing a production-ready, structured approach to storing and retrieving chat history.

Reference: [RedisVL Message History API](https://redis.io/docs/latest/develop/ai/redisvl/api/message_history/)

## Why RedisVL MessageHistory?

✅ **Production-ready**: Official Redis library, tested and maintained  
✅ **Structured storage**: Messages stored as HASHes with metadata  
✅ **Automatic timestamping**: Sequential ordering built-in  
✅ **Session isolation**: Each session_id has separate history  
✅ **Rich metadata**: Store intent, score, and custom fields  
✅ **Easy retrieval**: `get_recent()` method for context  

## Implementation

### memory/history.py

```python
from redisvl.extensions.llmcache import MessageHistory

def get_history(session_id: str) -> MessageHistory:
    """Get or create MessageHistory instance for a session"""
    return MessageHistory(
        name="bank:msg:history",
        session_tag=session_id,
        redis_url="redis://localhost:6379"
    )

def add_message(session_id: str, role: str, text: str, intent: str = "unknown", score: float = 0.0):
    """Add a message with metadata"""
    history = get_history(session_id)
    message = {
        "role": role,
        "content": text,
        "metadata": {
            "intent": intent,
            "score": score
        }
    }
    history.add_message(message, session_tag=session_id)

def get_context(session_id: str, limit: int = 6) -> str:
    """Get recent messages as formatted string"""
    history = get_history(session_id)
    messages = history.get_recent(top_k=limit, as_text=False, session_tag=session_id)
    # Format and return as string for orchestrator

def clear_conversation(session_id: str):
    """Clear all messages for a session"""
    history = get_history(session_id)
    history.clear()
```

## Data Structure in Redis

### Message Format
Each message is stored as a Redis HASH with:
```
{
  "role": "user" | "assistant",
  "content": "actual message text",
  "metadata": {
    "intent": "loan",
    "score": 0.72
  },
  "timestamp": 1728123456.789
}
```

### Redis Keys
```
bank:msg:history:{session_id}:{message_id}
```

Example:
```
bank:msg:history:session_123:01HZXYZ...
```

## Usage in main.py

### Store Messages
```python
# After orchestrator processes a turn
intent = result.get("router", {}).get("intent", "unknown")
score = result.get("router", {}).get("score", 0.0)

add_message(session_id, "user", query)
add_message(session_id, "assistant", result['reply'], intent, score)
```

### Retrieve Context
```python
# Before calling orchestrator
context_text = get_context(session_id, limit=6)

result = handle_turn(
    user_id=request.userId,
    session_id=session_id,
    text=query,
    context=context_text  # Pass to orchestrator
)
```

### Clear on Feedback
```python
# When user clicks "Yes" on feedback
if helpful:
    clear_conversation(session_id)
```

## Conversation Flow

```
Turn 1: User says "i want loan"
┌─────────────────────────────────────────┐
│ MessageHistory.add_message({            │
│   "role": "user",                       │
│   "content": "i want loan"              │
│ })                                       │
└─────────────────────────────────────────┘
        ↓
   Router processes
        ↓
┌─────────────────────────────────────────┐
│ MessageHistory.add_message({            │
│   "role": "assistant",                  │
│   "content": "What type of loan?",      │
│   "metadata": {                         │
│     "intent": "loan",                   │
│     "score": 0.72                       │
│   }                                      │
│ })                                       │
└─────────────────────────────────────────┘

Turn 2: User says "personal"
┌─────────────────────────────────────────┐
│ context = MessageHistory.get_recent(6)  │
│ Returns: ["User: i want loan",          │
│           "Assistant: What type?..."]   │
└─────────────────────────────────────────┘
        ↓
   Router sees "loan" in context
   Reuses intent → "loan" ✅
        ↓
   Stores new turn with metadata
```

## Features Used

### From RedisVL MessageHistory API

1. **`add_message(message, session_tag)`**
   - Adds single message with metadata
   - Automatic timestamp
   
2. **`get_recent(top_k, as_text, session_tag)`**
   - Retrieves last N messages
   - Returns as list of dicts or text
   
3. **`clear()`**
   - Removes all messages for session
   - Used for feedback "Yes" action

## Configuration

### Environment Variables (.env)
```env
REDIS_URL=redis://localhost:6379
HISTORY_INDEX=bank:msg:history
```

### Requirements
```
redisvl>=0.3.0
redis>=4.5.0
```

## Benefits Over Custom Implementation

| Feature | Custom (LIST) | RedisVL MessageHistory |
|---------|---------------|------------------------|
| Structure | Simple strings | Rich HASHes with metadata |
| Timestamps | Manual | Automatic |
| Ordering | Manual trim | Built-in chronological |
| Metadata | None | Intent, score, custom fields |
| API | Custom functions | Standard RedisVL API |
| Maintenance | DIY | Official library support |

## Testing

### Check Messages in Redis
```bash
# List all message keys for a session
docker exec redis-stack redis-cli KEYS "bank:msg:history:session_*"

# Get message details
docker exec redis-stack redis-cli HGETALL "bank:msg:history:session_123:01HZXYZ..."
```

### Verify Context Retrieval
```python
from memory.history import get_context

# Get last 6 messages
context = get_context("session_123", limit=6)
print(context)
# Output:
# User: i want loan
# Assistant: What type of loan?... Intent: loan (0.72)
# User: personal
# Assistant: What amount?... Intent: loan (0.95)
```

## Migration Notes

If upgrading from custom LIST-based storage:
1. Old data in `bank:chat:{session_id}:messages` won't auto-migrate
2. New sessions will use RedisVL MessageHistory
3. Old sessions will naturally expire (24hr TTL)
4. Or manually delete old keys: `redis-cli DEL bank:chat:*:messages`

---

**Status**: ✅ Implemented  
**Library**: [RedisVL](https://github.com/redis/redisvl)  
**Version**: redisvl>=0.3.0  
**Date**: October 2025

