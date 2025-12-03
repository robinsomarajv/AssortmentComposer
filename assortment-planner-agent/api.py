from fastapi import FastAPI, Request, Body
from fastapi.responses import JSONResponse, StreamingResponse
from .agent import a2a_app, root_agent
from .service import runner, call_with_session, get_system_prompt, llm_completion
from .config import get_settings
from langfuse import Langfuse
import asyncio

settings = get_settings()
langfuse = Langfuse(
    public_key=settings.LANGFUSE_PUBLIC_KEY,
    secret_key=settings.LANGFUSE_SECRET_KEY,
    host=settings.LANGFUSE_HOST
)

app = FastAPI(title="Assortment Planner Agent")
app.mount("/a2a", a2a_app)

@app.post("/assortment/plan")
async def plan_assortment(request: Request, body: dict = Body(...)):
    message = body.get("message", "")
    session_id = body.get("session_id")
    with langfuse.span("http_assortment_plan", input=body):
        result = await call_with_session(message, session_id)
        return JSONResponse(result)

@app.get("/assortment/plan/stream")
async def plan_assortment_stream(request: Request, q: str, session_id: str = None):
    async def event_stream():
        with langfuse.span("http_assortment_stream", input={"q": q, "session_id": session_id}):
            system_prompt = await get_system_prompt()
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": q}
            ]
            async for chunk in await llm_completion(messages, stream=True):
                token = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                if token:
                    yield f"data: {token}\n\n"
            yield "data: [DONE]\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get("/health")
async def health():
    return {"status": "ok"}

