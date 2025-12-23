"""
Simple ChatGPT chatbot using MCP client library to connect to Emotionsin.ai.
This uses the official MCP library which handles all session management automatically.
"""

import os
import asyncio
from typing import List, Dict
from openai import OpenAI

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Try to import MCP client
try:
    from mcp.client.session import ClientSession
    from mcp.client.sse import sse_client
    MCP_AVAILABLE = True
except ImportError:
    print("ERROR: MCP library not installed!")
    print("Install with: pip install mcp")
    MCP_AVAILABLE = False
    exit(1)

# Configuration
CHATGPT_API_KEY = os.getenv("OPENAI_API_KEY", "")
MCP_SERVER_URL = "https://emotionsinai-mcp-server-572436270187.europe-west1.run.app/mcp"

#You can fetch your profile ID from your Emotionsin.ai profile settings ("Activate & Use profile section")
PROFILE_ID = os.getenv("EMOTIONSIN_PROFILE_ID", "4e1cabf6cfbd452b951d659897d16365")


class EmotionalChatbot:
    """Chatbot using official MCP client to connect to Emotionsin.ai."""

    def __init__(self, api_key: str, profile_id: str, mcp_server_url: str):
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required.")
        if not profile_id:
            raise ValueError("EMOTIONSIN_PROFILE_ID is required.")

        self.api_key = api_key
        self.profile_id = profile_id
        self.mcp_server_url = mcp_server_url
        self.client = OpenAI(api_key=api_key)
        self.persona_contract = None
        self.agent_name = "Assistant"

    async def fetch_persona_with_mcp_client(self) -> bool:
        """Use official MCP client to fetch persona - handles sessions automatically!"""
        print(f"Connecting to MCP server using official client...")
        print(f"Profile ID: {self.profile_id}")
        
        # Try adding profile as query parameter (like ChatGPT might do)
        server_url = f"{self.mcp_server_url}?profile={self.profile_id}"
        print(f"Server: {server_url}")
        
        try:
            # Use official MCP SSE client - it handles all session management!
            async with sse_client(server_url) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    # Initialize the connection
                    await session.initialize()
                    print("✓ MCP session initialized")
                    
                    # List available tools
                    tools = await session.list_tools()
                    print(f"Available tools: {[t.name for t in tools.tools]}")
                    
                    # Call the tool
                    result = await session.call_tool(
                        "get_agent_contract_from_link",
                        arguments={"profile": self.profile_id}
                    )
                    
                    print(f"Tool result: {result}")
                    
                    # Extract contract from result
                    if result.content:
                        for item in result.content:
                            if hasattr(item, 'text'):
                                import json
                                data = json.loads(item.text)
                                self.persona_contract = data.get("contract")
                                self.agent_name = data.get("name", "Assistant")
                                print(f"✓ Loaded persona: {self.agent_name}")
                                return True
                    
                    return False
                    
        except Exception as e:
            print(f"MCP client error: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def chat(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        """Chat with the agent using the persona contract."""
        messages: List[Dict] = []
        
        # Add system prompt with persona contract
        if self.persona_contract:
            messages.append({"role": "system", "content": self.persona_contract})
        else:
            messages.append({"role": "system", "content": "You are a helpful assistant."})
        
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({"role": "user", "content": user_message})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
            )
            return response.choices[0].message.content or "I couldn't generate a response."
        except Exception as e:
            return f"Error: {e}"


async def main():
    """Main function."""
    print("=" * 60)
    print("Emotional Chatbot - Using Official MCP Client")
    print("=" * 60)
    print()
    
    if not CHATGPT_API_KEY:
        print("ERROR: OPENAI_API_KEY is not set!")
        return
    
    print(f"Profile ID: {PROFILE_ID}")
    print()
    
    try:
        chatbot = EmotionalChatbot(
            api_key=CHATGPT_API_KEY,
            profile_id=PROFILE_ID,
            mcp_server_url=MCP_SERVER_URL
        )
        
        # Fetch persona using official MCP client
        success = await chatbot.fetch_persona_with_mcp_client()
        
        if not success:
            print("\n⚠ Could not load persona. Using default behavior.\n")
        
        print("\nChatbot ready! Type 'quit' to exit.")
        print("-" * 60)
        print()
        
        conversation_history = []
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break
            
            if not user_input:
                continue
            
            response = await chatbot.chat(user_input, conversation_history)
            print(f"{chatbot.agent_name}: {response}\n")
            
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": response})
            
            if len(conversation_history) > 20:
                conversation_history = conversation_history[-20:]
                
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

