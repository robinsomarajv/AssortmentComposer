from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents import LlmAgent
from services.runtime import llm_completion
from tools.retail_tools import all_tools

root_agent = LlmAgent(
    name="assortment_planner_agent",
    description="Orchestrates Inventory, Procurement, and PO agents over A2A.",
    llm=llm_completion,
    tools=all_tools
)

# to_a2a wrapper will be implemented here.
my_agent_card = AgentCard(
    name="assortment_planner_agent",
    description="An agent that provides assortment planning capabilities via HTTP, SSE, WebSocket, and A2A protocols.",
    version="1.0.0",
    # Main base URL for the agent (can be overridden)
    capabilities=["streaming"],
    skills=[
        # Placeholder skill — replace with real ones
        {
            "name": "invoke",
            "description": "Invokes an agent operation through the A2A protocol.",
            "inputs": [
                {"name": "operation", "type": "string", "description": "Operation name"},
                {"name": "payload", "type": "object", "description": "Operation payload"},
            ],
            "outputs": [
                {"name": "response", "type": "object", "description": "Result of the operation"}
            ],
        }
    ]
)

a2a_app = to_a2a(root_agent, agent_card=my_agent_card)
