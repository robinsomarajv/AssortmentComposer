import litellm
from langfuse import Langfuse
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from .config import get_settings

settings = get_settings()

# Initialize Langfuse
langfuse = Langfuse(
    public_key=settings.LANGFUSE_PUBLIC_KEY,
    secret_key=settings.LANGFUSE_SECRET_KEY,
    host=settings.LANGFUSE_HOST
)

# Configure LiteLLM with Langfuse tracing
litellm.set_verbose(True)
litellm.callbacks = [langfuse.get_litellm_callback()]

# Session management
session_service = InMemorySessionService()
runner = Runner(agent=None, app_name=settings.APP_NAME, session_service=session_service)  # agent set in agent.py

async def get_system_prompt() -> str:
    """
    Fetches the system prompt from Langfuse Prompt Management.
    Prompt name: "assortment_planner_system", Label: "production"
    """
    prompt = langfuse.get_prompt(
        name="assortment_planner_system",
        label="production"
    )
    return prompt.content if prompt else "You are the Assortment Planner Agent."

async def llm_completion(messages: list[dict], stream: bool = False):
    """
    Wrapper around LiteLLM acompletion.
    Always includes the system prompt as the first message.
    """
    system_prompt = await get_system_prompt()
    messages = [{"role": "system", "content": system_prompt}] + messages
    response = await litellm.acompletion(
        model=settings.LLM_MODEL,
        messages=messages,
        stream=stream
    )
    return response

# Helper for running agent with session
async def call_with_session(message: str, session_id: str = None):
    """
    Runs the agent using Runner, manages session_id.
    """
    if not session_id:
        session_id = runner.session_service.create_session()
    events = await runner.run(message=message, session_id=session_id)
    # Extract final text reply and any plan result
    reply = events[-1].get("text", "") if events else ""
    plan_result = events[-1].get("plan_result", {}) if events else {}
    return {"reply": reply, "session_id": session_id, "plan_result": plan_result}

