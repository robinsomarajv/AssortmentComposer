from typing import Optional, Any
import litellm
from google.adk.runners import Runner, InMemorySessionService
from config import settings
from services.prompts import get_system_prompt

runner = None
session_service = None

def create_runner(agent):
    global runner, session_service
    if runner is None:
        session_service = InMemorySessionService()
        runner = Runner(agent=agent, session_service=session_service, app_name='AssortmentPlannerAgent-101',)
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
    result_generator = await r.run(
        message,
        session_id=session_id,
        model=settings.LLM_MODEL,
        stream=True  # <--- Pass the stream flag to the run method
    )  # type: ignore

    # Iterate over the generator returned by r.run()
    async for token in result_generator:
        # The token received is likely a chunk object; we extract the text content
        # You might need to adjust 'token.content.parts[0].text' based on the exact
        # structure returned by your ADK version if this doesn't work perfectly.
        yield token.content.parts[0].text
