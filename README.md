# Emotionin.ai – MCP Server (Open Source)

Welcome to the **Emotionin.ai MCP Server** — an open-source foundational MCP (Model Context Protocol) server designed to give every Emotionin.ai user the ability to integrate **emotional profiles** into any LLM-driven chatbot or AI agent.  
This repository provides a lightweight, extensible server that exposes:

- A **user-specific Emotionin.ai emotional profile**
- A framework to **add custom MCP tools** for personality shaping, immersive interactions, and context-adaptive AI behaviors

The goal: enable developers and creators to build **deeply personalized, emotionally intelligent conversational agents** using a fully open, modular, and MIT-licensed MCP server.

---

## ✨ Features

- **Open Source MCP Server** (MIT License)
- **Emotionin.ai Profile Integration**  
  Fetch and use a customer-specific emotional profile from **https://emotionin.ai**.
- **Custom Tool Extensibility**  
  Add your own MCP tools to tailor the LLM’s emotional expression, personality traits, or domain-specific behavior.
- **Dockerized Deployment**  
  Fully configured Docker container for local or cloud operation.
- **Minimal Installation Requirements**  
  `requirements.txt` includes all necessary dependencies for easy setup.
- **Developer-friendly Architecture**  
  Clean, modular codebase designed to be extended or embedded into larger agent frameworks.

---

## 📌 Purpose of This Project

Emotionin.ai provides emotional and personality profiling services.  
This MCP server acts as a **bridge** that exposes such a profile to any MCP-enabled LLM client (ChatGPT, open-source LLM frontends, custom agents, etc.).

Developers can:

- Build AI agents that **respond differently depending on the user’s emotional profile**
- Add custom logic, memory tools, context fetchers, API utilities, or domain-specific knowledge tools
- Shape the agent’s **tone, style, empathy, and interaction patterns**
- Create fully immersive, personalized experience layers powered by the Emotionin.ai ecosystem

---

┌──────────────────────────┐
│ Emotionin.ai Profile │ (external service: https://emotionin.ai
)
└───────────────┬──────────┘
│
Fetch emotional profile
│
┌───────────────▼───────────┐
│ MCP Server Core │ (This repository)
│ - Profile retrieval tool │
│ - Extensible MCP handlers │
└───────────────┬───────────┘
│
Custom Tools Added by Devs
│
┌───────────────▼────────────┐
│ LLM / Chatbot Client │
└─────────────────────────────┘

---

## 📦 Installation

### Prerequisites

- Docker (optional but recommended)
- Python 3.9+ (if running without Docker)

---

## 🚀 Quick Start (Docker)

This repository includes a preconfigured Dockerfile for fast setup.

```bash
docker build -t emotionin-mcp-server .
docker run -p 3000:3000 emotionin-mcp-server

git clone https://github.com/<your-repo>/emotionin-mcp-server.git
cd emotionin-mcp-server
pip install -r requirements.txt
python server.py

---

🧩 Adding Custom MCP Tools

This MCP server is intentionally minimal, giving developers freedom to add tools such as:

Personality modifiers

Domain knowledge injectors

User memory systems

Context APIs (calendar, CRM, IoT, etc.)

Emotional tone controllers

Add your tools via the /tools directory or extend the server configuration.

Example structure:
## 🏗️ Architecture Overview

tools/
  ├── emotion_profile.py
  ├── personality_modifier.py
  └── my_custom_tool.py

Each tool is automatically registered when the server starts.

🔐 Emotionin.ai Service Attribution Requirement

This project is MIT-licensed (see below).
If you use or distribute this MCP server, you must include attribution that it uses the Emotionin.ai emotional profile service (https://emotionin.ai
).

Example attribution:

“This custom MCP server uses an Emotionin.ai emotional profile (https://emotionin.ai).”

This is the only requirement beyond standard MIT terms.

🤝 Contributing

Contributions are welcome!

Fork the repository

Create a feature branch

Open a pull request

🙋 Support

For Emotionin.ai profile services or integration questions:
https://emotionin.ai

For issues with the MCP server code:
Open an issue in this repository.

⭐ If you find this useful…

Give the repository a star — it helps others discover the project!


---

If you want, I can also generate:

- A downloadable `.md` file  
- `CONTRIBUTING.md`  
- A template `/tools` example  
- A logo/banner for the repo  

Just tell me!


