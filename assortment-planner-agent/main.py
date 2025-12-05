from fastapi import FastAPI, Request

from api.a2a_mount import mount_a2a
from api.http_routes import router as http_router
from api.wellknown import agent_card

app = FastAPI(title="Assortment Planner Agent")

# Mount human endpoints
app.include_router(http_router)

# Mount A2A endpoints
A2A_MOUNTED = mount_a2a(app)


@app.get("/.well-known/agent-card")
async def wellknown_agent_card(request: Request):
    return await agent_card(request, a2a_mounted=A2A_MOUNTED)

