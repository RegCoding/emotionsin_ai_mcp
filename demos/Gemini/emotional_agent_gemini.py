"""
Google Gemini chatbot using Emotionsin.ai MCP server.
Uses proper session ID handling to fetch and apply emotional personas.
"""

import os
import json
import requests
from typing import List, Dict

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Try to import Google Generative AI
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    print("ERROR: google-generativeai library not installed!")
    print("Install with: pip install google-generativeai")
    GEMINI_AVAILABLE = False
    exit(1)

# Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyA1lz8KjXVt44E-I1CAqUFtDmajchxZxhw")
MCP_SERVER_URL = "https://emotionsinai-mcp-server-572436270187.europe-west1.run.app/mcp"
PROFILE_ID = os.getenv("EMOTIONSIN_PROFILE_ID", "4e1cabf6cfbd452b951d659897d16365")


class EmotionalChatbot:
    """Chatbot using Google Gemini with Emotionsin.ai MCP server."""

    def __init__(self, api_key: str, profile_id: str, mcp_server_url: str):
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is required.")
        if not profile_id:
            raise ValueError("EMOTIONSIN_PROFILE_ID is required.")

        self.api_key = api_key
        self.profile_id = profile_id
        self.mcp_server_url = mcp_server_url
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        self.persona_contract = None
        self.agent_name = "Assistant"
        self.session_id = None

    def fetch_persona_from_mcp(self) -> bool:
        """Fetch persona using proper session ID from headers."""
        print(f"Fetching persona from MCP server...")
        print(f"Profile ID: {self.profile_id}")
        
        try:
            # Step 1: GET request to obtain session ID
            print("Getting session ID...")
            response = requests.get(
                self.mcp_server_url,
                headers={"Accept": "text/event-stream"},
                timeout=10
            )
            
            # Extract session ID from headers
            self.session_id = response.headers.get('mcp-session-id')
            if self.session_id:
                print(f"✓ Session ID: {self.session_id[:20]}...")
            else:
                print("⚠ No session ID in headers")
                return False
            
            # Step 2: Initialize with session ID
            print("Initializing MCP session...")
            init_payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "emotional-chatbot-gemini",
                        "version": "1.0.0"
                    }
                }
            }
            
            init_response = requests.post(
                self.mcp_server_url,
                json=init_payload,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                    "mcp-session-id": self.session_id
                },
                timeout=10
            )
            
            print(f"Initialize status: {init_response.status_code}")
            if init_response.status_code == 200:
                print("✓ Session initialized")
            
            # Step 3: Call the tool with session ID
            print(f"Calling tool with profile {self.profile_id}...")
            tool_payload = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "get_agent_contract_from_link",
                    "arguments": {
                        "profile": self.profile_id
                    }
                }
            }
            
            tool_response = requests.post(
                self.mcp_server_url,
                json=tool_payload,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                    "mcp-session-id": self.session_id
                },
                timeout=30
            )
            
            print(f"Tool call status: {tool_response.status_code}")
            
            if tool_response.status_code == 200:
                response_text = tool_response.text
                print(f"Response preview: {response_text[:200]}")
                
                # Parse SSE format (event: message \n data: {...})
                data = None
                for line in response_text.split('\n'):
                    if line.startswith('data: '):
                        json_str = line[6:]  # Remove "data: " prefix
                        data = json.loads(json_str)
                        break
                
                if not data:
                    print("Could not parse SSE response")
                    return False
                
                # Extract contract from response
                if "result" in data:
                    result = data["result"]
                    content = result.get("content", [])
                    
                    for item in content:
                        if isinstance(item, dict) and "text" in item:
                            text_data = json.loads(item["text"])
                            self.persona_contract = text_data.get("contract")
                            self.agent_name = text_data.get("name", "Assistant")
                            print(f"✓ Loaded persona: {self.agent_name}")
                            return True
                
                # Fallback: check if response is direct JSON with contract
                if isinstance(data, dict) and "contract" in data:
                    self.persona_contract = data.get("contract")
                    self.agent_name = data.get("name", "Assistant")
                    print(f"✓ Loaded persona: {self.agent_name}")
                    return True
            
            print(f"Could not extract persona from response")
            return False
            
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            return False

    def chat(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        """Chat with the agent using the persona contract."""
        
        # Build the full prompt with persona contract
        full_prompt = ""
        
        # Add persona contract as system instruction
        if self.persona_contract:
            full_prompt += f"{self.persona_contract}\n\n"
        
        # Add conversation history
        if conversation_history:
            for msg in conversation_history:
                role = msg.get("role", "")
                content = msg.get("content", "")
                if role == "user":
                    full_prompt += f"User: {content}\n"
                elif role == "assistant":
                    full_prompt += f"{self.agent_name}: {content}\n"
        
        # Add current user message
        full_prompt += f"User: {user_message}\n{self.agent_name}:"

        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config={
                    'temperature': 0.7,
                    'top_p': 1,
                    'top_k': 1,
                    'max_output_tokens': 2048,
                }
            )
            
            return response.text if response.text else "I couldn't generate a response."
        except Exception as e:
            return f"Error: {e}"


def main():
    """Main function."""
    print("=" * 60)
    print("Emotional Chatbot - Google Gemini + Emotionsin.ai")
    print("=" * 60)
    print()
    
    if not GOOGLE_API_KEY:
        print("ERROR: GOOGLE_API_KEY is not set!")
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        print("Then set it with: export GOOGLE_API_KEY='your-key-here'")
        print("Or on Windows: set GOOGLE_API_KEY=your-key-here")
        return
    
    print(f"Profile ID: {PROFILE_ID}")
    print()
    
    try:
        chatbot = EmotionalChatbot(
            api_key=GOOGLE_API_KEY,
            profile_id=PROFILE_ID,
            mcp_server_url=MCP_SERVER_URL
        )
        
        # Fetch persona with proper session ID handling
        success = chatbot.fetch_persona_from_mcp()
        
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
            
            response = chatbot.chat(user_input, conversation_history)
            print(f"{chatbot.agent_name}: {response}\n")
            
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": response})
            
            # Limit history to last 10 exchanges
            if len(conversation_history) > 20:
                conversation_history = conversation_history[-20:]
                
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

