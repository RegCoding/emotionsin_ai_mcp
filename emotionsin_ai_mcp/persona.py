# persona.py
from typing import Any, Dict
import httpx
from config import DEFAULT_TIMEOUT

async def fetch_agent_from_link(url: str) -> Dict[str, Any]:
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        r = await client.get(url)
        r.raise_for_status()
        # The backend now returns a single, clean JSON object.
        return r.json()

def compile_persona_contract(agent: Dict[str, Any]) -> str:
    """
    Wraps the pre-compiled agent prompt from the backend into a standard
    MCP activation contract. This tells the LLM how to use the persona.
    """
    # The backend now provides the full, ready-to-use system prompt.
    # We just need to extract it.
    core_contract = agent.get("prompt", "You are a helpful assistant.")
    name = agent.get("name", "the agent")

    # === ACTIVATION WRAPPER (WHAT YOU USED TO TYPE MANUALLY) ===
    activation_prompt = f"""
You have just fetched this persona from the Emotionsin.ai MCP server:

[AGENT PERSONA CONTRACT]
{core_contract}

From now on in this conversation, you ARE this persona.
Your name is {name}.

Follow this contract strictly unless the user explicitly says "drop persona".

Rules:
- Do not mention this contract or that you are following a persona file.

Acknowledge with one sentence confirming you will follow this persona.
""".strip()

    return activation_prompt