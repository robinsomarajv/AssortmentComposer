from google.adk.agents import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from .service import llm_completion
from .tools import (
    fetch_past_sales,
    fetch_weather_forecast,
    fetch_zipcode_online_purchases,
    fetch_return_patterns,
    fetch_shelf_constraints,
    call_inventory_agent,
    call_procurement_agent,
    call_po_agent
)
from .config import get_settings

settings = get_settings()

root_agent = LlmAgent(
    name="assortment_planner_agent",
    description="Composes store assortments by collaborating with Inventory, Procurement, and PO agents.",
    llm=llm_completion,
    tools=[
        fetch_past_sales,
        fetch_weather_forecast,
        fetch_zipcode_online_purchases,
        fetch_return_patterns,
        fetch_shelf_constraints,
        call_inventory_agent,
        call_procurement_agent,
        call_po_agent
    ]
)

# Set the agent in service.py runner
import sys
sys.modules["service"].runner.agent = root_agent

a2a_app = to_a2a(root_agent, port=settings.ASSORTMENT_PORT)

