# User Feedback & Auto-Clear System 👍👎

## Overview

After completing a task (showing a proposal/recommendation), the system asks "Was this helpful?" with Yes/No buttons. When the user clicks **Yes**, the conversation memory is automatically cleared for a fresh start.

## Architecture

All conversation tracking uses **RedisVL MessageHistory** ([docs](https://redis.io/docs/latest/develop/ai/redisvl/api/message_history/)):
- **Library**: `redisvl.extensions.llmcache.MessageHistory`
- **Structure**: Redis HASHes with timestamps for sequential ordering
- **Session tagging**: Each session_id gets its own isolated history
- **Features**: Recent message retrieval, automatic timestamping, metadata support
- **Format**: Structured messages with role, content, and metadata (intent, score)

## How It Works

### 1. Backend Signals Completion
When the orchestrator returns a proposal (EMI calculation, card recommendation, etc.), the `/chat` endpoint sets `showFeedback: true`:

```python
# main.py
show_feedback = bool(result.get("proposal"))

return ChatResponse(
    ...
    showFeedback=show_feedback
)
```

### 2. Frontend Shows Feedback Buttons
The ChatDock component displays feedback buttons when `showFeedback` is true:

```tsx
{message.showFeedback && !message.feedbackGiven && (
  <div className="flex items-center gap-2">
    <span>Was this helpful?</span>
    <button onClick={() => handleFeedback(message.id, true)}>
      👍 Yes
    </button>
    <button onClick={() => handleFeedback(message.id, false)}>
      👎 No
    </button>
  </div>
)}
```

### 3. User Clicks Yes → Memory Cleared
When user clicks **Yes**, the frontend calls `/chat/feedback` with `helpful: true`, which triggers conversation clearing:

```python
@app.post("/chat/feedback")
async def chat_feedback(sessionId: str, helpful: bool):
    if helpful and memory_available:
        clear_conversation(session_id)
        print(f"✅ User feedback: helpful=true, cleared session {session_id}")
    return {"ok": True, "cleared": helpful}
```

### 4. Fresh Conversation
After clearing, the next "i want loan" request won't see old slot values, so the system properly asks all questions again.

## Benefits

✅ **No stale data**: Old conversation context doesn't interfere with new requests  
✅ **User-controlled**: Clearing happens only when user confirms helpfulness  
✅ **Smooth UX**: Automatic "fresh start" without manual session management  
✅ **Feedback tracking**: Backend logs user satisfaction

## API

### POST /chat/feedback

**Request Body:**
```json
{
  "sessionId": "session_xyz",
  "helpful": true
}
```

**Response:**
```json
{
  "ok": true,
  "message": "Thank you! Conversation cleared for a fresh start.",
  "cleared": true
}
```

## Flow Example

```
User: i want loan
Bot: What type of loan? (personal/home/car/education)

User: personal
Bot: What amount?

User: 50000
Bot: For how long?

User: 12 months
Bot: Your EMI will be ₹4,395/month
     [Proposal card with details]
     
     Was this helpful? [👍 Yes] [👎 No]  ← Feedback buttons appear

User clicks: 👍 Yes
→ Backend clears conversation memory
→ Frontend shows: "Great! Your conversation has been cleared..."

User: i want loan  ← New fresh request
Bot: What type of loan?  ← Starts from scratch, no old data
```

## Files Modified

1. **Backend (`main.py`)**:
   - Added `showFeedback` field to `ChatResponse`
   - Added `/chat/feedback` endpoint
   - Imported `clear_conversation` from `memory.history`

2. **Memory (`memory/history.py`)**:
   - Simple `clear_conversation()` function using Redis `DELETE`

3. **Frontend (`ChatDock.tsx`)**:
   - Added `showFeedback` and `feedbackGiven` to `Message` interface
   - Added `handleFeedback()` function
   - Rendered feedback buttons when `showFeedback` is true

## Configuration

Memory clearing requires Redis to be running:

```bash
docker run -d -p 6379:6379 redis/redis-stack:latest
```

Set in `.env`:
```env
REDIS_URL=redis://localhost:6379
```

## Testing

1. Start backend: `uvicorn main:app --reload --port 8000`
2. Start frontend: `cd nextjs-app && npm run dev`
3. Complete a loan flow (type, amount, tenure)
4. See feedback buttons after EMI calculation
5. Click "Yes" → check backend logs for "cleared session"
6. Start new loan request → verify it asks all questions again

---

**Status**: ✅ Implemented  
**Version**: 1.0  
**Date**: October 2025

