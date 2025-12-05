from google.adk.agent import LlmAgent
from services.runtime import llm_completion
from tools.retail_tools import all_tools

root_agent = LlmAgent(
    name="assortment_planner_agent",
    description="Orchestrates Inventory, Procurement, and PO agents over A2A.",
    llm=llm_completion,
    tools=all_tools
)
