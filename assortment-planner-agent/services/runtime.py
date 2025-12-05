from typing import Optional, Any
import litellm
from langfuse import Langfuse
from google.adk.runners import Runner, InMemorySessionService
from config import settings
from services.prompts import get_system_prompt

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

def get_api_key_for_model(model: Optional[str] = None) -> str:
    """
    Returns the correct API key for the given model/provider using values from `settings`.
    """
    m = (model or settings.LLM_MODEL or "").lower()
    # OpenAI / GPT family
    if m.startswith("gpt-") or "openai" in m:
        return settings.OPENAI_API_KEY or ""
    # Anthropic / Claude
    if m.startswith("claude") or "anthropic" in m:
        return settings.ANTHROPIC_API_KEY or ""
    # Google / Gemini
    if "gemini" in m or "google" in m:
        return settings.GOOGLE_API_KEY or ""
    # Mistral
    if "mistral" in m:
        return settings.MISTRAL_API_KEY or ""
    # default: no key
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
    r: Any = create_runner(root_agent)
    result: Any = await r.run(message, session_id=session_id, model=model)  # type: ignore
    return {
        "reply": getattr(result, "reply", None),
        "session_id": getattr(result, "session_id", None),
        "plan_result": getattr(result, "plan_result", None)
    }

async def stream_llm_tokens(message, session_id=None):
    from agent.agent import root_agent
    r: Any = create_runner(root_agent)
    async for token in r.stream(message, session_id=session_id):  # type: ignore
        yield token
