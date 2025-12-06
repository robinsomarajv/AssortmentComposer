from google.adk.tools import Tool
from google.adk.agents import RemoteA2aAgent
from config import settings

# Domain tool stubs
async def fetch_past_sales(*args, **kwargs):
    raise NotImplementedError("fetch_past_sales not implemented")

async def fetch_weather_forecast(*args, **kwargs):
    raise NotImplementedError("fetch_weather_forecast not implemented")

async def fetch_zipcode_online_purchases(*args, **kwargs):
    raise NotImplementedError("fetch_zipcode_online_purchases not implemented")

async def fetch_return_patterns(*args, **kwargs):
    raise NotImplementedError("fetch_return_patterns not implemented")

async def fetch_shelf_constraints(*args, **kwargs):
    raise NotImplementedError("fetch_shelf_constraints not implemented")

# Remote agent wrappers
inventory_client = RemoteA2aAgent(agent_card_url=settings.INVENTORY_AGENT_CARD_URL)
procurement_client = RemoteA2aAgent(agent_card_url=settings.PROCUREMENT_AGENT_CARD_URL)
po_client = RemoteA2aAgent(agent_card_url=settings.PO_AGENT_CARD_URL)

async def call_inventory_agent(payload):
    return await inventory_client.run(payload)

async def call_procurement_agent(payload):
    return await procurement_client.run(payload)

async def call_po_agent(payload):
    return await po_client.run(payload)

# ADK-compatible tool definitions
fetch_past_sales_tool = Tool(
    name="fetch_past_sales",
    description="Fetch past sales data.",
    func=fetch_past_sales
)
fetch_weather_forecast_tool = Tool(
    name="fetch_weather_forecast",
    description="Fetch weather forecast data.",
    func=fetch_weather_forecast
)
fetch_zipcode_online_purchases_tool = Tool(
    name="fetch_zipcode_online_purchases",
    description="Fetch online purchases by zipcode.",
    func=fetch_zipcode_online_purchases
)
fetch_return_patterns_tool = Tool(
    name="fetch_return_patterns",
    description="Fetch product return patterns.",
    func=fetch_return_patterns
)
fetch_shelf_constraints_tool = Tool(
    name="fetch_shelf_constraints",
    description="Fetch shelf constraints data.",
    func=fetch_shelf_constraints
)
call_inventory_agent_tool = Tool(
    name="call_inventory_agent",
    description="Call Inventory Agent via A2A.",
    func=call_inventory_agent
)
call_procurement_agent_tool = Tool(
    name="call_procurement_agent",
    description="Call Procurement Agent via A2A.",
    func=call_procurement_agent
)
call_po_agent_tool = Tool(
    name="call_po_agent",
    description="Call PO Agent via A2A.",
    func=call_po_agent
)

all_tools = [
    fetch_past_sales_tool,
    fetch_weather_forecast_tool,
    fetch_zipcode_online_purchases_tool,
    fetch_return_patterns_tool,
    fetch_shelf_constraints_tool,
    call_inventory_agent_tool,
    call_procurement_agent_tool,
    call_po_agent_tool
]
