from google.adk.tools import FunctionTool # Changed from Tool to FunctionTool
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from config import settings

# --- Domain tool stubs (with documentation added) ---

async def fetch_past_sales(*args, **kwargs) -> str:
    """Fetch historical sales data from the sales database.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        A string representation of the sales data.
    """
    raise NotImplementedError("fetch_past_sales not implemented")

async def fetch_weather_forecast(*args, **kwargs) -> str:
    """Fetch weather forecast data from an external service.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        A string representation of the weather forecast.
    """
    raise NotImplementedError("fetch_weather_forecast not implemented")

async def fetch_zipcode_online_purchases(*args, **kwargs) -> str:
    """Fetch online purchase patterns by zipcode.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        A string representation of the purchase data.
    """
    raise NotImplementedError("fetch_zipcode_online_purchases not implemented")

async def fetch_return_patterns(*args, **kwargs) -> str:
    """Fetch product return patterns and statistics.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        A string representation of the return patterns.
    """
    raise NotImplementedError("fetch_return_patterns not implemented")

async def fetch_shelf_constraints(*args, **kwargs) -> str:
    """Fetch physical shelf constraints and dimensions.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        A string representation of the shelf constraints data.
    """
    raise NotImplementedError("fetch_shelf_constraints not implemented")

# --- Remote agent wrappers ---

inventory_client = RemoteA2aAgent(
    name="inventory_client",
    agent_card=settings.INVENTORY_AGENT_CARD_URL
)

procurement_client = RemoteA2aAgent(
    name="procurement_client",
    agent_card=settings.PROCUREMENT_AGENT_CARD_URL
)

po_client = RemoteA2aAgent(
    name="po_client",
    agent_card=settings.PO_AGENT_CARD_URL
)

async def call_inventory_agent(payload: str) -> str:
    """Call the Inventory Agent via A2A communication.

    Args:
        payload: The task payload to send to the remote agent.

    Returns:
        The result string from the remote agent execution.
    """
    return await inventory_client.run(payload)

async def call_procurement_agent(payload: str) -> str:
    """Call the Procurement Agent via A2A communication.

    Args:
        payload: The task payload to send to the remote agent.

    Returns:
        The result string from the remote agent execution.
    """
    return await procurement_client.run(payload)

async def call_po_agent(payload: str) -> str:
    """Call the PO Agent (Purchase Order) via A2A communication.

    Args:
        payload: The task payload to send to the remote agent.

    Returns:
        The result string from the remote agent execution.
    """
    return await po_client.run(payload)


# --- ADK-compatible tool definitions (FunctionTool instantiated correctly) ---

# Removed `name` and `description` args as they are automatic.

fetch_past_sales_tool = FunctionTool(func=fetch_past_sales)
fetch_weather_forecast_tool = FunctionTool(func=fetch_weather_forecast)
fetch_zipcode_online_purchases_tool = FunctionTool(func=fetch_zipcode_online_purchases)
fetch_return_patterns_tool = FunctionTool(func=fetch_return_patterns)
fetch_shelf_constraints_tool = FunctionTool(func=fetch_shelf_constraints)
call_inventory_agent_tool = FunctionTool(func=call_inventory_agent)
call_procurement_agent_tool = FunctionTool(func=call_procurement_agent)
call_po_agent_tool = FunctionTool(func=call_po_agent)


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
