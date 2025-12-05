from typing import Any, Dict
from .config import get_settings
from langfuse import Langfuse
import os
import json

settings = get_settings()
langfuse = Langfuse(
    public_key=settings.LANGFUSE_PUBLIC_KEY,
    secret_key=settings.LANGFUSE_SECRET_KEY,
    host=settings.LANGFUSE_HOST
)

# Domain tools (stubs)
def fetch_past_sales(store_id: str, period: str) -> dict:
    """Fetch past sales data for a store from mock JSON file."""
    file_path = os.path.join(os.path.dirname(__file__), "mock_past_sales.json")
    with open(file_path, "r") as f:
        data = json.load(f)
    return {"sales": data}

def fetch_weather_forecast(zipcode: str, date: str) -> Dict[str, Any]:
    """Fetch weather forecast for a given zipcode and date."""
    raise NotImplementedError("TODO")

def fetch_zipcode_online_purchases(zipcode: str) -> Dict[str, Any]:
    """Fetch online purchase patterns for a zipcode."""
    raise NotImplementedError("TODO")

def fetch_return_patterns(store_id: str) -> dict:
    """Fetch product return patterns for a store from mock JSON file."""
    file_path = os.path.join(os.path.dirname(__file__), "mock_return_patterns.json")
    with open(file_path, "r") as f:
        data = json.load(f)
    return {"returns": data}

def fetch_shelf_constraints(store_id: str) -> Dict[str, Any]:
    """Fetch shelf constraints for a store."""
    raise NotImplementedError("TODO")

# Agent-as-tool wrappers
from a2a import RemoteA2aAgent

inventory_client = RemoteA2aAgent(agent_card_url=settings.INVENTORY_AGENT_CARD_URL)
procurement_client = RemoteA2aAgent(agent_card_url=settings.PROCUREMENT_AGENT_CARD_URL)
po_client = RemoteA2aAgent(agent_card_url=settings.PO_AGENT_CARD_URL)

async def call_inventory_agent(payload: dict) -> dict:
    with langfuse.span("a2a_inventory_call", input=payload):
        result = await inventory_client.run(payload)
        return result

async def call_procurement_agent(payload: dict) -> dict:
    with langfuse.span("a2a_procurement_call", input=payload):
        result = await procurement_client.run(payload)
        return result

async def call_po_agent(payload: dict) -> dict:
    with langfuse.span("a2a_po_call", input=payload):
        result = await po_client.run(payload)
        return result
