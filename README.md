# 🚀 AI Agent Task Planner API

A lightweight, robust FastAPI backend that takes structured, multi-step goals from a user, validates the payload configuration using Pydantic, and orchestrates a comprehensive execution report using the Google Gemini live API.

This project serves as an introductory backend module for structured AI Agent logic, showing how to safely transition raw client data streams into deterministic LLM execution steps.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Framework:** FastAPI
* **Data Validation:** Pydantic v2
* **Server Gateway:** Uvicorn
* **AI Integration:** Google GenAI SDK (`gemini-2.5-flash`)

---

## 📋 API Architecture & Payload

### Endpoint
`POST /items/`

### Example Request Body
```json
{
  "agent_request": {
    "user_goal": "Plan a grand opening launch for a neighborhood coffee shop.",
    "temperature": 0.3,
    "planned_steps": [
      {
        "step_id": 1,
        "action": "Brainstorm 3 unique marketing slogans for social media advertising.",
        "tools_required": "copywriting_assistant"
      },
      {
        "step_id": 2,
        "action": "Calculate a rough opening day budget assuming $500 max spend.",
        "tools_required": "budget_calculator"
      }
    ]
  }
}
