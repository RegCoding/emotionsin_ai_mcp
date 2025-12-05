# mcp_server.py
import os
from typing import Dict, Any
from fastapi import HTTPException, Request
from fastmcp import FastMCP

from persona import fetch_agent_from_link, compile_persona_contract
from config import REQUIRE_API_KEY, API_KEY, BACKEND_BASE

mcp = FastMCP("emotionsin-mcp")

def auth_guard(headers: Dict[str, Any]) -> None:
    """
    Optional: very simple API key guard at MCP level.
    If REQUIRE_API_KEY is True, expects MCP_API_KEY to be set and validates
    an incoming X-API-Key header (if your client passes one).
    For Claude Desktop you may not need this at first.
    """
    if not REQUIRE_API_KEY:
        return
    expected = API_KEY
    got = headers.get("X-API-Key") if headers else None
    if not expected or got != expected:
        raise PermissionError("Invalid or missing MCP API key.")


@mcp.tool()
async def get_agent_contract_from_link(profile: str, headers: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """
    Fetch an agent persona from the backend using a profile ID from the MCP URL
    and convert it into a fully structured, ready-to-use persona activation contract.

    This tool performs three tasks:
    1. Extracts the `profile` ID from the MCP connection URL (e.g., /mcp?profile=...).
    2. Downloads the full persona profile JSON from the backend using that ID.
    3. Wraps the pre-compiled system prompt from the backend into a standard MCP
       activation contract. The contract contains:
        - the agent's identity
        - emotional + behavioral rules
        - tone + communication constraints
        - denial and safety rules
        - persona consistency rules
        - an activation wrapper instructing the LLM to adopt the persona immediately

    The returned "contract" can be injected directly into the model context
    (system or assistant role) and requires no additional prompting to activate.

    Returns a dict containing:
        - id: agent identifier
        - name: agent name
        - contract: the final activation prompt string
        - raw_profile: the raw JSON for debugging or extended use
    """
    if not profile:
        raise HTTPException(
            status_code=400,
            detail="MCP tool 'get_agent_contract_from_link' requires a 'profile' query parameter in the MCP URL."
        )
    url = f"{BACKEND_BASE}?id={profile}"
    agent = await fetch_agent_from_link(url)
    contract = compile_persona_contract(agent)
    return {
        "id": agent.get("id"),
        "name": agent.get("name"),
        "contract": contract,
        "raw_profile": agent
    }


if __name__ == "__main__":
    # Cloud Run: listen on 0.0.0.0 and PORT from env
    port = int(os.environ.get("PORT", "8080"))

    # For most MCP clients (Claude, LangChain, Agno, etc.), Streamable HTTP is "streamable-http"
    # and the endpoint will be: http://<service-url>/mcp
    mcp.run(
        transport="streamable-http",  # or "http" if your version uses that name
        host="0.0.0.0",
        port=port,
        path="/mcp",
    )
