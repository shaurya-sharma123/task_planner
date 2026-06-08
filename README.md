# 🚀 AI Agent Task Planner API

A lightweight, robust FastAPI backend that accepts structured multi-step objectives, validates incoming payloads using Pydantic, and generates structured execution reports using Google's Gemini 2.5 Flash model.

This project demonstrates modern AI backend development concepts including:

* FastAPI endpoint creation
* Request and response validation with Pydantic
* Structured AI outputs using response schemas
* Deterministic JSON generation from LLMs
* Error handling and API design best practices
* Cross-Origin Resource Sharing (CORS) middleware implementation for secure client-server communication.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Frontend Framework:** Streamlit
* **Backend Framework:** FastAPI
* **Data Validation:** Pydantic v2
* **HTTP Client:** Requests
* **Server:** Uvicorn
* **AI Integration:** Google GenAI SDK
* **Model:** Gemini 2.5 Flash
* **Environment Management:** Python Dotenv

---

## ✨ Features

* **Interactive UI:** Build your task pipeline step-by-step dynamically in a beautiful dark-themed interface.
* **Payload Validation:** Front-end sanity checks paired with strict backend Pydantic enforcement.
* **Configurable Hyperparameters:** Control LLM creativity via a real-time temperature slider.
* **Structured Outputs:** Enforces strict structural output rules on Gemini to bypass text-parsing boilerplate and use type-safe `response.parsed` properties.
* **Resilient Error Handling:** Gracefully handles offline backends, missing fields, or validation failures.
* **CORS Enabled:** Fully configured to allow secure cross-origin communication between the frontend interface (`port 8501`) and the backend API (`port 8000`).

---

## 📋 API Endpoint

### Structured Execution Endpoint

```http
POST /items/structured/
```

This endpoint accepts a user goal along with a sequence of planned steps and generates a structured execution report.

---

## 📥 Example Request

```json
{
  "agent_request": {
    "user_goal": "Research the latest trends in Artificial Intelligence",
    "temperature": 0.2,
    "planned_steps": [
      {
        "step_id": 1,
        "action": "Identify major AI trends",
        "tools_required": "web_search"
      },
      {
        "step_id": 2,
        "action": "Analyze industry impact",
        "tools_required": "analysis"
      },
      {
        "step_id": 3,
        "action": "Generate learning recommendations",
        "tools_required": "reasoning"
      }
    ]
  }
}
```

---

## 📤 Example Response

```json
{
  "status": "success",
  "goal_processed": "Research the latest trends in Artificial Intelligence",
  "steps_executed_count": 3,
  "agent_final_report": {
    "summary": "Research completed successfully.",
    "detailed_findings": [
      {
        "step_id": 1,
        "status": "Completed",
        "findings": "Identified key trends including multimodal AI and AI agents."
      }
    ],
    "next_recommended_actions": [
      "Study AI agent frameworks",
      "Explore RAG architectures",
      "Review recent research papers"
    ]
  }
}
```

---

## 🧩 Data Models

### Task Step

```python
class Task_Step(BaseModel):
    step_id: int
    action: str
    tools_required: str
```

Represents a single step within the execution plan.

---

### Planner Request

```python
class AI_Planner_Request(BaseModel):
    user_goal: str
    temperature: float
    planned_steps: list[Task_Step]
```

Defines the complete request payload sent by the client.

---

### Step Report

```python
class Step_Report(BaseModel):
    step_id: int
    status: str
    findings: str
```

Represents the result generated for an individual step.

---

### Final Execution Report

```python
class AI_Final_Report(BaseModel):
    summary: str
    detailed_findings: list[Step_Report]
    next_recommended_actions: list[str]
```

Defines the structured output returned by Gemini.

---

## 🧠 Structured Output Generation

The application uses Gemini's structured output capability through:

```python
config={
    "response_mime_type": "application/json",
    "response_schema": AI_Final_Report
}
```

This ensures Gemini returns JSON matching the specified Pydantic schema, allowing the backend to receive validated, type-safe responses through:

```python
response.parsed
```

instead of parsing raw text manually.

---

## ▶️ Running the Project

Install dependencies:

```bash
pip install fastapi uvicorn google-genai python-dotenv
```

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Run the application:

```bash
uvicorn main:app --reload
```

Open the Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Start the Streamlit Frontend:

```bash
streamlit run main.py
```

---

## ⚠️ Current Limitation

This project currently generates execution reports based on the provided plan using Gemini.

The backend does not yet execute real tools such as:

* Web search
* Browser automation
* Database queries
* Terminal commands

The model generates a structured report describing how the plan would be executed.

Future versions may introduce real tool calling and agent execution workflows.
