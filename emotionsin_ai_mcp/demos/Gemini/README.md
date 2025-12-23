# Emotional Chatbot Demo

Chatbot demos that integrate with the Emotionsin.ai MCP server to fetch and apply emotional personas.

Available versions:
- **ChatGPT** (OpenAI GPT-4)
- **Google Gemini** (Gemini Pro)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:

### For ChatGPT version:
```bash
# Linux/Mac:
export OPENAI_API_KEY="your-openai-api-key-here"
export EMOTIONSIN_PROFILE_ID="4e1cabf6cfbd452b951d659897d16365"

# Windows (PowerShell):
$env:OPENAI_API_KEY="your-openai-api-key-here"
$env:EMOTIONSIN_PROFILE_ID="4e1cabf6cfbd452b951d659897d16365"
```

### For Gemini version:
```bash
# Linux/Mac:
export GOOGLE_API_KEY="your-google-api-key-here"
export EMOTIONSIN_PROFILE_ID="4e1cabf6cfbd452b951d659897d16365"

# Windows (PowerShell):
$env:GOOGLE_API_KEY="your-google-api-key-here"
$env:EMOTIONSIN_PROFILE_ID="4e1cabf6cfbd452b951d659897d16365"
```

Get your Google API key from: https://makersuite.google.com/app/apikey

Alternatively, create a `.env` file:
```
OPENAI_API_KEY=your-openai-api-key-here
GOOGLE_API_KEY=your-google-api-key-here
EMOTIONSIN_PROFILE_ID=4e1cabf6cfbd452b951d659897d16365
```

## Usage

Run the **ChatGPT** version:
```bash
python emotional_agent_chatgpt_working.py
```

Run the **Gemini** version:
```bash
python emotional_agent_gemini.py
```

Type your messages and press Enter. Type 'quit' or 'exit' to end the conversation.

## Configuration

### Environment Variables:
- **OPENAI_API_KEY**: Your OpenAI API key (for ChatGPT version)
- **GOOGLE_API_KEY**: Your Google API key (for Gemini version)
- **EMOTIONSIN_PROFILE_ID**: The Profile ID for the Emotionsin.ai MCP server
  - Default: `4e1cabf6cfbd452b951d659897d16365`
  - Get profiles from: https://agentprofile.emotionsin.ai/
- **MCP_SERVER_URL**: The MCP server URL
  - Default: `https://emotionsinai-mcp-server-572436270187.europe-west1.run.app/mcp`

## Features

- ✅ Fetches emotional personas from Emotionsin.ai MCP server
- ✅ Proper MCP session management with session ID from headers
- ✅ SSE (Server-Sent Events) response parsing
- ✅ Configurable Profile ID via environment variable
- ✅ Maintains conversation history
- ✅ Works with both **OpenAI GPT-4** and **Google Gemini Pro**
- ✅ Simple command-line interface

## How It Works

1. Connects to MCP server and extracts session ID from response headers
2. Initializes MCP session with proper protocol
3. Calls `get_agent_contract_from_link` tool with your Profile ID
4. Receives persona contract (personality, tone, behavior rules)
5. Uses the persona as system prompt for the LLM
6. Chat with your emotional AI agent!

