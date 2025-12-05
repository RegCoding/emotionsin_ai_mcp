import os

DEFAULT_TIMEOUT = float(os.environ.get("HTTP_TIMEOUT", "10"))
REQUIRE_API_KEY = os.environ.get("REQUIRE_API_KEY", "false").lower() == "true"
API_KEY = os.environ.get("MCP_API_KEY")  # optional, if you want MCP-level auth
BACKEND_BASE = os.environ.get("EMOTIONSIN_BACKEND", "https://fastapi-sql-isvbqdl2ba-oc.a.run.app/profiles/prompt")