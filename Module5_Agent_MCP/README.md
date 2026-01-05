# Intelligent Weather & News Agent 

## Overview

This project is a **Python-based Streamlit application** that answers user questions about ** weather conditions** and **news** using an **agent orchestration architecture** and **Model Context Protocol (MCP)–style server integrations**.

The system supports **natural language queries**, **multi-turn conversations**, and **combined requests** such as asking for weather and news in a single query.

**VIDEO LINK**: https://youtu.be/VzXr-b25MbY?si=io32pM20BjrvNMQ0

**Git**: https://github.com/aska-courses/generative-ai-for-software-development/tree/main/Module5_Agent_MCP
---

## Features

* 🌤️ Weather information by location
* 📰 News headlines and topic-based news
* 🤖 LLM-powered intent classification (weather / news / both)
* 🔀 Agent orchestrator for routing and aggregation
* 💬 Chat-style conversational interface
* 🔁 Multi-turn conversation support
* 💾 Response caching for performance

---

## Architecture

The application follows an **agent orchestration pattern**:

```
User Query
   ↓
Intent Classifier (LLM)
   ↓
Agent Orchestrator
   ├── Weather MCP Server (Open-Meteo)
   ├── News MCP Server (TheNews API)
   ↓
Response Aggregation
   ↓
Natural Language Response (LLM)
```

### Key Components

* **Streamlit UI** – user interaction and chat interface
* **Agent Orchestrator** – central routing and coordination logic
* **Intent Classifier** – determines whether weather, news, or both are required
* **MCP Client Layer** – standardized access to external data services
* **LLM (OpenAI)** – intent detection and response generation

---

## MCP Integration

The system uses **MCP-style server abstraction** to integrate external tools:

### Weather MCP Server

* **Provider:** Open-Meteo
* **Authentication:** Not required
* **Capabilities:**

  * Location-based weather lookup
  * Temperature, humidity, wind speed, conditions

### News MCP Server

* **Provider:** TheNews API
* **Capabilities:**

  * Latest headlines
  * Topic-based news search
* **Fallback behavior:**

  * Graceful error messages if unavailable

MCP server configuration is centralized in `mcp_config/config.json`.

---

## Supported Queries

### Weather

* “What’s the weather in London?”
* “Temperature in Tokyo”
* “Will it rain in Paris?”

### News

* “Latest tech news”
* “Top headlines today”
* “News about sports”

### Combined

* “Weather in NYC and tech news”
* “London weather and latest headlines”

---

## Project Structure

```
project/
├── app.py                  # Streamlit application
├── agents/
│   ├── orchestrator.py     # Agent orchestration logic
│   ├── intent_classifier.py# LLM-based intent detection
│   ├── mcp_client.py       # MCP-style client for external services
│   └── __init__.py
├── mcp_config/
│   └── config.json         # MCP server configuration
├── requirements.txt
└── README.md
```

---

## Technologies Used

* **Python 3.10+**
* **Streamlit**
* **OpenAI GPT models**
* **Async I/O (aiohttp)**
* **Model Context Protocol (MCP) concepts**
* **Open-Meteo API**
* **TheNews API**

---

## Installation

```bash
pip install -r requirements.txt
```

Set environment variables (if needed):

```bash
export OPENAI_API_KEY=your_key
export THENEWSAPI_KEY=your_key
```

---

## Running the App

```bash
streamlit run app.py
```

---
