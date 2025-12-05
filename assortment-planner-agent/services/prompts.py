import httpx
from config import settings

async def get_system_prompt(prompt_name: str) -> str:
    """
    Fetch system prompt from Langfuse Prompt Management.
    """
    url = f"{settings.LANGFUSE_HOST}/api/prompts/{prompt_name}"
    headers = {
        "Authorization": f"Bearer {settings.LANGFUSE_SECRET_KEY}",
        "X-Langfuse-Public-Key": settings.LANGFUSE_PUBLIC_KEY
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("prompt", "")
