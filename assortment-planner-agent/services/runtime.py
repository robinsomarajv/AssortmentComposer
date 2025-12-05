import litellm
from langfuse import Langfuse
from google.adk.runner import Runner, InMemorySessionService
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

async def llm_completion(messages, stream=False):
    system_prompt = await get_system_prompt("assortment_planner_system")
    messages = [{"role": "system", "content": system_prompt}] + messages
    response = await litellm.acompletion(
        model=settings.LLM_MODEL,
        messages=messages,
        stream=stream,
        callbacks=[langfuse]
    )
    return response

async def call_with_session(message, session_id=None):
    from agent.agent import root_agent
    create_runner(root_agent)
    result = await runner.run(message, session_id=session_id)
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
