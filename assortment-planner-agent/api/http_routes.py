from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import JSONResponse, StreamingResponse
from services.runtime import call_with_session, stream_llm_tokens

router = APIRouter()

@router.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message")
    session_id = data.get("session_id")
    result = await call_with_session(message, session_id)
    return JSONResponse(result)

@router.get("/chat/stream")
async def chat_stream(request: Request):
    data = dict(request.query_params)
    message = data.get("message")
    session_id = data.get("session_id")
    async def event_generator():
        async for token in stream_llm_tokens(message, session_id):
            yield f"data: {token}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.websocket("/chat/ws")
async def chat_ws(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_json()
    message = data.get("message")
    session_id = data.get("session_id")
    async for token in stream_llm_tokens(message, session_id):
        await websocket.send_text(token)
    await websocket.close()

@router.get("/health")
async def health():
    return {"status": "ok"}
