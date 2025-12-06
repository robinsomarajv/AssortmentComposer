# services/runtime.py
import uuid
from typing import Optional, Any
from google.adk.runners import Runner, InMemorySessionService
from google.genai import types
from config import settings

# --- Import the top-level 'agent' module ---
import agent

runner = None
session_service = None

def create_runner():
    """
    Creates and configures the ADK Runner instance without needing arguments.
    """
    global runner, session_service
    if runner is None:
        session_service = InMemorySessionService()
        runner = Runner(
            agent=agent.assrtmnt_agent,
            session_service=session_service,
            app_name='agents',
        )
    return runner

# ... (keep get_api_key_for_model function as is) ...

async def call_with_session(message, ssid=None, model=None):

    r: Runner = create_runner()
    target_session_id_str = ssid if ssid is not None else str(uuid.uuid4())

    # Create the session object in the service
    session_obj = await r.session_service.create_session(
        app_name='agents',
        user_id='u101',
        session_id=target_session_id_str  # Pass the string ID here during creation
    )

    # *** FIX IS HERE ***
    # Extract the actual string ID from the returned session object for the runner method
    effective_session_id_str = session_obj.id
    event_generator = r.run_async(
        new_message=types.Content(parts=[types.Part(text=message)], role="user"),
        user_id='u101',
        session_id=effective_session_id_str,
        # model=model # This argument may still cause an error, remove if needed
    )
    # ... rest of call_with_session ...
    final_reply_content = ""
    async for event in event_generator:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    final_reply_content += part.text

    return {
        "reply": final_reply_content,
        "session_id": effective_session_id_str,
        "plan_result": None
    }

async def stream_llm_tokens(message, session_id=None):
    # --- FIX: Call create_runner() with no arguments now ---
    r: Any = create_runner()
    result_generator = await r.run(
        message,
        session_id=session_id,
        model=settings.LLM_MODEL,
        stream=True  # <--- Pass the stream flag to the run method
    )  # type: ignore
    # ... rest of stream_llm_tokens ...
    async for token in result_generator:
        yield token.content.parts[0].text

