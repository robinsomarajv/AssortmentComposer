import litellm
from langfuse import Langfuse
from google.adk.runner import Runner, InMemorySessionService
from config import settings
from services.prompts import get_system_prompt
import os

langfuse = Langfuse(
    public_key=settings.LANGFUSE_PUBLIC_KEY,
    secret_key=settings.LANGFUSE_SECRET_KEY,
    host=settings.LANGFUSE_HOST
)

runner = None
session_service = None

def create_runner(agent):
    global runner, session_service
    if runner is None:
        session_service = InMemorySessionService()
        runner = Runner(agent=agent, session_service=session_service)
    return runner

def get_api_key_for_model(model: str) -> str:
    """
    Returns the correct API key for the given model/provider from environment variables.
    Extend this mapping as needed for more providers/models.
    """
    model = model.lower()
    if model.startswith("gpt-") or model.startswith("openai"):
        return os.getenv("OPENAI_API_KEY", "")
    elif model.startswith("claude") or model.startswith("anthropic"):
        return os.getenv("ANTHROPIC_API_KEY", "")
    elif model.startswith("gemini") or model.startswith("google"):
        return os.getenv("GOOGLE_API_KEY", "")
    elif model.startswith("mistral"):
        return os.getenv("MISTRAL_API_KEY", "")
    # Add more providers as needed
    return ""

async def llm_completion(messages, stream=False, model=None):
    system_prompt = await get_system_prompt("assortment_planner_system")
    messages = [{"role": "system", "content": system_prompt}] + messages
    model = model or settings.LLM_MODEL
    api_key = get_api_key_for_model(model)
    response = await litellm.acompletion(
        model=model,
        messages=messages,
        stream=stream,
        api_key=api_key,
        callbacks=[langfuse]
    )
    return response

async def call_with_session(message, session_id=None, model=None):
    from agent.agent import root_agent
    create_runner(root_agent)
    result = await runner.run(message, session_id=session_id, model=model)
    return {
        "reply": result.reply,
        "session_id": result.session_id,
        "plan_result": getattr(result, "plan_result", None)
    }

async def stream_llm_tokens(message, session_id=None):
    from agent.agent import root_agent
    create_runner(root_agent)
    async for token in runner.stream(message, session_id=session_id):
        yield token
