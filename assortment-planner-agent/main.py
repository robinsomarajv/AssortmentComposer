import sys
import os

# --- CRITICAL FIX ---
# Add the current directory to sys.path to ensure local imports are found first.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
from fastapi import FastAPI

import agent
from api.http_routes import router as http_router

app = FastAPI(title="Assortment Planner Agent - fast api")

# Mount human endpoints
app.include_router(http_router)
#mounting the A2A endpoints
agentic_assrtmnt = agent.a2a_app
agentic_assrtmnt.mount('/app', app)
