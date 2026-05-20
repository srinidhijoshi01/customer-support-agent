# Customer Support Agent with Hindsight Memory

An AI-powered customer support agent that remembers customer interactions and provides personalized responses using Hindsight memory layer and cascadeflow runtime intelligence.

## Features..

- *Persistent Memory*: Agent remembers customer interactions across sessions using Hindsight
- *Personalized Responses*: Adapts responses based on customer history
- *Cost-Optimized*: Uses cascadeflow for intelligent model routing
- *NovaSaaS Integration*: Built for SaaS customer support workflows

## Problem Solved

Traditional support agents forget everything between conversations. This agent:
- Recalls past billing issues
- Remembers customer preferences
- Escalates repeat problems proactively
- Saves costs through intelligent routing

## How It Works

### Interaction 1: Generic Response
Customer Priya Sharma reports a billing issue → Agent gives standard response

### Interaction 5: Personalized Response
Same customer returns → Agent recalls previous issues → Provides proactive help

This progression demonstrates the power of agent memory.

## Tech Stack

- *LLM*: Groq (qwen/qwen3-32b) - Free tier
- *Memory*: Hindsight Cloud API
- *Runtime Intelligence*: cascadeflow
- *Framework*: Pydantic AI
- *Language*: Python 3.10+

## Installation

```bash
# Clone the repository
git clone https://github.com/Dhanalakshmi-bn/customer-support-agent.git
cd customer-support-agent

# Create virtual environment
python -m venv venv
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Create .env file with API keys
# Add GROQ_API_KEY and HINDSIGHT_API_KEY
