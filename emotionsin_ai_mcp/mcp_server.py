# mcp_server.py
import os
import logging
from typing import Dict, Any
from fastmcp import FastMCP

from config import BACKEND_BASE
from persona import compile_persona_contract, fetch_agent_from_link

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create the FastMCP app as the main application
mcp = FastMCP("emotionsin-mcp")


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
    logging.info(f"Tool 'get_agent_contract_from_link' called with profile: '{profile}'")
    
    if not profile or profile.strip() == "":
        logging.error("Profile parameter is empty or missing")
        raise ValueError("Profile parameter is required but was empty or missing")
    
    url = f"{BACKEND_BASE}?id={profile}"
    logging.info(f"Fetching agent from backend URL: {url}")
    
    try:
        agent = await fetch_agent_from_link(url)
    except Exception as e:
        logging.error(f"Failed to fetch agent from backend: {type(e).__name__}: {e}")
        raise RuntimeError(f"Failed to fetch agent profile '{profile}' from backend: {e}")
    
    if not agent:
        logging.warning(f"Agent profile '{profile}' not found at backend (empty response).")
        raise ValueError(f"Agent profile '{profile}' not found at backend.")

    logging.info(f"Agent profile found for '{profile}': {agent.get('name', 'unnamed')}")
    
    try:
        contract = compile_persona_contract(agent)
    except Exception as e:
        logging.error(f"Failed to compile persona contract: {type(e).__name__}: {e}")
        raise RuntimeError(f"Failed to compile persona contract: {e}")
    
    logging.info(f"Contract compiled successfully for agent: {agent.get('name')}")
    return {
        "id": agent.get("id"),
        "name": agent.get("name"),
        "contract": contract,
        "raw_profile": agent
    }


if __name__ == "__main__":
    # Cloud Run: listen on 0.0.0.0 and PORT from env
    port = int(os.environ.get("PORT", "8080"))

    # Run the MCP server using SSE transport (compatible with Claude)
    # Streamable-http clients (like ChatGPT) also work with SSE
    # The endpoint will be available at: http://<service-url>/sse
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=port,
        path="/sse"
    )
