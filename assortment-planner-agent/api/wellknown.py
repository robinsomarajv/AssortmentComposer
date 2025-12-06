from fastapi import Request
from fastapi.responses import JSONResponse
from config import settings

# /.well-known/agent-card route will be implemented here.

async def agent_card(request: Request, a2a_mounted: bool):
    base_url = settings.PUBLIC_BASE_URL or str(request.base_url).rstrip("/")
    card = {
        "id": "assortment_planner_agent.v1",
        "name": "Assortment Planner Agent",
        "protocols": ["http", "sse", "websocket", "a2a"],
        "endpoints": {
            "http": {
                "base_url": base_url,
                "openapi": f"{base_url}/openapi.json",
                "chat": f"{base_url}/chat",
                "stream": f"{base_url}/chat/stream",
                "ws": f"{base_url}/chat/ws"
            },
            "a2a": {
                "mounted": a2a_mounted,
                "base_path": "/a2a",
                "invoke": "/a2a/invoke",
                "stream": "/a2a/stream",
                "metadata": "/a2a/metadata",
                "protocol_version": "1.0"
            }
        }
    }
    return JSONResponse(card)
