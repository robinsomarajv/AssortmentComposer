from fastapi import FastAPI, Request

from agent.agent import a2a_app
from api.http_routes import router as http_router

app = FastAPI(title="Assortment Planner Agent - fast api")

# Mount human endpoints
app.include_router(http_router)
#mounting the A2A endpoints
a2a_app.mount('/app', app)
