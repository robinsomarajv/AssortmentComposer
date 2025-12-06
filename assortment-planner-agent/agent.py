# agent.py (Refactored to satisfy Pydantic validation)

from a2a.types import (
    AgentCard,
    AgentCapabilities,
    AgentSkill
)
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents import LlmAgent
from config import settings
from tools.retail_tools import all_tools

assrtmnt_agent = LlmAgent(
    name="assortment_planner_agent",
    description="Orchestrates Inventory, Procurement, and PO agents over A2A.",
    model=settings.LLM_MODEL,
    tools=all_tools
)


# Define the specific skill using the Skill Pydantic model
invoke_skill = AgentSkill(
    id="invoke-skill-1", # REQUIRED FIELD ADDED
    name="invoke",
    description="Invokes an agent operation through the A2A protocol.",
    tags=["core", "a2a"] # REQUIRED FIELD ADDED
)

# Define the full AgentCard using Pydantic models
my_agent_card = AgentCard(
    name="assortment_planner_agent",
    description="An agent that provides assortment planning capabilities via HTTP, SSE, WebSocket, and A2A protocols.",
    version="1.0.0",
    url=settings.AGENT_BASE_URL, # REQUIRED FIELD ADDED (Assuming settings.AGENT_BASE_URL exists)
    capabilities=AgentCapabilities(streaming=True),
    default_input_modes=["http", "a2a"],
    default_output_modes=["http", "a2a"],
    skills=[invoke_skill] # Pass the Pydantic Skill object
)

a2a_app = to_a2a(assrtmnt_agent, agent_card=my_agent_card)
